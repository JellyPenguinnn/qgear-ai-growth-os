from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class BacktestObservation:
    ticker: str
    decision_date: str
    data_available_date: str
    score: float
    decision_state: str
    forward_return_pct: float
    benchmark_return_pct: float


@dataclass(frozen=True)
class BacktestSummary:
    observation_count: int
    average_forward_return_pct: float
    average_benchmark_return_pct: float
    excess_return_pct: float
    no_lookahead_passed: bool
    errors: tuple[str, ...]


def validate_no_lookahead(observations: tuple[BacktestObservation, ...]) -> tuple[str, ...]:
    errors: list[str] = []
    for observation in observations:
        decision_date = date.fromisoformat(observation.decision_date)
        available_date = date.fromisoformat(observation.data_available_date)
        if decision_date < available_date:
            errors.append(
                f"{observation.ticker} decision_date {observation.decision_date} precedes data_available_date {observation.data_available_date}."
            )
    return tuple(errors)


def summarize_backtest(observations: tuple[BacktestObservation, ...]) -> BacktestSummary:
    if not observations:
        return BacktestSummary(0, 0, 0, 0, True, ())
    errors = validate_no_lookahead(observations)
    avg_return = sum(observation.forward_return_pct for observation in observations) / len(observations)
    avg_benchmark = sum(observation.benchmark_return_pct for observation in observations) / len(observations)
    return BacktestSummary(
        observation_count=len(observations),
        average_forward_return_pct=round(avg_return, 2),
        average_benchmark_return_pct=round(avg_benchmark, 2),
        excess_return_pct=round(avg_return - avg_benchmark, 2),
        no_lookahead_passed=not errors,
        errors=errors,
    )
