# Project Status

Last updated: 2026-06-23

## Current Milestone

Active milestone: v2.0 Polished Release Pass, locally verified and pushed to GitHub.

v1.0 local/demo completion was achieved on 2026-06-22 and pushed as commit `26d55a4`. The v2.0 local release pass was verified locally on 2026-06-23 and pushed to `main` as commit `f167a3d`. GitHub-hosted CI still needs to be observed because the local `gh` CLI is unavailable and the GitHub connector did not return push-triggered workflow runs.

Important working-tree note: `AGENTS.md` was modified before this run and was not edited during the v2.0 release pass. It is included in the release as the current repo contract.

## Audit Summary

Nine read-only specialist audits were completed on 2026-06-23:

- Product/UX: v1 UI is functional but table-heavy; Today, Pipeline, Workbench, and first-5-minutes IA are not yet implemented.
- AI Integration: `qgear-ai` is mostly a placeholder; no AI provider mode, draft routes, validation service, or frontend AI hooks exist yet.
- Core Decision Engine: the gate-first brain is strong, but future AI evidence needs provenance/verification metadata and price-only evidence needs semantic rejection.
- Backend/API: v1 routes are healthy, but v2 needs explicit Today, Pipeline, AI, Evidence Workbench, and persistent valuation contracts.
- Frontend/UI: fallback demo detail can make allowed states look actionable without an approved thesis; v2 UI needs reusable decision/evidence/review components.
- Data Provider: demo mode is safe; live SEC throttling/User-Agent behavior and per-provider live/mock disclosure should be tightened later.
- QA/Test: CI exists but docs are stale; future work should add process-level API smoke, built-web smoke, visual checks, and AI safety tests.
- Security/Privacy: no tracked secrets, no auto-trading/broker layer, and no absolute local paths were found; local API write endpoints remain unauthenticated and should stay loopback-only.
- Documentation/PM: roadmap/status/docs lag behind the v2 product spec and CI reality.

## Accepted Work Plan

v1.0.1 accepted scope:

- Document the existing GitHub Actions workflow.
- Add README CI status badge.
- Add `docs/ci.md`.
- Update roadmap/status/log docs to reflect the v2 upgrade path.
- Confirm tracked-file hygiene for secrets, local DBs, caches, virtualenvs, `node_modules`, and build outputs.
- Run local CI-equivalent checks.

v1.1 accepted scope after v1.0.1 passes:

- Create UX audit, information architecture, and v2 user journey docs.
- Define Today/Pipeline/Workbench acceptance criteria.
- Do not begin a large UI rewrite until the IA is clear.

## Deferred Items

- GitHub-hosted Actions run verification until a push or remote run is observed.
- Full process-level API smoke in CI.
- Built Next route smoke in CI.
- Browser visual regression and screenshots.
- Python dependency lock/audit and secret-scanning workflow.
- Live SEC/FRED/EIA/provider verification.
- AI provider implementation until v1.4.
- Core evidence provenance hardening until the decision-brain hardening batch before AI evidence affects decisions.

## v1.0.1 Exit Criteria

- Completed: GitHub Actions workflow file exists.
- Completed: local CI-equivalent checks pass.
- Completed: CI commands are documented in `docs/ci.md`.
- Completed: README exposes CI status.
- Completed: no secrets or local generated artifacts are tracked.
- Completed: no Q-GEAR safety rule is weakened.
- Caveat: GitHub-hosted Actions run was not observed in this session.

## v1.1 Exit Criteria

- Completed: created `docs/ux_audit.md`.
- Completed: created `docs/information_architecture.md`.
- Completed: created `docs/user_journey_v2.md`.
- Completed: audited current pages: `/`, `/universe`, `/universe/[ticker]`, `/earnings`, `/portfolio`, `/journal`, `/reports`, and `/settings`.
- Completed: defined v2 IA: Today, Pipeline, Universe, Workbench, Earnings, Portfolio, Journal, Reports, Settings.
- Completed: defined the first-5-minutes user journey.
- Completed: avoided large UI rewrite in this milestone.

## v1.2 Exit Criteria

- Completed: improved global app shell and navigation.
- Completed: added reusable UI components for page headers, metrics, decisions, blockers, evidence, provider status, empty states, and section cards.
- Completed: added design tokens for color, spacing, radius, shadows, typography, and semantic state colors.
- Completed: redesigned core pages without moving domain logic into the frontend.
- Completed: frontend lint/typecheck/build pass.
- Completed: decision state, blockers, evidence, and next review/action context are more visually obvious.
- Completed: no trading-signal vibe was introduced.
- Completed: frontend fallback stock detail now blocks action permission when thesis/invalidation context is unavailable.

