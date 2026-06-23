from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.serializers import to_jsonable
from app.schemas.requests import ValuationUnderwriteRequest
from qgear_core.backtest import BacktestObservation, summarize_backtest
from qgear_core.demo import get_company
from qgear_core.valuation import (
    ValuationAssumptions,
    ValuationCase,
    build_sensitivity_table,
    expected_irr_pct,
    summarize_valuation,
    validate_valuation_cases,
)

router = APIRouter(prefix="/valuation", tags=["valuation"])


def _target_price(current_price: float, irr_pct: float, years: int) -> float:
    return round(current_price * ((1 + irr_pct / 100) ** years), 2)


def _demo_cases(company, current_price: float) -> tuple[ValuationCase, ...]:
    metrics = company.metrics
    base_irr = metrics.expected_irr_base_pct
    return (
        ValuationCase(
            "bear",
            0.25,
            current_price,
            _target_price(current_price, base_irr - 8, 3),
            _target_price(current_price, base_irr - 8, 5),
            "Bear case reduces the demo base IRR by 8 percentage points and assumes weaker margins/multiple.",
            assumptions=ValuationAssumptions(
                revenue_cagr_pct=max(-20, metrics.revenue_growth_pct - 12),
                gross_margin_pct=max(-100, metrics.gross_margin_pct - 4),
                operating_margin_pct=max(-100, metrics.operating_margin_pct - 5),
                fcf_margin_pct=max(-100, metrics.fcf_margin_pct - 5),
                terminal_multiple=18,
                dilution_buyback_pct=-2,
                net_cash_debt_per_share=0,
            ),
            evidence_refs=(company.evidence[0].claim,),
        ),
        ValuationCase(
            "base",
            0.50,
            current_price,
            _target_price(current_price, base_irr, 3),
            _target_price(current_price, base_irr, 5),
            "Base case uses the deterministic demo expected IRR input and current demo margins.",
            assumptions=ValuationAssumptions(
                revenue_cagr_pct=metrics.revenue_growth_pct,
                gross_margin_pct=metrics.gross_margin_pct,
                operating_margin_pct=metrics.operating_margin_pct,
                fcf_margin_pct=metrics.fcf_margin_pct,
                terminal_multiple=25,
                dilution_buyback_pct=0,
                net_cash_debt_per_share=0,
            ),
            evidence_refs=(company.evidence[0].claim,),
        ),
        ValuationCase(
            "bull",
            0.25,
            current_price,
            _target_price(current_price, base_irr + 8, 3),
            _target_price(current_price, base_irr + 8, 5),
            "Bull case increases the demo base IRR by 8 percentage points and assumes stronger growth/multiple.",
            assumptions=ValuationAssumptions(
                revenue_cagr_pct=metrics.revenue_growth_pct + 8,
                gross_margin_pct=min(100, metrics.gross_margin_pct + 3),
                operating_margin_pct=min(100, metrics.operating_margin_pct + 4),
                fcf_margin_pct=min(100, metrics.fcf_margin_pct + 4),
                terminal_multiple=32,
                dilution_buyback_pct=1,
                net_cash_debt_per_share=0,
            ),
            evidence_refs=(company.evidence[0].claim,),
        ),
    )


def _underwriting_response(ticker: str, company_name: str, cases: tuple[ValuationCase, ...], hurdle_irr_pct: float, mode: str) -> dict:
    try:
        validate_valuation_cases(cases, require_assumptions=True, require_standard_cases=True)
        summary = summarize_valuation(cases, hurdle_irr_pct=hurdle_irr_pct)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    base_case = next((case for case in cases if case.name.lower() == "base"), cases[len(cases) // 2])
    sensitivity = build_sensitivity_table(
        current_price=base_case.current_price,
        base_target_price_5y=base_case.target_price_5y,
    )
    return to_jsonable(
        {
            "ticker": ticker,
            "company_name": company_name,
            "mode": mode,
            "summary": summary,
            "case_irrs": [
                {
                    "name": case.name,
                    "irr_3y_pct": expected_irr_pct(case.current_price, case.target_price_3y, 3),
                    "irr_5y_pct": expected_irr_pct(case.current_price, case.target_price_5y, 5),
                }
                for case in cases
            ],
            "sensitivity_table": sensitivity,
            "valuation_notes": [
                "Demo underwriting assumptions are placeholders for local research workflow testing.",
                "Expected IRR is transparent underwriting input, not a return promise.",
                "Valuation can support or block action, but cannot create buy/add without thesis, evidence, technical, and risk gates.",
            ],
            "evidence_links": sorted({ref for case in cases for ref in case.evidence_refs}),
            "decision_gate": {
                "valuation_clears_hurdle": summary.clears_hurdle,
                "hurdle_irr_pct": summary.hurdle_irr_pct,
                "note": "Valuation can support or block action, but cannot create buy/add without thesis, evidence, technical, and risk gates.",
            },
            "trade_instruction": False,
        }
    )


def _request_case_to_core(case) -> ValuationCase:
    assumptions = case.assumptions
    return ValuationCase(
        case.name,
        case.probability,
        case.current_price,
        case.target_price_3y,
        case.target_price_5y,
        case.notes,
        assumptions=ValuationAssumptions(
            revenue_cagr_pct=assumptions.revenue_cagr_pct,
            gross_margin_pct=assumptions.gross_margin_pct,
            operating_margin_pct=assumptions.operating_margin_pct,
            fcf_margin_pct=assumptions.fcf_margin_pct,
            terminal_multiple=assumptions.terminal_multiple,
            dilution_buyback_pct=assumptions.dilution_buyback_pct,
            net_cash_debt_per_share=assumptions.net_cash_debt_per_share,
        ),
        evidence_refs=tuple(case.evidence_refs),
    )


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
    return _underwriting_response(company.ticker, company.company_name, _demo_cases(company, current_price), 15, "demo")


@router.post("/underwrite")
def underwrite_valuation(payload: ValuationUnderwriteRequest) -> dict:
    company = get_company(payload.ticker)
    if not company:
        raise HTTPException(status_code=404, detail="Ticker not found in demo universe")
    cases = tuple(_request_case_to_core(case) for case in payload.cases)
    return _underwriting_response(company.ticker, company.company_name, cases, payload.hurdle_irr_pct, "user_draft")


@router.post("/{ticker}/calculate")
def calculate_ticker_valuation(ticker: str, payload: ValuationUnderwriteRequest) -> dict:
    if payload.ticker.upper() != ticker.upper():
        raise HTTPException(status_code=422, detail="Path ticker and payload ticker must match")
    return underwrite_valuation(payload)
