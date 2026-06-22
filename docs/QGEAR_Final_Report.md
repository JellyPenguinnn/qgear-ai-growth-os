# Q-GEAR AI Growth OS — Final System Report

## 1. Final project identity

**Recommended repo name:** `qgear-ai-growth-os`

**Full name:** Q-GEAR AI Growth OS

**Meaning:** Quality Growth, Earnings Acceleration, AI Relevance, Risk Control.

**Purpose:** A local, personal-use US equity research operating system for identifying, underwriting, tracking, and reviewing high-quality AI-era growth stocks. The system is not an auto-trader and not a public advisory product. It is a disciplined research, scoring, portfolio, and decision-journal tool.

**Target user profile:** 20–30 year old Singapore/Malaysia investor, starting with approximately USD 10,000, focused on US technology and AI infrastructure stocks.

**Core style:** Long-term, slightly aggressive, fundamental-first growth investing, supported by technical analysis for timing and risk control.

**Primary objective:** Aim for 20–25% annualised return over rolling 5-year periods, with 30% annualised treated as an aspirational bull-cycle outcome, not a guaranteed objective.

**Risk objective:** Normal max drawdown budget 25–30%; hard portfolio drawdown limit 35%. If the portfolio drawdown exceeds 35%, the system enters hard strategy-audit mode and blocks normal risk-taking.

## 2. Why this system exists

The AI infrastructure cycle is broad enough to justify a dedicated research system. The theme is not only about GPUs. It includes accelerators, custom silicon, memory, storage, foundry, semiconductor equipment, networking, optical interconnect, hyperscale cloud, data-centre power, cooling, electrical infrastructure, and software monetisation.

The key problem is that the AI theme attracts hype. The system must therefore separate:

- real AI earnings power,
- measurable segment growth,
- margin expansion,
- guidance improvement,
- backlog/RPO/order evidence,
- and free cash flow,

from weak narratives where a company only says “AI” without financial proof.

## 3. Research foundation

The system is based on five evidence pillars.

### Pillar 1 — Rare stock-market winners matter

Bessembinder’s work shows that long-term wealth creation in equities is highly concentrated in a small minority of stocks. This supports building a system that tries to identify and hold exceptional compounders instead of constantly rotating through average companies.

### Pillar 2 — Quality and profitability matter

AQR’s Quality Minus Junk research and Novy-Marx’s gross profitability research support the idea that profitable, growing, well-managed companies with strong balance sheets and better economic quality deserve attention. The system therefore should not chase low-quality AI hype.

### Pillar 3 — Earnings acceleration matters

Post-earnings-announcement drift research supports paying attention to earnings surprises, guidance, and post-earnings price behaviour. The system treats quarterly earnings as the main evidence-update event.

### Pillar 4 — Momentum and trend matter, but only as confirmation

Momentum and trend-following research support using relative strength and trend as confirmation and risk control. But technicals cannot create a buy thesis by themselves. They only help answer when and how much.

### Pillar 5 — Active investing is difficult

SPIVA data shows that many active managers underperform benchmarks. The system therefore must benchmark against SPY, QQQ, XLK, and SMH, maintain decision logs, avoid overfitting, and honestly tell the user when the strategy is not adding value.

## 4. Return and drawdown policy

For a USD 10,000 starting portfolio:

| Metric | Final default |
|---|---:|
| Base CAGR objective | 18–22% |
| Strong objective | 22–25% |
| Stretch objective | 25–30% |
| Normal max drawdown budget | 25–30% |
| Hard max drawdown limit | 35% |
| Live positions | 6–10 |
| Cash buffer | 10–20% |
| Max single stock | 15% |
| Holding period | 1–5 years |
| Margin | Disabled |
| Options | Disabled at launch |
| Auto-trading | Disabled |

## 5. Portfolio model for USD 10,000

Suggested allocation:

| Bucket | Allocation | USD amount |
|---|---:|---:|
| Core AI compounders | 45–55% | $4,500–$5,500 |
| AI infrastructure satellites | 25–35% | $2,500–$3,500 |
| Opportunistic growth | 5–10% | $500–$1,000 |
| Cash/opportunity reserve | 10–20% | $1,000–$2,000 |

