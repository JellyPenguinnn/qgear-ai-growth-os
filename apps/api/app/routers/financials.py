from __future__ import annotations

from fastapi import APIRouter

from app.core.ticker_map import ticker_cik
from app.routers.providers import _bundle, _data_mode
from app.serializers import to_jsonable
from qgear_core.enums import DataMode as CoreDataMode
from qgear_core.models import DataQualitySnapshot
from qgear_ingest.providers.financials import FinancialMetricSnapshot, parse_companyfacts_financial_snapshot

router = APIRouter(prefix="/financials", tags=["financials"])


def financial_snapshot_for_ticker(ticker: str) -> tuple[FinancialMetricSnapshot | None, dict]:
    normalized = ticker.upper()
    cik = ticker_cik(normalized)
    if not cik:
        return None, {
            "status": "missing_mapping",
            "ticker": normalized,
            "message": "No CIK mapping is available for this ticker.",
        }

    response = _bundle().company_facts_provider.company_facts(cik)
    try:
        snapshot = parse_companyfacts_financial_snapshot(ticker=normalized, cik=cik, response=response)
    except ValueError as exc:
        return None, {
            "status": "error",
            "ticker": normalized,
            "cik": cik,
            "message": str(exc),
            "source_metadata": response.metadata,
        }

    return snapshot, {
        "status": "ok",
        "ticker": normalized,
        "cik": cik,
        "snapshot": snapshot,
    }


@router.get("/{ticker}")
def financials(ticker: str) -> dict:
    snapshot, payload = financial_snapshot_for_ticker(ticker)
    if not snapshot:
        return to_jsonable(payload)
    return to_jsonable(payload)


@router.get("/{ticker}/metrics")
def financial_metrics(ticker: str) -> dict:
    snapshot, payload = financial_snapshot_for_ticker(ticker)
    if not snapshot:
        return to_jsonable(payload)
    return to_jsonable(
        {
            "status": "ok",
            "ticker": snapshot.ticker,
            "cik": snapshot.cik,
            "metrics": {
                "revenue": snapshot.revenue,
                "gross_profit": snapshot.gross_profit,
                "operating_income": snapshot.operating_income,
                "net_income": snapshot.net_income,
                "eps_diluted": snapshot.eps_diluted,
                "operating_cash_flow": snapshot.operating_cash_flow,
                "capital_expenditure": snapshot.capital_expenditure,
                "free_cash_flow": snapshot.free_cash_flow,
                "cash_and_equivalents": snapshot.cash_and_equivalents,
                "total_assets": snapshot.total_assets,
                "total_liabilities": snapshot.total_liabilities,
                "short_term_debt": snapshot.short_term_debt,
                "long_term_debt": snapshot.long_term_debt,
                "shares_diluted": snapshot.shares_diluted,
            },
            "period": {
                "fiscal_period": snapshot.fiscal_period,
                "fiscal_year": snapshot.fiscal_year,
                "period_end_date": snapshot.period_end_date,
                "filing_date": snapshot.filing_date,
                "data_available_date": snapshot.data_available_date,
                "form": snapshot.form,
            },
            "missing_metrics": snapshot.missing_metrics,
            "source_metadata": snapshot.source_metadata,
            "not_trade_instruction": True,
        }
    )


def data_quality_for_ticker(ticker: str) -> dict:
    snapshot, payload = financial_snapshot_for_ticker(ticker)
    normalized = ticker.upper()
    mode = CoreDataMode(_data_mode().value)
    missing_required_inputs: list[str] = []
    provider_errors: list[str] = []
    financial_status = "ok"

    if not snapshot:
        financial_status = payload["status"]
        missing_required_inputs.append("sec_companyfacts")
        if payload["status"] == "error":
            provider_errors.append(payload["message"])

    source_quality_score = 80 if snapshot else 35
    evidence_coverage_score = 75 if snapshot else 25
    quality = DataQualitySnapshot(
        ticker=normalized,
        mode=mode,
        financial_data_status=financial_status,
        price_data_status="demo",
        filing_data_status="demo",
        earnings_data_status="demo",
        valuation_data_status="demo",
        technical_data_status="demo",
        source_quality_score=source_quality_score,
        evidence_coverage_score=evidence_coverage_score,
        missing_required_inputs=tuple(missing_required_inputs),
        provider_errors=tuple(provider_errors),
    )
    reason = (
        "Demo financial data is useful for workflow testing but cannot support live-mode buy/add decisions."
        if mode == CoreDataMode.DEMO
        else "Financial data quality is sufficient for review; all Q-GEAR gates still apply."
    )
    return to_jsonable(
        {
            "ticker": normalized,
            "status": "ok" if snapshot else payload["status"],
            "data_quality": quality,
            "can_support_action_in_live_mode": bool(snapshot and mode != CoreDataMode.DEMO and not provider_errors),
            "reason": reason,
            "source_metadata": snapshot.source_metadata if snapshot else payload.get("source_metadata"),
            "not_trade_instruction": True,
        }
    )
