# Roadmap

## v0.1.1 — Hardening and Verification

- Fix frontend lint, typecheck, and build.
- Pin frontend dependencies from the lockfile.
- Add seed/demo universe validation.
- Add missing hard-gate tests.
- Add API examples and PM tracking docs.
- Remove local path leakage from health output.
- Keep demo mode fully runnable without API keys.

## v0.1.2 — API and Persistence Tightening

- Add file-backed FastAPI smoke tests.
- Add response models for key routes.
- Enforce safer portfolio/journal API guardrails.
- Improve portfolio settings persistence for cash and drawdown assumptions.
- Add structured evidence storage for journal entries.

## v0.2 — Data Foundation

- Add price provider contracts and mock daily OHLC snapshots.
- Add benchmark snapshot support for SPY, QQQ, XLK, and SMH.
- Add SEC submissions and filing metadata provider.
- Add provider response metadata: source date, retrieved at, cached at, as-of date, status, and error fields.
- Keep live providers optional and demo mode default.

Exit criteria:

- Demo mode works without API keys.
- Provider failures degrade gracefully with metadata/error status.
- Provider source metadata is visible through API responses.
- File-backed provider tests pass without live network access.
- No provider data creates buy/add actions by itself.

## v0.3 — Earnings and Evidence Engine

- Add earnings calendar/provider interface.
- Add structured earnings analysis objects.
- Add thesis strengthened/unchanged/weakened/broken workflow from sourced evidence.
- Add prompts and validation for AI extraction JSON.

Exit criteria:

- User can perform pre-earnings and post-earnings reviews.
- Fresh positive evidence is required for add actions.
- Weakening evidence blocks buy/add.
- Evidence objects include claim, evidence, source, source date, confidence, and disproof criteria.
- Earnings-strengthened and earnings-weakened tests pass.

## v0.4 — Valuation and Backtesting

- Add bear/base/bull valuation cases.
- Add expected IRR engine with dilution, net cash/debt, and margin assumptions.
- Add no-look-ahead backtesting with filing/availability dates.
- Add benchmark comparison reports.

Exit criteria:

- Buy/add requires valuation hurdle clearance.
- Great company with poor expected IRR becomes Watch/Hold, not Buy/Add.
- Backtest code is separated from live decision state.
- Backtest docs explain no-lookahead limits.
- Valuation edge-case tests pass.

## v0.5 — Reports and Local Alerts

- Completed: expanded daily brief, weekly ranking, monthly review, quarterly earnings review, and annual strategy audit.
- Completed: added local alert rules for filings, earnings thesis risk, stale evidence, technical breaks, concentration, drawdown, and thesis review dates.
- Completed: added journal analytics for action mix, evidence coverage, and unresolved outcomes.

Exit criteria:

- Completed: reports are generated from local/demo state.
- Completed: daily brief keeps “no action unless evidence changed” as the default stance.
- Completed: alerts never become trade instructions.
- Completed: journal analytics and report routes are tested.

## v1.0 — Complete Local Personal Research OS

- Completed: stable local/demo app with documented setup and smoke tests.
- Completed: configurable provider foundation exists, with live providers still optional and demo mode default.
- Completed: evidence-backed stock memos, thesis approval, invalidation rules, risk-aware sizing, journal workflows, benchmark reporting, and no brokerage execution.
- Completed: final documentation pass for current local/demo functionality, known limitations, and safe future provider work.
- Blocked by environment: browser visual smoke if the in-app browser runtime is available.

Exit criteria:

- Completed: end-to-end flow works: settings, universe, stock detail, thesis, valuation, earnings evidence, risk confirmation, sizing, journal, reports, benchmark/risk review.
- Completed: actionable outputs show state, reasons, blockers, evidence, source metadata, confidence, disproof criteria, risk impact, and audit trail in API/UI surfaces.
- Completed: tests, docs, and known limitations are current.

## Future Work After v1.0

- Add GitHub CI for Python tests, compile checks, frontend lint/typecheck/build, and dependency audit.
- Verify live SEC/FRED/EIA/provider behavior with real credentials and network access.
- Expand backtesting beyond fixtures with historical provider data and strict availability timestamps.
- Add visual regression/browser smoke when the in-app browser runtime is available.