## v1.3 Exit Criteria

- Completed: redesigned home page into API-backed Today.
- Completed: added `/pipeline` research board grouped by Q-GEAR decision state.
- Completed: added review queue categories for thesis/invalidation gaps, earnings review, stale evidence, technical breaks/weakening, valuation hurdle failures, concentration risk, drawdown risk, and journal review.
- Completed: default stance remains “No action justified today unless evidence changed and every hard gate clears.”
- Completed: pipeline and alerts remain review prompts, not trade instructions.
- Completed: added `/today` and `/pipeline` API support so the workflow is not UI-only.
- Completed: frontend fallback pipeline/Today data is conservative and blocks action permission.
- Completed: tests and frontend build pass.

## v1.4 Exit Criteria

- Completed: added optional AI provider configuration with default `QGEAR_AI_PROVIDER=none`.
- Completed: expanded `packages/qgear-ai` with provider interfaces, schemas, prompts, validation, and service layer.
- Completed: added draft-only AI API routes for status, evidence extraction, earnings summarization, thesis update, and decision explanation.
- Completed: OpenAI mode requires explicit per-request external AI acknowledgement before any provider call.
- Completed: AI calls require explicit POST requests and do not mutate decision state automatically.
- Completed: added tests for disabled mode, schema validation, malformed output rejection, external acknowledgement, LOW-confidence/action evidence rejection, price-only evidence rejection, and AI outputs not changing actions until verified.
- Completed: surfaced AI disabled/status state in the Settings UI.
- Completed: preserved local/demo operation without API keys.

## v1.5 Exit Criteria

- Completed: added Evidence Workbench UI for source title/type/date/URL-or-description/pasted text.
- Completed: manual evidence object creation works when AI is disabled.
- Completed: explicit AI evidence extraction path is present when AI is enabled and acknowledged.
- Completed: evidence must be verified/edited in separate fields before saving.
- Completed: saved evidence uses the existing evidence schema and source metadata.
- Completed: LOW-confidence or malformed evidence cannot support action-changing decisions through core/AI validation.
- Completed: verified evidence appears in the Stock Workbench evidence timeline.
- Completed: tests and frontend build pass.

## v1.6 Exit Criteria

- Completed: improved Earnings page into guided before/after/evidence/thesis/blockers/journal workflow.
- Completed: added AI earnings summarizer UI call when AI is enabled and acknowledged.
- Completed: manual earnings review remains usable when AI is disabled.
- Completed: AI output remains draft-only and requires user verification before any saving or decision use.
- Completed: deterministic thesis strengthened/unchanged/weakened/broken classification remains tested.
- Completed: manual earnings review generates a draft journal note without auto-saving.
- Completed: weakening evidence blocks buy/add; strengthening still requires valuation, technical, freshness, and risk gates.
- Completed: tests and frontend build pass.

## v1.7 Exit Criteria

- Completed: first screen answers decision state, why, blockers, evidence quality, next review, and max new money.
- Completed: Stock Workbench visibly includes decision, reasons/blockers, next research task, evidence timeline, thesis, earnings, valuation, technical/risk, portfolio impact, journal trail, and AI assistant sections.
- Completed: AI assistant actions are explicit buttons and draft-only.
- Completed: evidence and disproof criteria remain visible.
- Completed: AI external acknowledgement copy lists the fields that would be sent.
- Completed: prompt templates now treat pasted source material as untrusted data and require insufficient-evidence language when source support is missing.
- Completed: tests and frontend build pass.

## v1.8 Exit Criteria

- Completed: added editable/API-backed bear/base/bull valuation assumptions for revenue CAGR, gross margin, operating margin, FCF margin, terminal multiple, dilution/buyback, net cash/debt, and probability weight.
- Completed: added stricter probability/case validation and probability-weighted expected IRR visibility.
- Completed: added a sensitivity table and transparent valuation-underwriting view.
- Completed: linked valuation notes back to evidence references where practical.
- Completed: decision engine can use probability-weighted IRR when supplied, and valuation still cannot create buy/add alone.
- Completed: tests and frontend build pass.

## v1.9 Exit Criteria

