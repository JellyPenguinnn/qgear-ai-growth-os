from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.db.sqlite import get_thesis, list_evidence_objects, list_journal_entries, list_positions
from app.serializers import to_jsonable
from qgear_core.demo import DEMO_UNIVERSE, get_company
from qgear_core.models import PortfolioContext
from qgear_core.risk import recommend_position_size

router = APIRouter(prefix="/universe", tags=["universe"])


@router.get("")
def list_universe(
    ai_layer: str | None = Query(default=None),
    decision_state: str | None = Query(default=None),
    min_score: float | None = Query(default=None),
) -> dict:
    companies = []
    for company in DEMO_UNIVERSE:
        if ai_layer and company.ai_layer.value != ai_layer:
            continue
        if decision_state and company.status.value != decision_state:
            continue
        if min_score is not None and company.score.total < min_score:
            continue
        companies.append(company)

    return {
        "mode": "demo",
        "not_recommendations": True,
        "count": len(companies),
        "companies": to_jsonable(companies),
    }


@router.get("/{ticker}")
def stock_detail(ticker: str) -> dict:
    company = get_company(ticker)
    if not company:
        raise HTTPException(status_code=404, detail="Ticker not found in demo universe")

    thesis = get_thesis(company.ticker)
    positions = [position for position in list_positions() if position["ticker"].upper() == company.ticker]
    journal = [entry for entry in list_journal_entries() if entry["ticker"].upper() == company.ticker]
    stored_evidence = [
        {
            "claim": item["claim"],
            "evidence": item["evidence"],
            "source": item["source"],
            "source_date": item["source_date"],
            "confidence": item["confidence"],
            "disproves_if": item["disproves_if"],
            "related_type": item["related_type"],
            "id": item["id"],
        }
        for item in list_evidence_objects(company.ticker)
    ]
    metrics = company.metrics
    current_position_value = sum(position["market_value"] for position in positions)
    cash = 1_500 if positions else 2_000
    total_equity = max(10_000, current_position_value + cash)
    position_weight = current_position_value / total_equity * 100 if total_equity else 0
    sizing = recommend_position_size(
        company.status,
        company.score.total,
        PortfolioContext(
            total_equity=total_equity,
            cash=cash,
            current_position_weight_pct=position_weight,
            current_position_value=current_position_value,
            owned=bool(positions),
        ),
    )

    detail = {
        "company": company,
        "business_summary": f"{company.company_name} is classified in {company.ai_layer.value} for demo research workflows. Seed data is not a buy recommendation.",
        "ai_thesis": company.evidence_summary,
        "evidence_table": [*stored_evidence, *company.evidence],
        "financial_metrics": {
            "revenue_growth_pct": metrics.revenue_growth_pct,
            "revenue_growth_acceleration_pct": metrics.revenue_growth_acceleration_pct,
            "gross_margin_pct": metrics.gross_margin_pct,
            "operating_margin_pct": metrics.operating_margin_pct,
            "fcf_margin_pct": metrics.fcf_margin_pct,
            "net_debt_to_ebitda": metrics.net_debt_to_ebitda,
            "roic_pct": metrics.roic_pct,
        },
        "latest_earnings_analysis": {
            "thesis_change": metrics.latest_earnings_change.value,
            "guidance_raised": metrics.guidance_raised,
            "ai_evidence_improved": metrics.ai_evidence_improved,
            "margin_expanded": metrics.margin_expanded,
            "fcf_improved": metrics.fcf_improved,
        },
        "valuation_scenarios": {
            "bear_case_irr_pct": round(metrics.expected_irr_base_pct - 8, 1),
            "base_case_irr_pct": metrics.expected_irr_base_pct,
            "bull_case_irr_pct": round(metrics.expected_irr_base_pct + 10, 1),
            "hurdle_irr_pct": 15,
        },
        "technical_state": {
            "regime": metrics.technical_regime.value,
            "relative_strength_pct": metrics.relative_strength_pct,
            "drawdown_from_high_pct": metrics.drawdown_from_high_pct,
        },
        "portfolio_risk_impact": {
            "positions": positions,
            "single_stock_limit_pct": 15,
            "benchmark_placeholders": ["SPY", "QQQ", "XLK", "SMH"],
        },
        "decision_state": company.decision,
        "position_sizing": sizing,
        "approved_thesis": thesis,
        "invalidation_rule": thesis["breaks_if"] if thesis else "",
        "journal_entries": journal,
    }
    return to_jsonable(detail)
