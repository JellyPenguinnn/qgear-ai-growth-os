# Q-GEAR Live Data and Provider Specification v2.1

## 1. Purpose

v2.1 must make Q-GEAR live-data-capable while preserving demo mode and local-first safety.

Live data is used to improve evidence, metrics, valuation, technical risk, and review quality. Live data must not directly create buy/add actions.

---

## 2. Provider hierarchy

### 2.1 Core official/free providers

```text
SEC EDGAR — filings, submissions, company facts, XBRL financial data
FRED — macro data
EIA — electricity and energy data
```

### 2.2 Optional market-data providers

```text
Alpha Vantage — initial optional daily price provider
Financial Modeling Prep — optional future financials/transcripts/calendar
Finnhub — optional future transcripts/market/fundamentals
Nasdaq Data Link — optional future structured datasets
```

### 2.3 Fallback

```text
yfinance — experimental only, not mission-critical source of truth
```

---

## 3. Provider mode rules

Default mode:

```text
QGEAR_ENV=demo
QGEAR_PRICE_PROVIDER=mock
QGEAR_AI_PROVIDER=none
```

Live mode must be explicit.

Suggested env vars:

```text
QGEAR_ENV=demo | live | mixed
QGEAR_PRICE_PROVIDER=mock | alpha_vantage
SEC_USER_AGENT="qgear-ai-growth-os personal research app your-email@example.com"
SEC_MAX_REQUESTS_PER_SECOND=10
ALPHA_VANTAGE_API_KEY=
FRED_API_KEY=
EIA_API_KEY=
```

Rules:

```text
Demo mode must work without keys.
Missing API keys must return metadata errors, not crash.
Provider errors must not corrupt local state.
Refresh calls should be explicit user/API actions.
No hidden background network refresh unless clearly documented.
```

---

## 4. Provider response envelope

All provider calls should return a stable envelope:

```json
{
  "payload": {},
  "metadata": {
    "provider": "sec_edgar | mock | alpha_vantage | fred | eia",
    "status": "ok | missing_api_key | unavailable | not_implemented | error",
    "source_url": "...",
    "source_name": "...",
    "retrieved_at": "YYYY-MM-DDTHH:MM:SSZ",
    "cached": false,
    "source_date": "YYYY-MM-DD",
    "as_of_date": "YYYY-MM-DD",
    "cache_written_at": "YYYY-MM-DDTHH:MM:SSZ",
    "cache_key": "...",
    "error": null,
    "mode": "demo | live | mixed"
  }
}
```

---

## 5. SEC financial foundation

### 5.1 Ticker to CIK mapping

Add a local mapping file or table:

```text
data/demo/ticker_cik_map.json
```

Example shape:

```json
{
  "NVDA": "0001045810",
  "MSFT": "0000789019",
  "GOOGL": "0001652044"
}
```

If a ticker has no CIK mapping, API should return:

```json
{
  "status": "missing_mapping",
  "ticker": "...",
  "message": "No CIK mapping is available for this ticker."
}
```

### 5.2 Canonical financial metrics

Extract from SEC company facts where possible:

```text
revenue
gross_profit
operating_income
net_income
eps_diluted
operating_cash_flow
capital_expenditure
free_cash_flow
cash_and_equivalents
total_assets
total_liabilities
short_term_debt
long_term_debt
shares_diluted
```

Important: SEC tag names vary by company. The parser must support fallback tag candidates.

Example tag candidates:

```text
Revenue:
- Revenues
- RevenueFromContractWithCustomerExcludingAssessedTax
- SalesRevenueNet

Gross profit:
- GrossProfit

Operating income:
- OperatingIncomeLoss

Net income:
- NetIncomeLoss

Operating cash flow:
- NetCashProvidedByUsedInOperatingActivities

Capex:
- PaymentsToAcquirePropertyPlantAndEquipment
- PaymentsToAcquireProductiveAssets

Assets:
- Assets

Liabilities:
- Liabilities

Long-term debt:
- LongTermDebt
- LongTermDebtAndFinanceLeaseObligations
```

### 5.3 Financial snapshot shape

Suggested model:

```python
@dataclass(frozen=True)
class FinancialMetricSnapshot:
    ticker: str
    cik: str
    fiscal_period: str
    fiscal_year: int
    period_end_date: str
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
```

### 5.4 SEC routes

