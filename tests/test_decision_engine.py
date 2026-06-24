from __future__ import annotations

import unittest

from qgear_core.decision import evaluate_decision
from qgear_core.enums import (
    Confidence,
    DataMode,
    DecisionState,
    EarningsThesisChange,
    EvidenceSourceType,
    EvidenceVerificationStatus,
    TechnicalRegime,
)
from qgear_core.models import DataQualitySnapshot, Evidence
from qgear_core.models import DecisionInput, PortfolioContext, ScoreBreakdown
from qgear_core.risk import classify_drawdown_mode
from qgear_core.enums import DrawdownMode


def strong_score(totalish: float = 90) -> ScoreBreakdown:
    scale = totalish / 100
    return ScoreBreakdown(
        ai_relevance=12 * scale,
        business_quality=18 * scale,
        revenue_earnings_acceleration=18 * scale,
        earnings_guidance_revisions=17 * scale,
        valuation_expected_irr=15 * scale,
        technical_trend=10 * scale,
        portfolio_fit=10 * scale,
    )


def evidence() -> Evidence:
    return Evidence(
        claim="Revenue growth accelerated with measurable AI demand evidence.",
        evidence="Demo fixture: revenue growth, margin, and guidance improved.",
        source="Q-GEAR test fixture",
        source_date="2026-06-22",
        confidence=Confidence.HIGH,
        disproves_if="Guidance is cut, margins deteriorate, or AI demand slows.",
    )


def provider_verified_evidence(source_type: EvidenceSourceType = EvidenceSourceType.SEC_FILING) -> Evidence:
    return Evidence(
        claim="Revenue growth accelerated with measurable AI demand evidence.",
        evidence="SEC fixture: revenue growth, margin, and guidance improved.",
        source="SEC company facts fixture",
        source_date="2026-06-22",
        confidence=Confidence.HIGH,
        disproves_if="Future filings contradict the acceleration.",
        source_type=source_type,
        verification_status=EvidenceVerificationStatus.PROVIDER_VERIFIED,
        source_url="https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json",
        provider="sec_edgar",
        filing_date="2026-06-20",
        period_end_date="2026-04-30",
    )


def ai_draft_evidence() -> Evidence:
    return Evidence(
        claim="Revenue growth accelerated with measurable AI demand evidence.",
        evidence="AI draft says revenue growth accelerated, pending user verification.",
        source="AI draft extraction",
        source_date="2026-06-22",
        confidence=Confidence.HIGH,
        disproves_if="Future filings contradict the claim.",
        source_type=EvidenceSourceType.AI_DRAFT,
        verification_status=EvidenceVerificationStatus.UNVERIFIED,
    )


def ai_user_verified_evidence() -> Evidence:
    return Evidence(
        claim="Revenue growth accelerated with measurable AI demand evidence.",
        evidence="User verified AI extraction against an earnings release.",
        source="User-verified earnings release extraction",
        source_date="2026-06-22",
        confidence=Confidence.HIGH,
        disproves_if="Future guidance is cut or margins deteriorate.",
        source_type=EvidenceSourceType.AI_USER_VERIFIED,
        verification_status=EvidenceVerificationStatus.USER_VERIFIED,
    )


def missing_source_type_evidence() -> Evidence:
    return Evidence(
        claim="Revenue growth accelerated with measurable AI demand evidence.",
        evidence="Fixture evidence missing source type.",
        source="Q-GEAR test fixture",
        source_date="2026-06-22",
        confidence=Confidence.HIGH,
        disproves_if="Guidance is cut.",
        source_type=None,
        verification_status=EvidenceVerificationStatus.USER_VERIFIED,
    )


def price_only_evidence() -> Evidence:
    return Evidence(
        claim="Price dropped 20 percent and looks cheaper.",
        evidence="The stock price fell sharply from recent highs.",
        source="Manual note",
        source_date="2026-06-22",
        confidence=Confidence.HIGH,
        disproves_if="Price stops falling.",
        source_type=EvidenceSourceType.MANUAL,
        verification_status=EvidenceVerificationStatus.USER_VERIFIED,
    )


