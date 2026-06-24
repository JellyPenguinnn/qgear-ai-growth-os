from __future__ import annotations

from fastapi import APIRouter

from app.routers.providers import _bundle
from app.serializers import to_jsonable

router = APIRouter(prefix="/macro", tags=["macro"])

DEFAULT_FRED_SERIES = ("FEDFUNDS", "DGS10", "DGS2", "CPIAUCSL", "UNRATE")


@router.get("/status")
def macro_status() -> dict:
    response = _bundle().fred_provider.series(DEFAULT_FRED_SERIES[0])
    return to_jsonable(
        {
            "status": response.status,
            "provider": response.metadata.provider,
            "metadata": response.metadata,
            "default_series": DEFAULT_FRED_SERIES,
            "review_only": True,
            "not_trade_instruction": True,
        }
    )


@router.get("/fred/{series_id}")
def fred_series(series_id: str) -> dict:
    response = _bundle().fred_provider.series(series_id.upper())
    return to_jsonable(
        {
            "status": response.status,
            "series_id": series_id.upper(),
            "payload": response.payload,
            "metadata": response.metadata,
            "review_only": True,
            "not_trade_instruction": True,
        }
    )
