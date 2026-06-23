from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValuationAssumptions:
    revenue_cagr_pct: float
    gross_margin_pct: float
    operating_margin_pct: float
    fcf_margin_pct: float
    terminal_multiple: float
    dilution_buyback_pct: float
    net_cash_debt_per_share: float


@dataclass(frozen=True)
class ValuationCase:
    name: str
    probability: float
    current_price: float
    target_price_3y: float
    target_price_5y: float
    notes: str
    assumptions: ValuationAssumptions | None = None
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class ValuationSensitivityCell:
    terminal_multiple_delta_pct: float
    fcf_margin_delta_pct: float
    target_price_5y: float
    expected_irr_5y_pct: float


@dataclass(frozen=True)
class ValuationSummary:
    cases: tuple[ValuationCase, ...]
    probability_weighted_irr_3y_pct: float
    probability_weighted_irr_5y_pct: float
    hurdle_irr_pct: float
    clears_hurdle: bool


STANDARD_CASE_NAMES = frozenset({"bear", "base", "bull"})


def expected_irr_pct(current_price: float, target_price: float, years: int) -> float:
    if current_price <= 0:
        raise ValueError("current_price must be positive")
    if target_price < 0:
        raise ValueError("target_price cannot be negative")
    if years <= 0:
        raise ValueError("years must be positive")
    if target_price == 0:
        return -100.0
    return round(((target_price / current_price) ** (1 / years) - 1) * 100, 2)


def validate_valuation_cases(
    cases: tuple[ValuationCase, ...],
    *,
    require_assumptions: bool = False,
    require_standard_cases: bool = False,
) -> None:
    if not cases:
        raise ValueError("at least one valuation case is required")

    normalized_names = [case.name.strip().lower() for case in cases]
    if len(normalized_names) != len(set(normalized_names)):
        raise ValueError("valuation case names must be unique")
    if require_standard_cases and set(normalized_names) != STANDARD_CASE_NAMES:
        raise ValueError("valuation cases must include exactly bear, base, and bull")

    probability_sum = sum(case.probability for case in cases)
    if abs(probability_sum - 1.0) > 0.001:
        raise ValueError("valuation case probabilities must sum to 1.0")

    for case in cases:
        if not 0 <= case.probability <= 1:
            raise ValueError("valuation case probabilities must be between 0 and 1")
        if case.current_price <= 0:
            raise ValueError("current_price must be positive")
        if case.target_price_3y < 0 or case.target_price_5y < 0:
            raise ValueError("target prices cannot be negative")
        if require_assumptions and case.assumptions is None:
            raise ValueError("valuation assumptions are required for underwriting")


def probability_weighted_irr_pct(cases: tuple[ValuationCase, ...], *, years: int) -> float:
    validate_valuation_cases(cases)
    total = 0.0
    for case in cases:
        target = case.target_price_3y if years == 3 else case.target_price_5y
        total += case.probability * expected_irr_pct(case.current_price, target, years)
    return round(total, 2)


def summarize_valuation(cases: tuple[ValuationCase, ...], *, hurdle_irr_pct: float) -> ValuationSummary:
    weighted_3y = probability_weighted_irr_pct(cases, years=3)
    weighted_5y = probability_weighted_irr_pct(cases, years=5)
    return ValuationSummary(
        cases=cases,
        probability_weighted_irr_3y_pct=weighted_3y,
        probability_weighted_irr_5y_pct=weighted_5y,
        hurdle_irr_pct=hurdle_irr_pct,
        clears_hurdle=weighted_5y >= hurdle_irr_pct,
    )


def build_sensitivity_table(
    *,
    current_price: float,
    base_target_price_5y: float,
    terminal_multiple_deltas_pct: tuple[float, ...] = (-20, 0, 20),
    fcf_margin_deltas_pct: tuple[float, ...] = (-3, 0, 3),
) -> tuple[ValuationSensitivityCell, ...]:
    if current_price <= 0:
        raise ValueError("current_price must be positive")
    if base_target_price_5y < 0:
        raise ValueError("base_target_price_5y cannot be negative")

    cells: list[ValuationSensitivityCell] = []
    for multiple_delta in terminal_multiple_deltas_pct:
        for margin_delta in fcf_margin_deltas_pct:
            multiple_factor = max(0, 1 + multiple_delta / 100)
            margin_factor = max(0, 1 + margin_delta / 100)
            target_price = round(base_target_price_5y * multiple_factor * margin_factor, 2)
            cells.append(
                ValuationSensitivityCell(
                    terminal_multiple_delta_pct=multiple_delta,
                    fcf_margin_delta_pct=margin_delta,
                    target_price_5y=target_price,
                    expected_irr_5y_pct=expected_irr_pct(current_price, target_price, 5),
                )
            )
    return tuple(cells)