Position sizing:

| Status | Allocation | USD amount on $10k |
|---|---:|---:|
| Research only | 0% | $0 |
| Starter allowed | 2.5–5% | $250–$500 |
| Normal position | 5–8% | $500–$800 |
| High conviction | 8–12% | $800–$1,200 |
| Exceptional conviction | 12–15% | $1,200–$1,500 |
| Absolute cap | 15% | $1,500 |

The system must never recommend deploying all capital immediately. It should allow gradual deployment only when evidence improves.

## 6. The system brain

The brain is not a single indicator. It is a multi-engine decision system.

Final master formula:

```text
Final Action =
AI Relevance
× Business Quality
× Earnings Acceleration
× Valuation/Expected IRR
× Technical Regime
× Portfolio Risk Budget
× Evidence Freshness
− Red Flags
```

Core rule:

```text
Price movement alone can never create a buy or add signal.
```

A lower price improves only the valuation input. It does not improve business quality, earnings quality, management execution, AI relevance, or competitive advantage.

## 7. Seven core engines

### Engine 1 — AI infrastructure causal map

Map the AI stack:

```text
AI model demand
→ compute demand
→ GPU/ASIC demand
→ HBM/DRAM/NAND/storage demand
→ networking/optical demand
→ data-centre buildout
→ power/cooling/grid demand
→ cloud and software monetisation
```

Classify tickers into layers:

- Compute
- Memory
- Storage
- Foundry
- Semiconductor equipment
- Networking/optical
- Hyperscale cloud
- Data-centre power/cooling
- Data-centre real estate
- AI software/security/data platforms

A ticker cannot qualify just because it mentions AI. It needs measurable evidence.

### Engine 2 — Quality-growth filter

Measures:

- revenue growth,
- revenue acceleration,
- gross margin,
- operating margin,
- FCF margin,
- ROIC/ROE,
- net cash/debt,
- dilution,
- stock-based compensation,
- inventory risk,
- capex efficiency,
- competitive advantage.

### Engine 3 — Earnings acceleration engine

For each earnings report, compare:

- revenue/EPS vs consensus,
- segment growth,
- AI-related growth,
- gross margin,
- operating leverage,
- FCF,
- guidance,
- backlog/RPO/orders,
- management tone,
- estimate revisions,
- price/volume reaction.

Output:

```text
Thesis strengthened / unchanged / weakened / broken
```

### Engine 4 — Valuation and expected-return engine

For each stock, build bear/base/bull cases:

- revenue CAGR,
- margin path,
- FCF margin,
- terminal multiple,
- dilution/buyback,
- net cash/debt,
- 3-year and 5-year expected price,
- expected IRR,
- downside risk.

Minimum hurdle:

| Case | Requirement |
|---|---:|
| Base-case IRR | 15–18%+ |
| Probability-weighted IRR | 18–22%+ |
| Bull-case IRR | 30%+ but credible |
| Bear-case portfolio damage | preferably <= 1.5–2.0% of portfolio |

### Engine 5 — Technical confirmation engine

Technicals are risk/timing only.

Track:

- price vs 50/150/200-day moving averages,
- relative strength vs SPY, QQQ, XLK, SMH,
- volume trend,
- drawdown from 52-week high,
- volatility regime,
- base/breakout/breakdown status,
- support/resistance zones.

Rule:

```text
Fundamentals decide what to buy.
Valuation decides what it is worth.
Technicals decide when and how much.
```

### Engine 6 — Portfolio risk engine

Before any buy/add:

- check cash,
- check current position size,
- check single-stock cap,
- check theme/sub-theme concentration,
- check drawdown mode,
- check expected portfolio IRR,
- check worst-case scenario,
- block adds if risk budget is exceeded.

### Engine 7 — Anti-generic guardrail engine

Block these behaviours:

- buy because price dropped,
- buy because AI is popular,
- buy because stock is oversold,
- buy because old target price is higher,
- buy because the user has cash,
- average down without fresh evidence,
- move fair value down/up only because price changed,
- ignore guidance cuts,
- ignore margin deterioration,
- ignore broken trend.

