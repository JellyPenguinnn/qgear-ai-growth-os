from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from qgear_ingest.providers.base import ProviderMetadata, ProviderResponse, ProviderStatus


TAG_CANDIDATES: dict[str, tuple[str, ...]] = {
    "revenue": (
        "Revenues",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "SalesRevenueNet",
    ),
    "gross_profit": ("GrossProfit",),
    "operating_income": ("OperatingIncomeLoss",),
    "net_income": ("NetIncomeLoss",),
    "eps_diluted": ("EarningsPerShareDiluted",),
    "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",),
    "capital_expenditure": (
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsToAcquireProductiveAssets",
    ),
    "cash_and_equivalents": (
        "CashAndCashEquivalentsAtCarryingValue",
        "CashAndCashEquivalents",
    ),
    "total_assets": ("Assets",),
    "total_liabilities": ("Liabilities",),
    "short_term_debt": ("ShortTermBorrowings", "ShortTermDebt"),
    "long_term_debt": (
        "LongTermDebt",
        "LongTermDebtAndFinanceLeaseObligations",
    ),
    "shares_diluted": ("WeightedAverageNumberOfDilutedSharesOutstanding",),
}


@dataclass(frozen=True)
class FinancialMetricSnapshot:
    ticker: str
    cik: str
    fiscal_period: str | None
    fiscal_year: int | None
    period_end_date: str | None
    filing_date: str | None
    data_available_date: str | None
    form: str | None
    revenue: float | None
    gross_profit: float | None
    operating_income: float | None
    net_income: float | None
    eps_diluted: float | None
    operating_cash_flow: float | None
    capital_expenditure: float | None
    free_cash_flow: float | None
    cash_and_equivalents: float | None
    total_assets: float | None
    total_liabilities: float | None
    short_term_debt: float | None
    long_term_debt: float | None
    shares_diluted: float | None
    source_metadata: ProviderMetadata
    missing_metrics: tuple[str, ...] = ()


def parse_companyfacts_financial_snapshot(
    *,
    ticker: str,
    cik: str,
    response: ProviderResponse,
) -> FinancialMetricSnapshot:
    if response.status != ProviderStatus.OK:
        raise ValueError(response.metadata.error or f"Provider status is {response.status.value}.")
    payload = response.payload
    facts = payload.get("facts", {}).get("us-gaap", {}) if isinstance(payload, dict) else {}
    if not isinstance(facts, dict) or not facts:
        raise ValueError("SEC companyfacts payload does not contain us-gaap facts.")

    selected: dict[str, dict[str, Any] | None] = {
        metric: _latest_fact(facts, tags) for metric, tags in TAG_CANDIDATES.items()
    }
    base_fact = _first_fact(selected)
    if not base_fact:
        raise ValueError("SEC companyfacts payload does not contain supported financial metric tags.")

    operating_cash_flow = _value(selected["operating_cash_flow"])
    capital_expenditure = _value(selected["capital_expenditure"])
    free_cash_flow = None
    if operating_cash_flow is not None and capital_expenditure is not None:
        free_cash_flow = operating_cash_flow - abs(capital_expenditure)

    missing = tuple(metric for metric, fact in selected.items() if fact is None)
    return FinancialMetricSnapshot(
        ticker=ticker.upper(),
        cik=cik.zfill(10),
        fiscal_period=_str_or_none(base_fact.get("fp")),
        fiscal_year=_int_or_none(base_fact.get("fy")),
        period_end_date=_str_or_none(base_fact.get("end")),
        filing_date=_str_or_none(base_fact.get("filed")),
        data_available_date=_str_or_none(base_fact.get("filed")),
        form=_str_or_none(base_fact.get("form")),
        revenue=_value(selected["revenue"]),
        gross_profit=_value(selected["gross_profit"]),
        operating_income=_value(selected["operating_income"]),
        net_income=_value(selected["net_income"]),
        eps_diluted=_value(selected["eps_diluted"]),
        operating_cash_flow=operating_cash_flow,
        capital_expenditure=capital_expenditure,
        free_cash_flow=free_cash_flow,
        cash_and_equivalents=_value(selected["cash_and_equivalents"]),
        total_assets=_value(selected["total_assets"]),
        total_liabilities=_value(selected["total_liabilities"]),
        short_term_debt=_value(selected["short_term_debt"]),
        long_term_debt=_value(selected["long_term_debt"]),
        shares_diluted=_value(selected["shares_diluted"]),
        source_metadata=response.metadata,
        missing_metrics=missing,
    )


def _latest_fact(facts: dict[str, Any], tags: tuple[str, ...]) -> dict[str, Any] | None:
    rows: list[dict[str, Any]] = []
    for tag in tags:
        fact = facts.get(tag)
        if not isinstance(fact, dict):
            continue
        units = fact.get("units", {})
        if not isinstance(units, dict):
            continue
        for unit_rows in units.values():
            if not isinstance(unit_rows, list):
                continue
            rows.extend(row for row in unit_rows if isinstance(row, dict) and "val" in row)
    if not rows:
        return None
    return max(rows, key=lambda row: (_str_or_none(row.get("filed")) or "", _str_or_none(row.get("end")) or ""))


def _first_fact(selected: dict[str, dict[str, Any] | None]) -> dict[str, Any] | None:
    for metric in ("revenue", "net_income", "total_assets"):
        fact = selected.get(metric)
        if fact:
            return fact
    return next((fact for fact in selected.values() if fact), None)


def _value(fact: dict[str, Any] | None) -> float | None:
    if not fact:
        return None
    value = fact.get("val")
    if isinstance(value, bool) or value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _str_or_none(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
