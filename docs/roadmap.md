# Roadmap

This roadmap tracks the v1.0 to v2.1 upgrade path. `AGENTS.md` is the fixed repo contract; this file is the evolving milestone plan.

## v1.0 — Local/Demo Research OS

Status: completed on 2026-06-22.

- Completed: pure Q-GEAR decision brain, FastAPI backend, Next.js frontend, SQLite state, optional DuckDB analytics, demo universe, provider metadata, earnings/evidence, valuation, reports, alerts, and local journal workflows.
- Completed: end-to-end local flow for settings, universe, stock detail, thesis, valuation, earnings evidence, risk-aware sizing, journal, and reports.
- Caveat: live providers and browser visual smoke remain limited by environment/provider availability.

## v1.0.1 — Repo Quality And CI

Status: locally completed on 2026-06-23.

Goal: make the repository verifiable and coherent before major product changes.

Exit criteria:

- Completed: GitHub Actions workflow exists.
- Completed: CI command matrix is documented.
- Completed: README exposes CI status.
- Completed: local CI-equivalent checks pass.
- Completed: no secrets, local DBs, caches, virtualenvs, `node_modules`, or build outputs are tracked.
- Completed: no Q-GEAR investment guardrail is weakened.
- Caveat: GitHub-hosted Actions run was not observed in this session.

Accepted scope:

- Reconcile stale docs that still say CI is missing.
- Add `docs/ci.md`.
- Keep GitHub-hosted Actions run verification honest until pushed/observed.

Deferred:

- Full browser visual regression.
- Process-level API curl smoke in GitHub Actions.
- Built Next route smoke in GitHub Actions.
- Python dependency lock/audit.
- Secret-scanning workflow.

## v1.1 — UX Audit And Information Architecture

Status: completed on 2026-06-23.

Goal: make the product understandable before rewriting visuals.

Deliverables:

- Completed: `docs/ux_audit.md`.
- Completed: `docs/information_architecture.md`.
- Completed: `docs/user_journey_v2.md`.
- Completed: screen-by-screen simplification plan.
- Completed: v2 IA around Today, Pipeline, Universe, Workbench, Earnings, Portfolio, Journal, Reports, and Settings.

Exit criteria:

- UX audit is complete.
- IA map is complete.
- First-5-minutes user journey is defined.
- Next UI milestone has clear acceptance criteria.

## v1.2 — Visual Redesign Foundation

Status: completed on 2026-06-23.

Goal: make the app clean, modern, calm, and professional.

Deliverables:

- Reusable shell, navigation, metric, decision, evidence, blocker, review queue, provider status, empty-state, and section components.
- Broader design tokens for spacing, radius, shadows, typography, semantic state colors, and responsive layouts.
- Consistent redesign of dashboard/Today, universe, stock detail, earnings, portfolio, journal, reports, and settings.

Exit criteria:

- Frontend lint/typecheck/build pass.
- Major pages share a consistent layout.
- Decision state, blockers, evidence, and next action/review task are visually obvious.
- No trading-signal vibe.

## v1.3 — Today Page And Research Pipeline

Status: completed on 2026-06-23.

Goal: make the app tell the user what matters now without becoming a signal bot.

Deliverables:

- Completed: API-backed Today page with daily stance, review queue, alert summary, top blockers, provider mode, and research-priority rankings demoted below review prompts.
- Completed: `/pipeline` board grouped by Q-GEAR decision state with reasons, blockers, review flags, next task, and evidence/source metadata.
- Completed: `/today` and `/pipeline` API routes so workflow logic is not UI-only.
- Completed: pipeline/alert payloads keep `trade_instruction: false`.

Exit criteria:

- Completed: user can open Today and know what to review.
- Completed: Pipeline is clearer than a dense table.
- Completed: alerts and pipeline cards remain review prompts only.

## v1.4 — AI Provider Foundation

Status: completed on 2026-06-23.

Goal: make AI real, optional, explicit, and safe.

Deliverables:

- Completed: expanded `qgear-ai` package with provider interface, `NoopAIProvider`, optional `OpenAIProvider`, schemas, prompts, validation, and service layer.
- Completed: `QGEAR_AI_PROVIDER=none | openai`, default `none`; API key alone does not enable AI.
- Completed: `/ai/status` and explicit draft-only AI routes for evidence extraction, earnings summarization, thesis update, and decision explanation.
- Completed: OpenAI mode requires per-request `external_ai_acknowledged: true` before sending supplied text externally.
- Completed: tests for disabled mode, schema validation, malformed output rejection, price-only evidence rejection, LOW-confidence action evidence rejection, and no automatic action-state mutation.
- Completed: Settings UI shows AI disabled/draft-only/no external upload status.

Exit criteria:

- Completed: app works without an AI key.
- Completed: AI status is visible.
- Completed: AI calls are explicit user actions.
- Completed: AI draft outputs require user verification.

## v1.5 — AI Evidence Workbench

Status: completed on 2026-06-23.

Goal: let the user paste source text and convert it into verified evidence.

Deliverables:

- Completed: Evidence Workbench UI at `/evidence`.
- Completed: source title/type/date/URL-or-description/pasted text fields.
- Completed: AI extraction button when AI is enabled.
- Completed: manual verified evidence fallback when AI is disabled.
- Completed: separate user verification/edit fields before saving evidence.
- Completed: saved evidence appears in Stock Workbench evidence timeline.

Exit criteria:

- Completed: user can paste an earnings/filing excerpt and save verified evidence.
- Completed: AI evidence cannot affect decisions until verified.
- Completed: LOW-confidence or malformed evidence cannot support action-changing decisions.

## v1.6 — AI Earnings Review

Status: completed on 2026-06-23.

Goal: make earnings review the product’s highest-value workflow.

Deliverables:

- Completed: guided pre-earnings and post-earnings workflow.
- Completed: AI earnings summarizer UI when enabled and explicitly acknowledged.
- Completed: deterministic thesis strengthened/unchanged/weakened/broken classification remained in the tested core flow.
- Completed: manual earnings review creates a journal draft that requires user confirmation.
- Completed: decision blockers make clear that weakened/broken thesis status blocks buy/add and strengthened evidence still needs valuation, technical, freshness, and risk gates.

Exit criteria:

- Completed: manual workflow works with AI disabled.
- Completed: AI workflow is draft-only when enabled.
- Completed: weakening evidence blocks buy/add.
- Completed: strengthened evidence still requires valuation, technical, freshness, and risk gates.

## v1.7 — Stock Workbench Redesign

Status: completed on 2026-06-23.

Goal: make the stock detail page the best screen in the app.

Deliverables:

- Completed: first-screen decision card and summary strip answer state, why, blockers, evidence quality, next review, action permission, and max new money.
- Completed: Evidence timeline, thesis card, earnings card, valuation card, technical/risk card, portfolio impact card, journal trail, and AI assistant panel.
- Completed: AI assistant actions for decision explanation, thesis update, evidence extraction, and journal draft are explicit and draft-only.
- Completed: prompt hardening now treats pasted source material as untrusted data and requires insufficient-evidence language when support is missing.

Exit criteria:

- Completed: user can understand action/blockers quickly.
- Completed: evidence and disproof criteria are visible.
- Completed: build/test checks pass.

## v1.8 — Valuation Underwriting Upgrade

Status: completed on 2026-06-23.

Goal: make expected IRR transparent and professional.

Deliverables:

- Completed: editable/API-backed bear/base/bull assumptions.
- Completed: revenue CAGR, margins, terminal multiple, dilution/buyback, net cash/debt, and probability weights.
- Completed: stateless `/valuation/{ticker}/calculate` route for local draft underwriting.
- Completed: sensitivity table and evidence-linked valuation notes.
- Completed: decision gate can use probability-weighted IRR when supplied.

Exit criteria:

- Completed: expected IRR is transparent.
- Completed: poor expected IRR blocks action.
- Completed: valuation cannot create buy/add alone.

## v1.9 — Portfolio And Journal Intelligence

Status: completed and locally verified on 2026-06-23.

Goal: improve behavior and portfolio discipline.

Deliverables:

- Completed: portfolio risk dashboard with cash, drawdown, total-equity position weights, AI-layer exposure, benchmark placeholders, expected IRR distribution, concentration risks, blocked adds, and review calendar.
- Completed: journal with outcome, mistake category, evidence quality, followed-system flag, later review, and process score.
- Completed: monthly/quarterly report UX shows richer review prompts and queues.
- Completed: portfolio AI review visibility is disabled/draft-only and sends nothing automatically.

Exit criteria:

- Completed: portfolio risk is more obvious.
- Completed: journal helps improve user behavior.
- Completed: AI review is draft-only.
- Completed: no brokerage execution exists.
- Completed: Python tests, compile, seed validation, frontend lint/typecheck/build, dependency audit, API smoke, and built-route smoke passed.
- Caveat: browser visual smoke remains blocked by the in-app Browser runtime before navigation.

## v2.0 — Polished AI-Assisted Local Research OS

Status: completed and locally verified on 2026-06-23; pending GitHub-hosted CI observation after push.

Goal: complete a polished local personal AI research OS.

Exit criteria:

- Clean impressive UI.
- Clear user flow.
- AI research assistance works when configured.
- Manual workflow works when AI disabled.
- Evidence workbench works.
- Earnings workflow works.
- Valuation workflow works.
- Portfolio/journal workflow works.
- Reports are readable.
- CI and local tests pass.
- No auto-trading, margin, options-by-default, or buy-the-dip behavior.
- Demo mode works without keys.
- External providers are optional and explicit.
- Docs are current and limitations are honest.

Verification summary:

- `python3 scripts/run_tests.py`: passed, 63 tests.
- `python3 -m compileall packages apps/api scripts tests`: passed.
- `python3 scripts/seed_local_data.py`: passed; DuckDB remained optional/unavailable in the global Python context.
- `npm run lint`, `npm run typecheck`, `npm run build`: passed in `apps/web`.
- `npm audit --omit=dev`: passed with 0 vulnerabilities after approved registry access.
- API smoke passed for health, Today, Pipeline, AI status, Universe, Portfolio, Earnings, Weekly report, Alerts, Journal analytics, Valuation, valuation calculate POST, and backtest fixture routes.
- Built route smoke passed for `/`, `/pipeline`, `/evidence`, `/universe`, `/universe/NVDA`, `/earnings`, `/portfolio`, `/journal`, `/reports`, and `/settings`.
- Browser visual smoke was attempted but blocked by the in-app Browser runtime initialization issue before navigation.

