# Project Status

## Current Milestone

v1.0 local/demo completion standard is met as of 2026-06-22, subject to the documented caveats below.

The repository has a working v0.1 skeleton plus v0.1.1 safety hardening: pure core decision logic, FastAPI routes, local SQLite state, optional DuckDB setup, demo universe, seed validation, Next.js screens, prompts, API examples, and PM tracking docs. v0.1.1 was re-verified on 2026-06-22 before starting v0.2.

v0.2 data foundation was completed and verified on 2026-06-22. It does not make live data mandatory and does not turn provider data into trade instructions. Provider work is limited to safe provenance, demo/live routing, provider interfaces, fixture tests, and API visibility.

v0.3 earnings and evidence engine was completed and verified on 2026-06-22. It keeps the existing rule that fresh positive evidence is required for buy/add and weakened evidence blocks buy/add.

v0.4 valuation and backtesting foundation was completed and verified on 2026-06-22. It adds deterministic valuation math, demo valuation API responses, and fixture no-lookahead backtest validation. It is not a performance promise and does not create trade instructions.

v0.5 reports, alerts, and review cycles was completed and verified on 2026-06-22. It adds local review-cycle reports, alert rules, journal analytics, frontend report visibility, and regression tests proving alerts remain review prompts rather than trade instructions.

The v1.0 completion pass fixed production rendering issues found during web route smoke: API-backed pages now use dynamic local fetches instead of stale build-time fallback snapshots, the dynamic stock route resolves its ticker correctly under the installed Next version, and API serialization now includes computed score totals required by the frontend.

## v0.2 Completion Results

- Completed: demo mode works without API keys.
- Completed: provider responses include source metadata: provider, status, source URL/name, source date/as-of date when available, retrieved timestamp, cache status, cache timestamp/key, mode, and error message when applicable.
- Completed: demo/live routing is explicit through `/providers/status` and health output.
- Completed: SEC company facts, submissions, and filing metadata provider methods exist with custom User-Agent, local cache, backoff/retry, graceful failures, and a max rate of 10 requests/second.
- Completed: price provider interface exists with mock daily OHLC snapshots.
- Completed: benchmark snapshot support exists for SPY, QQQ, XLK, and SMH.
- Completed: provider metadata is visible through API routes, README, and API examples.
- Completed: file-backed tests cover provider metadata, SEC cache reads, SEC filing metadata extraction, mock price snapshots, benchmark snapshots, and API provider routes.
- Completed: no secrets are hardcoded and live network access is not required for tests.
- Completed: existing decision-brain, API, seed, and frontend checks remained green.

## v0.3 Completion Results

- Completed: earnings review model exists for pre-earnings and post-earnings workflows.
- Completed: earnings review schema includes revenue/EPS surprise, guidance changes, segment/AI evidence, margin trend, FCF trend, management tone, thesis status change, score change, and action change.
- Completed: manual evidence input path stores structured evidence with claim, evidence, source, source date, confidence, and disproves_if.
- Completed: thesis strengthened/unchanged/weakened/broken logic is deterministic and tested.
- Completed: structured evidence and earnings review persistence exists in local SQLite.
- Completed: earnings API exposes event details, stored reviews, and evidence objects in demo mode without external providers.
- Completed: tests prove fresh positive evidence is required for add and weakened evidence blocks buy/add.
- Completed: prompt templates use canonical evidence field names.

## v0.4 Completion Results

- Completed: bear/base/bull valuation case model exists.
- Completed: 3-year and 5-year expected IRR calculations exist.
- Completed: probability-weighted IRR calculation exists.
- Completed: valuation hurdle API output can support decision gates.
- Completed: benchmark comparison uses SPY, QQQ, XLK, and SMH demo snapshots from the provider layer.
- Completed: backtest skeleton uses fixture data and records availability dates to avoid look-ahead bias.
- Completed: backtest endpoint summarizes limitations.
- Completed: tests cover great-company-too-expensive, probability-weighted IRR, probability validation, and no-lookahead guardrails.

## v0.5 Exit Criteria

- Completed: daily brief, weekly ranking, monthly portfolio review, quarterly earnings review, and annual strategy audit are generated from local/demo state.
- Completed: alert rules exist for filings, earnings, stale evidence, technical breaks, concentration, drawdown, and thesis review dates.
- Completed: alerts never become trade instructions.
- Completed: journal analytics summarize action mix, evidence coverage, and unresolved outcomes.
- Completed: reports expose decision states, reasons, blockers, evidence, source metadata, confidence, and review cadence where applicable.
- Completed: the Reports UI now surfaces alert queues and monthly/quarterly/annual review summaries.
- Completed: tests cover alert generation, journal analytics, and report integration.

## v1.0 Completion Criteria

- Completed: end-to-end local flow works: settings, universe, stock detail, thesis, valuation, earnings evidence, risk confirmation, sizing, journal, reports, benchmark/risk review.
- Completed: actionable output surfaces state, reasons, blockers, evidence, source metadata, confidence, disproof criteria, risk impact, and audit trail in API responses and the main UI surfaces.
- Completed: setup docs, API examples, PM docs, final system report, and known limitations are current.
- Completed: full local test stack passes, with unavailable live/provider/browser checks documented honestly.

