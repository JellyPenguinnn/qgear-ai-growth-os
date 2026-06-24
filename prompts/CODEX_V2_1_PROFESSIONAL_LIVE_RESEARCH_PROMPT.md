/goal Upgrade Q-GEAR AI Growth OS from v2.0 local/demo research OS to v2.1 Professional Live Research Foundation. Prioritize the deterministic Q-GEAR brain, live-data readiness, source/evidence/data-quality gates, professional UI/UX clarity, and verification. Do not weaken any investment guardrail. Stop after v2.1 is fully locally verified and commit-ready, or if a real blocker requires user approval.

Repository:

```text
JellyPenguinnn/qgear-ai-growth-os
```

Start from the current main branch, currently expected around:

```text
f167a3d0537766a618c1917142f65210e4fff8a4
Upgrade Q-GEAR to v2.0 research OS
```

## Read first

Before editing, read:

```text
AGENTS.md
docs/QGEAR_VISION_AND_PRODUCT_SPEC.md
docs/QGEAR_V2_1_PROFESSIONAL_LIVE_RESEARCH_SPEC.md
docs/QGEAR_CORE_BRAIN_V2_1_SPEC.md
docs/QGEAR_LIVE_DATA_AND_PROVIDER_SPEC.md
docs/QGEAR_UI_UX_V2_1_SPEC.md
docs/QGEAR_V2_1_QA_AND_RELEASE_CHECKLIST.md
README.md
docs/project_status.md
docs/roadmap.md
docs/iteration_log.md
docs/API_EXAMPLES.md
docs/research/source_library.md
packages/qgear-core/src/qgear_core/
packages/qgear-ingest/src/qgear_ingest/
packages/qgear-ai/src/qgear_ai/
apps/api/app/
apps/web/src/
tests/
.github/workflows/ci.yml
```

Run:

```bash
git status --short --branch
```

Do not modify `AGENTS.md` unless a serious safety/security correction is required and clearly justified. `AGENTS.md` is the stable repo contract.

---

## Current v2.0 understanding

v2.0 already includes:

```text
Today page
Research Pipeline
Evidence Workbench
Stock Workbench
AI provider foundation
Draft-only AI routes
AI output validation
Editable valuation underwriting
Portfolio/journal intelligence
Reports
CI workflow file
Local test/build/smoke verification documented
```

Do not reimplement v2.0 from scratch. Build on it.

---

## Main v2.1 objective

v2.1 should move Q-GEAR beyond demo without becoming a trading bot.

The goal is:

```text
Professional live-data-capable research OS
+ stronger core decision brain
+ source-quality and evidence-quality gates
+ live SEC financial foundation
+ optional live price/benchmark foundation
+ technical engine from price history
+ FRED/EIA macro and energy context foundation
+ clean UI/UX for live/demo/mixed state
+ full verification and release docs
```

The core brain is the highest priority. UI, AI, and live data must support the brain; they must not bypass it.

---

## Non-negotiables

Never add:

```text
auto-trading
broker execution
margin
options-by-default
day-trading workflow
price-only buy-the-dip logic
AI-generated trade actions
hardcoded API keys
silent upload of local portfolio/journal/thesis/evidence data
```

Preserve:

```text
No buy/add without approved thesis and invalidation rule.
No buy/add because price dropped.
Fresh positive verified evidence required.
Valuation, technical, freshness, and risk budget must all matter.
AI output is draft-only until user verifies it.
Technical analysis is risk/timing confirmation only.
Demo mode works without keys.
Live provider failures degrade gracefully.
```

---

## Operating mode

Act as Project Manager plus bounded specialist agents.

Use these read-only audit agents before implementation:

```text
1. Core Brain / Strategy Agent
2. Live Data / Provider Agent
3. Backend/API Agent
4. Frontend/UI/UX Agent
5. AI Safety Agent
6. QA/CI Agent
7. Security/Privacy Agent
8. Documentation/PM Agent
```

