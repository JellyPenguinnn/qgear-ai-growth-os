from __future__ import annotations

from dataclasses import asdict
from datetime import date, timedelta

from qgear_ingest.providers.base import (
    BenchmarkSnapshot,
    DataMode,
    FilingMetadata,
    PriceHistoryPoint,
    PriceSnapshot,
    ProviderName,
    ProviderResponse,
)


DEMO_SOURCE_DATE = "2026-06-22"


DEMO_FILING_ROWS: tuple[FilingMetadata, ...] = (
    FilingMetadata(
        accession_number="0001045810-26-000001",
        form="10-Q",
        filing_date="2026-05-22",
        report_date="2026-04-30",
        primary_document="nvda-20260430.htm",
        source_url="local://demo/sec/submissions/0001045810",
    ),
    FilingMetadata(
        accession_number="0001045810-26-000002",
        form="8-K",
        filing_date="2026-05-22",
        report_date="2026-05-21",
        primary_document="nvda-20260522x8k.htm",
        source_url="local://demo/sec/submissions/0001045810",
    ),
)


DEMO_PRICES: dict[str, PriceSnapshot] = {
    "NVDA": PriceSnapshot("NVDA", DEMO_SOURCE_DATE, 142.1, 145.3, 140.8, 144.5, 144.5, 182_000_000),
    "AMD": PriceSnapshot("AMD", DEMO_SOURCE_DATE, 163.2, 166.4, 160.1, 164.8, 164.8, 55_000_000),
    "MU": PriceSnapshot("MU", DEMO_SOURCE_DATE, 129.4, 133.2, 128.9, 132.6, 132.6, 31_000_000),
    "SPY": PriceSnapshot("SPY", DEMO_SOURCE_DATE, 640.0, 644.2, 638.4, 642.1, 642.1, 72_000_000),
    "QQQ": PriceSnapshot("QQQ", DEMO_SOURCE_DATE, 565.2, 570.7, 562.8, 568.9, 568.9, 49_000_000),
    "XLK": PriceSnapshot("XLK", DEMO_SOURCE_DATE, 250.4, 253.1, 249.8, 252.4, 252.4, 8_000_000),
    "SMH": PriceSnapshot("SMH", DEMO_SOURCE_DATE, 290.0, 296.2, 288.7, 294.9, 294.9, 12_000_000),
}


DEMO_BENCHMARKS: dict[str, BenchmarkSnapshot] = {
    "SPY": BenchmarkSnapshot("SPY", DEMO_SOURCE_DATE, 642.1, 642.1),
    "QQQ": BenchmarkSnapshot("QQQ", DEMO_SOURCE_DATE, 568.9, 568.9),
    "XLK": BenchmarkSnapshot("XLK", DEMO_SOURCE_DATE, 252.4, 252.4),
    "SMH": BenchmarkSnapshot("SMH", DEMO_SOURCE_DATE, 294.9, 294.9),
}


def _build_history(
    ticker: str,
    *,
    start_price: float,
    end_price: float,
    days: int = 260,
    volume: int = 10_000_000,
) -> tuple[PriceHistoryPoint, ...]:
    start_date = date.fromisoformat(DEMO_SOURCE_DATE) - timedelta(days=days - 1)
    points: list[PriceHistoryPoint] = []
    for index in range(days):
        progress = index / (days - 1)
        drift = start_price + (end_price - start_price) * progress
        cycle = ((index % 19) - 9) * 0.08
        close = round(max(1, drift + cycle), 2)
        open_price = round(close * (0.997 + (index % 5) * 0.001), 2)
        high = round(max(open_price, close) * 1.012, 2)
        low = round(min(open_price, close) * 0.988, 2)
        points.append(
            PriceHistoryPoint(
                ticker=ticker,
                date=(start_date + timedelta(days=index)).isoformat(),
                open=open_price,
                high=high,
                low=low,
                close=close,
                adjusted_close=close,
                volume=volume + (index % 20) * 25_000,
            )
        )
    return tuple(points)


DEMO_PRICE_HISTORY: dict[str, tuple[PriceHistoryPoint, ...]] = {
    "NVDA": _build_history("NVDA", start_price=92, end_price=144.5, volume=182_000_000),
    "AMD": _build_history("AMD", start_price=150, end_price=164.8, volume=55_000_000),
    "MU": _build_history("MU", start_price=95, end_price=132.6, volume=31_000_000),
    "SPY": _build_history("SPY", start_price=540, end_price=642.1, volume=72_000_000),
    "QQQ": _build_history("QQQ", start_price=470, end_price=568.9, volume=49_000_000),
    "XLK": _build_history("XLK", start_price=205, end_price=252.4, volume=8_000_000),
    "SMH": _build_history("SMH", start_price=235, end_price=294.9, volume=12_000_000),
}


def _fact(value: float, unit: str = "USD") -> dict:
    return {
        "units": {
            unit: [
                {
                    "fy": 2026,
                    "fp": "Q1",
                    "form": "10-Q",
                    "filed": "2026-05-22",
                    "end": "2026-04-30",
                    "val": value,
                    "accn": "0001045810-26-000001",
                }
            ]
        }
    }


