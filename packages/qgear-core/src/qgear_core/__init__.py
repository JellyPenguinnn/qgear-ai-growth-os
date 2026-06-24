"""Core domain logic for Q-GEAR AI Growth OS."""

from qgear_core.decision import evaluate_decision
from qgear_core.evidence import (
    calculate_evidence_coverage_score,
    calculate_source_quality_score,
    is_evidence_action_supporting,
    validate_action_evidence,
)
from qgear_core.earnings import EarningsReview, classify_earnings_review
from qgear_core.models import DataQualitySnapshot, Evidence
from qgear_core.backtest import BacktestObservation, summarize_backtest, validate_no_lookahead
from qgear_core.risk import classify_drawdown_mode, recommend_position_size
from qgear_core.scoring import score_from_metrics
from qgear_core.valuation import (
    ValuationAssumptions,
    ValuationCase,
    ValuationSensitivityCell,
    build_sensitivity_table,
    expected_irr_pct,
    probability_weighted_irr_pct,
    summarize_valuation,
    validate_valuation_cases,
)

__all__ = [
    "BacktestObservation",
    "ValuationAssumptions",
    "ValuationCase",
    "ValuationSensitivityCell",
    "build_sensitivity_table",
    "calculate_evidence_coverage_score",
    "calculate_source_quality_score",
    "classify_drawdown_mode",
    "classify_earnings_review",
    "DataQualitySnapshot",
    "Evidence",
    "EarningsReview",
    "evaluate_decision",
    "expected_irr_pct",
    "is_evidence_action_supporting",
    "probability_weighted_irr_pct",
    "recommend_position_size",
    "score_from_metrics",
    "summarize_backtest",
    "summarize_valuation",
    "validate_no_lookahead",
    "validate_action_evidence",
    "validate_valuation_cases",
]