## v2.1 — Professional Live Research Foundation

Status: locally completed and ready for GitHub publish on 2026-06-24; GitHub-hosted CI observation remains pending after push.

Goal: move from a polished local/demo research OS toward a professional live-data-capable research foundation without weakening Q-GEAR guardrails.

Milestones:

- A. Baseline and CI reality check.
- B. Core source/evidence/data-quality gates.
- C. SEC financial foundation with ticker-CIK mapping and canonical companyfacts parsing.
- D. Price, benchmark, and technical engine from price history.
- E. FRED/EIA macro and energy context as review-only data.
- F. Professional UI/UX live/demo clarity with Data Health.
- G. Release pass with full tests, smoke checks, docs, and known limitations.

Progress:

- Completed: baseline Python tests, compile, seed validation, frontend lint/typecheck/build, and dependency audit.
- Completed: read-only audits for Core Brain, Live Data, Backend/API, Frontend/UI/UX, AI Safety, QA/CI, Security/Privacy, and Documentation/PM.
- Completed: pure-core v2.1 evidence/source models and source-quality gates.
- Completed: regression tests for AI_DRAFT, AI_USER_VERIFIED, demo evidence in live mode, SEC/provider-verified evidence, missing source type, price-only evidence, source-quality threshold, provider errors, and mixed-mode caution.
- Completed: SEC-style ticker-CIK demo mapping, companyfacts financial snapshot parser, NVDA fixture/mock companyfacts, `/financials/{ticker}`, `/financials/{ticker}/metrics`, `/data/quality/{ticker}`, `/data/health`, and explicit SEC refresh route.
- Completed: provider/API tests for SEC fixture parsing and data-quality route review-only behavior.
- Completed: deterministic mock price history, technical snapshot calculations, Alpha Vantage missing-key stub, `/prices/{ticker}`, `/technical/{ticker}`, price/benchmark refresh routes, FRED/EIA metadata-safe routes, Data Health UI, Today data-health summary, and Stock Workbench data-quality card.
- Completed: provider/API/frontend verification for price/technical/macro/energy/Data Health implementation.
- Completed: source type, verification status, source URL, provider, filing/accession, and period metadata now persist through SQLite/API evidence saves and appear in stock-detail evidence tables.
- Completed: final v2.1 release pass with Python tests, compile checks, seed validation, frontend lint/typecheck/build, dependency audit, API smoke, and built-route smoke.

Verification summary:

- `python3 scripts/run_tests.py`: passed, 76 tests.
- `python3 -m compileall packages apps/api scripts tests`: passed.
- `python3 scripts/seed_local_data.py`: passed; DuckDB remained optional/unavailable in the global Python context.
- `npm run lint`, `npm run typecheck`, `npm run build`: passed in `apps/web`.
- `npm audit --omit=dev`: passed with 0 vulnerabilities after approved registry access.
- API smoke passed for health, data health, financials, technicals, macro, universe, portfolio, earnings, weekly reports, energy, and prices.
- Built route smoke passed for `/`, `/data-health`, `/universe/NVDA`, `/pipeline`, `/settings`, `/universe`, `/evidence`, `/earnings`, `/portfolio`, `/journal`, and `/reports`.
- Browser visual smoke was attempted but blocked by the in-app Browser runtime initialization issue before navigation.

Remaining caveats:

- GitHub-hosted CI needs to be observed after push.
- Live SEC/FRED/EIA/Alpha Vantage network behavior remains optional and unverified.
- Local write APIs remain intended for loopback personal use, not public deployment.

## v2.1 UI Polish Layer — Research Workstation Experience

Status: locally completed on 2026-06-24; pending GitHub-hosted CI observation after push.

Goal: make the verified v2.1 app feel like a clearer, calmer, more professional local research workstation without changing the decision engine or weakening Q-GEAR guardrails.

Completed:

- App shell and navigation polish with skip-link support, active page semantics, stronger focus states, and visible safety boundaries.
- Today page command panel focused on daily stance, review queue, data mode, drawdown mode, and manual review states.
- Data Health page with provider tiles, repair queue, missing-key context, and review-only boundaries.
- Card-first Universe, Portfolio, Journal, and Reports surfaces to reduce table density.
- Stock Workbench first-screen blocker and data-quality context.
- Evidence Workbench step flow with explicit source intake, optional AI draft, and user verification before saving.
- Route-level loading, error, and not-found states.

Verification summary:

- Python tests, compile checks, seed validation, frontend lint/typecheck/build, dependency audit, API smoke, and built-route smoke passed locally.
- Browser visual smoke remains blocked by the in-app Browser runtime initialization issue before navigation.

Deferred:

- Actual browser screenshot/visual regression once the in-app Browser runtime is available.
- Further visual refinement from real-device screenshots.
