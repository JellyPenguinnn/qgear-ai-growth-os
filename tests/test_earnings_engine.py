from __future__ import annotations

import unittest

from qgear_core.earnings import EarningsReview, classify_earnings_review
from qgear_core.enums import Confidence, EarningsThesisChange
from qgear_core.models import Evidence


def evidence() -> Evidence:
    return Evidence(
        claim="AI demand became more measurable in the quarter.",
        evidence="Demo fixture: revenue growth accelerated, AI evidence improved, and margins expanded.",
        source="Q-GEAR earnings fixture",
        source_date="2026-06-22",
        confidence=Confidence.HIGH,
        disproves_if="Guidance is cut, AI demand slows, or margins deteriorate.",
    )


class EarningsEngineTests(unittest.TestCase):
    def test_positive_earnings_with_evidence_strengthens_thesis(self) -> None:
        result = classify_earnings_review(
            EarningsReview(
                ticker="NVDA",
                fiscal_period="2026Q1",
                report_date="2026-06-22",
                revenue_surprise_pct=8,
                eps_surprise_pct=6,
                guidance_raised=True,
                revenue_growth_accelerated=True,
                ai_evidence_improved=True,
                margin_expanded=True,
                evidence=(evidence(),),
            )
        )

        self.assertEqual(result, EarningsThesisChange.STRENGTHENED)

    def test_positive_flags_without_evidence_do_not_strengthen_thesis(self) -> None:
        result = classify_earnings_review(
            EarningsReview(
                ticker="NVDA",
                fiscal_period="2026Q1",
                report_date="2026-06-22",
                guidance_raised=True,
                revenue_growth_accelerated=True,
                ai_evidence_improved=True,
                margin_expanded=True,
            )
        )

        self.assertEqual(result, EarningsThesisChange.UNCHANGED)

    def test_negative_earnings_weaken_thesis(self) -> None:
        result = classify_earnings_review(
            EarningsReview(
                ticker="DEMO",
                fiscal_period="2026Q1",
                report_date="2026-06-22",
                revenue_surprise_pct=-8,
                guidance_cut=True,
                margin_deteriorated=True,
            )
        )

        self.assertEqual(result, EarningsThesisChange.WEAKENED)

    def test_structural_guidance_cut_breaks_thesis(self) -> None:
        result = classify_earnings_review(
            EarningsReview(
                ticker="DEMO",
                fiscal_period="2026Q1",
                report_date="2026-06-22",
                guidance_cut=True,
                guidance_cut_structural=True,
            )
        )

        self.assertEqual(result, EarningsThesisChange.BROKEN)


if __name__ == "__main__":
    unittest.main()
