# AGENTS.md — Q-GEAR AI Growth OS

## 0. How to use this file

This file is the repository-level operating contract for Codex. Read it before changing code. Keep it concise enough for Codex project-instruction limits. If more detail is needed, place it in `docs/` and reference it here.

This repo should be managed as a serious local software product and a serious investment-research workflow. Do not treat it as a toy stock picker, signal bot, or auto-trader.

## 1. Project identity

Project name: `qgear-ai-growth-os`

Full name: Q-GEAR AI Growth OS

Q-GEAR means: **Quality Growth, Earnings Acceleration, AI Infrastructure Relevance, and Risk Control**.

This repository implements a local, personal-use US equity research operating system for a Singapore/Malaysia-based individual investor starting with approximately USD 10,000. The system focuses on US-listed AI-era growth stocks, especially technology and AI infrastructure companies across compute, semiconductors, memory, storage, cloud, networking, data-centre power/cooling, and software monetisation.

This is not a public advisory product, not a paid investment service, not an auto-trader, and not a day-trading system. It is a private local research, scoring, portfolio, and decision-journal application.

Required disclaimer in user-facing docs/UI:

> This tool is for personal research and educational use only. It does not provide licensed financial advice, tax advice, or legal advice. Final investment decisions are made by the user.

## 2. Non-negotiable investment and product rules

1. No auto-trading.
2. No margin trading.
3. No options trading in the MVP.
4. No generic buy-the-dip system.
5. No “buy because price dropped.”
6. No averaging down without fresh positive fundamental evidence.
7. No buy/add without an approved thesis and invalidation rule.
8. Price movement alone is never investment evidence.
9. Technical analysis is only timing and risk confirmation, not thesis creation.
10. Every AI-generated investment claim must include evidence, source, confidence, and what would disprove it.
11. The app must be comfortable saying: “No action justified today.”
12. The system must benchmark itself against SPY, QQQ, XLK, and SMH.
13. The app must remain local-first and personal-use.
14. Never hardcode secrets, API keys, or broker credentials.

## 3. Strategy defaults

For a USD 10,000 starting portfolio, use these defaults:

- Base CAGR objective: 18–22%.
- Strong objective: 22–25%.
- Stretch objective: 25–30%.
- Normal max drawdown budget: 25–30%.
- Hard max drawdown limit: 35%.
- Live positions: 6–10.
- Cash buffer: 10–20%.
- Max single stock: 15%.
- Holding period: 1–5 years.
- Margin: disabled.
- Options: disabled in MVP.
- Auto-trading: disabled.

These are strategy settings and research assumptions, not performance promises.

## 4. Core system brain

Implement the decision engine around this formula:

```text
Final Action =
AI Relevance
× Business Quality
× Earnings Acceleration
× Valuation / Expected IRR
× Technical Regime
× Portfolio Risk Budget
× Evidence Freshness
− Red Flags
```

A lower price only improves the valuation input. It does not improve business quality, earnings quality, AI relevance, management execution, competitive advantage, balance-sheet strength, or free cash flow.

Score alone must never create a buy/add action.

## 5. Required decision states

Use professional decision states instead of simple buy/sell/hold only:

- `REJECTED`
- `RESEARCH_CANDIDATE`
- `WATCHLIST`
- `APPROVED_THESIS`
- `APPROVED_VALUATION_ZONE`
- `TECHNICAL_WAIT`
- `STARTER_ALLOWED`
- `ADD_ALLOWED`
- `HOLD`
- `TRIM_CANDIDATE`
- `EXIT_THESIS_BROKEN`
- `BLOCKED_BY_RISK`
- `NO_ACTION`

## 6. Buy/add blocking rules

A buy or add action must be blocked when any of the following is true:

- No approved thesis exists.
- No invalidation rule exists.
- AI relevance is weak or unproven.
- Latest earnings weakened the thesis.
- Guidance was cut for structural reasons.
- Margin deterioration is unexplained or persistent.
- Valuation does not support the required expected IRR.
- Technical regime is broken and there is no stabilisation.
- Portfolio concentration limit would be breached.
- Evidence is stale.
- The only positive argument is that price has fallen.
- Portfolio drawdown is at or above the hard drawdown limit.

## 7. Valid buy/add evidence

A buy/add decision may be allowed only when the reasoning is based on evidence such as:

