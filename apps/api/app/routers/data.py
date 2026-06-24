from __future__ import annotations

from fastapi import APIRouter

from app.routers.financials import data_quality_for_ticker
from app.routers.macro import DEFAULT_FRED_SERIES
from app.routers.providers import provider_status

router = APIRouter(prefix="/data", tags=["data-quality"])


@router.get("/quality/{ticker}")
def ticker_data_quality(ticker: str) -> dict:
    return data_quality_for_ticker(ticker)


@router.get("/health")
def data_health() -> dict:
    providers = provider_status()
    provider_names = providers["providers"]
    return {
        "mode": providers["mode"],
        "status": "review_only",
        "provider_status": providers,
        "sections": [
            {
                "name": "SEC financials",
                "status": provider_names["company_facts"],
                "can_support_action": providers["mode"] != "demo",
                "note": "SEC data improves source quality, but cannot create buy/add without Q-GEAR gates.",
            },
            {
                "name": "Price and technical",
                "status": f"prices={provider_names['prices']}; history={provider_names.get('price_history', 'not configured')}",
                "can_support_action": False,
                "note": "Technical data is timing/risk confirmation only.",
            },
            {
                "name": "Macro and energy",
                "status": f"FRED={provider_names['fred']}; EIA={provider_names['eia']}",
                "can_support_action": False,
                "note": "Macro and energy context is review-only.",
            },
            {
                "name": "AI assistant",
                "status": providers["ai"]["provider_metadata"]["status"],
                "can_support_action": False,
                "note": "AI drafts require explicit user action and verification before saving evidence.",
            },
        ],
        "missing_keys": {
            "fred": "FRED_API_KEY" if provider_names["fred"] == "FredProvider" else None,
            "eia": "EIA_API_KEY" if provider_names["eia"] == "EiaProvider" else None,
        },
        "default_fred_series": DEFAULT_FRED_SERIES,
        "what_can_support_action": [
            "Provider-verified SEC/company evidence can support source-quality gates only when live/mixed mode and all Q-GEAR gates pass.",
            "User-verified evidence with source date, disproof condition, and medium/high confidence can support action gates.",
        ],
        "review_only_data": [
            "Price history and technical regime",
            "Benchmark relative strength",
            "Macro and energy context",
            "AI draft output before user verification",
        ],
        "not_trade_instruction": True,
    }
