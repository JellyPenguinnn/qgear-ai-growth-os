from __future__ import annotations

from fastapi import APIRouter

from app.db.sqlite import get_settings, save_settings
from app.schemas.requests import OnboardingSettingsRequest

router = APIRouter(prefix="/settings", tags=["settings"])


DEFAULT_SETTINGS = {
    "starting_capital": 10_000,
    "base_currency": "USD",
    "country": "Singapore",
    "risk_style": "BALANCED",
    "target_cagr_low_pct": 18,
    "target_cagr_high_pct": 22,
    "hard_drawdown_limit_pct": 35,
    "cash_buffer_pct": 15,
    "max_single_stock_pct": 15,
    "benchmarks": ["SPY", "QQQ", "XLK", "SMH"],
    "broker_mode": "manual",
    "margin_enabled": False,
    "options_enabled": False,
    "auto_trading_enabled": False,
    "disclaimer": "This tool is for personal research and educational use only. It does not provide licensed financial advice, tax advice, or legal advice. Final investment decisions are made by the user.",
}


@router.get("")
def read_settings() -> dict:
    return get_settings() or DEFAULT_SETTINGS


@router.post("")
def update_settings(payload: OnboardingSettingsRequest) -> dict:
    data = payload.model_dump()
    data["margin_enabled"] = False
    data["options_enabled"] = False
    data["auto_trading_enabled"] = False
    data["disclaimer"] = DEFAULT_SETTINGS["disclaimer"]
    return save_settings(data)
