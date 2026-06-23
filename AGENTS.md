# AGENTS.md — Q-GEAR AI Growth OS Permanent Repo Contract

## 0. Purpose of this file

This file is the stable, permanent operating contract for Codex and future coding agents working in this repository.

Do not treat this file as a sprint plan, roadmap, product backlog, or iteration log. Those evolving details belong in:

- `docs/QGEAR_VISION_AND_PRODUCT_SPEC.md`
- `docs/project_status.md`
- `docs/roadmap.md`
- `docs/iteration_log.md`
- `prompts/`

Only modify this `AGENTS.md` if the user explicitly asks to change the permanent repo contract or if a serious safety/security correction is required.

Before changing code, Codex must read this file and the product spec.

---

## 1. Project identity

Repository: `qgear-ai-growth-os`

Product name: **Q-GEAR AI Growth OS**

Q-GEAR means:

```text
Quality Growth
Earnings Acceleration
AI Infrastructure Relevance
Risk Control
```

The product is a local, personal-use US equity research operating system for AI-era growth stocks. It is intended for a Singapore/Malaysia-based individual investor starting around USD 10,000.

This is not a public advisory product, not a paid investment service, not an auto-trader, and not a day-trading system.

Required user-facing disclaimer:

> This tool is for personal research and educational use only. It does not provide licensed financial advice, tax advice, or legal advice. Final investment decisions are made by the user.

---

## 2. Non-negotiable product and investment rules

These rules must never be removed or weakened:

1. No auto-trading.
2. No broker execution layer unless explicitly requested in a future milestone.
3. No margin trading.
4. No options trading in MVP/default mode.
5. No generic buy-the-dip system.
6. No “buy because price dropped.”
7. No averaging down without fresh positive fundamental evidence.
8. No buy/add without approved thesis and invalidation rule.
9. Price movement alone is never evidence.
10. Technical analysis is timing/risk confirmation only, not thesis creation.
11. Every action-changing investment claim must include evidence, source, source date, confidence, and what would disprove it.
12. Score alone must never create buy/add action.
13. The app must be comfortable saying: “No action justified today.”
14. The system must benchmark itself against SPY, QQQ, XLK, and SMH.
15. The app must remain local-first and personal-use.
16. Never hardcode secrets, API keys, tokens, or broker credentials.
17. Do not send portfolio, journal, watchlist, or thesis data to external services unless the user explicitly configures that provider.
18. AI output must be treated as draft research assistance, not final truth.

---

## 3. Core Q-GEAR decision brain

The decision engine must remain centered on this formula:

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

The final action must be:

```text
Score + Hard Gates + Risk Budget + Evidence Freshness + Source Quality
```

Never:

```text
Score only
Price drop only
AI hype only
Chart only
```

---

## 4. Required decision states

Use professional workflow states, not simple buy/sell labels only:

```text
REJECTED
RESEARCH_CANDIDATE
WATCHLIST
APPROVED_THESIS
APPROVED_VALUATION_ZONE
TECHNICAL_WAIT
STARTER_ALLOWED
ADD_ALLOWED
HOLD
TRIM_CANDIDATE
EXIT_THESIS_BROKEN
BLOCKED_BY_RISK
NO_ACTION
```

The UI may translate these into friendly labels, but the domain model must preserve these states.

---

## 5. Required buy/add blockers

A buy/add action must be blocked if any of the following is true:

- No approved thesis exists.
- No invalidation rule exists.
- AI relevance is weak or unproven.
- Latest earnings weakened or broke the thesis.
- Guidance was structurally cut.
- Margin deterioration is unexplained or persistent.
- Valuation does not support required expected IRR.
- Technical regime is broken without stabilisation.
- Portfolio concentration limit would be breached.
- Evidence is stale.
- The only positive argument is that price has fallen.
- Portfolio drawdown is at or above the hard drawdown limit.
- Evidence object is missing claim, source, source date, confidence, or disproof criteria.
- Evidence confidence is LOW.
- User cash buffer or risk budget does not allow new money.

---

## 6. Valid buy/add evidence

A buy/add decision may only be allowed when reasoning is supported by evidence such as:

- Revenue growth accelerated.
- AI-related demand became more measurable.
- AI-related segment, backlog, RPO, order, or customer evidence improved.
- Gross margin or operating margin expanded.
- Free cash flow improved.
- Guidance was raised.
- Management tone materially improved and is backed by numbers.
- Valuation supports required expected return.
- Technical trend is supportive or stabilising.
- Portfolio risk budget allows the position size.

Invalid reason:

```text
The stock is down, so it is cheaper.
```

Valid reason:

```text
The stock entered a pre-approved valuation zone AND earnings evidence improved AND the technical regime stabilised AND risk budget allows a starter/add.
```

---

## 7. Evidence object standard

All action-changing claims must use this shape:

```json
{
  "claim": "Revenue growth accelerated due to measurable AI demand.",
  "evidence": "Latest quarter data, filing excerpt, earnings release, transcript excerpt, or provider data.",
  "source": "SEC filing, earnings release, transcript, API data, or manual source.",
  "source_date": "YYYY-MM-DD",
  "confidence": "LOW | MEDIUM | HIGH",
  "disproves_if": "Guidance is cut, demand slows, margins deteriorate, or future filings contradict this."
}
```

Rules:

- LOW confidence cannot support action-changing buy/add output.
- Missing source date cannot support action-changing output.
- AI-generated evidence must be validated before it affects decisions.
- Manual evidence is allowed but must still follow the same schema.
- Demo/mock evidence must be clearly labeled as demo/mock.

---

## 8. Strategy defaults

Default personal-use portfolio assumptions:

```text
Starting portfolio: USD 10,000
Base objective: 18–22% annualised CAGR
Strong objective: 22–25%
Stretch objective: 25–30%
Normal max drawdown budget: 25–30%
Hard max drawdown limit: 35%
Live positions: 6–10
Cash buffer: 10–20%
Max single stock: 15%
Holding period: 1–5 years
Margin: disabled
Options: disabled by default
Auto-trading: disabled
```

These are assumptions and risk controls, not performance promises.

---

## 9. Architecture rules

Respect the monorepo layout:

```text
apps/
  api/        FastAPI backend
  web/        Next.js frontend

packages/
  qgear-core/ Pure scoring, risk, decision policy, earnings, valuation, backtest logic
  qgear-ingest/ Provider interfaces and ingestion utilities
  qgear-ai/   AI prompt, schema, and evidence helpers

data/
  demo/       Demo universe metadata
  sqlite/     Local app DB, ignored except placeholders
  duckdb/     Local analytics DB, ignored except placeholders
  cache/      Provider cache, ignored except placeholders

docs/
  Product docs, research notes, roadmap, API examples, status

prompts/
  Codex prompts and AI prompt templates

scripts/
  Local dev/test/seed scripts

tests/
  Python unittest suite
```

Hard architecture boundaries:

- Keep `qgear-core` pure and independent.
- Do not move decision rules into the frontend.
- Do not make live APIs required for demo mode.
- Do not let provider failures crash the local app.
- Keep AI outputs behind validation and evidence schema.
- The API may adapt domain outputs, but the decision brain must remain testable without web app or live APIs.

---

## 10. AI usage rules

Q-GEAR should use AI to make research easier, clearer, and more disciplined.

AI may:

- Draft stock memos.
- Summarize earnings releases and transcripts.
- Extract evidence objects.
- Compare current quarter vs prior thesis.
- Surface risks and disproof criteria.
- Explain blockers in plain English.
- Generate review checklists.
- Help the user understand “what changed.”

AI must not:

- Produce ungrounded buy/sell recommendations.
- Override hard gates.
- Invent sources.
- Treat social media as primary evidence.
- Send private local data externally without explicit provider configuration.
- Hide uncertainty.
- Replace the deterministic decision engine.

All AI-generated outputs must be labeled as draft research assistance and must preserve the educational/personal-use disclaimer.

---

## 11. Provider and data-source rules

Core free provider roadmap:

- SEC EDGAR company facts, submissions, filings, and XBRL data.
- FRED macro data.
- EIA energy/electricity data.

Optional providers:

- Alpha Vantage.
- Financial Modeling Prep.
- Finnhub.
- Nasdaq Data Link.

Experimental fallback:

- `yfinance` may only be used as an experimental fallback, not mission-critical source of truth.

SEC provider requirements:

- Custom User-Agent from env.
- Local cache.
- Retry with backoff.
- Max 10 requests/second.
- No endpoint hammering.
- Source timestamps and metadata stored.

Never hardcode API keys. `.env` is local only and must be ignored by git.

---

## 12. UI/UX product rules

The product must be clean, clear, impressive, and easy to use.

Prioritize:

- Fewer screens with better hierarchy.
- Clear “what should I review today?” workflow.
- Decision cards with reasons and blockers.
- Progressive disclosure: summary first, details on demand.
- Plain-English explanations.
- Evidence/source visibility.
- Fast local experience.
- Responsive layout.
- Professional visual design.
- Dark/light theme if practical.
- Clear empty states.
- Clear demo/live data labels.
- Clear “not financial advice” language.

