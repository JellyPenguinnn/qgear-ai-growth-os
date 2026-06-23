from __future__ import annotations

from collections import defaultdict
from datetime import date

from fastapi import APIRouter, HTTPException

from app.db.sqlite import add_position, list_positions
from app.schemas.requests import PortfolioPositionRequest
from qgear_core.demo import get_company
from qgear_core.risk import classify_drawdown_mode

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

BENCHMARKS = ("SPY", "QQQ", "XLK", "SMH")


def _benchmark_placeholders() -> list[dict]:
    return [
        {
            "benchmark": benchmark,
            "status": "pending_local_market_data",
            "total_return_pct": None,
            "relative_return_pct": None,
            "note": "Benchmark comparison placeholder until local price history is configured.",
        }
        for benchmark in BENCHMARKS
    ]


@router.get("")
def portfolio_summary() -> dict:
    raw_positions = list_positions()
    total_market_value = round(sum(position["market_value"] for position in raw_positions), 2)
    cash = 1_500 if raw_positions else 10_000
    total_equity = round(total_market_value + cash, 2)
    layer_weights: dict[str, float] = defaultdict(float)
    max_position = 0
    expected_irr_weighted = 0.0
    expected_irrs: list[float] = []
    enriched_positions: list[dict] = []
    concentration_risks: list[dict] = []
    blocked_adds: list[dict] = []
    review_calendar: list[dict] = []

    for position in raw_positions:
        company = get_company(position["ticker"])
        position_weight = round((position["market_value"] / total_equity * 100) if total_equity else 0, 2)
        enriched = {**position, "position_weight_pct": position_weight}
        if company and total_equity:
            layer_weights[company.ai_layer.value] += position_weight
            expected_irr_weighted += company.metrics.expected_irr_base_pct * position["market_value"] / total_equity
            expected_irrs.append(company.metrics.expected_irr_base_pct)
            enriched["ai_layer"] = company.ai_layer.value
            enriched["expected_irr_base_pct"] = company.metrics.expected_irr_base_pct
            if company.decision.blocked_reasons:
                blocked_adds.append(
                    {
                        "ticker": company.ticker,
                        "reason": company.decision.blocked_reasons[0],
                        "state": company.status.value,
                        "trade_instruction": False,
                    }
                )
        max_position = max(max_position, position_weight)
        if position_weight >= 15:
            concentration_risks.append(
                {
                    "ticker": position["ticker"],
                    "severity": "high",
                    "message": "Position is at or above the 15% single-stock cap.",
                    "trade_instruction": False,
                }
            )
        elif position_weight >= 12:
            concentration_risks.append(
                {
                    "ticker": position["ticker"],
                    "severity": "medium",
                    "message": "Position is approaching the 15% single-stock cap.",
                    "trade_instruction": False,
                }
            )
        if position.get("next_review_date"):
            review_calendar.append(
                {
                    "ticker": position["ticker"],
                    "next_review_date": position["next_review_date"],
                    "status": position["status"],
                    "thesis_status": position["thesis_status"],
                    "review_type": "THESIS_OR_POSITION_REVIEW",
                    "trade_instruction": False,
                }
            )
        enriched_positions.append(enriched)

    drawdown_pct = 4
    drawdown_mode = classify_drawdown_mode(drawdown_pct).value
    if drawdown_mode != "NORMAL":
        concentration_risks.append(
            {
                "ticker": None,
                "severity": "medium",
                "message": f"Portfolio drawdown mode is {drawdown_mode}; new risk-taking needs review.",
                "trade_instruction": False,
            }
        )
    review_calendar = sorted(review_calendar, key=lambda item: item["next_review_date"] or "9999-12-31")
    return {
        "mode": "manual_demo",
        "manual_only": True,
        "cash": cash,
        "cash_pct": round((cash / total_equity * 100) if total_equity else 0, 2),
        "total_equity": total_equity,
        "drawdown_pct": drawdown_pct,
        "drawdown_mode": drawdown_mode,
        "single_stock_concentration_pct": round(max_position, 2),
        "ai_layer_concentration": {key: round(value, 2) for key, value in layer_weights.items()},
        "expected_portfolio_irr_pct": round(expected_irr_weighted, 2) if raw_positions else 0,
        "expected_irr_distribution": {
            "min_pct": round(min(expected_irrs), 2) if expected_irrs else 0,
            "max_pct": round(max(expected_irrs), 2) if expected_irrs else 0,
            "weighted_pct": round(expected_irr_weighted, 2) if raw_positions else 0,
            "note": "Expected IRR is a research assumption, not a promise.",
        },
        "benchmark_comparison": _benchmark_placeholders(),
        "benchmark_comparison_placeholders": {benchmark: "pending local market data" for benchmark in BENCHMARKS},
        "concentration_risks": concentration_risks,
        "blocked_adds": blocked_adds,
        "review_calendar": review_calendar,
        "positions": enriched_positions,
        "as_of": date.today().isoformat(),
        "risk_note": "Portfolio analytics are local manual review prompts only. Q-GEAR does not execute trades.",
    }


@router.post("/positions")
def create_position(payload: PortfolioPositionRequest) -> dict:
    if not get_company(payload.ticker):
        raise HTTPException(status_code=404, detail="Ticker not found in demo universe")
    return add_position(payload.model_dump())
