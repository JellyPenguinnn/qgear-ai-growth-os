from __future__ import annotations

from dataclasses import dataclass

from qgear_core.enums import EarningsThesisChange
from qgear_core.models import Evidence


@dataclass(frozen=True)
class EarningsReview:
    ticker: str
    fiscal_period: str
    report_date: str
    revenue_surprise_pct: float | None = None
    eps_surprise_pct: float | None = None
    guidance_raised: bool = False
    guidance_cut: bool = False
    guidance_cut_structural: bool = False
    revenue_growth_accelerated: bool = False
    ai_evidence_improved: bool = False
    segment_growth_improved: bool = False
    margin_expanded: bool = False
    margin_deteriorated: bool = False
    fcf_improved: bool = False
    fcf_deteriorated: bool = False
    management_tone: str = "neutral"
    evidence: tuple[Evidence, ...] = ()


def classify_earnings_review(review: EarningsReview) -> EarningsThesisChange:
    """Classify thesis impact from sourced earnings evidence.

    This classifier is deliberately conservative. Positive surprises alone do
    not create action; they only classify the evidence update that later flows
    through thesis, valuation, technical, and portfolio gates.
    """

    if review.guidance_cut_structural:
        return EarningsThesisChange.BROKEN

    negative_count = sum(
        (
            review.guidance_cut,
            review.margin_deteriorated,
            review.fcf_deteriorated,
            (review.revenue_surprise_pct or 0) < -5,
            (review.eps_surprise_pct or 0) < -5,
        )
    )
    if negative_count >= 2:
        return EarningsThesisChange.WEAKENED

    positive_count = sum(
        (
            review.guidance_raised,
            review.revenue_growth_accelerated,
            review.ai_evidence_improved,
            review.segment_growth_improved,
            review.margin_expanded,
            review.fcf_improved,
            (review.revenue_surprise_pct or 0) > 5,
            (review.eps_surprise_pct or 0) > 5,
        )
    )
    if positive_count >= 3 and negative_count == 0 and bool(review.evidence):
        return EarningsThesisChange.STRENGTHENED

    return EarningsThesisChange.UNCHANGED