Valid add reason:

```text
Revenue growth accelerated.
AI-related segment improved.
Gross margin expanded.
Guidance was raised.
Free cash flow improved.
Valuation now supports required IRR.
Technical trend stabilised.
Portfolio risk budget allows the add.
```

Invalid add reason:

```text
The stock is down 20%, so it is cheaper.
```

## 8. Scoring model

100-point model:

| Component | Weight |
|---|---:|
| AI infrastructure relevance | 12 |
| Business quality | 18 |
| Revenue and earnings acceleration | 18 |
| Earnings report/guidance/revisions | 17 |
| Valuation and expected IRR | 15 |
| Technical trend/relative strength | 10 |
| Portfolio fit/risk control | 10 |
| Total | 100 |

Final action is not based only on score. It is:

```text
Action = Score + Hard Gates + Risk Budget + Evidence Freshness
```

A score of 90 can still be blocked if latest earnings weakened, valuation is extreme, technicals are broken, or portfolio concentration is too high.

## 9. Decision states

Do not use only buy/sell/hold.

Use these states:

| State | Meaning |
|---|---|
| Rejected | Not good enough |
| Research candidate | Interesting but incomplete |
| Watchlist | Good but not actionable |
| Approved thesis | Business case is strong |
| Approved valuation zone | Price supports required return |
| Technical wait | Fundamentals good, chart/risk not ready |
| Starter allowed | Small position allowed |
| Add allowed | New evidence confirms thesis |
| Hold | Own it, but no add |
| Trim candidate | Valuation/concentration/risk too high |
| Exit / thesis broken | Original thesis invalidated |

## 10. User flow

### Onboarding

User inputs:

- starting capital,
- base currency SGD/MYR,
- country Singapore/Malaysia,
- risk style,
- target CAGR,
- hard drawdown limit,
- cash buffer,
- max position size,
- broker/manual portfolio,
- margin disabled,
- options disabled,
- auto-trading disabled.

### Universe building

System builds AI stock universe, classifies companies by stack layer, and stores evidence.

### Screening

System applies hard gates:

- AI relevance,
- business quality,
- earnings quality,
- valuation/IRR,
- technical state,
- risk budget,
- evidence freshness.

### Stock deep dive

User opens stock page:

- company summary,
- AI thesis,
- financial trends,
- latest earnings,
- valuation cases,
- technical status,
- risk flags,
- decision state,
- source evidence.

### Thesis approval

Before any buy/add is actionable, user must approve a thesis and invalidation rule.

### Position sizing

System calculates allowed position amount for $10k:

- starter $250–$500,
- normal $500–$800,
- high conviction $800–$1,200,
- max $1,500.

### Manual trade and journal

The user manually executes trade in broker. The app logs:

- date,
- ticker,
- action,
- amount,
- price,
- score,
- thesis,
- evidence,
- expected IRR,
- invalidation rule,
- next review date.

### Daily workflow

Light monitoring only:

- major price moves,
- filings,
- earnings dates,
- alerts,
- technical damage,
- thesis-changing news.

Daily output should usually say “No action.”

### Weekly workflow

Weekly report:

- top 10 candidates,
- upgrades/downgrades,
- valuation-zone entries,
- technical trend changes,
- portfolio risk,
- cash deployment opportunities.

### Monthly workflow

Portfolio review:

- performance vs benchmarks,
- position contribution,
- exposure,
- drawdown,
- expected IRR,
- mistake review.

### Quarterly workflow

Core workflow:

- pre-earnings checklist,
- post-earnings analysis,
- thesis update,
- score update,
- action update.

### Annual workflow

Strategy audit:

- beat benchmarks or not,
- risk-adjusted performance,
- signal review,
- mistake review,
- strategy calibration.

## 11. Data sources

### Free/core

- SEC EDGAR APIs for submissions, filings, and XBRL company facts.
- FRED API for macro data.
- EIA API for energy/electricity data.

### Optional paid/third-party

