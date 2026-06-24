from __future__ import annotations

from qgear_core.enums import DataMode, DecisionState, DrawdownMode, EarningsThesisChange, TechnicalRegime
from qgear_core.evidence import (
    EVIDENCE_COVERAGE_MINIMUM,
    SOURCE_QUALITY_MINIMUM,
    calculate_evidence_coverage_score,
    calculate_source_quality_score,
    validate_action_evidence,
)
from qgear_core.models import DecisionInput, DecisionResult
from qgear_core.risk import classify_drawdown_mode


MAX_EVIDENCE_AGE_DAYS = 90


def _result(
    decision_input: DecisionInput,
    state: DecisionState,
    reasons: list[str],
    blocked_reasons: list[str] | None = None,
    action_allowed: bool = False,
    drawdown_mode: DrawdownMode | None = None,
) -> DecisionResult:
    return DecisionResult(
        ticker=decision_input.ticker,
        state=state,
        score_total=decision_input.score.total,
        reasons=tuple(reasons),
        blocked_reasons=tuple(blocked_reasons or ()),
        drawdown_mode=drawdown_mode or classify_drawdown_mode(decision_input.portfolio.portfolio_drawdown_pct),
        action_allowed=action_allowed,
    )


def _decision_mode(decision_input: DecisionInput) -> DataMode:
    if decision_input.data_quality_snapshot:
        return decision_input.data_quality_snapshot.mode
    return decision_input.mode


def _data_quality_gate_errors(decision_input: DecisionInput) -> tuple[str, ...]:
    snapshot = decision_input.data_quality_snapshot
    mode = _decision_mode(decision_input)
    source_quality_score = snapshot.source_quality_score if snapshot else decision_input.source_quality_score
    evidence_coverage_score = snapshot.evidence_coverage_score if snapshot else decision_input.evidence_coverage_score
    provider_errors = snapshot.provider_errors if snapshot else ()
    missing_required_inputs = snapshot.missing_required_inputs if snapshot else ()
    stale_inputs = snapshot.stale_inputs if snapshot else ()

    errors: list[str] = []
    if source_quality_score < SOURCE_QUALITY_MINIMUM:
        errors.append(
            f"Source quality score {source_quality_score:g} is below the {SOURCE_QUALITY_MINIMUM:g} action threshold."
        )
    if evidence_coverage_score < EVIDENCE_COVERAGE_MINIMUM:
        errors.append(
            f"Evidence coverage score {evidence_coverage_score:g} is below the {EVIDENCE_COVERAGE_MINIMUM:g} action threshold."
        )
    if stale_inputs:
        errors.append(f"Stale data inputs block action-changing decisions: {', '.join(stale_inputs)}.")
    if missing_required_inputs:
        errors.append(f"Missing required data inputs block action-changing decisions: {', '.join(missing_required_inputs)}.")
    if mode == DataMode.LIVE and provider_errors:
        errors.append(f"Provider errors block live-mode action-changing decisions: {', '.join(provider_errors)}.")
    if decision_input.requires_live_data and mode == DataMode.DEMO:
        errors.append("Live data is required for this decision, but current mode is demo.")
    if mode == DataMode.MIXED and provider_errors:
        errors.append(f"Mixed-mode provider errors require review before adding risk: {', '.join(provider_errors)}.")
    return tuple(errors)


