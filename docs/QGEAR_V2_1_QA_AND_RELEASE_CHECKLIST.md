# Q-GEAR v2.1 QA and Release Checklist

## 1. Purpose

Use this checklist before marking v2.1 complete.

The goal is not only “tests pass.” The goal is:

```text
core brain safe
live data safe
AI draft-only
UI clear
demo mode working
provider failure safe
docs honest
no secrets
no trading execution
```

---

## 2. Git hygiene

Run:

```bash
git status --short --branch
git ls-files -i -c --exclude-standard
```

Confirm no tracked:

```text
.env
.env.local
API keys
private keys
.venv
node_modules
.next
SQLite DB files
DuckDB files
cache files
__pycache__
pytest cache
local screenshots with private data
```

---

## 3. Core brain regression checklist

Confirm tests cover:

```text
No thesis blocks buy/add.
No invalidation rule blocks buy/add.
Price-only evidence blocks buy/add.
AI_DRAFT evidence blocks buy/add.
LOW-confidence evidence blocks buy/add.
Missing source date/type blocks buy/add.
Demo evidence blocks live-mode action support.
Provider error blocks action-changing live decision.
Expected IRR below hurdle blocks buy/add.
Broken technical regime blocks buy/add.
Weakened/broken earnings blocks buy/add.
Concentration/cash buffer/drawdown block buy/add.
Score alone cannot override hard gates.
```

---

## 4. Provider checks

### 4.1 SEC

Check:

```text
ticker → CIK mapping works
missing CIK returns structured error
SEC fixture parses financial metrics
SEC malformed cache returns structured error
source metadata is retained
filing_date and data_available_date exist where available
refresh route is explicit POST
no live network needed for tests
```

### 4.2 Price / benchmark

Check:

```text
mock price history works without API key
missing Alpha Vantage key returns missing_api_key
price history stored/returned with metadata
benchmarks SPY/QQQ/XLK/SMH supported
technical indicators calculated from history
technical regime classification tested
```

### 4.3 FRED/EIA

Check:

```text
missing keys return safe metadata errors
fixtures parse when available
macro/energy context is review-only
no action mutation from macro/energy context
```

---

## 5. AI safety checks

Check:

```text
QGEAR_AI_PROVIDER=none by default
AI status visible
AI calls are explicit POST requests
OpenAI mode requires explicit external_ai_acknowledged=true
AI output is draft-only
AI output does not mutate decision state
AI draft evidence requires user verification before saving
AI draft cannot support buy/add
price-only AI evidence rejected
malformed AI JSON rejected
LOW-confidence AI evidence rejected for action support
```

---

## 6. UI/UX checks

Check routes:

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

For each route confirm:

```text
clear page title
clear purpose
not financial advice / local research tone where relevant
live/demo/source status visible where relevant
no buy/sell signal vibe
actions are review or draft actions
empty states are understandable
forms have labels
errors are clear
mobile layout is acceptable if possible
```

---

## 7. Command verification

Run Python:

```bash
python3 scripts/run_tests.py
python3 -m compileall packages apps/api scripts tests
python3 scripts/seed_local_data.py
```

Run frontend:

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

Built web smoke:

```bash
cd apps/web
npm run build
npm run start
```

Check:

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

---

## 8. Docs to update

Before final v2.1 summary, update:

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

---

## 9. Known limitation format

Document limitations honestly:

```text
Live provider behavior verified / not verified
Which providers require keys
Which tests used fixtures only
Whether GitHub-hosted CI was observed
Whether browser visual smoke passed
Whether backtesting is still fixture-only
Whether valuation remains draft/underwriting only
```

---

## 10. Final v2.1 report template

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

