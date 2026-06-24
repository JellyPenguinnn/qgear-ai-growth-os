from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.core.config import settings
from app.core.ticker_map import ticker_cik
from app.serializers import to_jsonable
from qgear_ai.providers import build_ai_provider
from qgear_ai.service import AIResearchService
from qgear_ingest.providers.base import DataMode, ProviderResponse
from qgear_ingest.providers.factory import ProviderConfig, build_provider_bundle

router = APIRouter(prefix="/providers", tags=["providers"])

DEFAULT_BENCHMARKS = ("SPY", "QQQ", "XLK", "SMH")


def _data_mode() -> DataMode:
    environment = settings.environment.lower()
    if environment == "live":
        return DataMode.LIVE
    if environment == "mixed":
        return DataMode.MIXED
    return DataMode.DEMO


def _bundle():
    return build_provider_bundle(
        ProviderConfig(
            mode=_data_mode(),
            cache_dir=settings.cache_dir,
            sec_user_agent=settings.sec_user_agent,
            sec_max_requests_per_second=settings.sec_max_requests_per_second,
            price_provider=settings.price_provider,
            alpha_vantage_api_key=settings.alpha_vantage_api_key,
            fred_api_key=settings.fred_api_key,
            eia_api_key=settings.eia_api_key,
        )
    )


def _clean_cik(cik: str) -> str:
    normalized = cik.strip().lstrip("0") or "0"
    if not normalized.isdigit():
        raise HTTPException(status_code=422, detail="CIK must contain only digits")
    return normalized.zfill(10)


def _split_symbols(value: str) -> tuple[str, ...]:
    symbols = tuple(symbol.strip().upper() for symbol in value.split(",") if symbol.strip())
    if not symbols:
        raise HTTPException(status_code=422, detail="At least one symbol is required")
    return symbols


def _response(response: ProviderResponse) -> dict:
    return to_jsonable({"payload": response.payload, "metadata": response.metadata})


@router.get("/status")
def provider_status() -> dict:
    payload = _bundle().status_payload()
    payload["ai"] = AIResearchService(
        build_ai_provider(settings.ai_provider, api_key=settings.openai_api_key, model=settings.ai_model)
    ).status()
    return payload


@router.get("/company-facts/{cik}")
def company_facts(cik: str) -> dict:
    normalized = _clean_cik(cik)
    response = _bundle().company_facts_provider.company_facts(normalized)
    return _response(response)


@router.get("/submissions/{cik}")
def submissions(cik: str) -> dict:
    normalized = _clean_cik(cik)
    response = _bundle().filings_provider.submissions(normalized)
    return _response(response)


@router.get("/filings/{cik}")
def filing_metadata(cik: str, limit: int = Query(default=20, ge=1, le=100)) -> dict:
    normalized = _clean_cik(cik)
    response = _bundle().filings_provider.filing_metadata(normalized, limit=limit)
    return _response(response)


@router.get("/prices")
def price_snapshots(tickers: str = Query(default="NVDA,AMD,MU")) -> dict:
    response = _bundle().price_provider.daily_prices(_split_symbols(tickers))
    return _response(response)


@router.get("/benchmarks")
def benchmark_snapshots(benchmarks: str = Query(default=",".join(DEFAULT_BENCHMARKS))) -> dict:
    response = _bundle().benchmark_provider.benchmark_snapshots(_split_symbols(benchmarks))
    return _response(response)


@router.post("/prices/refresh/{ticker}")
def refresh_price_history(ticker: str) -> dict:
    normalized = ticker.upper()
    response = _bundle().price_history_provider.daily_adjusted_history(normalized)
    return to_jsonable(
        {
            "status": response.status,
            "ticker": normalized,
            "metadata": response.metadata,
            "rows": len(response.payload.get("prices", [])),
            "explicit_refresh": True,
            "not_trade_instruction": True,
            "note": "Price data can confirm timing/risk only; it cannot create a thesis or buy/add action.",
        }
    )


@router.post("/benchmarks/refresh")
def refresh_benchmarks(benchmarks: str = Query(default=",".join(DEFAULT_BENCHMARKS))) -> dict:
    symbols = _split_symbols(benchmarks)
    bundle = _bundle()
    snapshots = bundle.benchmark_provider.benchmark_snapshots(symbols)
    histories = {
        symbol: bundle.price_history_provider.daily_adjusted_history(symbol).metadata
        for symbol in symbols
    }
    return to_jsonable(
        {
            "status": snapshots.status,
            "benchmarks": symbols,
            "snapshot_metadata": snapshots.metadata,
            "history_metadata": histories,
            "explicit_refresh": True,
            "not_trade_instruction": True,
        }
    )


@router.post("/sec/refresh/{ticker}")
def refresh_sec_ticker(ticker: str) -> dict:
    normalized = ticker.upper()
    cik = ticker_cik(normalized)
    if not cik:
        return {
            "status": "missing_mapping",
            "ticker": normalized,
            "message": "No CIK mapping is available for this ticker.",
            "not_trade_instruction": True,
        }

    bundle = _bundle()
    facts = bundle.company_facts_provider.company_facts(cik)
    filings = bundle.filings_provider.filing_metadata(cik, limit=5)
    return to_jsonable(
        {
            "status": "ok" if facts.status.value == "ok" and filings.status.value == "ok" else "provider_issue",
            "ticker": normalized,
            "cik": cik,
            "mode": bundle.mode,
            "company_facts": {"metadata": facts.metadata},
            "filings": {"metadata": filings.metadata, "payload": filings.payload},
            "explicit_refresh": True,
            "not_trade_instruction": True,
        }
    )