Each agent must report:

```text
Role:
Files reviewed:
Findings:
Severity:
Recommended changes:
Affected files:
Tests to run:
Blockers:
```

The main agent must consolidate findings before editing.

Do not allow broad overlapping edits from subagents.

---

# Milestone A — Baseline audit and CI reality check

## Goal

Verify current v2.0 state before making changes.

## Tasks

1. Run local baseline if dependencies are available:

```bash
python3 scripts/run_tests.py
python3 -m compileall packages apps/api scripts tests
python3 scripts/seed_local_data.py
cd apps/web && npm run lint
cd apps/web && npm run typecheck
cd apps/web && npm run build
cd apps/web && npm audit --omit=dev
```

2. Check GitHub CI workflow exists.

3. If possible, check current GitHub Actions run status after push.

4. Update docs with reality, not assumptions.

## Exit criteria

```text
Baseline status recorded.
Any failing or unverified checks documented.
No code changes except docs if necessary.
```

---

# Milestone B — Core brain source-quality upgrade

## Goal

Strengthen Q-GEAR before trusting live data or AI evidence.

## Required design

Add or extend core models to support:

```text
EvidenceSourceType:
  DEMO
  MANUAL
  AI_DRAFT
  AI_USER_VERIFIED
  SEC_FILING
  EARNINGS_RELEASE
  TRANSCRIPT
  PRICE_PROVIDER
  MACRO_PROVIDER
  ENERGY_PROVIDER
  OTHER

EvidenceVerificationStatus:
  UNVERIFIED
  USER_VERIFIED
  PROVIDER_VERIFIED
  SYSTEM_VALIDATED
  REJECTED

EvidenceQuality:
  LOW
  MEDIUM
  HIGH
```

Add evidence-quality logic:

```text
AI_DRAFT cannot support buy/add.
LOW confidence cannot support buy/add.
DEMO evidence cannot support live-mode buy/add.
Missing source_date blocks action.
Missing source_type blocks action.
Stale evidence blocks action based on source type.
Provider errors reduce data_quality_score.
```

Add a `DataQualitySnapshot` or equivalent:

```text
ticker
mode
financial_data_status
price_data_status
filing_data_status
earnings_data_status
valuation_data_status
technical_data_status
source_quality_score
evidence_coverage_score
missing_required_inputs
stale_inputs
provider_errors
```

DecisionInput should consume data/evidence quality.

Hard-gate logic should block action if:

```text
source_quality_score below threshold
evidence_coverage_score below threshold
live mode has only demo evidence
AI evidence is unverified
required provider data is stale or failed
```

Preserve demo mode usability:

```text
In demo mode, demo evidence can show workflow states, but the UI must clearly label it as demo.
```

## Tests required

Add regression tests:

```text
AI draft evidence cannot support buy/add.
Verified AI evidence may support evidence gate but cannot override other gates.
Demo evidence cannot support buy/add in live mode.
SEC/provider evidence with source metadata can support evidence gate.
Missing source_type blocks action.
Missing source_date blocks action.
Source quality below threshold blocks action.
Provider failure blocks action-changing live decision.
```

## Exit criteria

```text
qgear-core remains pure.
Existing decision tests still pass.
New source-quality tests pass.
No UI-only decision logic.
```

---

# Milestone C — Live SEC financial foundation

## Goal

Make SEC EDGAR the first professional live financial source.

## Tasks

1. Add ticker → CIK mapping.

At minimum include demo universe tickers where known. For unknown CIKs, return structured missing status.

Suggested file:

```text
data/demo/ticker_cik_map.json
```

2. Extend SEC provider to parse company facts into canonical facts.

Create models such as:

```text
CanonicalFinancialFact
FinancialPeriod
FinancialStatementSnapshot
FinancialMetricSnapshot
```

Canonical metrics:

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

3. Preserve source metadata:

```text
provider
source_url
source_name
filing_date
period_end_date
form
accession_number
retrieved_at
cached
data_available_date
```