Add routes:

```text
GET  /data/quality/{ticker}
GET  /financials/{ticker}
GET  /financials/{ticker}/metrics
POST /providers/sec/refresh/{ticker}
```

POST refresh should be explicit and safe.

---

## 6. Price and benchmark provider

### 6.1 Provider interface

Add:

```python
class PriceHistoryProvider(Protocol):
    def daily_adjusted_history(self, ticker: str, *, output_size: str = "compact") -> ProviderResponse:
        ...
```

Implement:

```text
MockPriceHistoryProvider
AlphaVantagePriceProvider
```

### 6.2 Stored price history

Suggested table:

```text
price_history
  ticker
  date
  open
  high
  low
  close
  adjusted_close
  volume
  provider
  source_url
  retrieved_at
  as_of_date
```

Benchmarks:

```text
SPY
QQQ
XLK
SMH
```

### 6.3 Technical engine

Calculate locally:

```text
50DMA
150DMA
200DMA
relative strength vs SPY
relative strength vs QQQ
relative strength vs XLK
relative strength vs SMH
drawdown from 52-week high
volume trend
technical regime
```

Technical regime should be derived from price history and documented.

Suggested first classification:

```text
SUPPORTIVE:
  price above 50DMA and 200DMA, positive relative strength

STABILISING:
  price above 200DMA or recovering above 50DMA, relative strength not strongly negative

WEAKENING:
  price below 50DMA, or falling relative strength, but not fully broken

BROKEN:
  price below 200DMA and weak relative strength / deep drawdown
```

Technical state cannot create thesis or buy/add alone.

### 6.4 Routes

```text
GET  /prices/{ticker}
GET  /technical/{ticker}
POST /providers/prices/refresh/{ticker}
POST /providers/benchmarks/refresh
```

---

## 7. FRED and EIA context

### 7.1 FRED initial series

```text
FEDFUNDS
DGS10
DGS2
CPIAUCSL
UNRATE
```

### 7.2 EIA initial context

Prioritize useful AI-infrastructure context:

```text
electricity demand
retail electricity prices
generation by fuel
regional grid/power context when available
```

### 7.3 Macro/energy rule

Macro and energy context can produce review warnings or context cards, but cannot directly create buy/add actions.

Routes:

```text
GET /macro/status
GET /macro/fred/{series_id}
GET /energy/status
GET /energy/eia/context
```

---

## 8. Data Quality API

Add:

```text
GET /data/quality/{ticker}
GET /data/health
```

Ticker quality response should include:

```json
{
  "ticker": "NVDA",
  "mode": "demo | live | mixed",
  "source_quality_score": 82,
  "evidence_coverage_score": 76,
  "financial_data_status": "ok | stale | missing | error",
  "price_data_status": "ok | stale | missing | error",
  "filing_data_status": "ok | stale | missing | error",
  "earnings_data_status": "ok | stale | missing | error",
  "valuation_data_status": "ok | stale | missing | error",
  "technical_data_status": "ok | stale | missing | error",
  "missing_required_inputs": [],
  "stale_inputs": [],
  "provider_errors": [],
  "can_support_action_in_live_mode": false,
  "reason": "Demo evidence cannot support live-mode buy/add."
}
```

---

## 9. Testing requirements

Provider tests must be fixture-based and no-network by default.

Required tests:

```text
Ticker CIK mapping found/missing.
SEC companyfacts fixture parses metrics.
SEC malformed fixture returns structured error.
Missing SEC User-Agent returns config error.
Alpha Vantage missing API key returns missing_api_key.
Mock price history produces technical indicators.
Technical regime classification works.
FRED/EIA missing key returns metadata error.
Data quality route works for demo ticker.
Provider failure does not crash API.
```

---

## 10. UI implications

UI must show:

```text
Demo / Live / Mixed mode
Provider status
Last refresh
Source dates
Data quality score
Missing inputs
Stale inputs
Provider errors
Whether evidence can support action
```

Add a dedicated page:

```text
/data-health
```

or:

```text
/settings/data
```

---

## 11. Release note

v2.1 should be described as:

```text
Professional live-data foundation with source/evidence/data-quality gates, SEC financial parsing, optional price/benchmark history, technical engine, and clearer live/demo UI.
```

Not:

```text
fully live trading system
investment adviser
performance-proven strategy
```