- Revenue growth accelerated.
- AI-related demand became more measurable.
- AI-related segment, backlog, RPO, order, or customer evidence improved.
- Gross margin or operating margin expanded.
- Free cash flow improved.
- Guidance was raised or management tone materially improved.
- Valuation supports the required expected return.
- Technical trend is supportive or stabilising.
- Portfolio risk budget allows the position size.

## 8. Seven core engines

Preserve these seven engines:

1. AI infrastructure causal map.
2. Quality-growth filter.
3. Earnings acceleration engine.
4. Valuation and expected-return underwriting engine.
5. Technical confirmation engine.
6. Portfolio risk engine.
7. Anti-generic guardrail engine.

## 9. AI infrastructure map

Classify companies into AI infrastructure layers, including:

- Compute: GPUs, ASICs, accelerators.
- Memory: HBM, DRAM.
- Storage: NAND, SSD, HDD, enterprise storage.
- Foundry: advanced semiconductor manufacturing.
- Semiconductor equipment: lithography, deposition, etch, inspection.
- Networking: switches, optical, interconnect.
- Cloud: hyperscalers and AI platforms.
- Power/cooling: electrical, thermal, grid, data-centre infrastructure.
- Software: AI monetisation, cybersecurity, observability, data platforms.

Do not treat a company as AI-relevant only because management says “AI.” Require measurable evidence where possible.

## 10. Evidence object standard

Represent evidence using a structured object similar to:

```json
{
  "claim": "Revenue growth accelerated due to AI-related demand.",
  "evidence": "Latest quarter data, management commentary, segment growth, or filing excerpt.",
  "source": "SEC filing, earnings release, transcript, API data, or manually entered source.",
  "source_date": "YYYY-MM-DD",
  "confidence": "LOW | MEDIUM | HIGH",
  "disproves_if": "Guidance is cut, segment demand slows, or margins deteriorate."
}
```

All stock actions must be traceable to evidence objects or explicitly marked as demo/mock examples.

## 11. Research source protocol

When adding or changing strategy logic, use reliable sources and document them in `docs/research/`.

Preferred source hierarchy:

1. Academic papers, official working papers, journal pages, or author/institution pages.
2. Official company filings and investor relations documents.
3. Official data-provider/API documentation.
4. Reputable institutional research from firms such as AQR, S&P Dow Jones Indices, Gartner, IEA, SEC, FRED, EIA, and exchange/data providers.
5. Reputable financial news only for context, not as core model evidence.
6. Blogs/social media only as low-confidence context and never as the sole reason for an investment rule.

For each research-backed rule, document:

```text
Source title:
Author / institution:
URL or citation:
What it supports:
How Q-GEAR implements it:
Limitations / caveats:
Date reviewed:
```

Do not invent sources. If web access is unavailable, create a `docs/research/TODO_sources.md` note and clearly mark the claim as unverified.

## 12. Research-backed strategy anchors to preserve

The system should continue to reflect these evidence anchors:

- Wealth creation is concentrated in a small number of exceptional stocks; this supports a focused research process rather than owning everything.
- Quality/profitability matters; prefer profitable, growing, safe, well-managed companies and avoid low-quality AI hype.
- Earnings acceleration and guidance changes matter; quarterly earnings are the main thesis-update event.
- Momentum/trend and relative strength can support timing and risk control, but they do not create the thesis.
- Active stock selection is difficult; benchmark honestly against SPY, QQQ, XLK, and SMH.
- Backtests must avoid look-ahead bias and must use filing/availability dates where possible.

## 13. Technical stack

Use this local-first stack unless there is a strong documented reason to deviate:

- Frontend: Next.js + TypeScript.
- Backend: Python FastAPI.
- App DB: SQLite.
- Analytics DB: DuckDB.
- Scheduler: APScheduler or a simple local scheduled-job abstraction.
- Data ingestion: modular providers with mock/demo data first, then real providers.
- AI layer: prompt templates with structured JSON output and evidence logging.

## 14. Current repository architecture

Respect the current monorepo layout:

```text
apps/
  api/        FastAPI backend, SQLite state, DuckDB analytics setup
  web/        Next.js dashboard
packages/
  qgear-core/ Pure scoring, risk, and decision policy
  qgear-ingest/ Provider interfaces and respectful ingestion utilities
  qgear-ai/   Evidence schema and prompt helpers
data/
  demo/       Demo universe metadata
  sqlite/     Local app DB, ignored except placeholders
  duckdb/     Local analytics DB, ignored except placeholders
  cache/      Provider cache, ignored except placeholders
docs/
prompts/
scripts/
tests/
```

