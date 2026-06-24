from __future__ import annotations

from fastapi import APIRouter

from app.routers.providers import _bundle
from app.serializers import to_jsonable

router = APIRouter(prefix="/energy", tags=["energy"])

DEFAULT_EIA_CONTEXT_ROUTE = "electricity/retail-sales"


@router.get("/status")
def energy_status() -> dict:
    response = _bundle().eia_provider.series(DEFAULT_EIA_CONTEXT_ROUTE)
    return to_jsonable(
        {
            "status": response.status,
            "provider": response.metadata.provider,
            "metadata": response.metadata,
            "default_context_route": DEFAULT_EIA_CONTEXT_ROUTE,
            "review_only": True,
            "not_trade_instruction": True,
        }
    )


@router.get("/eia/context")
def eia_context() -> dict:
    response = _bundle().eia_provider.series(DEFAULT_EIA_CONTEXT_ROUTE)
    return to_jsonable(
        {
            "status": response.status,
            "context": "US electricity and energy context for AI infrastructure review.",
            "payload": response.payload,
            "metadata": response.metadata,
            "review_only": True,
            "not_trade_instruction": True,
        }
    )