## Audit Summary

Eight specialist audits were completed on 2026-06-22.

Critical findings: none.

High findings accepted for v0.1.1:

- Frontend verification is broken under installed Next/TypeScript tooling.
- `ADD_ALLOWED` can be returned for owned positions even when an add was not requested.
- Buy/add allowance is not structurally tied to evidence objects.
- Decision allowance and position sizing can disagree when cash/risk budget leaves no room.
- `/health` exposes local filesystem paths.
- Required PM tracking and API example docs are missing.
- Seed universe validation is missing.
- API request schemas are too permissive for core local workflows.

High findings deferred to later milestones:

- Full provider factory and live/demo data routing.
- Real FRED/EIA clients.
- SEC submissions/filing metadata ingestion.
- Full response-model coverage for every API route.
  - Live benchmark return history beyond demo snapshots.
  - Full historical backtesting beyond fixture/no-lookahead skeleton.

## Accepted Work Plan

1. v0.1.1 hardening:
   - Completed: fixed frontend lint/typecheck/build blockers.
   - Completed: pinned frontend dependency versions and added a targeted PostCSS security override.
   - Completed: removed local path disclosure from API health output.
   - Completed: added `.gitignore` coverage for TypeScript build info.
   - Completed: added seed/demo universe validation.
   - Completed: added API examples.
   - Completed: updated PM docs and setup docs.
   - Completed: added missing hard-gate tests.

2. v0.2 through v0.5 foundation:
   - Completed: provider metadata and price-provider contracts.
   - Completed: file-backed API tests.
   - Completed: benchmark snapshot ingestion placeholders.
   - Completed: earnings evidence engine and prompt alignment.
   - Completed: valuation and fixture backtest foundation.
   - Completed: local reports, alerts, and journal analytics.

3. v1.0 completion pass:
   - Verify and document the full end-to-end local flow.
   - Close any docs/API/UI gaps that prevent the project from meeting local personal research OS criteria.
   - Keep live network providers optional and demo mode runnable without keys.

## Rejected Or Deferred Items

- Auto-trading, margin, options, broker execution, and day-trading workflows remain out of scope.
- Live paid data integration is deferred; demo mode must remain useful without keys.
- Full authentication is deferred while the app is localhost-only, but scripts should bind to `127.0.0.1`.
- Python dependency lock workflow is deferred, but documented as needed.

## Test Plan

Minimum checks for this milestone:

```bash
python3 scripts/run_tests.py
python3 -m compileall packages apps/api scripts tests
cd apps/web && npm run lint
cd apps/web && npm run typecheck
cd apps/web && npm run build
```

API smoke checks when server binding is available:

```bash
./scripts/dev_api.sh
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/universe
curl http://127.0.0.1:8000/portfolio
curl http://127.0.0.1:8000/earnings
curl http://127.0.0.1:8000/reports/weekly
curl http://127.0.0.1:8000/alerts
curl http://127.0.0.1:8000/journal/analytics
curl http://127.0.0.1:8000/reports/daily
curl http://127.0.0.1:8000/reports/monthly
curl http://127.0.0.1:8000/reports/quarterly
curl http://127.0.0.1:8000/reports/annual
```

## Verification Results

Latest verification on 2026-06-22:

- `python3 scripts/run_tests.py`: passed, 48 tests.
- `python3 -m compileall packages apps/api scripts tests`: passed.
- `python3 scripts/seed_local_data.py`: passed seed validation; DuckDB reported unavailable in the global Python environment where `duckdb` was not installed, which is an optional safe failure.
- `cd apps/web && npm run lint`: passed.
- `cd apps/web && npm run typecheck`: passed.
- `cd apps/web && npm run build`: passed.
- `cd apps/web && npm audit --omit=dev`: passed after approved registry access.
- API smoke checks against `127.0.0.1:8000`: passed for `/health`, `/universe`, `/portfolio`, `/earnings`, `/reports/weekly`, `/alerts`, `/journal/analytics`, `/reports/daily`, `/reports/monthly`, `/reports/quarterly`, `/reports/annual`, and `/valuation/NVDA`.
- Built Next server route smoke against `127.0.0.1:3000`: passed for `/`, `/universe`, `/universe/NVDA`, `/earnings`, `/portfolio`, `/journal`, `/reports`, and `/settings`.
- Ignore checks confirmed `.env`, `.venv`, `node_modules`, `.next`, local SQLite/DuckDB files, caches, and TypeScript build info are ignored.

Open verification caveats:

- The frontend was build-verified but not visually inspected in a browser during this pass because the in-app browser runtime failed to initialize before navigation.
- Live provider behavior has not been verified and remains deferred.
- No GitHub CI workflow exists yet.

## Known Blockers

- The repository has no baseline commit yet, so all source files appear untracked.
- Local generated artifacts exist but should remain ignored: `.env`, `.venv`, `node_modules`, `.next`, SQLite/DuckDB files, caches, `__pycache__`, and TypeScript build info.
- Live provider behavior has not been verified.
- `npm install` reports an engine warning for a dev dependency requiring newer Node ranges than the current `v20.15.0`, but lint/typecheck/build still pass locally.