DEMO_COMPANY_FACTS: dict[str, dict] = {
    "0001045810": {
        "cik": 1045810,
        "entityName": "NVIDIA CORP",
        "facts": {
            "us-gaap": {
                "RevenueFromContractWithCustomerExcludingAssessedTax": _fact(44_062_000_000),
                "GrossProfit": _fact(33_000_000_000),
                "OperatingIncomeLoss": _fact(28_000_000_000),
                "NetIncomeLoss": _fact(24_500_000_000),
                "EarningsPerShareDiluted": _fact(0.96, "USD/shares"),
                "NetCashProvidedByUsedInOperatingActivities": _fact(27_000_000_000),
                "PaymentsToAcquirePropertyPlantAndEquipment": _fact(1_100_000_000),
                "CashAndCashEquivalentsAtCarryingValue": _fact(15_000_000_000),
                "Assets": _fact(125_000_000_000),
                "Liabilities": _fact(39_000_000_000),
                "LongTermDebtAndFinanceLeaseObligations": _fact(8_500_000_000),
                "WeightedAverageNumberOfDilutedSharesOutstanding": _fact(24_500_000_000, "shares"),
            }
        },
    }
}


class MockProvider:
    def company_facts(self, cik: str) -> ProviderResponse:
        normalized = cik.zfill(10)
        payload = DEMO_COMPANY_FACTS.get(normalized) or {
            "cik": cik,
            "mode": "demo",
            "message": "No mock company facts are available for this CIK.",
        }
        return ProviderResponse.ok(
            provider=ProviderName.MOCK,
            payload=payload,
            source_url="local://demo/company-facts",
            source_name="Q-GEAR demo company facts",
            cached=True,
            source_date=DEMO_SOURCE_DATE,
            as_of_date=DEMO_SOURCE_DATE,
            cache_key=f"mock_company_facts_{normalized}",
            mode=DataMode.DEMO,
        )

    def submissions(self, cik: str) -> ProviderResponse:
        return ProviderResponse.ok(
            provider=ProviderName.MOCK,
            payload={
                "cik": cik,
                "mode": "demo",
                "filings": {"recent": [asdict(row) for row in DEMO_FILING_ROWS]},
            },
            source_url="local://demo/sec/submissions",
            source_name="Q-GEAR demo SEC submissions",
            cached=True,
            source_date=DEMO_SOURCE_DATE,
            as_of_date=DEMO_SOURCE_DATE,
            cache_key=f"mock_submissions_{cik}",
            mode=DataMode.DEMO,
        )

    def filing_metadata(self, cik: str, *, limit: int = 20) -> ProviderResponse:
        rows = DEMO_FILING_ROWS[:limit]
        return ProviderResponse.ok(
            provider=ProviderName.MOCK,
            payload={"cik": cik, "filings": [asdict(row) for row in rows]},
            source_url="local://demo/sec/filings",
            source_name="Q-GEAR demo filing metadata",
            cached=True,
            source_date=DEMO_SOURCE_DATE,
            as_of_date=DEMO_SOURCE_DATE,
            cache_key=f"mock_filing_metadata_{cik}_{limit}",
            mode=DataMode.DEMO,
        )

    def daily_prices(self, tickers: tuple[str, ...]) -> ProviderResponse:
        normalized = tuple(ticker.upper() for ticker in tickers)
        snapshots = []
        missing = []
        for ticker in normalized:
            snapshot = DEMO_PRICES.get(ticker)
            if snapshot:
                snapshots.append(asdict(snapshot))
            else:
                missing.append(ticker)
        return ProviderResponse.ok(
            provider=ProviderName.MOCK,
            payload={"prices": snapshots, "missing": missing},
            source_url="local://demo/prices",
            source_name="Q-GEAR demo price snapshots",
            cached=True,
            source_date=DEMO_SOURCE_DATE,
            as_of_date=DEMO_SOURCE_DATE,
            cache_key="mock_daily_prices_" + "_".join(normalized),
            mode=DataMode.DEMO,
        )

    def daily_adjusted_history(self, ticker: str, *, output_size: str = "compact") -> ProviderResponse:
        normalized = ticker.upper()
        rows = DEMO_PRICE_HISTORY.get(normalized)
        payload = {
            "ticker": normalized,
            "prices": [asdict(row) for row in rows] if rows else [],
            "missing": [] if rows else [normalized],
            "output_size": output_size,
        }
        return ProviderResponse.ok(
            provider=ProviderName.MOCK,
            payload=payload,
            source_url="local://demo/price-history",
            source_name="Q-GEAR demo adjusted price history",
            cached=True,
            source_date=DEMO_SOURCE_DATE,
            as_of_date=DEMO_SOURCE_DATE,
            cache_key=f"mock_price_history_{normalized}_{output_size}",
            mode=DataMode.DEMO,
        )

    def benchmark_snapshots(self, benchmarks: tuple[str, ...]) -> ProviderResponse:
        normalized = tuple(benchmark.upper() for benchmark in benchmarks)
        snapshots = []
        missing = []
        for benchmark in normalized:
            snapshot = DEMO_BENCHMARKS.get(benchmark)
            if snapshot:
                snapshots.append(asdict(snapshot))
            else:
                missing.append(benchmark)
        return ProviderResponse.ok(
            provider=ProviderName.MOCK,
            payload={"benchmarks": snapshots, "missing": missing},
            source_url="local://demo/benchmarks",
            source_name="Q-GEAR demo benchmark snapshots",
            cached=True,
            source_date=DEMO_SOURCE_DATE,
            as_of_date=DEMO_SOURCE_DATE,
            cache_key="mock_benchmarks_" + "_".join(normalized),
            mode=DataMode.DEMO,
        )

    def series(self, series_id: str) -> ProviderResponse:
        return ProviderResponse.ok(
            provider=ProviderName.MOCK,
            payload={"series_id": series_id, "mode": "demo", "observations": []},
            source_url="local://demo/macro-series",
            source_name="Q-GEAR demo macro series",
            cached=True,
            source_date=DEMO_SOURCE_DATE,
            as_of_date=DEMO_SOURCE_DATE,
            cache_key=f"mock_macro_{series_id}",
            mode=DataMode.DEMO,
        )
