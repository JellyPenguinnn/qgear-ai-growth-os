from __future__ import annotations

from fastapi import APIRouter

from app.routers.providers import DEFAULT_BENCHMARKS, _bundle
from app.serializers import to_jsonable
from qgear_ingest.providers.technical import calculate_technical_snapshot

router = APIRouter(tags=["prices-technical"])


@router.get("/prices/{ticker}")
def price_history(ticker: str) -> dict:
    normalized = ticker.upper()
    response = _bundle().price_history_provider.daily_adjusted_history(normalized)
    return to_jsonable(
        {
            "status": response.status,
            "ticker": normalized,
            "prices": response.payload.get("prices", []),
            "missing": response.payload.get("missing", []),
            "metadata": response.metadata,
            "not_trade_instruction": True,
            "note": "Price history is timing/risk context only and cannot create buy/add permission.",
        }
    )


@router.get("/technical/{ticker}")
def technical_snapshot(ticker: str) -> dict:
    normalized = ticker.upper()
    bundle = _bundle()
    price_response = bundle.price_history_provider.daily_adjusted_history(normalized)
    benchmark_responses = {
        benchmark: bundle.price_history_provider.daily_adjusted_history(benchmark)
        for benchmark in DEFAULT_BENCHMARKS
    }
    try:
        snapshot = calculate_technical_snapshot(
            ticker=normalized,
            price_response=price_response,
            benchmark_responses=benchmark_responses,
        )
    except ValueError as exc:
        return to_jsonable(
            {
                "status": "error",
                "ticker": normalized,
                "message": str(exc),
                "price_metadata": price_response.metadata,
                "not_trade_instruction": True,
            }
        )
    return to_jsonable(
        {
            "status": "ok",
            "ticker": normalized,
            "technical": snapshot,
            "not_trade_instruction": True,
            "note": "Technical regime is risk/timing confirmation only and cannot create the investment thesis.",
        }
    )