- Completed: upgraded portfolio dashboard with drawdown mode, total-equity position weights, AI-layer exposure, benchmark placeholders, expected IRR distribution, concentration risks, blocked adds, and review calendar.
- Completed: upgraded journal with decision outcome, mistake category, evidence quality, followed-system flag, later review, and process score.
- Completed: added monthly/quarterly review UX improvements.
- Completed: kept manual-only portfolio; no broker execution exists.
- Completed: AI review surfaces remain disabled/draft-only and do not mutate decisions.
- Completed: Python tests, compile, seed validation, frontend lint/typecheck/build, `npm audit --omit=dev`, API smoke, and built-route smoke pass.
- Caveat: Browser visual smoke remains blocked by the in-app Browser runtime initialization issue before navigation.

## v2.0 Exit Criteria

- Completed: full UI/docs release pass.
- Completed: README, API examples, project status, roadmap, and known limitations are current.
- Completed: full local Python/core/API test pass and frontend lint/typecheck/build pass.
- Completed: API smoke and built-route smoke pass with local server binding escalation.
- Completed: `npm audit --omit=dev` passes with registry access and reports 0 vulnerabilities.
- Completed: no auto-trading, margin, options-by-default, broker execution, buy-the-dip, or ungrounded AI decision mutation exists.
- Completed: demo mode works without keys; external providers and AI remain optional and explicit.
- Caveat: Browser visual smoke could not be completed because the in-app Browser runtime failed before navigation with `sandboxCwd must be an absolute file URI`.

## Test Plan

Required local checks:

```bash
python3 scripts/run_tests.py
python3 -m compileall packages apps/api scripts tests
python3 scripts/seed_local_data.py
```

Frontend checks:

```bash
cd apps/web
npm run lint
npm run typecheck
npm run build
npm audit --omit=dev
```

Tracked hygiene check:

```bash
git ls-files
```

Confirm no tracked `.env`, local DB, DuckDB, cache, virtualenv, `node_modules`, `.next`, `__pycache__`, pytest cache, private key, or secret files exist.

## Latest Verification Results

Latest verification on 2026-06-23 for v2.0:

- `python3 scripts/run_tests.py`: passed, 63 tests.
- `python3 -m compileall packages apps/api scripts tests`: passed.
- `python3 scripts/seed_local_data.py`: passed; DuckDB reported optional unavailable in the global Python context.
- `cd apps/web && npm run lint`: passed.
- `cd apps/web && npm run typecheck`: passed.
- `cd apps/web && npm run build`: passed, including Today, Pipeline, Evidence, Universe, Stock Workbench, Earnings, Portfolio, Journal, Reports, and Settings routes.
- `cd apps/web && npm audit --omit=dev`: sandbox DNS failed first, then passed after approved registry access with 0 vulnerabilities.
- API smoke required escalation because sandboxed port binding was blocked; escalated FastAPI server on `127.0.0.1:8001` returned HTTP 200 for `/health`, `/today`, `/pipeline`, `/ai/status`, `/universe`, `/portfolio`, `/earnings`, `/reports/weekly`, `/alerts`, `/journal/analytics`, `/valuation/NVDA`, `POST /valuation/NVDA/calculate`, and `/valuation/backtest/demo`.
- Built Next route smoke required escalation because sandboxed port binding was blocked; escalated web server on `127.0.0.1:3001` returned HTTP 200 for `/`, `/pipeline`, `/evidence`, `/universe`, `/universe/NVDA`, `/earnings`, `/portfolio`, `/journal`, `/reports`, and `/settings`.
- Browser visual smoke remained blocked by the in-app Browser runtime `sandboxCwd` initialization issue before navigation.
- `git ls-files -i -c --exclude-standard`: no ignored tracked files.

Previous verification on 2026-06-23 for v1.8:

- `python3 scripts/run_tests.py`: passed, 62 tests.
- `python3 -m compileall packages apps/api scripts tests`: passed.
- `python3 scripts/seed_local_data.py`: passed; DuckDB reported optional unavailable in the global Python context.
- `cd apps/web && npm run lint`: passed.
- `cd apps/web && npm run typecheck`: passed.
- `cd apps/web && npm run build`: passed, including the valuation-enabled `/universe/[ticker]`.
- `cd apps/web && npm audit --omit=dev`: sandbox DNS failed first, then passed after approved npm registry access with 0 vulnerabilities.
- Fresh local API smoke required escalation because sandboxed port binding was blocked; escalated FastAPI server on `127.0.0.1:8001` returned HTTP 200 for `/valuation/NVDA`, `/valuation/PLTR`, and `POST /valuation/NVDA/calculate`.
- Built Next route smoke required escalation because sandboxed port binding was blocked; escalated web server on `127.0.0.1:3001` returned HTTP 200 for `/universe/NVDA`.
- HTML/API phrase checks confirmed Valuation Underwriting, Probability-weighted IRR, Recalculate draft valuation, Sensitivity Table, AI valuation explainer disabled, `sensitivity_table`, `probability_weighted_irr_5y_pct`, and `valuation_clears_hurdle`.
- Browser visual smoke remained blocked by the in-app browser runtime `sandboxCwd` initialization issue before navigation.

