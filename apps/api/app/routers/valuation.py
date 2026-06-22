from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.serializers import to_jsonable
from qgear_core.backtest import BacktestObservation, summarize_backtest
from qgear_core.demo import get_company
from qgear_core.valuation import ValuationCase, summarize_valuation

router = APIRouter(prefix="/valuation", tags=["valuation"])


def _target_price(current_price: float, irr_pct: float, years: int) -> float:
    return round(current_price * ((1 + irr_pct / 100) ** years), 2)


@router.get("/backtest/demo")
def demo_backtest() -> dict:
    observations = (
        BacktestObservation("NVDA", "2026-06-22", "2026-05-22", 90.28, "STARTER_ALLOWED", 18.5, 9.1),
        BacktestObservation("MU", "2026-06-22", "2026-05-22", 77.69, "ADD_ALLOWED", 12.0, 8.6),
        BacktestObservation("PLTR", "2026-06-22", "2026-05-22", 73.44, "WATCHLIST", 2.1, 8.6),
    )
    summary = summarize_backtest(observations)
    return to_jsonable(
        {
            "mode": "fixture",
            "summary": summary,
            "observations": observations,
            "limitations": [
                "Fixture backtest only; not evidence of expected future returns.",
                "Live backtests must use data_available_date to avoid look-ahead bias.",
                "Broker execution, margin, options, and auto-trading are not implemented.",
            ],
        }
    )


@router.get("/{ticker}")
def ticker_valuation(ticker: str) -> dict:
    company = get_company(ticker)
    if not company:
        raise HTTPException(status_code=404, detail="Ticker not found in demo universe")

    current_price = 100.0
    base_irr = company.metrics.expected_irr_base_pct
    cases = (
        ValuationCase(
            "bear",
            0.25,
            current_price,
            _target_price(current_price, base_irr - 8, 3),
            _target_price(current_price, base_irr - 8, 5),
            "Bear case reduces the demo base IRR by 8 percentage points.",
        ),
        ValuationCase(
            "base",
            0.50,
            current_price,
            _target_price(current_price, base_irr, 3),
            _target_price(current_price, base_irr, 5),
            "Base case uses the deterministic demo expected IRR input.",
        ),
        ValuationCase(
            "bull",
            0.25,
            current_price,
            _target_price(current_price, base_irr + 8, 3),
            _target_price(current_price, base_irr + 8, 5),
            "Bull case increases the demo base IRR by 8 percentage points.",
        ),
    )
    summary = summarize_valuation(cases, hurdle_irr_pct=15)
    return to_jsonable(
        {
            "ticker": company.ticker,
            "company_name": company.company_name,
            "mode": "demo",
            "summary": summary,
            "decision_gate": {
                "valuation_clears_hurdle": summary.clears_hurdle,
                "hurdle_irr_pct": summary.hurdle_irr_pct,
                "note": "Valuation can support or block action, but cannot create buy/add without thesis, evidence, technical, and risk gates.",
            },
        }
    )