def low_confidence_evidence() -> Evidence:
    return Evidence(
        claim="Revenue growth accelerated with measurable AI demand evidence.",
        evidence="Demo fixture: revenue growth, margin, and guidance improved.",
        source="Q-GEAR test fixture",
        source_date="2026-06-22",
        confidence=Confidence.LOW,
        disproves_if="Guidance is cut, margins deteriorate, or AI demand slows.",
    )


def invalid_date_evidence() -> Evidence:
    return Evidence(
        claim="Revenue growth accelerated with measurable AI demand evidence.",
        evidence="Demo fixture: revenue growth, margin, and guidance improved.",
        source="Q-GEAR test fixture",
        source_date="June 22, 2026",
        confidence=Confidence.HIGH,
        disproves_if="Guidance is cut, margins deteriorate, or AI demand slows.",
    )


def decision_case(**overrides: object) -> DecisionInput:
    base = {
        "ticker": "DEMO",
        "score": strong_score(),
        "thesis_approved": True,
        "invalidation_rule_present": True,
        "ai_relevance_proven": True,
        "latest_earnings_change": EarningsThesisChange.STRENGTHENED,
        "expected_irr_base_pct": 18,
        "hurdle_irr_pct": 15,
        "technical_regime": TechnicalRegime.STABILISING,
        "evidence_age_days": 21,
        "portfolio": PortfolioContext(total_equity=10_000, cash=2_000),
        "fresh_positive_evidence": True,
        "positive_evidence": (evidence(),),
    }
    base.update(overrides)
    return DecisionInput(**base)