Previous verification on 2026-06-23 for v1.7:

- `cd apps/web && npm run lint`: passed.
- `cd apps/web && npm run typecheck`: passed.
- `python3 scripts/run_tests.py`: passed, 57 tests.
- `python3 -m compileall packages apps/api scripts tests`: passed.
- `python3 scripts/seed_local_data.py`: passed; DuckDB reported optional unavailable in the global Python context.
- `cd apps/web && npm run build`: passed, including `/universe/[ticker]`.
- `cd apps/web && npm audit --omit=dev`: sandbox DNS failed first, then passed after approved npm registry access with 0 vulnerabilities.
- Fresh local API smoke required escalation because sandboxed port binding was blocked; escalated FastAPI server on `127.0.0.1:8001` returned HTTP 200 for `/universe/NVDA` and `/ai/status`.
- Built Next route smoke required escalation because sandboxed port binding was blocked; escalated web server on `127.0.0.1:3001` returned HTTP 200 for `/universe/NVDA`.
- HTML phrase checks confirmed Evidence quality, AI Assistant Panel, Thesis Card, Portfolio Impact, Journal Trail, Technical / Risk State, Create journal draft, and AI disabled-by-default copy rendered.
- Browser visual smoke remained blocked by the in-app browser runtime `sandboxCwd` initialization issue before navigation.

Previous verification on 2026-06-23 for v1.6:

- `python3 scripts/run_tests.py`: passed, 57 tests.
- `python3 -m compileall packages apps/api scripts tests`: passed.
- `python3 scripts/seed_local_data.py`: passed; DuckDB reported optional unavailable in the global Python context.
- `cd apps/web && npm run lint`: passed.
- `cd apps/web && npm run typecheck`: passed.
- `cd apps/web && npm run build`: passed, including the redesigned `/earnings` page.
- `cd apps/web && npm audit --omit=dev`: sandbox DNS failed first, then passed after approved npm registry access with 0 vulnerabilities.
- Added API regression coverage for disabled-mode `/ai/earnings/summarize`; Python tests confirm it returns draft-disabled output without mutating decisions.
- Built Next route smoke against `127.0.0.1:3001/earnings`: passed with HTTP 200.
- HTML phrase checks confirmed Earnings Review Lab, Before Earnings, AI Earnings Draft, Manual Post-Earnings Review, Decision Blockers, and Journal Discipline rendered.
- Browser visual smoke remained blocked by the in-app browser runtime `sandboxCwd` initialization issue before navigation.

Previous verification on 2026-06-23 for v1.5:

- `python3 scripts/run_tests.py`: passed, 57 tests.
- `python3 -m compileall packages apps/api scripts tests`: passed.
- `python3 scripts/seed_local_data.py`: passed; DuckDB reported optional unavailable in the global Python context.
- `cd apps/web && npm run lint`: passed.
- `cd apps/web && npm run typecheck`: passed.
- `cd apps/web && npm run build`: passed, including `/evidence`.
- `cd apps/web && npm audit --omit=dev`: sandbox DNS failed first, then passed after approved npm registry access with 0 vulnerabilities.
- Fresh API smoke on `127.0.0.1:8001`: saving verified NVDA evidence returned HTTP 200; fetching `/universe/NVDA` returned HTTP 200 and included the saved evidence in `evidence_table`.
- Removed the smoke-test evidence row from local SQLite after verification.
- Built Next route smoke against `127.0.0.1:3001/evidence`: passed with HTTP 200 while pointed at an unavailable API port, verifying conservative frontend fallback.
- HTML phrase checks confirmed Evidence Workbench, Verify Before Saving, Save verified evidence, AI disabled, and LOW-confidence action-blocking copy rendered.
- Browser visual smoke attempted again, but the in-app browser runtime failed before navigation with the known `sandboxCwd` initialization issue.

Previous verification on 2026-06-23 for v1.4:

- `python3 scripts/run_tests.py`: passed, 57 tests.
- `python3 -m compileall packages apps/api scripts tests`: passed.
- `python3 scripts/seed_local_data.py`: passed; DuckDB reported optional unavailable in the global Python context.
- `cd apps/web && npm run lint`: passed.
- `cd apps/web && npm run typecheck`: passed.
- `cd apps/web && npm run build`: passed.
- `cd apps/web && npm audit --omit=dev`: sandbox DNS failed first, then passed after approved npm registry access with 0 vulnerabilities.
- Fresh API smoke on `127.0.0.1:8001`: passed with HTTP 200 for `/health`, `/ai/status`, `/ai/evidence/extract` disabled-mode POST, `/today`, `/pipeline`, `/universe`, `/portfolio`, `/earnings`, `/reports/weekly`, and `/valuation/NVDA`.
- AI disabled-mode POST returned `draft_status: disabled`, `external_call_performed: false`, and `mutates_decision_state: false`.
- Initial fresh API smoke without local package paths failed because the global Python environment did not have editable `qgear-ai` installed; rerun with explicit local `PYTHONPATH` passed. Normal README setup installs editable packages into the virtualenv.
- Built Next route smoke against `127.0.0.1:3001/settings`: passed with HTTP 200.
- HTML phrase checks confirmed Settings rendered AI Research Assistance, disabled-by-default status, no decision mutation, and no automatic external upload copy.

Previous verification on 2026-06-23 for v1.3:

- `python3 scripts/run_tests.py`: passed, 50 tests.
- `python3 -m compileall packages apps/api scripts tests`: passed.
- `python3 scripts/seed_local_data.py`: passed; DuckDB reported optional unavailable in the global Python context.
- `cd apps/web && npm run lint`: passed.
- `cd apps/web && npm run typecheck`: passed.
- `cd apps/web && npm run build`: passed.
- `cd apps/web && npm audit --omit=dev`: sandbox DNS failed first, then passed after approved npm registry access with 0 vulnerabilities.
- API smoke against `127.0.0.1:8000`: passed with HTTP 200 for `/health`, `/today`, `/pipeline`, `/universe`, `/portfolio`, `/earnings`, `/reports/weekly`, `/alerts`, and `/valuation/NVDA`.
- Built Next route smoke against `127.0.0.1:3001`: passed with HTTP 200 for `/`, `/pipeline`, `/universe`, `/universe/NVDA`, `/earnings`, `/portfolio`, `/journal`, `/reports`, and `/settings`.
- HTML phrase checks confirmed the built pages rendered the Today review queue, Pipeline board, and stock evidence/decision content.
- Browser visual smoke attempted again, but the in-app browser runtime failed before navigation with the known `sandboxCwd` initialization issue.

Previous verification on 2026-06-23 for v1.2:

- `python3 scripts/run_tests.py`: passed, 48 tests.
- `python3 -m compileall packages apps/api scripts tests`: passed.
- `python3 scripts/seed_local_data.py`: passed; DuckDB reported optional unavailable in the global Python context.
- `cd apps/web && npm run lint`: passed.
- `cd apps/web && npm run typecheck`: passed.
- `cd apps/web && npm run build`: passed.
- `cd apps/web && npm audit --omit=dev`: passed after approved npm registry access, 0 vulnerabilities.
- Built Next route smoke against `127.0.0.1:3000`: passed with HTTP 200 for `/`, `/universe`, `/universe/NVDA`, `/earnings`, `/portfolio`, `/journal`, `/reports`, and `/settings`.
- Browser visual smoke attempted, but the in-app browser runtime failed before navigation with the known `sandboxCwd` initialization issue.

Previous v1.0.1 hygiene verification:

- `git ls-files -i -c --exclude-standard`: no ignored tracked files.
- Strict OpenAI-style secret scan: no matches.
- Tracked local artifact scan for `.env`, local DBs, DuckDB files, cache contents, virtualenvs, `node_modules`, `.next`, `__pycache__`, pytest cache, private keys: no matches.

Previous v1.0 verification on 2026-06-22:

- `python3 scripts/run_tests.py`: passed, 48 tests.
- `python3 -m compileall packages apps/api scripts tests`: passed.
- `python3 scripts/seed_local_data.py`: passed seed validation; DuckDB was optional and unavailable in the global Python environment.
- Frontend lint/typecheck/build: passed.
- `npm audit --omit=dev`: passed after approved registry access.
- API smoke and built Next route smoke: passed for documented v1 local/demo routes.

## Known Blockers And Caveats

- Browser visual smoke was previously blocked by the in-app browser runtime initialization.
- Live provider behavior has not been verified.
- GitHub-hosted CI run has not been observed in this session.
- DuckDB may be unavailable in global Python contexts and is optional by design.
- The local app has unauthenticated write endpoints and should remain bound to loopback unless future local-auth work is added.
