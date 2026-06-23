from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date

from fastapi import APIRouter

from app.serializers import to_jsonable
from qgear_core.demo import DEMO_LAST_REVIEWED, DEMO_UNIVERSE
from qgear_core.enums import DecisionState, EarningsThesisChange, TechnicalRegime
from qgear_core.models import UniverseCompany

router = APIRouter(prefix="/pipeline", tags=["pipeline"])

PIPELINE_ORDER: tuple[DecisionState, ...] = (
    DecisionState.REJECTED,
    DecisionState.RESEARCH_CANDIDATE,
    DecisionState.WATCHLIST,
    DecisionState.APPROVED_THESIS,
    DecisionState.APPROVED_VALUATION_ZONE,
    DecisionState.TECHNICAL_WAIT,
    DecisionState.STARTER_ALLOWED,
    DecisionState.ADD_ALLOWED,
    DecisionState.HOLD,
    DecisionState.TRIM_CANDIDATE,
    DecisionState.EXIT_THESIS_BROKEN,
    DecisionState.BLOCKED_BY_RISK,
    DecisionState.NO_ACTION,
)

STATE_DESCRIPTIONS: dict[DecisionState, str] = {
    DecisionState.REJECTED: "AI relevance or quality evidence is not sufficient.",
    DecisionState.RESEARCH_CANDIDATE: "Worth learning about, but thesis work is incomplete.",
    DecisionState.WATCHLIST: "Research continues; a hard gate blocks action.",
    DecisionState.APPROVED_THESIS: "Thesis exists, but more underwriting is required.",
    DecisionState.APPROVED_VALUATION_ZONE: "Valuation looks plausible, but action evidence is missing.",
    DecisionState.TECHNICAL_WAIT: "Fundamental work may be valid; technical confirmation is absent.",
    DecisionState.STARTER_ALLOWED: "All gates clear for a manually reviewed starter, if the user confirms.",
    DecisionState.ADD_ALLOWED: "All gates clear for a manually reviewed add, if the user confirms.",
    DecisionState.HOLD: "Owned or approved name remains under monitoring.",
    DecisionState.TRIM_CANDIDATE: "Risk, concentration, or thesis pressure requires review.",
    DecisionState.EXIT_THESIS_BROKEN: "Thesis may be broken; invalidation review is required.",
    DecisionState.BLOCKED_BY_RISK: "Portfolio risk budget blocks normal risk-taking.",
    DecisionState.NO_ACTION: "No action is justified by the current evidence.",
}


def _is_stale(company: UniverseCompany) -> bool:
    evidence_date = date.fromisoformat(company.evidence[0].source_date)
    as_of = date.fromisoformat(DEMO_LAST_REVIEWED)
    return (as_of - evidence_date).days > 90


def _review_flags(company: UniverseCompany) -> list[str]:
    flags: list[str] = []
    blockers = " ".join(company.decision.blocked_reasons).lower()

    if "no approved thesis" in blockers:
        flags.append("THESIS_MISSING")
    if "invalidation" in blockers:
        flags.append("INVALIDATION_RULE_MISSING")
    if company.metrics.latest_earnings_change in {EarningsThesisChange.WEAKENED, EarningsThesisChange.BROKEN}:
        flags.append("EARNINGS_REVIEW_DUE")
    if company.metrics.expected_irr_base_pct < 15:
        flags.append("VALUATION_HURDLE_FAILED")
    if company.metrics.technical_regime == TechnicalRegime.BROKEN:
        flags.append("TECHNICAL_BROKEN")
    if company.metrics.technical_regime == TechnicalRegime.WEAKENING:
        flags.append("TECHNICAL_WEAKENING")
    if _is_stale(company):
        flags.append("EVIDENCE_STALE")
    if "concentration" in blockers:
        flags.append("CONCENTRATION_RISK")
    if "drawdown" in blockers:
        flags.append("DRAWDOWN_RISK")
    if company.decision.action_allowed:
        flags.append("JOURNAL_REVIEW_REQUIRED")

    return flags


