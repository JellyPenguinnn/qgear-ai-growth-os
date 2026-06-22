from __future__ import annotations

from collections import defaultdict

from fastapi import APIRouter, HTTPException

from app.db.sqlite import add_position, list_positions
from app.schemas.requests import PortfolioPositionRequest
from qgear_core.demo import get_company
from qgear_core.risk import classify_drawdown_mode

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("")
def portfolio_summary() -> dict:
    positions = list_positions()
    total_market_value = round(sum(position["market_value"] for position in positions), 2)
    cash = 1_500 if positions else 10_000
    total_equity = round(total_market_value + cash, 2)
    layer_weights: dict[str, float] = defaultdict(float)
    max_position = 0

    for position in positions:
        company = get_company(position["ticker"])
        if company and total_equity:
            layer_weights[company.ai_layer.value] += position["market_value"] / total_equity * 100
        max_position = max(max_position, position["position_weight_pct"])

    drawdown_pct = 4
    return {
        "mode": "manual_demo",
        "cash": cash,
        "total_equity": total_equity,
        "drawdown_pct": drawdown_pct,
        "drawdown_mode": classify_drawdown_mode(drawdown_pct).value,
        "single_stock_concentration_pct": round(max_position, 2),
        "ai_layer_concentration": {key: round(value, 2) for key, value in layer_weights.items()},
        "expected_portfolio_irr_pct": 16.8 if positions else 0,
        "benchmark_comparison_placeholders": {
            "SPY": "pending local market data",
            "QQQ": "pending local market data",
            "XLK": "pending local market data",
            "SMH": "pending local market data",
        },
        "positions": positions,
    }


@router.post("/positions")
def create_position(payload: PortfolioPositionRequest) -> dict:
    if not get_company(payload.ticker):
        raise HTTPException(status_code=404, detail="Ticker not found in demo universe")
    return add_position(payload.model_dump())
