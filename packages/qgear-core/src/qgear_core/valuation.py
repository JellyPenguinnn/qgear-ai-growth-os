from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValuationCase:
    name: str
    probability: float
    current_price: float
    target_price_3y: float
    target_price_5y: float
    notes: str


@dataclass(frozen=True)
class ValuationSummary:
    cases: tuple[ValuationCase, ...]
    probability_weighted_irr_3y_pct: float
    probability_weighted_irr_5y_pct: float
    hurdle_irr_pct: float
    clears_hurdle: bool


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


def probability_weighted_irr_pct(cases: tuple[ValuationCase, ...], *, years: int) -> float:
    if not cases:
        raise ValueError("at least one valuation case is required")
    probability_sum = sum(case.probability for case in cases)
    if abs(probability_sum - 1.0) > 0.001:
        raise ValueError("valuation case probabilities must sum to 1.0")
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
