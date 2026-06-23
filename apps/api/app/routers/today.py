from __future__ import annotations

from fastapi import APIRouter

from app.routers.alerts import build_alerts
from app.routers.pipeline import build_pipeline
from app.routers.portfolio import portfolio_summary
from app.routers.providers import provider_status
from qgear_core.demo import DEMO_LAST_REVIEWED, DEMO_UNIVERSE

router = APIRouter(prefix="/today", tags=["today"])


@router.get("")
def today() -> dict:
    pipeline = build_pipeline()
    portfolio = portfolio_summary()
    providers = provider_status()
    alerts = build_alerts()["alerts"]
    top_rankings = sorted(DEMO_UNIVERSE, key=lambda company: company.score.total, reverse=True)[:8]

    return {
        "mode": "demo",
        "as_of": DEMO_LAST_REVIEWED,
        "title": "Today",
        "default_stance": "No action justified today unless evidence changed and every hard gate clears.",
        "stance_reason": (
            "Score, price movement, or technical movement alone cannot create a buy/add action. "
            "The user must verify thesis, invalidation rule, fresh evidence, valuation, technical regime, and risk budget."
        ),
        "not_trade_instructions": True,
        "metrics": {
            "universe_count": len(DEMO_UNIVERSE),
            "review_queue_count": pipeline["summary"]["review_queue_count"],
            "action_allowed_count": pipeline["summary"]["action_allowed_count"],
            "blocked_count": pipeline["summary"]["blocked_count"],
            "drawdown_pct": portfolio["drawdown_pct"],
            "drawdown_mode": portfolio["drawdown_mode"],
            "total_equity": portfolio["total_equity"],
        },
        "review_queue": pipeline["review_queue"][:8],
        "pipeline_snapshot": [
            {
                "state": state["state"],
                "label": state["label"],
                "count": state["count"],
                "description": state["description"],
            }
            for state in pipeline["states"]
            if state["count"] > 0
        ],
        "top_rankings": [
            {
                "ticker": company.ticker,
                "company_name": company.company_name,
                "ai_layer": company.ai_layer.value,
                "score": company.score.total,
                "decision_state": company.status.value,
                "primary_reason": company.decision.reasons[0] if company.decision.reasons else "No action justified by current evidence.",
                "primary_blocker": company.decision.blocked_reasons[0] if company.decision.blocked_reasons else "",
                "trade_instruction": False,
            }
            for company in top_rankings
        ],
        "alerts": alerts[:6],
        "provider_status": providers,
        "safety": {
            "auto_trading": "disabled",
            "margin": "disabled",
            "options": "disabled_in_mvp",
            "daily_stance": "review_only",
        },
    }