def evaluate_decision(decision_input: DecisionInput) -> DecisionResult:
    """Apply Q-GEAR hard gates after scoring.

    This is intentionally gate-first. A high score can support conviction, but it
    cannot override thesis, earnings, valuation, technical, freshness, or risk
    gates.
    """

    reasons: list[str] = []
    blocked: list[str] = []
    drawdown_mode = classify_drawdown_mode(decision_input.portfolio.portfolio_drawdown_pct)
    mode = _decision_mode(decision_input)
    evidence_errors = validate_action_evidence(decision_input.positive_evidence, mode=mode)
    if decision_input.positive_evidence:
        evidence_errors = (
            *evidence_errors,
            *_derived_source_quality_errors(decision_input, mode),
        )
    has_valid_positive_evidence = decision_input.fresh_positive_evidence and not evidence_errors

    if drawdown_mode == DrawdownMode.HARD_AUDIT:
        blocked.append("Portfolio drawdown is at or above the 35% hard limit; enter strategy audit mode.")
        return _result(
            decision_input,
            DecisionState.BLOCKED_BY_RISK,
            ["Hard drawdown limit reached; normal risk-taking is blocked."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    if not decision_input.ai_relevance_proven:
        blocked.append("AI relevance is weak or unproven.")
        return _result(
            decision_input,
            DecisionState.REJECTED,
            ["Rejected because measurable AI infrastructure relevance is not proven."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    if not decision_input.thesis_approved:
        blocked.append("No approved thesis exists.")
        state = DecisionState.WATCHLIST if decision_input.score.total >= 65 else DecisionState.RESEARCH_CANDIDATE
        return _result(
            decision_input,
            state,
            ["Needs an approved thesis before any buy/add action is possible."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    if not decision_input.invalidation_rule_present:
        blocked.append("No invalidation rule exists.")
        return _result(
            decision_input,
            DecisionState.APPROVED_THESIS,
            ["Thesis is present but lacks a clear invalidation rule."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    if decision_input.latest_earnings_change == EarningsThesisChange.BROKEN:
        blocked.append("Latest earnings broke the thesis.")
        state = DecisionState.EXIT_THESIS_BROKEN if decision_input.portfolio.owned else DecisionState.WATCHLIST
        return _result(
            decision_input,
            state,
            ["Latest earnings broke the thesis; buy/add is not allowed."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    if decision_input.latest_earnings_change == EarningsThesisChange.WEAKENED:
        blocked.append("Latest earnings weakened the thesis.")
        state = DecisionState.HOLD if decision_input.portfolio.owned else DecisionState.WATCHLIST
        return _result(
            decision_input,
            state,
            ["Latest earnings weakened the thesis; score cannot override this gate."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    if decision_input.guidance_cut_structural:
        blocked.append("Guidance was cut for structural reasons.")
        state = DecisionState.HOLD if decision_input.portfolio.owned else DecisionState.WATCHLIST
        return _result(
            decision_input,
            state,
            ["Structural guidance cut blocks buy/add until evidence repairs the thesis."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    if decision_input.margin_deterioration_unexplained:
        blocked.append("Margin deterioration is unexplained or persistent.")
        state = DecisionState.HOLD if decision_input.portfolio.owned else DecisionState.WATCHLIST
        return _result(
            decision_input,
            state,
            ["Unexplained margin deterioration blocks buy/add."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    decision_grade_expected_irr = (
        decision_input.expected_irr_weighted_pct
        if decision_input.expected_irr_weighted_pct is not None
        else decision_input.expected_irr_base_pct
    )
    if decision_grade_expected_irr < decision_input.hurdle_irr_pct:
        blocked.append("Valuation does not support the required expected IRR.")
        state = DecisionState.HOLD if decision_input.portfolio.owned else DecisionState.WATCHLIST
        return _result(
            decision_input,
            state,
            ["Great businesses still need enough expected return to clear the hurdle."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    if decision_input.evidence_age_days > MAX_EVIDENCE_AGE_DAYS:
        blocked.append("Evidence is stale.")
        state = DecisionState.HOLD if decision_input.portfolio.owned else DecisionState.WATCHLIST
        return _result(
            decision_input,
            state,
            ["Evidence is stale; refresh earnings, valuation, and thesis data before action."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    data_quality_errors = _data_quality_gate_errors(decision_input)
    if data_quality_errors:
        blocked.extend(data_quality_errors)
        state = DecisionState.HOLD if decision_input.portfolio.owned else DecisionState.WATCHLIST
        return _result(
            decision_input,
            state,
            ["Source/data quality is not sufficient for an action-changing decision."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    if decision_input.portfolio.current_position_weight_pct > decision_input.portfolio.max_single_stock_pct:
        blocked.append("Portfolio concentration limit is already breached.")
        return _result(
            decision_input,
            DecisionState.TRIM_CANDIDATE,
            ["Position is above the max single-stock allocation; trim review is required."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    if (
        decision_input.add_requested
        and decision_input.portfolio.owned
        and decision_input.portfolio.current_position_weight_pct >= decision_input.portfolio.max_single_stock_pct - 0.5
    ):
        blocked.append("Portfolio concentration limit would be breached by a normal add.")
        return _result(
            decision_input,
            DecisionState.HOLD,
            ["Add blocked because the position is already near the max single-stock allocation."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    price_only_add = (
        decision_input.add_requested
        and decision_input.portfolio.owned
        and decision_input.price_change_pct <= -10
        and not decision_input.fresh_positive_evidence
    )
    if price_only_add:
        blocked.append("Price decline alone is insufficient evidence for adding.")
        state = (
            DecisionState.TECHNICAL_WAIT
            if decision_input.technical_regime in {TechnicalRegime.BROKEN, TechnicalRegime.WEAKENING}
            else DecisionState.HOLD
        )
        return _result(
            decision_input,
            state,
            ["Add blocked: price decline alone is insufficient; require fresh positive fundamental evidence."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    if decision_input.technical_regime == TechnicalRegime.BROKEN:
        blocked.append("Technical trend is broken and there is no stabilisation.")
        return _result(
            decision_input,
            DecisionState.TECHNICAL_WAIT,
            ["Technical regime is broken; fundamentals may be intact, but timing/risk confirmation is absent."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    if drawdown_mode in {DrawdownMode.RISK_CONTROL, DrawdownMode.DEFENSIVE} and not decision_input.fresh_positive_evidence:
        blocked.append("Portfolio drawdown mode blocks non-essential risk-taking without fresh evidence.")
        return _result(
            decision_input,
            DecisionState.HOLD if decision_input.portfolio.owned else DecisionState.WATCHLIST,
            ["Risk-control mode requires fresh positive evidence before new risk is added."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    if decision_input.red_flags:
        blocked.extend(decision_input.red_flags)
        state = DecisionState.HOLD if decision_input.portfolio.owned else DecisionState.WATCHLIST
        return _result(
            decision_input,
            state,
            ["Open red flags require review before action."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    if decision_input.fresh_positive_evidence and evidence_errors:
        blocked.extend(evidence_errors)
        state = DecisionState.HOLD if decision_input.portfolio.owned else DecisionState.WATCHLIST
        return _result(
            decision_input,
            state,
            ["Action-changing evidence must include claim, source, date, confidence, and disproof criteria."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    if (
        (not decision_input.portfolio.owned or decision_input.add_requested)
        and decision_input.portfolio.cash_pct <= decision_input.portfolio.cash_buffer_pct
    ):
        blocked.append("Cash is at or below the required buffer; risk budget does not allow new money.")
        state = DecisionState.HOLD if decision_input.portfolio.owned else DecisionState.WATCHLIST
        return _result(
            decision_input,
            state,
            ["Portfolio risk budget blocks new money because cash is at or below the required buffer."],
            blocked,
            drawdown_mode=drawdown_mode,
        )

    if has_valid_positive_evidence and decision_input.technical_regime in {
        TechnicalRegime.SUPPORTIVE,
        TechnicalRegime.STABILISING,
    }:
        if decision_input.portfolio.owned:
            if not decision_input.add_requested:
                return _result(
                    decision_input,
                    DecisionState.HOLD,
                    ["Thesis has fresh supporting evidence, but no add was requested; maintain hold discipline."],
                    drawdown_mode=drawdown_mode,
                )
            return _result(
                decision_input,
                DecisionState.ADD_ALLOWED,
                ["Thesis confirmed, valuation clears hurdle, technicals are supportive/stabilising, and risk budget allows an add."],
                action_allowed=True,
                drawdown_mode=drawdown_mode,
            )
        return _result(
            decision_input,
            DecisionState.STARTER_ALLOWED,
            ["Thesis confirmed, valuation clears hurdle, technicals are supportive/stabilising, and risk budget allows a starter position."],
            action_allowed=True,
            drawdown_mode=drawdown_mode,
        )

    state = DecisionState.APPROVED_VALUATION_ZONE if decision_input.score.valuation_expected_irr >= 10 else DecisionState.APPROVED_THESIS
    reasons.append("Thesis and valuation are acceptable, but no fresh action-changing evidence is present.")
    return _result(decision_input, state, reasons, drawdown_mode=drawdown_mode)


def _derived_source_quality_errors(decision_input: DecisionInput, mode: DataMode) -> tuple[str, ...]:
    source_quality_score = calculate_source_quality_score(decision_input.positive_evidence)
    evidence_coverage_score = calculate_evidence_coverage_score(decision_input.positive_evidence)
    errors: list[str] = []
    if source_quality_score < SOURCE_QUALITY_MINIMUM:
        errors.append(
            f"Positive evidence source quality score {source_quality_score:g} is below the {SOURCE_QUALITY_MINIMUM:g} action threshold."
        )
    if evidence_coverage_score < EVIDENCE_COVERAGE_MINIMUM:
        errors.append(
            f"Positive evidence coverage score {evidence_coverage_score:g} is below the {EVIDENCE_COVERAGE_MINIMUM:g} action threshold."
        )
    if mode == DataMode.MIXED:
        demo_only = all(item.source_type and item.source_type.value == "DEMO" for item in decision_input.positive_evidence)
        if demo_only:
            errors.append("Mixed mode requires at least one non-demo verified evidence item before adding risk.")
    return tuple(errors)