Keep `qgear-core` pure and independent. Do not move the decision brain into the frontend. The API may adapt decision outputs, but the core decision rules must remain testable without the web app or live APIs.

## 15. Provider and data-source rules

v0.1 uses mock/demo data. Add live providers behind interfaces.

Core free providers:

- SEC EDGAR company facts, submissions, filings, and XBRL data.
- FRED macro data.
- EIA energy/electricity data.

Optional providers:

- Alpha Vantage.
- Financial Modeling Prep.
- Finnhub.
- Nasdaq Data Link.

Experimental fallback:

- `yfinance` may be added later only as experimental fallback, not mission-critical truth.

SEC provider requirements:

- custom User-Agent from env,
- local cache,
- retry with backoff,
- max 10 requests/second,
- no endpoint hammering,
- source timestamps stored.

Never hardcode API keys. `.env` is local only and must be ignored by git.

## 16. Project Manager operating mode

When the user asks Codex to “check, fix, test, iterate, use subagents, or complete the roadmap,” Codex must operate as a Project Manager plus specialist subagents.

The main Codex thread is the **Project Manager**. It owns planning, scope control, merging findings, implementation order, tests, documentation, and final status. The Project Manager must not blindly apply subagent suggestions; it must reconcile conflicts and preserve Q-GEAR rules.

Project Manager loop:

```text
1. Read AGENTS.md, README.md, docs/, prompts/, tests/, and current git status.
2. Create or update docs/project_status.md with current milestone, known gaps, tests, and next actions.
3. Audit the repo against the roadmap and non-negotiables.
4. Spawn specialist subagents when the task is broad enough.
5. Consolidate subagent findings into a prioritized implementation plan.
6. Implement one coherent milestone or fix batch at a time.
7. Run the relevant tests and smoke checks.
8. Fix failures and rerun tests until green or clearly blocked.
9. Update docs/project_status.md and docs/iteration_log.md.
10. Provide a final report with files changed, tests run, failures, risks, and next milestone.
```

Do not skip tests because the change “looks small.” Do not claim verification if a command was not run.

## 17. Specialist subagent roles

When explicitly asked to use subagents, spawn focused agents such as:

1. **Strategy Research Agent**
   - Audits scoring, gates, portfolio rules, and research documentation.
   - Uses primary/authoritative sources where web is available.
   - Flags weak or unsupported strategy assumptions.

2. **Core Decision Engine Agent**
   - Audits `packages/qgear-core`.
   - Checks scoring, gates, drawdown modes, position sizing, and anti-buy-the-dip tests.

3. **Backend/API Agent**
   - Audits FastAPI routes, schemas, persistence, provider interfaces, seed loading, and error handling.

4. **Frontend/UI Agent**
   - Audits Next.js pages, user flow, clarity, fallback data, forms, and visible decision evidence.

5. **Data Ingestion Agent**
   - Audits SEC/FRED/EIA/provider interfaces, caching, rate limits, source logging, and future live-data readiness.

6. **QA/Test Agent**
   - Audits unit tests, smoke tests, build scripts, seed validation, CI readiness, and regression coverage.

7. **Security/Privacy Agent**
   - Audits secrets handling, local-first assumptions, `.gitignore`, file paths, dependency risks, and no-broker/no-autotrade boundaries.

8. **Documentation/PM Agent**
   - Audits README, docs, API examples, setup instructions, project status, and milestone tracking.

Expected subagent output format:

```text
Role:
Scope checked:
Findings:
Severity: critical | high | medium | low
Recommended changes:
Files likely affected:
Tests to run:
Open questions / blockers:
```

## 18. Iteration and self-monitoring files

Maintain these files when doing multi-step work:

```text
docs/project_status.md       Current milestone, health, checklist, blockers.
docs/iteration_log.md        Chronological implementation/testing notes.
docs/roadmap.md              v0.1.x → v1.0 milestone plan.
docs/research/               Source-backed strategy and data-provider notes.
docs/API_EXAMPLES.md         API examples and expected response shapes.
```

If a file does not exist, create it when useful. Keep updates factual and concise. Do not write fake progress.

## 19. Roadmap and milestone order

Do not attempt the entire dream system in one huge diff. Work in milestones:

### v0.1.1 — hardening and verification

- Clean absolute local paths from docs.
- Improve `.gitignore`.
- Verify Python tests and compile checks.
- Verify or document frontend install/build status.
- Add API examples.
- Add seed-data validation.
- Improve setup docs.

