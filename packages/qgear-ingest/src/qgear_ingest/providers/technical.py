from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Any

from qgear_ingest.providers.base import ProviderMetadata, ProviderResponse, ProviderStatus


BENCHMARKS = ("SPY", "QQQ", "XLK", "SMH")


@dataclass(frozen=True)
class TechnicalSnapshot:
    ticker: str
    as_of_date: str
    close: float
    dma_50: float | None
    dma_150: float | None
    dma_200: float | None
    relative_strength_vs_spy_pct: float | None
    relative_strength_vs_qqq_pct: float | None
    relative_strength_vs_xlk_pct: float | None
    relative_strength_vs_smh_pct: float | None
    drawdown_from_52w_high_pct: float
    volume_trend_pct: float | None
    technical_regime: str
    reasons: tuple[str, ...]
    price_source_metadata: ProviderMetadata
    benchmark_source_metadata: dict[str, ProviderMetadata]


def calculate_technical_snapshot(
    *,
    ticker: str,
    price_response: ProviderResponse,
    benchmark_responses: dict[str, ProviderResponse],
) -> TechnicalSnapshot:
    if price_response.status != ProviderStatus.OK:
        raise ValueError(price_response.metadata.error or f"Price provider status is {price_response.status.value}.")

    rows = _price_rows(price_response.payload)
    if len(rows) < 50:
        raise ValueError("At least 50 price-history rows are required for a technical snapshot.")

    close = _close(rows[-1])
    as_of_date = str(rows[-1].get("date") or rows[-1].get("snapshot_date") or "")
    closes = [_close(row) for row in rows]
    volumes = [_volume(row) for row in rows]
    dma_50 = _moving_average(closes, 50)
    dma_150 = _moving_average(closes, 150)
    dma_200 = _moving_average(closes, 200)
    drawdown = _drawdown_from_high(closes)
    volume_trend = _volume_trend(volumes)

    relative_strength: dict[str, float | None] = {}
    benchmark_metadata: dict[str, ProviderMetadata] = {}
    for benchmark in BENCHMARKS:
        response = benchmark_responses.get(benchmark)
        if not response:
            relative_strength[benchmark] = None
            continue
        benchmark_metadata[benchmark] = response.metadata
        benchmark_rows = _price_rows(response.payload)
        relative_strength[benchmark] = _relative_strength_pct(rows, benchmark_rows)

    avg_rs_values = [value for value in relative_strength.values() if value is not None]
    avg_rs = mean(avg_rs_values) if avg_rs_values else None
    regime, reasons = _classify_regime(
        close=close,
        dma_50=dma_50,
        dma_200=dma_200,
        avg_relative_strength_pct=avg_rs,
        drawdown_from_high_pct=drawdown,
    )

    return TechnicalSnapshot(
        ticker=ticker.upper(),
        as_of_date=as_of_date,
        close=close,
        dma_50=dma_50,
        dma_150=dma_150,
        dma_200=dma_200,
        relative_strength_vs_spy_pct=relative_strength.get("SPY"),
        relative_strength_vs_qqq_pct=relative_strength.get("QQQ"),
        relative_strength_vs_xlk_pct=relative_strength.get("XLK"),
        relative_strength_vs_smh_pct=relative_strength.get("SMH"),
        drawdown_from_52w_high_pct=drawdown,
        volume_trend_pct=volume_trend,
        technical_regime=regime,
        reasons=reasons,
        price_source_metadata=price_response.metadata,
        benchmark_source_metadata=benchmark_metadata,
    )


def _price_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = payload.get("prices", [])
    if not isinstance(rows, list):
        return []
    return sorted((row for row in rows if isinstance(row, dict)), key=lambda row: str(row.get("date") or row.get("snapshot_date") or ""))


def _close(row: dict[str, Any]) -> float:
    value = row.get("adjusted_close", row.get("close"))
    return float(value)


def _volume(row: dict[str, Any]) -> int:
    return int(row.get("volume") or 0)


def _moving_average(values: list[float], window: int) -> float | None:
    if len(values) < window:
        return None
    return round(sum(values[-window:]) / window, 2)


def _period_return(values: list[dict[str, Any]], window: int = 60) -> float | None:
    if len(values) <= window:
        return None
    start = _close(values[-window - 1])
    end = _close(values[-1])
    if start <= 0:
        return None
    return (end / start - 1) * 100


def _relative_strength_pct(ticker_rows: list[dict[str, Any]], benchmark_rows: list[dict[str, Any]]) -> float | None:
    ticker_return = _period_return(ticker_rows)
    benchmark_return = _period_return(benchmark_rows)
    if ticker_return is None or benchmark_return is None:
        return None
    return round(ticker_return - benchmark_return, 2)


def _drawdown_from_high(values: list[float]) -> float:
    high = max(values[-252:] if len(values) >= 252 else values)
    if high <= 0:
        return 0
    return round((1 - values[-1] / high) * 100, 2)


def _volume_trend(values: list[int]) -> float | None:
    if len(values) < 60:
        return None
    recent = mean(values[-20:])
    prior = mean(values[-60:-20])
    if prior <= 0:
        return None
    return round((recent / prior - 1) * 100, 2)


def _classify_regime(
    *,
    close: float,
    dma_50: float | None,
    dma_200: float | None,
    avg_relative_strength_pct: float | None,
    drawdown_from_high_pct: float,
) -> tuple[str, tuple[str, ...]]:
    reasons: list[str] = []
    above_50 = dma_50 is not None and close >= dma_50
    above_200 = dma_200 is not None and close >= dma_200
    rs_ok = avg_relative_strength_pct is not None and avg_relative_strength_pct >= 0
    rs_weak = avg_relative_strength_pct is not None and avg_relative_strength_pct < -5

    if above_50:
        reasons.append("Price is above the 50-day moving average.")
    if above_200:
        reasons.append("Price is above the 200-day moving average.")
    if rs_ok:
        reasons.append("Relative strength is positive versus benchmark set.")
    if rs_weak:
        reasons.append("Relative strength is weak versus benchmark set.")
    if drawdown_from_high_pct > 35:
        reasons.append("Drawdown from the 52-week high is deep.")

    if (not above_200 and rs_weak) or drawdown_from_high_pct > 35:
        return "BROKEN", tuple(reasons or ["Technical regime is broken by trend and drawdown conditions."])
    if above_50 and above_200 and rs_ok:
        return "SUPPORTIVE", tuple(reasons)
    if above_200 or (above_50 and not rs_weak):
        return "STABILISING", tuple(reasons or ["Trend is stabilising but not fully supportive."])
    return "WEAKENING", tuple(reasons or ["Trend is weakening and should be treated as risk confirmation only."])