class DecisionEngineTests(unittest.TestCase):
    def test_price_falls_without_new_evidence_blocks_add(self) -> None:
        result = evaluate_decision(
            decision_case(
                portfolio=PortfolioContext(
                    total_equity=10_000,
                    cash=2_000,
                    owned=True,
                    current_position_weight_pct=6,
                ),
                add_requested=True,
                price_change_pct=-20,
                fresh_positive_evidence=False,
                technical_regime=TechnicalRegime.WEAKENING,
            )
        )

        self.assertNotEqual(result.state, DecisionState.ADD_ALLOWED)
        self.assertEqual(result.state, DecisionState.TECHNICAL_WAIT)
        self.assertIn("Price decline alone is insufficient evidence for adding.", result.blocked_reasons)

    def test_no_approved_thesis_blocks_buy(self) -> None:
        result = evaluate_decision(decision_case(thesis_approved=False))

        self.assertNotIn(result.state, {DecisionState.STARTER_ALLOWED, DecisionState.ADD_ALLOWED})
        self.assertIn(result.state, {DecisionState.RESEARCH_CANDIDATE, DecisionState.WATCHLIST})
        self.assertIn("No approved thesis exists.", result.blocked_reasons)

    def test_strong_confirmation_allows_starter_when_not_owned(self) -> None:
        result = evaluate_decision(decision_case(portfolio=PortfolioContext(total_equity=10_000, cash=2_000, owned=False)))

        self.assertEqual(result.state, DecisionState.STARTER_ALLOWED)
        self.assertTrue(result.action_allowed)

    def test_strong_confirmation_allows_add_when_owned_and_risk_room_exists(self) -> None:
        result = evaluate_decision(
            decision_case(
                portfolio=PortfolioContext(
                    total_equity=10_000,
                    cash=2_000,
                    owned=True,
                    current_position_weight_pct=6,
                ),
                add_requested=True,
            )
        )

        self.assertEqual(result.state, DecisionState.ADD_ALLOWED)
        self.assertTrue(result.action_allowed)

    def test_owned_position_with_confirmation_but_no_add_request_holds(self) -> None:
        result = evaluate_decision(
            decision_case(
                portfolio=PortfolioContext(
                    total_equity=10_000,
                    cash=2_000,
                    owned=True,
                    current_position_weight_pct=6,
                ),
                add_requested=False,
            )
        )

        self.assertEqual(result.state, DecisionState.HOLD)
        self.assertFalse(result.action_allowed)

    def test_position_near_concentration_cap_blocks_add(self) -> None:
        result = evaluate_decision(
            decision_case(
                portfolio=PortfolioContext(
                    total_equity=10_000,
                    cash=2_000,
                    owned=True,
                    current_position_weight_pct=14.5,
                    max_single_stock_pct=15,
                ),
                add_requested=True,
                score=strong_score(92),
            )
        )

        self.assertEqual(result.state, DecisionState.HOLD)
        self.assertIn("Portfolio concentration limit would be breached by a normal add.", result.blocked_reasons)

    def test_latest_earnings_weakened_blocks_even_high_score(self) -> None:
        result = evaluate_decision(
            decision_case(
                score=strong_score(95),
                latest_earnings_change=EarningsThesisChange.WEAKENED,
            )
        )

        self.assertNotIn(result.state, {DecisionState.STARTER_ALLOWED, DecisionState.ADD_ALLOWED})
        self.assertIn("Latest earnings weakened the thesis.", result.blocked_reasons)

    def test_expected_irr_below_hurdle_blocks_buy(self) -> None:
        result = evaluate_decision(
            decision_case(
                expected_irr_base_pct=9,
                hurdle_irr_pct=15,
                score=strong_score(88),
            )
        )

        self.assertEqual(result.state, DecisionState.WATCHLIST)
        self.assertIn("Valuation does not support the required expected IRR.", result.blocked_reasons)

    def test_weighted_irr_below_hurdle_blocks_even_when_base_irr_clears(self) -> None:
        result = evaluate_decision(
            decision_case(
                expected_irr_base_pct=22,
                expected_irr_weighted_pct=9,
                hurdle_irr_pct=15,
                score=strong_score(90),
            )
        )

        self.assertEqual(result.state, DecisionState.WATCHLIST)
        self.assertIn("Valuation does not support the required expected IRR.", result.blocked_reasons)

    def test_valuation_clears_without_fresh_evidence_does_not_buy(self) -> None:
        result = evaluate_decision(
            decision_case(
                expected_irr_base_pct=25,
                expected_irr_weighted_pct=23,
                fresh_positive_evidence=False,
                positive_evidence=(),
            )
        )

        self.assertNotIn(result.state, {DecisionState.STARTER_ALLOWED, DecisionState.ADD_ALLOWED})
        self.assertFalse(result.action_allowed)
        self.assertIn("Thesis and valuation are acceptable, but no fresh action-changing evidence is present.", result.reasons)

    def test_hard_drawdown_blocks_normal_risk_taking(self) -> None:
        result = evaluate_decision(
            decision_case(
                portfolio=PortfolioContext(
                    total_equity=10_000,
                    cash=2_000,
                    portfolio_drawdown_pct=35,
                )
            )
        )

        self.assertEqual(result.state, DecisionState.BLOCKED_BY_RISK)
        self.assertEqual(result.drawdown_mode, DrawdownMode.HARD_AUDIT)

    def test_no_invalidation_rule_blocks_buy(self) -> None:
        result = evaluate_decision(decision_case(invalidation_rule_present=False))

        self.assertEqual(result.state, DecisionState.APPROVED_THESIS)
        self.assertIn("No invalidation rule exists.", result.blocked_reasons)

    def test_stale_evidence_blocks_buy(self) -> None:
        result = evaluate_decision(decision_case(evidence_age_days=120))

        self.assertEqual(result.state, DecisionState.WATCHLIST)
        self.assertIn("Evidence is stale.", result.blocked_reasons)

    def test_weak_ai_relevance_is_rejected(self) -> None:
        result = evaluate_decision(decision_case(ai_relevance_proven=False, score=strong_score(92)))

        self.assertEqual(result.state, DecisionState.REJECTED)
        self.assertIn("AI relevance is weak or unproven.", result.blocked_reasons)

    def test_structural_guidance_cut_blocks_buy(self) -> None:
        result = evaluate_decision(decision_case(guidance_cut_structural=True, score=strong_score(94)))

        self.assertEqual(result.state, DecisionState.WATCHLIST)
        self.assertIn("Guidance was cut for structural reasons.", result.blocked_reasons)

    def test_margin_deterioration_blocks_buy(self) -> None:
        result = evaluate_decision(decision_case(margin_deterioration_unexplained=True, score=strong_score(94)))

        self.assertEqual(result.state, DecisionState.WATCHLIST)
        self.assertIn("Margin deterioration is unexplained or persistent.", result.blocked_reasons)

    def test_broken_technical_regime_blocks_buy(self) -> None:
        result = evaluate_decision(decision_case(technical_regime=TechnicalRegime.BROKEN, score=strong_score(94)))

        self.assertEqual(result.state, DecisionState.TECHNICAL_WAIT)
        self.assertIn("Technical trend is broken and there is no stabilisation.", result.blocked_reasons)

    def test_red_flags_block_high_score(self) -> None:
        result = evaluate_decision(decision_case(red_flags=("Customer concentration risk unresolved.",), score=strong_score(96)))

        self.assertEqual(result.state, DecisionState.WATCHLIST)
        self.assertIn("Customer concentration risk unresolved.", result.blocked_reasons)

    def test_fresh_positive_evidence_requires_structured_evidence_object(self) -> None:
        result = evaluate_decision(decision_case(positive_evidence=(), score=strong_score(94)))

        self.assertEqual(result.state, DecisionState.WATCHLIST)
        self.assertIn("Fresh positive evidence must include a structured evidence object.", result.blocked_reasons)

    def test_action_evidence_requires_valid_source_date(self) -> None:
        result = evaluate_decision(decision_case(positive_evidence=(invalid_date_evidence(),), score=strong_score(94)))

        self.assertEqual(result.state, DecisionState.WATCHLIST)
        self.assertIn("Positive evidence #1 source date must be ISO format YYYY-MM-DD.", result.blocked_reasons)

    def test_action_evidence_requires_medium_or_high_confidence(self) -> None:
        result = evaluate_decision(decision_case(positive_evidence=(low_confidence_evidence(),), score=strong_score(94)))

        self.assertEqual(result.state, DecisionState.WATCHLIST)
        self.assertIn(
            "Positive evidence #1 confidence is LOW; action-changing evidence must be at least MEDIUM confidence.",
            result.blocked_reasons,
        )

    def test_ai_draft_evidence_cannot_support_buy_add(self) -> None:
        result = evaluate_decision(decision_case(positive_evidence=(ai_draft_evidence(),), score=strong_score(94)))

        self.assertEqual(result.state, DecisionState.WATCHLIST)
        self.assertIn(
            "Positive evidence #1 is AI_DRAFT; AI drafts require user verification before supporting buy/add.",
            result.blocked_reasons,
        )

    def test_ai_user_verified_evidence_can_support_evidence_gate(self) -> None:
        result = evaluate_decision(decision_case(positive_evidence=(ai_user_verified_evidence(),), score=strong_score(90)))

        self.assertEqual(result.state, DecisionState.STARTER_ALLOWED)
        self.assertTrue(result.action_allowed)

    def test_demo_evidence_blocks_live_mode_buy_add(self) -> None:
        result = evaluate_decision(decision_case(mode=DataMode.LIVE, positive_evidence=(evidence(),), score=strong_score(94)))

        self.assertEqual(result.state, DecisionState.WATCHLIST)
        self.assertIn(
            "Positive evidence #1 is DEMO evidence; demo evidence cannot support live-mode buy/add decisions.",
            result.blocked_reasons,
        )

    def test_sec_filing_evidence_can_support_live_mode_when_data_quality_passes(self) -> None:
        result = evaluate_decision(
            decision_case(
                mode=DataMode.LIVE,
                positive_evidence=(provider_verified_evidence(),),
                data_quality_snapshot=DataQualitySnapshot(
                    ticker="DEMO",
                    mode=DataMode.LIVE,
                    financial_data_status="ok",
                    price_data_status="ok",
                    filing_data_status="ok",
                    earnings_data_status="ok",
                    valuation_data_status="ok",
                    technical_data_status="ok",
                    source_quality_score=90,
                    evidence_coverage_score=80,
                ),
            )
        )

        self.assertEqual(result.state, DecisionState.STARTER_ALLOWED)
        self.assertTrue(result.action_allowed)

    def test_missing_source_type_blocks_action(self) -> None:
        result = evaluate_decision(decision_case(positive_evidence=(missing_source_type_evidence(),), score=strong_score(94)))

        self.assertEqual(result.state, DecisionState.WATCHLIST)
        self.assertIn("Positive evidence #1 is missing a source type.", result.blocked_reasons)

    def test_price_only_evidence_blocks_action(self) -> None:
        result = evaluate_decision(decision_case(positive_evidence=(price_only_evidence(),), score=strong_score(94)))

        self.assertEqual(result.state, DecisionState.WATCHLIST)
        self.assertIn("Positive evidence #1 appears price-only; price movement alone is insufficient evidence.", result.blocked_reasons)

    def test_source_quality_below_threshold_blocks_action(self) -> None:
        result = evaluate_decision(decision_case(source_quality_score=45, score=strong_score(94)))

        self.assertEqual(result.state, DecisionState.WATCHLIST)
        self.assertIn("Source quality score 45 is below the 70 action threshold.", result.blocked_reasons)

    def test_provider_error_blocks_live_action(self) -> None:
        result = evaluate_decision(
            decision_case(
                mode=DataMode.LIVE,
                positive_evidence=(provider_verified_evidence(),),
                data_quality_snapshot=DataQualitySnapshot(
                    ticker="DEMO",
                    mode=DataMode.LIVE,
                    financial_data_status="error",
                    price_data_status="ok",
                    filing_data_status="ok",
                    earnings_data_status="ok",
                    valuation_data_status="ok",
                    technical_data_status="ok",
                    source_quality_score=90,
                    evidence_coverage_score=80,
                    provider_errors=("SEC company facts unavailable",),
                ),
            )
        )

        self.assertEqual(result.state, DecisionState.WATCHLIST)
        self.assertIn(
            "Provider errors block live-mode action-changing decisions: SEC company facts unavailable.",
            result.blocked_reasons,
        )

    def test_mixed_mode_with_provider_error_warns_before_add_risk(self) -> None:
        result = evaluate_decision(
            decision_case(
                mode=DataMode.MIXED,
                positive_evidence=(provider_verified_evidence(),),
                data_quality_snapshot=DataQualitySnapshot(
                    ticker="DEMO",
                    mode=DataMode.MIXED,
                    source_quality_score=85,
                    evidence_coverage_score=85,
                    provider_errors=("Price provider missing API key",),
                ),
            )
        )

        self.assertEqual(result.state, DecisionState.WATCHLIST)
        self.assertIn(
            "Mixed-mode provider errors require review before adding risk: Price provider missing API key.",
            result.blocked_reasons,
        )

    def test_cash_buffer_blocks_new_money(self) -> None:
        result = evaluate_decision(
            decision_case(
                portfolio=PortfolioContext(
                    total_equity=10_000,
                    cash=1_000,
                    cash_buffer_pct=15,
                )
            )
        )

        self.assertEqual(result.state, DecisionState.WATCHLIST)
        self.assertIn("Cash is at or below the required buffer; risk budget does not allow new money.", result.blocked_reasons)

    def test_drawdown_mode_thresholds(self) -> None:
        self.assertEqual(classify_drawdown_mode(0), DrawdownMode.NORMAL)
        self.assertEqual(classify_drawdown_mode(10), DrawdownMode.CAUTION_REVIEW)
        self.assertEqual(classify_drawdown_mode(15), DrawdownMode.REDUCE_AGGRESSIVE_NEW_BUYS)
        self.assertEqual(classify_drawdown_mode(20), DrawdownMode.FREEZE_WEAK_THESIS_ADDITIONS)
        self.assertEqual(classify_drawdown_mode(25), DrawdownMode.RISK_CONTROL)
        self.assertEqual(classify_drawdown_mode(30), DrawdownMode.DEFENSIVE)
        self.assertEqual(classify_drawdown_mode(35), DrawdownMode.HARD_AUDIT)


if __name__ == "__main__":
    unittest.main()