### v0.2 — live SEC and price-data foundation

- SEC submissions/company facts ingestion with cache/rate limits.
- Filing metadata and source logging.
- Daily price provider interface.
- Benchmark snapshots for SPY, QQQ, XLK, SMH.
- Real financial metric calculation where possible.
- Clear demo/live mode separation.

### v0.3 — earnings and evidence engine

- Earnings calendar interface.
- Earnings release/transcript ingestion when provider configured.
- Structured evidence objects.
- Earnings summary and thesis-change detection.
- Guidance and segment metric extraction.

### v0.4 — valuation and backtesting

- Bear/base/bull valuation cases.
- Expected IRR engine.
- Backtesting framework with no look-ahead bias.
- Benchmark comparison.
- Filing-date availability handling.

### v0.5 — portfolio reports and alerts

- Daily brief.
- Weekly report.
- Monthly portfolio review.
- Quarterly earnings review.
- Annual strategy audit.
- Local alert rules.

### v1.0 — complete local personal research OS

- Stable local app with documented setup.
- Live-data providers configurable but optional.
- Evidence-backed decision engine.
- Stock memos, thesis approval, invalidation rules.
- Portfolio risk and journal workflows.
- Backtesting and benchmark reporting.
- No auto-trading, no margin, no options by default.

## 20. Test and verification harness

Use the available commands from repo docs. At minimum for Python/core/API changes:

```bash
python3 scripts/run_tests.py
python3 -m compileall packages apps/api scripts tests
```

For API smoke tests when dependencies are installed:

```bash
./scripts/dev_api.sh
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/universe
curl http://127.0.0.1:8000/portfolio
curl http://127.0.0.1:8000/earnings
curl http://127.0.0.1:8000/reports/weekly
```

For frontend changes, when `apps/web/node_modules` exists or install succeeds:

```bash
cd apps/web
npm run lint
npm run build
```

If `npm install` fails due to network, document the exact error and do not claim the frontend runtime was verified.

## 21. Required tests for decision brain

Keep or add tests for these scenarios:

1. Price falls but fundamentals do not improve → add must be blocked.
2. No approved thesis → buy must be blocked.
3. No invalidation rule → buy/add must be blocked.
4. Thesis exists, earnings improve, valuation attractive, technicals stabilising, risk budget available → starter allowed.
5. Position concentration exceeds limit → add blocked by risk.
6. Latest earnings weaken the thesis → do not buy.
7. Expected IRR below hurdle → watch/hold, not buy.
8. Portfolio drawdown exceeds 35% → hard audit / defensive mode.
9. Score is high but hard gate fails → no buy/add.
10. Evidence stale → watch/hold, not buy/add.

## 22. User flow to preserve

The target end-to-end flow:

```text
Onboarding
→ build AI universe
→ screen candidates
→ open stock deep dive
→ approve thesis and invalidation rule
→ calculate position size
→ user manually trades outside app if desired
→ journal decision
→ daily light monitoring
→ weekly ranking
→ monthly portfolio review
→ quarterly earnings review
→ annual strategy audit
```

Daily output should usually be calm and action-sparse. Quarterly earnings reviews should be the main evidence-update workflow.

## 23. Coding style

- Prefer simple, readable code over clever abstractions.
- Use explicit types where practical.
- Keep pure domain logic in `qgear-core`.
- Keep AI prompts versioned in `prompts/`.
- Keep configuration in environment variables and `.env.example`.
- Never commit secrets or API keys.
- Make the app runnable locally with documented commands.
- Include clear seed/demo data for development.
- Avoid absolute local paths in docs.
- Do not introduce large dependencies without a clear reason.

## 24. Security, privacy, and compliance boundaries

- Local-first by default.
- Do not send portfolio data to external services unless explicitly configured.
- Store user data locally.
- Keep API keys in environment variables.
- No broker integration unless explicitly requested in a future milestone.
- No trading execution layer.
- No background upload of user portfolio, watchlist, or notes.
- Include personal-use educational disclaimers.

## 25. Git discipline

- Run `git status` before and after significant work.
- Do not commit `.env`, local DB files, cache files, `node_modules`, `.next`, `.venv`, or secrets.
- Prefer small coherent commits by milestone if the user explicitly asks Codex to commit.
- Never rewrite git history unless explicitly instructed.
- End each run with a clear “commit-ready” summary and suggested commit message.

## 26. Final reporting format for Codex

