from __future__ import annotations

import unittest

from qgear_core.backtest import BacktestObservation, summarize_backtest, validate_no_lookahead
from qgear_core.valuation import (
    ValuationAssumptions,
    ValuationCase,
    build_sensitivity_table,
    expected_irr_pct,
    probability_weighted_irr_pct,
    summarize_valuation,
    validate_valuation_cases,
)


class ValuationBacktestTests(unittest.TestCase):
    def test_expected_irr_calculation(self) -> None:
        self.assertEqual(expected_irr_pct(100, 161.05, 5), 10.0)

    def test_probability_weighted_irr_and_hurdle(self) -> None:
        cases = (
            ValuationCase("bear", 0.25, 100, 115, 130, "bear"),
            ValuationCase("base", 0.50, 100, 155, 220, "base"),
            ValuationCase("bull", 0.25, 100, 200, 350, "bull"),
        )
        summary = summarize_valuation(cases, hurdle_irr_pct=15)

        self.assertAlmostEqual(probability_weighted_irr_pct(cases, years=5), summary.probability_weighted_irr_5y_pct)
        self.assertTrue(summary.clears_hurdle)

    def test_probability_must_sum_to_one(self) -> None:
        cases = (ValuationCase("base", 0.80, 100, 120, 140, "bad probability"),)

        with self.assertRaises(ValueError):
            probability_weighted_irr_pct(cases, years=5)

    def test_underwriting_validation_requires_standard_cases_and_assumptions(self) -> None:
        assumptions = ValuationAssumptions(20, 60, 30, 25, 25, 0, 0)
        cases = (
            ValuationCase("bear", 0.25, 100, 110, 120, "bear", assumptions=assumptions),
            ValuationCase("base", 0.50, 100, 140, 170, "base", assumptions=assumptions),
            ValuationCase("bull", 0.25, 100, 180, 240, "bull", assumptions=assumptions),
        )

        validate_valuation_cases(cases, require_assumptions=True, require_standard_cases=True)

        with self.assertRaises(ValueError):
            validate_valuation_cases(cases[:2], require_assumptions=True, require_standard_cases=True)

        with self.assertRaises(ValueError):
            validate_valuation_cases(
                (ValuationCase("bear", -0.1, 100, 110, 120, "bad probability", assumptions=assumptions),) + cases[1:],
                require_assumptions=True,
                require_standard_cases=True,
            )

    def test_sensitivity_table_shape(self) -> None:
        cells = build_sensitivity_table(current_price=100, base_target_price_5y=200)

        self.assertEqual(len(cells), 9)
        self.assertTrue(any(cell.terminal_multiple_delta_pct == 0 and cell.fcf_margin_delta_pct == 0 for cell in cells))

    def test_no_lookahead_guard_passes_when_data_was_available(self) -> None:
        observations = (
            BacktestObservation("NVDA", "2026-06-22", "2026-05-22", 90, "STARTER_ALLOWED", 18, 9),
        )

        summary = summarize_backtest(observations)

        self.assertTrue(summary.no_lookahead_passed)
        self.assertEqual(summary.errors, ())

    def test_no_lookahead_guard_flags_future_data(self) -> None:
        observations = (
            BacktestObservation("NVDA", "2026-05-01", "2026-05-22", 90, "STARTER_ALLOWED", 18, 9),
        )

        errors = validate_no_lookahead(observations)

        self.assertIn("precedes data_available_date", errors[0])


if __name__ == "__main__":
    unittest.main()
