from __future__ import annotations

from qgear_core.enums import AILayer, Confidence, EarningsThesisChange, TechnicalRegime
from qgear_core.models import ScoreBreakdown, StockMetrics


WEIGHTS = {
    "ai_relevance": 12,
    "business_quality": 18,
    "revenue_earnings_acceleration": 18,
    "earnings_guidance_revisions": 17,
    "valuation_expected_irr": 15,
    "technical_trend": 10,
    "portfolio_fit": 10,
}


def _bounded(value: float, maximum: float) -> float:
    return round(max(0, min(maximum, value)), 2)


def _linear(value: float, low: float, high: float, maximum: float) -> float:
    if value <= low:
        return 0
    if value >= high:
        return maximum
    return (value - low) / (high - low) * maximum


def score_from_metrics(metrics: StockMetrics, portfolio_fit_score: float = 8) -> ScoreBreakdown:
    """Create a deterministic 100-point Q-GEAR score from local/demo metrics.

    The score is deliberately descriptive. It does not create a buy/add action
    without hard gates, evidence freshness, and risk budget checks.
    """

    if metrics.ai_layer == AILayer.NOT_RELEVANT:
        ai_score = 0
    else:
        confidence_base = {
            Confidence.LOW: 3,
            Confidence.MEDIUM: 7,
            Confidence.HIGH: 9,
        }[metrics.classification_confidence]
        evidence_bonus = 1.5 if metrics.ai_evidence_improved else 0
        growth_bonus = _linear(metrics.revenue_growth_pct, 0, 30, 1.5)
        ai_score = _bounded(confidence_base + evidence_bonus + growth_bonus, 12)

    quality_score = _bounded(
        _linear(metrics.gross_margin_pct, 25, 75, 5)
        + _linear(metrics.operating_margin_pct, 5, 40, 4)
        + _linear(metrics.fcf_margin_pct, 0, 35, 4)
        + _linear(metrics.roic_pct, 5, 35, 3)
        + (2 if metrics.net_debt_to_ebitda <= 1 else 1 if metrics.net_debt_to_ebitda <= 2 else 0),
        18,
    )

    acceleration_score = _bounded(
        _linear(metrics.revenue_growth_pct, 0, 40, 8)
        + _linear(metrics.revenue_growth_acceleration_pct, -5, 15, 5)
        + (2 if metrics.ai_evidence_improved else 0)
        + (1.5 if metrics.margin_expanded else 0)
        + (1.5 if metrics.fcf_improved else 0),
        18,
    )

    earnings_base = {
        EarningsThesisChange.STRENGTHENED: 9,
        EarningsThesisChange.UNCHANGED: 5,
        EarningsThesisChange.WEAKENED: 1.5,
        EarningsThesisChange.BROKEN: 0,
    }[metrics.latest_earnings_change]
    earnings_score = _bounded(
        earnings_base
        + (3 if metrics.guidance_raised else 0)
        + (2 if metrics.ai_evidence_improved else 0)
        + (1.5 if metrics.margin_expanded else 0)
        + (1.5 if metrics.fcf_improved else 0),
        17,
    )

    valuation_score = _bounded(_linear(metrics.expected_irr_base_pct, 5, 25, 15), 15)

    technical_base = {
        TechnicalRegime.SUPPORTIVE: 6,
        TechnicalRegime.STABILISING: 5,
        TechnicalRegime.WEAKENING: 2,
        TechnicalRegime.BROKEN: 0,
    }[metrics.technical_regime]
    technical_score = _bounded(
        technical_base
        + _linear(metrics.relative_strength_pct, -20, 30, 3)
        - _linear(metrics.drawdown_from_high_pct, 20, 60, 2),
        10,
    )

    portfolio_score = _bounded(portfolio_fit_score - metrics.red_flag_count, 10)

    return ScoreBreakdown(
        ai_relevance=ai_score,
        business_quality=quality_score,
        revenue_earnings_acceleration=acceleration_score,
        earnings_guidance_revisions=earnings_score,
        valuation_expected_irr=valuation_score,
        technical_trend=technical_score,
        portfolio_fit=portfolio_score,
    )