4. Store normalized financial snapshots locally.

Keep persistence simple and documented. Use SQLite for local app state and/or DuckDB for analytics where appropriate.

5. Add API routes:

```text
GET /data/quality/{ticker}
GET /financials/{ticker}
GET /financials/{ticker}/metrics
POST /providers/sec/refresh/{ticker}
```

POST refresh must be explicit. No automatic background network calls unless documented and user-triggered.

6. Demo mode must continue working without network.

7. Live mode must degrade gracefully if SEC network or CIK mapping fails.

## Tests required

```text
SEC companyfacts fixture parses canonical metrics.
Missing CIK returns structured provider error.
Malformed SEC facts return structured error.
Financial snapshots include source metadata.
Data availability date is present.
No live network required for tests.
```

## Exit criteria

```text
User can inspect financial metrics sourced from SEC fixture/live provider.
Financial metrics are traceable to source metadata.
Provider failure does not crash app.
Demo mode remains keyless.
```

---

# Milestone D — Live price / benchmark provider and technical engine

## Goal

Replace mock-only technicals with optional real daily price history.

## Provider design

Add a price provider interface that can support:

```text
MockPriceProvider
AlphaVantagePriceProvider
Future providers: FMP/Finnhub/Nasdaq Data Link
```

Use Alpha Vantage only if API key is configured.

Environment variables:

```text
QGEAR_PRICE_PROVIDER=mock | alpha_vantage
ALPHA_VANTAGE_API_KEY=
```

Default:

```text
QGEAR_PRICE_PROVIDER=mock
```

## Tasks

1. Implement daily adjusted price history provider.

2. Store price history locally:

```text
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

3. Add benchmark history for:

```text
SPY
QQQ
XLK
SMH
```

4. Add technical calculation in pure code:

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

5. Add routes:

```text
GET /prices/{ticker}
GET /technical/{ticker}
POST /providers/prices/refresh/{ticker}
POST /providers/benchmarks/refresh
```

6. UI:

```text
Stock Workbench technical card shows live/mock badge.
Technical state shows source date and provider.
Today/Pipeline flags missing/stale technical data.
```

## Tests required

```text
Fixture price history calculates moving averages.
Relative strength calculation works.
Technical regime classification works.
Missing price data returns structured error.
Mock mode works without API key.
Alpha Vantage mode missing key returns missing_api_key, not crash.
```

## Exit criteria

```text
Technicals are calculated from price history, not hardcoded demo values.
Technical analysis remains timing/risk confirmation only.
No buy/add from chart alone.
```

---

# Milestone E — FRED/EIA macro and AI infrastructure context

## Goal

Add live macro/energy context without turning it into direct trade signals.

## Tasks

1. Implement FRED provider if `FRED_API_KEY` is configured.

Initial series:

```text
FEDFUNDS
DGS10
DGS2
CPIAUCSL
UNRATE
```

2. Implement EIA provider if `EIA_API_KEY` is configured.

Initial focus:

```text
electricity demand
retail electricity prices
generation by fuel
grid/power context useful for AI data-center beneficiaries
```

3. Store macro/energy snapshots with metadata.

4. Add UI context cards:

```text
Macro backdrop
Data-center power context
Rates/liquidity caution
Energy/power demand context
```

5. Do not allow macro/energy context to create buy/add.

## Tests required

```text
FRED missing key returns metadata error.
EIA missing key returns metadata error.
Fixture observations parse.
Macro context is review-only.
```

## Exit criteria

```text
Macro/energy data supports research context only.
No action state mutation from macro/energy data alone.
```

---

# Milestone F — UI/UX professional polish and live/demo clarity

## Goal

Make the app cleaner, clearer, and less complicated to use.

## Tasks

1. Add a Data Health page:

```text
/data-health
```

or:

```text
/settings/data
```

It should show:

```text
Demo / Live / Mixed mode
SEC status
Price provider status
Benchmark provider status
FRED status
EIA status
AI status
last successful refresh
last error
missing keys
what is live vs demo
what data can support action
what data is review-only
```

2. Improve onboarding flow:

```text
Step 1: Portfolio assumptions
Step 2: Data mode
Step 3: Providers / API keys explanation
Step 4: AI mode
Step 5: Start with demo or refresh live data
```

3. Improve Stock Workbench:

```text
Show data quality before decision card.
Show evidence quality.
Show live/demo badges.
Show missing required inputs.
Show “why blocked” clearly.
```

4. Improve Today:

```text
Top priority should be review queue and data-health problems, not rankings.
```

5. Improve visual polish:

```text
Better spacing
Better typography
Cleaner cards
Less dense tables
Better empty states
Loading states
Error states
Mobile-friendly layout
```

6. Add UI smoke tests if practical.

Prefer a route-level smoke script if Playwright would add too much dependency cost.

## Exit criteria

```text
UI is clearer and easier to use.
Live/demo status is obvious.
A new user understands what to review first.
Frontend lint/typecheck/build pass.
Route smoke passes.
```

---

# Milestone G — Professional verification and release pass

## Goal

Make sure everything works.

## Required checks

Run:

```bash
python3 scripts/run_tests.py
python3 -m compileall packages apps/api scripts tests
python3 scripts/seed_local_data.py
```

Frontend:

```bash
cd apps/web
npm run lint
npm run typecheck
npm run build
npm audit --omit=dev
```

API smoke:

```bash
./scripts/dev_api.sh
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/today
curl http://127.0.0.1:8000/pipeline
curl http://127.0.0.1:8000/ai/status
curl http://127.0.0.1:8000/providers/status
curl http://127.0.0.1:8000/universe
curl http://127.0.0.1:8000/portfolio
curl http://127.0.0.1:8000/earnings
curl http://127.0.0.1:8000/reports/weekly
curl http://127.0.0.1:8000/alerts
curl http://127.0.0.1:8000/journal/analytics
curl http://127.0.0.1:8000/valuation/NVDA
curl http://127.0.0.1:8000/financials/NVDA
curl http://127.0.0.1:8000/technical/NVDA
curl http://127.0.0.1:8000/data/quality/NVDA
curl http://127.0.0.1:8000/data/health
```

Built web route smoke:

```text
/
/pipeline
/evidence
/universe
/universe/NVDA
/earnings
/portfolio
/journal
/reports
/settings
/data-health or /settings/data
```

If browser visual smoke is unavailable, document the exact blocker.

## Docs to update

```text
README.md
docs/project_status.md
docs/iteration_log.md
docs/roadmap.md
docs/API_EXAMPLES.md
docs/QGEAR_VISION_AND_PRODUCT_SPEC.md
docs/research/
docs/ci.md
.env.example
```

## v2.1 exit criteria

```text
Core brain includes source/evidence/data-quality gates.
Live SEC financial foundation exists and is fixture-tested.
Optional price provider and technical engine exist and are fixture-tested.
FRED/EIA provider behavior is improved and fixture-tested.
UI clearly distinguishes live/demo/mixed data.
Data Health page exists.
Demo mode works without keys.
Provider failures degrade gracefully.
No auto-trading/margin/options/broker execution exists.
AI remains draft-only and explicit.
All local tests pass.
Frontend build passes.
API smoke passes.
Built route smoke passes.
Docs are current.
Commit-ready summary provided.
```

## Final report format

End with:

```text
Summary:
Files changed:
Core brain changes:
Provider/live-data changes:
UI/UX changes:
AI safety changes:
Tests run:
Results:
What was verified:
What could not be verified:
Known risks:
Remaining limitations:
Recommended next milestone:
Suggested commit message:
```

Do not claim live provider verification unless live network/API-key checks were actually run.
Do not claim visual QA if browser smoke could not run.
Do not modify AGENTS.md unless absolutely necessary for safety.