Avoid:

- Dense tables as the only interface.
- Too many forms on first view.
- Ugly default styling.
- Developer-oriented UI text.
- Hidden blockers.
- Buy/sell-looking language without context.
- Any UI that encourages overtrading.

---

## 13. Testing requirements

For Python/core/API changes, run:

```bash
python3 scripts/run_tests.py
python3 -m compileall packages apps/api scripts tests
python3 scripts/seed_local_data.py
```

For frontend changes, run when dependencies are installed:

```bash
cd apps/web
npm run lint
npm run typecheck
npm run build
npm audit --omit=dev
```

For API smoke when server binding is available:

```bash
./scripts/dev_api.sh
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/universe
curl http://127.0.0.1:8000/portfolio
curl http://127.0.0.1:8000/earnings
curl http://127.0.0.1:8000/reports/weekly
curl http://127.0.0.1:8000/alerts
curl http://127.0.0.1:8000/valuation/NVDA
```

Do not claim verification if a command was not run.

If a command fails because of network, environment, missing browser runtime, or unavailable provider credentials, document the blocker honestly.

---

## 14. Required regression coverage

Keep or add tests for:

1. Price falls but fundamentals do not improve → add blocked.
2. No approved thesis → buy blocked.
3. No invalidation rule → buy/add blocked.
4. Thesis exists + earnings improve + valuation attractive + technicals stabilising + risk budget available → starter allowed.
5. Owned position requires explicit add intent before ADD_ALLOWED.
6. Concentration exceeds limit → add blocked.
7. Latest earnings weaken thesis → no buy/add.
8. Expected IRR below hurdle → watch/hold, not buy/add.
9. Portfolio drawdown >=35% → hard audit / blocked by risk.
10. Score high but hard gate fails → no buy/add.
11. Evidence stale → no buy/add.
12. LOW-confidence or malformed evidence → no buy/add.
13. Alerts are review prompts, not trade instructions.
14. AI-generated evidence requires validation before affecting decisions.
15. Demo mode works without API keys.
16. Live provider failures degrade gracefully.

---

## 15. Research source protocol

When adding or changing strategy logic, document reliable sources under `docs/research/`.

Preferred evidence hierarchy:

1. Academic papers, official working papers, journal pages, or author/institution pages.
2. Official company filings and investor relations documents.
3. Official data-provider/API documentation.
4. Reputable institutional sources such as AQR, S&P Dow Jones Indices, Gartner, IEA, SEC, FRED, EIA, and exchange/data providers.
5. Reputable financial news only for context, not as core model evidence.
6. Blogs/social media only as low-confidence context and never as the sole reason for an investment rule.

For each source note, use:

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

Do not invent sources. If web access is unavailable, create or update `docs/research/TODO_sources.md`.

---

## 16. Codex project-manager loop

For any broad task, Codex must operate as project manager:

```text
1. Read AGENTS.md and docs/QGEAR_VISION_AND_PRODUCT_SPEC.md.
2. Read README.md, docs/project_status.md, docs/roadmap.md, docs/iteration_log.md, and relevant code/tests.
3. Run git status.
4. Audit before editing.
5. Spawn bounded subagents when useful.
6. Consolidate findings.
7. Implement one coherent milestone or fix batch.
8. Run tests and smoke checks.
9. Fix failures and rerun.
10. Update docs/status/logs.
11. Stop at checkpoint if user requested review, or continue only if a goal prompt explicitly says to continue.
```

Use subagents for read-heavy or review-heavy tasks, such as:

- Product/UX Agent.
- AI Integration Agent.
- Core Decision Engine Agent.
- Backend/API Agent.
- Frontend/UI Agent.
- Data Ingestion Agent.
- QA/Test Agent.
- Security/Privacy Agent.
- Documentation/PM Agent.

Subagent reports must include:

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

---

## 17. Git discipline

- Run `git status` before and after significant work.
- Do not commit `.env`, local DB files, cache files, `node_modules`, `.next`, `.venv`, or secrets.
- Prefer branch-per-milestone work.
- Prefer small coherent commits.
- Do not rewrite history unless explicitly instructed.
- End each substantial run with a commit-ready summary and suggested commit message.
- Do not create tags unless explicitly asked.

---

## 18. Final reporting format

Every substantial Codex run must end with:

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

Be honest. Do not claim research, tests, builds, UI checks, or live-provider verification if they were not performed.