- Alpha Vantage for prices, fundamentals, technicals, FX.
- Financial Modeling Prep for transcripts, financial statements, calendars.
- Finnhub for market data, fundamentals, transcripts, estimates.
- Nasdaq Data Link for structured datasets.

### Fallback

- yfinance only for experiments/fallback, not mission-critical.

## 12. Recommended technical architecture

### Monorepo

```text
qgear-ai-growth-os/
  apps/
    web/          # Next.js frontend
    api/          # FastAPI backend
  packages/
    qgear-core/   # scoring, data models, domain logic
    qgear-ingest/ # data connectors
    qgear-ai/     # LLM prompt templates and evaluators
  data/
    duckdb/
    sqlite/
    cache/
  docs/
  scripts/
  tests/
  AGENTS.md
  README.md
```

### Frontend

- Next.js + TypeScript
- Tailwind CSS
- shadcn/ui or clean custom components
- ECharts/Recharts/TradingView lightweight charts

### Backend

- Python FastAPI
- Pydantic models
- SQLAlchemy or SQLModel for app state
- DuckDB for analytics
- SQLite for local app state
- APScheduler or Prefect Lite for scheduled jobs

### AI layer

- Structured JSON output only
- Prompt templates by task
- Source citation required for claims
- Confidence and disproof criteria required
- No hallucinated financial advice

### Testing

- Unit tests for scoring and decision gates
- Integration tests for API endpoints
- Fixture-based tests for sample earnings
- No look-ahead backtest tests
- Frontend smoke tests

## 13. MVP scope

### Build in v0.1

- local app skeleton,
- onboarding/settings,
- watchlist,
- portfolio tracker,
- AI universe,
- SEC ingestion,
- price ingestion,
- basic technical indicators,
- fundamental metrics,
- scoring model,
- decision engine,
- stock memo page,
- journal,
- weekly report.

### Defer to v0.2

- transcript ingestion,
- advanced valuation engine,
- backtesting lab,
- broker CSV import,
- macro/energy overlays,
- alerts,
- estimate revisions.

### Defer to v0.3

- IBKR integration,
- paper trading,
- advanced risk simulation,
- multi-user mode,
- cloud sync.

Auto-trading is not in scope.

## 14. Final rulebook

1. No buy without thesis.
2. No add without new evidence.
3. Price movement alone is not evidence.
4. Earnings override price.
5. Technicals are risk control, not thesis.
6. Valuation must be tied to expected future cash flows.
7. Position size follows evidence quality.
8. Every position needs an invalidation rule.
9. The system must allow “do nothing.”
10. The model must be benchmarked and audited.

## 15. Key sources to include in project docs

- OpenAI Codex docs: https://developers.openai.com/codex
- SEC EDGAR APIs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- SEC fair access: https://www.sec.gov/about/developer-resources
- FRED API: https://fred.stlouisfed.org/docs/api/fred/
- EIA Open Data: https://www.eia.gov/opendata/
- Alpha Vantage docs: https://www.alphavantage.co/documentation/
- FMP docs: https://site.financialmodelingprep.com/developer/docs
- Finnhub docs: https://finnhub.io/docs/api
- Nasdaq Data Link docs: https://docs.data.nasdaq.com/
- AQR Quality Minus Junk: https://www.aqr.com/Insights/Research/Working-Paper/Quality-Minus-Junk
- Novy-Marx gross profitability: https://ideas.repec.org/a/eee/jfinec/v108y2013i1p1-28.html
- Bessembinder ASU research page: https://wpcarey.asu.edu/department-finance/faculty-research/do-stocks-outperform-treasury-bills
- Jegadeesh & Titman momentum: https://ideas.repec.org/a/bla/jfinan/v48y1993i1p65-91.html
- AQR trend following: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2993026
- Gartner AI spending: https://www.gartner.com/en/newsroom/press-releases/2026-1-15-gartner-says-worldwide-ai-spending-will-total-2-point-5-trillion-dollars-in-2026
- Gartner semiconductor forecast: https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026
- IEA Energy and AI: https://www.iea.org/reports/energy-and-ai
