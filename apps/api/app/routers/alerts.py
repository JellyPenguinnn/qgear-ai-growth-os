from __future__ import annotations

from datetime import date

from fastapi import APIRouter

from app.serializers import to_jsonable
from qgear_core.demo import DEMO_LAST_REVIEWED, DEMO_UNIVERSE
from qgear_core.enums import EarningsThesisChange, TechnicalRegime

router = APIRouter(prefix="/alerts", tags=["alerts"])

ALERT_RULES = (
    "FILING_REVIEW",
    "EARNINGS_THESIS_RISK",
    "STALE_EVIDENCE",
    "TECHNICAL_BREAK",
    "CONCENTRATION_RISK",
    "DRAWDOWN_RISK",
    "THESIS_REVIEW_DUE",
)


def _alert(
    *,
    alert_type: str,
    severity: str,
    message: str,
    ticker: str | None = None,
    source: str = "Q-GEAR local rules",
    source_date: str = DEMO_LAST_REVIEWED,
    confidence: str = "MEDIUM",
    disproves_if: str = "Fresh sourced evidence shows the condition no longer applies.",
) -> dict:
    return {
        "type": alert_type,
        "severity": severity,
        "ticker": ticker,
        "message": message,
        "source": source,
        "source_date": source_date,
        "confidence": confidence,
        "disproves_if": disproves_if,
        "trade_instruction": False,
        "next_step": "Review evidence and journal the decision; do not auto-trade.",
    }


def build_alerts() -> dict:
    as_of = date.fromisoformat(DEMO_LAST_REVIEWED)
    generated: list[dict] = [
        _alert(
            alert_type="FILING_REVIEW",
            severity="info",
            message="Review latest SEC filings before changing any thesis or valuation case.",
            source="SEC EDGAR provider metadata",
            confidence="HIGH",
            disproves_if="Provider metadata confirms filings were reviewed and no thesis-changing facts were found.",
        )
    ]
    for company in DEMO_UNIVERSE:
        if company.metrics.latest_earnings_change in {EarningsThesisChange.WEAKENED, EarningsThesisChange.BROKEN}:
            generated.append(
                _alert(
                    alert_type="EARNINGS_THESIS_RISK",
                    severity="high",
                    ticker=company.ticker,
                    message=f"{company.ticker} earnings status is {company.metrics.latest_earnings_change.value}; buy/add is blocked until evidence repairs the thesis.",
                    confidence=company.classification_confidence.value,
                    disproves_if="Next earnings review strengthens the thesis with sourced evidence.",
                )
            )
        if company.metrics.technical_regime == TechnicalRegime.BROKEN:
            generated.append(
                _alert(
                    alert_type="TECHNICAL_BREAK",
                    severity="medium",
                    ticker=company.ticker,
                    message=f"{company.ticker} technical regime is broken; technicals can only confirm timing/risk, not create a thesis.",
                    confidence="MEDIUM",
                    disproves_if="Technical regime stabilises while fundamental thesis remains intact.",
                )
            )
        evidence_date = date.fromisoformat(company.evidence[0].source_date)
        if (as_of - evidence_date).days > 90:
            generated.append(
                _alert(
                    alert_type="STALE_EVIDENCE",
                    severity="medium",
                    ticker=company.ticker,
                    message=f"{company.ticker} evidence is stale and must be refreshed before action.",
                    confidence="HIGH",
                    disproves_if="New sourced evidence updates the thesis and review date.",
                )
            )
        if any("concentration" in reason.lower() for reason in company.decision.blocked_reasons):
            generated.append(
                _alert(
                    alert_type="CONCENTRATION_RISK",
                    severity="high",
                    ticker=company.ticker,
                    message=f"{company.ticker} is blocked by concentration risk.",
                    confidence="HIGH",
                    disproves_if="Position weight falls below the risk budget and the thesis remains valid.",
                )
            )
    generated.append(
        _alert(
            alert_type="DRAWDOWN_RISK",
            severity="info",
            message="Portfolio drawdown rule is active; current demo drawdown is normal.",
            confidence="MEDIUM",
            disproves_if="Drawdown moves into caution, risk-control, defensive, or hard-audit mode.",
        )
    )
    generated.append(
        _alert(
            alert_type="THESIS_REVIEW_DUE",
            severity="info",
            message="Review dates should be checked before approving new thesis-driven actions.",
            confidence="MEDIUM",
            disproves_if="All approved theses have future review dates and current evidence.",
        )
    )
    return to_jsonable(
        {
            "as_of": DEMO_LAST_REVIEWED,
            "rules": ALERT_RULES,
            "alerts": generated,
            "note": "Alerts are local review prompts only. They are never trade instructions.",
        }
    )


@router.get("")
def alerts() -> dict:
    return build_alerts()
