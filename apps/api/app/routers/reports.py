from __future__ import annotations

from fastapi import APIRouter

from app.db.sqlite import list_journal_entries, list_positions
from app.routers.alerts import ALERT_RULES, build_alerts
from app.routers.journal import build_journal_analytics
from qgear_core.demo import DEMO_UNIVERSE

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/daily")
def daily_brief() -> dict:
    changed = [company for company in DEMO_UNIVERSE if company.decision.action_allowed]
    alerts = build_alerts()["alerts"]
    return {
        "title": "Daily Brief",
        "default_action": "No action justified today unless evidence changed.",
        "evidence_changes": [
            {
                "ticker": company.ticker,
                "state": company.status.value,
                "reason": company.decision.reasons[0],
                "source": company.evidence[0].source,
                "source_date": company.evidence[0].source_date,
                "confidence": company.evidence[0].confidence.value,
                "disproves_if": company.evidence[0].disproves_if,
            }
            for company in changed[:5]
        ],
        "top_alerts": alerts[:5],
        "alert_note": "Alerts are review prompts only and never trade instructions.",
        "disclaimer": "Demo data only. This is not financial advice.",
    }


@router.get("/weekly")
def weekly_ranking_report() -> dict:
    ranked = sorted(DEMO_UNIVERSE, key=lambda company: company.score.total, reverse=True)
    return {
        "title": "Weekly Ranking Report",
        "rankings": [
            {
                "rank": index + 1,
                "ticker": company.ticker,
                "score": company.score.total,
                "decision_state": company.status.value,
                "ai_layer": company.ai_layer.value,
            }
            for index, company in enumerate(ranked[:15])
        ],
        "note": "High score is not an action. Hard gates and risk budget still apply.",
    }


@router.get("/monthly")
def monthly_portfolio_review() -> dict:
    return {
        "title": "Monthly Portfolio Review",
        "positions": list_positions(),
        "journal_entries": list_journal_entries(),
        "journal_analytics": build_journal_analytics(),
        "alerts": build_alerts()["alerts"][:10],
        "review_prompts": [
            "Did decisions follow thesis and invalidation rules?",
            "Did the portfolio beat SPY, QQQ, XLK, and SMH placeholders?",
            "Is concentration inside the 15% single-stock cap?",
        ],
    }


@router.get("/quarterly")
def quarterly_earnings_review() -> dict:
    weakened = [company for company in DEMO_UNIVERSE if company.metrics.latest_earnings_change.value in {"WEAKENED", "BROKEN"}]
    earnings_alerts = [alert for alert in build_alerts()["alerts"] if alert["type"] == "EARNINGS_THESIS_RISK"]
    return {
        "title": "Quarterly Earnings Review",
        "weakened_or_broken": [{"ticker": company.ticker, "state": company.status.value} for company in weakened],
        "earnings_alerts": earnings_alerts,
        "review_prompts": [
            "Which theses were strengthened by earnings?",
            "Which invalidation rules moved closer to triggering?",
            "Which valuation cases need revision?",
        ],
    }


@router.get("/annual")
def annual_strategy_audit() -> dict:
    return {
        "title": "Annual Strategy Audit",
        "alert_rules": ALERT_RULES,
        "journal_analytics": build_journal_analytics(),
        "benchmark_policy": "Compare against SPY, QQQ, XLK, and SMH before judging process quality.",
        "backtest_note": "Backtests must use fixture or timestamped historical data with no look-ahead bias.",
        "audit_items": [
            "Compare total return against SPY, QQQ, XLK, and SMH.",
            "Review drawdown versus 25-30% normal budget and 35% hard limit.",
            "Check whether journal outcomes show process drift.",
            "Reassess whether AI infrastructure classifications remained evidence-based.",
        ],
    }