def _next_task(company: UniverseCompany, flags: list[str]) -> str:
    if "EARNINGS_REVIEW_DUE" in flags:
        return "Complete an earnings review and decide whether the thesis is weakened or broken."
    if "THESIS_MISSING" in flags:
        return "Draft a thesis, invalidation rule, key metrics, and next review date before action."
    if "INVALIDATION_RULE_MISSING" in flags:
        return "Add a clear invalidation rule before the thesis can support any decision."
    if "VALUATION_HURDLE_FAILED" in flags:
        return "Refresh valuation assumptions; great businesses still need enough expected return."
    if "TECHNICAL_BROKEN" in flags:
        return "Wait for technical stabilisation; technicals can confirm risk, not create the thesis."
    if "CONCENTRATION_RISK" in flags:
        return "Review position size and concentration before adding any new money."
    if "EVIDENCE_STALE" in flags:
        return "Refresh sourced evidence before any action-changing decision."
    if company.decision.action_allowed:
        return "Review the journal draft, position size, and evidence provenance before any manual decision."
    if company.status == DecisionState.APPROVED_VALUATION_ZONE:
        return "Wait for fresh positive evidence and technical support before changing action state."
    if company.status == DecisionState.HOLD:
        return "Monitor thesis metrics, valuation, and next earnings review."
    if company.status == DecisionState.REJECTED:
        return "No active work unless new measurable AI infrastructure evidence appears."
    return "Review thesis, evidence, valuation, technical regime, and portfolio risk gates."


def _priority(company: UniverseCompany, flags: list[str]) -> int:
    if company.status in {DecisionState.EXIT_THESIS_BROKEN, DecisionState.TRIM_CANDIDATE, DecisionState.BLOCKED_BY_RISK}:
        return 0
    if {"EARNINGS_REVIEW_DUE", "CONCENTRATION_RISK", "DRAWDOWN_RISK"} & set(flags):
        return 1
    if {"TECHNICAL_BROKEN", "EVIDENCE_STALE", "VALUATION_HURDLE_FAILED"} & set(flags):
        return 2
    if company.decision.action_allowed:
        return 3
    return 4


def build_pipeline() -> dict:
    grouped: dict[DecisionState, list[dict]] = defaultdict(list)
    review_queue: list[dict] = []

    for company in DEMO_UNIVERSE:
        evidence = company.evidence[0]
        flags = _review_flags(company)
        item = {
            "ticker": company.ticker,
            "company_name": company.company_name,
            "ai_layer": company.ai_layer.value,
            "score": company.score.total,
            "decision_state": company.status.value,
            "action_allowed": company.decision.action_allowed,
            "trade_instruction": False,
            "primary_reason": company.decision.reasons[0] if company.decision.reasons else "No action justified by current evidence.",
            "primary_blocker": company.decision.blocked_reasons[0] if company.decision.blocked_reasons else "",
            "reasons": company.decision.reasons,
            "blockers": company.decision.blocked_reasons,
            "review_flags": flags,
            "next_task": _next_task(company, flags),
            "evidence_summary": company.evidence_summary,
            "evidence": {
                "claim": evidence.claim,
                "evidence": evidence.evidence,
                "source": evidence.source,
                "source_date": evidence.source_date,
                "confidence": evidence.confidence.value,
                "disproves_if": evidence.disproves_if,
            },
            "source_metadata": {
                "source": evidence.source,
                "source_date": evidence.source_date,
                "confidence": evidence.confidence.value,
                "disproves_if": evidence.disproves_if,
            },
            "last_reviewed": company.last_reviewed,
        }
        grouped[company.status].append(item)
        if flags or company.decision.blocked_reasons or company.decision.action_allowed:
            review_queue.append(item)

    state_counts = Counter(company.status for company in DEMO_UNIVERSE)
    states = [
        {
            "state": state.value,
            "label": state.value.replace("_", " ").title(),
            "description": STATE_DESCRIPTIONS[state],
            "count": state_counts[state],
            "items": sorted(grouped[state], key=lambda item: item["score"], reverse=True),
        }
        for state in PIPELINE_ORDER
    ]
    sorted_queue = sorted(
        review_queue,
        key=lambda item: (_priority(next(company for company in DEMO_UNIVERSE if company.ticker == item["ticker"]), item["review_flags"]), -item["score"]),
    )

    return to_jsonable(
        {
            "mode": "demo",
            "as_of": DEMO_LAST_REVIEWED,
            "default_stance": "No action justified today unless evidence changed and every hard gate clears.",
            "not_trade_instructions": True,
            "summary": {
                "total": len(DEMO_UNIVERSE),
                "review_queue_count": len(sorted_queue),
                "action_allowed_count": sum(1 for company in DEMO_UNIVERSE if company.decision.action_allowed),
                "blocked_count": sum(1 for company in DEMO_UNIVERSE if company.decision.blocked_reasons),
            },
            "states": states,
            "review_queue": sorted_queue,
        }
    )


@router.get("")
def pipeline() -> dict:
    return build_pipeline()