Every substantial Codex run should end with:

```text
Summary:
Files changed:
Tests run:
Results:
What was verified:
What could not be verified:
Risks / caveats:
Next recommended milestone:
Suggested commit message:
```

Be honest. Do not claim that research, tests, builds, or smoke checks were completed if they were not.

## Continuous Project Manager Operating Mode

When the user asks for project-wide progress, continuous improvement, or "continue until complete", Codex must operate as the **Q-GEAR Project Manager**.

The Project Manager must not treat a single milestone as the final goal unless the user explicitly says to stop after that milestone. The final goal is a complete local personal-use Q-GEAR AI Growth OS that implements the strategy, portfolio workflow, evidence engine, reporting, and data-provider roadmap while preserving all non-negotiable investment guardrails.

### Core rule

Work milestone by milestone. After each milestone, run quality checks, fix failures, update docs, update version/status, then continue to the next milestone unless:

1. the user requested a stop,
2. a required approval is blocked,
3. tests cannot proceed due to an external dependency or network issue,
4. a design decision requires user input,
5. continuing would risk breaking the non-negotiable product or investment rules.

Never claim the complete project is done unless all roadmap milestones have passed their exit criteria.

---

## Roadmap Milestones

Maintain and update `docs/roadmap.md`, `docs/project_status.md`, and `docs/iteration_log.md`.

Default milestone order:

### v0.1.1 — Hardening and verification

Goal: make the demo MVP reliable, documented, testable, and safe.

Required exit criteria:

- Python tests pass.
- Python compile checks pass.
- Frontend lint/typecheck/build pass, or blocker is documented honestly.
- API smoke tests pass.
- Demo universe validates.
- `.gitignore` protects `.env`, virtualenvs, node_modules, local DBs, caches, and build artifacts.
- README, API examples, project status, and iteration log are updated.
- No auto-trading, margin, options, or generic buy-the-dip behavior exists.

### v0.2 — Data foundation

Goal: add safe, modular live-data foundations without corrupting the decision brain.

Scope:

- Provider metadata model.
- Safe demo/live routing.
- SEC company facts and filings metadata provider with custom User-Agent, cache, backoff, and <=10 requests/sec.
- Price provider interface and at least one safe implementation or documented placeholder.
- Benchmark snapshot model for SPY, QQQ, XLK, and SMH.
- Source/evidence provenance records.
- File-backed API tests for provider responses.

Exit criteria:

- Demo mode still works without API keys.
- Provider failures degrade gracefully.
- No secrets are hardcoded.
- Ingestion tests pass with fixtures/mocks.
- Source metadata is visible through API models.

### v0.3 — Earnings and evidence engine

Goal: make earnings review the heart of the system.

Scope:

- Earnings event model.
- Pre-earnings checklist.
- Post-earnings analysis schema.
- Guidance/beat/miss/manual evidence input.
- Thesis strengthened/unchanged/weakened/broken logic.
- Structured evidence object persistence.
- Evidence freshness rules.
- Prompt templates for earnings summariser, thesis updater, risk extractor, and scoring explainer.

Exit criteria:

- A user can review a stock before and after earnings.
- Fresh positive evidence is required for add actions.
- Weakening evidence blocks buy/add.
- Evidence objects include claim, source, source date, confidence, and disproves_if.
- Tests cover earnings-strengthened and earnings-weakened paths.

### v0.4 — Valuation and backtesting

Goal: add disciplined valuation underwriting and strategy testing.

Scope:

- Bear/base/bull valuation cases.
- 3-year and 5-year expected IRR.
- Probability-weighted IRR.
- Valuation hurdle gates.
- Benchmark comparison.
- Backtest skeleton with no-lookahead rules and fixture data.
- Strategy audit report.

Exit criteria:

- Buy/add requires valuation hurdle clearance.
- Great company but poor expected IRR becomes Watch/Hold, not Buy.
- Backtest code is separated from live decision state.
- Backtest docs explain limitations.
- Tests cover valuation edge cases.

### v0.5 — Portfolio reports, alerts, and review cycles

Goal: make the app useful as a recurring personal research OS.

Scope:

- Daily brief.
- Weekly ranking report.
- Monthly portfolio review.
- Quarterly earnings review.
- Annual strategy audit.
- Alert rules for filings, earnings, technical breaks, stale evidence, concentration, drawdown, and thesis review dates.
- Decision journal analytics and mistake review.

Exit criteria:

- Reports are generated from local state.
- Most daily reports can say "No action justified today."
- Alerts never become auto-trade instructions.
- Journal entries link to evidence and decision state.

### v1.0 — Complete local personal research OS

Goal: complete the planned system without turning it into an advisory product or trading bot.

Exit criteria:

- Local setup is documented and repeatable.
- Demo mode works fully.
- Live-data mode is optional, configurable, and safe.
- Strategy brain is implemented in core domain logic, not only UI copy.
- Evidence, thesis, valuation, technical, and risk gates all affect decisions.
- Portfolio review and journal workflows are usable end to end.
- Tests, docs, and project status are current.
- Known limitations are clearly listed.

---

## Required Iteration Loop

For every milestone, Codex must execute this loop:

1. **Audit**
   - Read `AGENTS.md`, `README.md`, `docs/roadmap.md`, `docs/project_status.md`, and `docs/iteration_log.md`.
   - Run `git status`.
   - Inspect relevant code and tests.
   - Identify blockers and risks.

2. **Subagent review**
   Spawn bounded subagents when useful. Prefer subagents for read-heavy or review-heavy work.

   Suggested subagents:
   - Strategy Research Agent
   - Core Decision Engine Agent
   - Backend/API Agent
   - Frontend/UI Agent
   - Data Ingestion Agent
   - QA/Test Agent
   - Security/Privacy/Compliance Agent
   - Documentation/PM Agent

   Each subagent report must include:
   - role,
   - files reviewed,
   - findings,
   - severity,
   - proposed changes,
   - tests to run,
   - blockers.

3. **Plan**
   - Create a concise implementation plan for the current milestone.
   - Do not start the next milestone until current exit criteria pass or a blocker is documented.

4. **Implement**
   - Make focused changes.
   - Keep qgear-core pure and testable.
   - Keep live data behind providers.
   - Keep demo mode working.
   - Do not add broker execution, auto-trading, margin, or options.

5. **Test and QC**
   Run relevant checks. Default checks include:

   ```bash
   python3 scripts/run_tests.py
   python3 -m compileall packages apps/api scripts tests
   python3 scripts/seed_local_data.py
   ```

   If frontend dependencies are installed:

   ```bash
   cd apps/web
   npm run lint
   npm run typecheck
   npm run build
   npm audit --omit=dev
   ```

   API smoke checks should cover:

   ```text
   /health
   /universe
   /portfolio
   /earnings
   /reports/weekly
   ```

6. **Fix loop**
   - If tests fail, fix and rerun.
   - Do not proceed with known failing tests unless the failure is external and documented.

7. **Documentation and status update**
   Update:
   - `docs/project_status.md`
   - `docs/iteration_log.md`
   - `docs/roadmap.md`
   - relevant API/setup docs
   - known limitations

8. **Version checkpoint**
   - Update version/status labels where the project already tracks them.
   - Recommend a Git commit message.
   - Do not create tags unless asked.

9. **Continue or stop decision**
   - If the milestone passed and the user asked for continuous progress, proceed to the next milestone.
   - If approval, network, environment, or design input is required, stop and report exactly what is needed.

---

## Research Rules for Strategy Work

When implementing or changing strategy logic, Codex must not invent research claims. Use `docs/research/source_library.md` as the starting bibliography and add source notes under `docs/research/`.

For each research-backed strategy decision, record:

```text
Title:
Author/organisation:
URL or citation:
Date accessed:
Summary:
How it affects Q-GEAR:
Implementation consequence:
Limitations:
```

Preferred evidence types:

1. Academic papers and working papers.
2. Primary data-provider documentation.
3. Reputable institutional research.
4. Company filings and earnings materials.
5. Official regulatory/tax/data-source documentation.

Do not use social media or blogs as primary evidence for strategy rules.

---

## Completion Standard

The project is not complete when the code merely compiles. The project is complete only when the end-to-end local user flow works:

```text
onboarding/settings
→ AI universe
→ stock deep dive
→ thesis approval
→ valuation and expected IRR
→ earnings evidence update
→ technical/risk confirmation
→ portfolio sizing
→ journal entry
→ daily/weekly/monthly/quarterly/annual reports
→ benchmark/risk review
```

The system must preserve these outputs:

- clear decision state,
- reasons,
- blockers,
- evidence,
- source metadata,
- confidence,
- what would disprove the thesis,
- position-size/risk impact,
- journal/audit trail.

If the system cannot justify an action, it must say:

```text
No action justified today.
```
