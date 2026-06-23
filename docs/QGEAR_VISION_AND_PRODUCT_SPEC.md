# Q-GEAR Vision and Product Specification

## 1. Purpose

This file explains what Q-GEAR AI Growth OS is supposed to become.

`AGENTS.md` contains permanent rules. This file contains product direction, roadmap, user experience goals, AI enhancement goals, and milestone definitions.

When Codex works on product improvements, it must read both:

```text
AGENTS.md
docs/QGEAR_VISION_AND_PRODUCT_SPEC.md
```

---

## 2. Current state summary

Current pushed repo state is a v1.0 local/demo research OS.

It already has:

- Pure Q-GEAR decision brain in `qgear-core`.
- FastAPI backend.
- Next.js frontend.
- SQLite local persistence.
- Optional DuckDB analytics setup.
- Demo AI universe.
- Provider metadata foundation.
- Earnings/evidence engine.
- Valuation/IRR fixture engine.
- Fixture no-lookahead backtest skeleton.
- Local alerts and reports.
- Tests for the core decision guardrails.

Current limitations:

- UI/UX is functional but not impressive.
- User flow is too complex and developer-like.
- AI is not yet meaningfully integrated into the user workflow.
- `qgear-ai` is still mostly a placeholder/helper package.
- Price/benchmark data is mock only.
- FRED/EIA are placeholders.
- Live SEC behavior exists but is not fully verified.
- Backtesting is fixture-only.
- Valuation is too simple.
- Research-source notes are incomplete.
- GitHub Actions CI workflow exists; hosted run status should be verified after each push.
- Visual browser smoke is not robust.

The next goal is not “more screens.” The next goal is a polished, AI-assisted research experience.

---

## 3. Product vision

Q-GEAR AI Growth OS should become a local personal AI research copilot for long-term AI-era growth investing.

The user should open the app and immediately understand:

```text
What changed?
What needs review?
Which stocks are blocked and why?
Which stocks are promising but not actionable?
Which evidence supports the thesis?
What would disprove the thesis?
Is valuation acceptable?
Is technical risk acceptable?
Is portfolio risk acceptable?
What should I do next as a research task?
```

Most days, the app should calmly say:

```text
No action justified today.
```

But when evidence changes, the app should guide the user through:

```text
New evidence
→ thesis update
→ valuation update
→ technical/risk confirmation
→ journal decision
→ review schedule
```

The app should feel like:

```text
Personal AI investment research desk
+ professional decision journal
+ evidence tracker
+ portfolio risk monitor
```

It should not feel like:

```text
Generic screener
trading signal dashboard
messy table app
AI hype chatbot
```

---

## 4. Target user

Primary user:

- 20–30 years old.
- Singapore or Malaysia based.
- Starting portfolio around USD 10,000.
- Interested in US-listed AI-era growth stocks.
- Long-term investment mindset.
- Slightly aggressive but not reckless.
- Wants professional process, not random tips.
- Wants clear UI, simple flow, and evidence-based reasoning.

The app must support:

```text
Base currency: USD, SGD, MYR
Country setting: Singapore, Malaysia, Other
Manual portfolio mode
Local data storage
Optional API keys
No broker execution
No public advisory behavior
```

---

## 5. Strategy brain to preserve

Q-GEAR strategy:

```text
Quality Growth
+ Earnings Acceleration
+ AI Infrastructure Relevance
+ Valuation / Expected IRR
+ Technical Risk Confirmation
+ Portfolio Risk Budget
+ Evidence Freshness
```

Core principle:

```text
Price movement alone can never create a buy/add signal.
```

A lower price can improve valuation, but it cannot improve:

- business quality,
- earnings quality,
- AI relevance,
- management execution,
- competitive advantage,
- free cash flow,
- balance-sheet strength,
- thesis validity.

---

## 6. AI infrastructure map

The stock universe should classify companies by AI infrastructure layer:

```text
Compute accelerators
Custom silicon
HBM / DRAM memory
NAND / SSD / HDD storage
Foundry
Semiconductor equipment
Networking / optical
Hyperscale cloud
Data-centre power / cooling
Data-centre REIT
AI software
Cybersecurity
Data platform
Other AI beneficiary
Not relevant
```

AI relevance requires measurable evidence, such as:

- segment revenue,
- backlog,
- RPO,
- customer wins,
- capex exposure,
- order growth,
- margin expansion,
- management commentary backed by numbers,
- filings,
- earnings releases,
- transcripts.

AI relevance must not be assigned only because management says “AI.”

---

## 7. The v2.0 product goal

v2.0 should transform Q-GEAR from a working local/demo scaffold into a polished AI-assisted research workstation.

v2.0 should achieve:

```text
1. Clean, impressive, easy-to-use UI.
2. A guided daily/weekly/quarterly workflow.
3. AI-assisted research, not AI-generated trade calls.
4. Better stock memo and evidence experience.
5. Better earnings review workflow.
6. Better valuation underwriting workflow.
7. Better portfolio risk dashboard.
8. Better journal and mistake-review system.
9. Optional live/provider mode with safe fallbacks.
10. CI and quality gates.
```

v2.0 is not complete unless a non-technical user can open the app and understand how to use it without reading the code.

---

## 8. UX north star

The v2.0 app should be built around these main areas:

```text
Today
Research Pipeline
Stock Workbench
Earnings Review
Portfolio Risk
Journal
Reports
Settings
```

### 8.1 Today

Purpose: answer “what matters now?”

Should show:

- Daily stance.
- Important alerts.
- Evidence changes.
- Upcoming reviews.
- Stocks needing thesis refresh.
- Top blocked opportunities and why.
- Portfolio risk mode.
- Demo/live provider status.

Default message:

```text
No action justified today unless evidence changed.
```

### 8.2 Research Pipeline

Purpose: show where every stock sits.

Suggested columns:

```text
Research candidates
Watchlist
Approved thesis
Valuation zone
Technical wait
Starter allowed
Add allowed
Hold
Trim / exit review
```

This should be more useful than a dense screener table.

### 8.3 Stock Workbench

Purpose: one clean page for each stock.

Sections:

1. Header summary.
2. Decision card.
3. Why / why not action.
4. Evidence timeline.
5. Thesis.
6. Earnings.
7. Valuation.
8. Technical risk.
9. Portfolio impact.
10. Journal history.
11. AI research assistant panel.

The first screen should answer:

```text
State:
Reason:
Blockers:
Next research task:
```

### 8.4 Earnings Review

Purpose: quarterly evidence engine.

Workflow:

```text
Before earnings:
- What must go right?
- What would break the thesis?
- What metrics matter?

After earnings:
- Paste/upload earnings release or transcript.
- AI extracts evidence objects.
- User verifies evidence.
- System classifies thesis strengthened/unchanged/weakened/broken.
- Valuation and risk gates update.
- Journal entry is generated.
```

### 8.5 Portfolio Risk

Purpose: answer “am I taking too much risk?”

Show:

- Total equity.
- Cash.
- Drawdown mode.
- Single-stock concentration.
- AI-layer exposure.
- Benchmark comparison.
- Positions by state.
- Risk alerts.
- Expected IRR distribution.
- Worst-case scenario.
- What is blocked due to risk.

### 8.6 Journal

Purpose: improve user behavior.

Show:

- Every decision.
- Evidence attached.
- Thesis/invalidation rule.
- Expected IRR at decision date.
- Later outcome.
- Mistake category.
- Process quality score.
- “Did I follow the system?” review.

### 8.7 Reports

Purpose: recurring review cadence.

Reports:

```text
Daily brief
Weekly ranking
Monthly portfolio review
Quarterly earnings review
Annual strategy audit
```

Reports must be readable, not raw JSON-looking pages.

---

## 9. Visual design direction

The current UI should be redesigned.

Desired feel:

```text
Modern
Clean
Professional
High-trust
Minimal
Calm
Premium research terminal
Clear but not flashy
```

Avoid:

```text
Generic bootstrap look
Too many borders
Too many dense tables
Unstyled forms
Developer-like layout
Color chaos
Overloaded dashboard
```

Suggested design system:

- CSS variables for color, spacing, radius, shadows.
- Dark mode first or clean light/dark toggle.
- Card-based layout.
- Strong typography hierarchy.
- Soft background.
- Subtle accent color.
- Clear badges for decision states.
- Consistent spacing.
- Sticky top nav.
- Responsive mobile/tablet layout.
- Empty states with guidance.
- Skeleton/loading states if practical.
- No heavy UI library unless justified.

Suggested navigation:

```text
Today
Pipeline
Universe
Workbench
Earnings
Portfolio
Journal
Reports
Settings
```

But keep it simple. Do not add too many top-level items if the product feels cluttered.

---

## 10. AI integration vision

Q-GEAR should make meaningful use of AI, but AI must remain evidence-gated.

AI features for v2.0:

### 10.1 AI Research Assistant

A local UI panel where user can ask:

```text
What changed for this stock?
Why is this blocked?
What evidence is missing?
Summarize the latest earnings evidence.
Draft a stock memo from verified evidence.
What would disprove my thesis?
Explain valuation assumptions.
What should I review before adding?
```

The assistant must answer from local evidence, filings, transcripts, provider data, and user notes. If it does not have evidence, it must say so.

### 10.2 AI Evidence Extractor

Input:

- pasted earnings release,
- transcript text,
- filing excerpt,
- investor deck notes,
- manual source text.

Output:

```json
{
  "evidence_objects": [
    {
      "claim": "...",
      "evidence": "...",
      "source": "...",
      "source_date": "YYYY-MM-DD",
      "confidence": "LOW | MEDIUM | HIGH",
      "disproves_if": "..."
    }
  ],
  "thesis_change_candidate": "STRENGTHENED | UNCHANGED | WEAKENED | BROKEN",
  "risk_flags": [],
  "requires_user_verification": true
}
```

AI extraction must be draft-only until user verifies it.

### 10.3 AI Earnings Summarizer

Should produce:

- revenue summary,
- EPS summary,
- guidance,
- segment evidence,
- AI evidence,
- margin/FCF trend,
- management tone,
- red flags,
- thesis change,
- next metrics to monitor.

### 10.4 AI Thesis Updater

Compares:

```text
existing thesis
+ latest evidence
+ latest valuation
+ latest technical state
+ portfolio risk
```

Then drafts:

```text
thesis strengthened / unchanged / weakened / broken
what changed
what did not change
what needs follow-up
what would disprove this
```

### 10.5 AI Scoring Explainer

Explains:

```text
Why score changed
Which components changed
Which hard gates block action
What evidence is missing
```

### 10.6 AI Prompt Library

Maintain prompt templates in `prompts/` or `packages/qgear-ai/`.

Required prompts:

```text
company_classifier.md
earnings_summarizer.md
evidence_extractor.md
thesis_updater.md
risk_extractor.md
valuation_explainer.md
decision_explainer.md
portfolio_reviewer.md
weekly_research_memo.md
```

### 10.7 AI Provider Safety

AI provider must be optional.

Supported mode:

```text
QGEAR_AI_PROVIDER=none | openai
OPENAI_API_KEY=
```

Default:

```text
QGEAR_AI_PROVIDER=none
```

If provider is `none`, app still works and shows manual workflows.

If provider is `openai`, user must explicitly configure key and understand that submitted text may leave local machine.

Never send local portfolio/journal data to AI automatically.

---

## 11. Data-provider roadmap

Current providers:

- Mock/demo provider.
- SEC provider foundation.
- FRED placeholder.
- EIA placeholder.
- Mock prices and benchmarks.

Future provider priorities:

### v1.1 / v1.2

- CI and quality gates.
- UI/UX redesign.
- AI provider skeleton.

### v1.3

- Live SEC verification.
- SEC company facts parser.
- Financial metric extraction from SEC facts.

### v1.4

- Real price provider.
- Benchmark history for SPY, QQQ, XLK, SMH.
- Technical indicators from real price data.

### v1.5

- Earnings calendar/transcript provider interface.
- Optional FMP/Finnhub integration if user configures keys.

### v1.6+

- Real backtesting with availability dates.
- Historical scoring snapshots.
- Portfolio performance tracking.

Live data must remain optional and safe.

---

## 12. v1.0 to v2.0 roadmap

### v1.0.1 — Repo quality and CI

Goal: make the repo safe and verifiable on GitHub.

Deliverables:

- GitHub Actions CI.
- Python tests.
- Python compile check.
- Seed validation.
- Frontend lint/typecheck/build.
- npm audit.
- README CI badge.
- CI docs.
- Project status update.

Exit criteria:

- CI workflow file exists and is documented.
- Local CI-equivalent commands still pass.
- GitHub-hosted run is verified after push when network/GitHub access is available.
- No secrets committed.
- No auto-trading/margin/options introduced.

---

### v1.1 — UX audit and information architecture

Goal: make the app understandable before redesigning visuals.

Deliverables:

- UX audit doc.
- New IA map.
- User journey map.
- Screen-by-screen simplification plan.
- Rename confusing labels.
- Define `Today`, `Pipeline`, `Workbench`, `Earnings`, `Portfolio`, `Journal`, `Reports`, `Settings`.

Exit criteria:

- User can understand app flow in under 2 minutes.
- Docs show the future UI architecture.
- No major code rewrite yet unless necessary.

---

### v1.2 — Visual redesign foundation

Goal: make the app look professional.

Deliverables:

- Design tokens.
- CSS variables.
- Layout shell.
- Navigation.
- Card components.
- State badges.
- Metric cards.
- Empty states.
- Clean table styles.
- Responsive layout.
- Optional dark/light theme.

Exit criteria:

- Frontend build passes.
- Dashboard, universe, stock detail, earnings, portfolio, journal, reports, settings look consistent.
- No dense “developer dashboard” feel.

---

### v1.3 — Today and Research Pipeline

Goal: make the app action-oriented without becoming a signal bot.

Deliverables:

- `/today` or redesigned home page.
- Review queue.
- Alert summary.
- Evidence changes.
- Research pipeline board.
- Clear blockers.
- “No action justified today” default stance.
- Demo/live provider state visible.

Exit criteria:

- User knows exactly what needs review today.
- Starter/add states remain gated.
- Alerts remain review prompts only.

---

### v1.4 — AI provider and prompt foundation

Goal: add meaningful AI support safely.

Deliverables:

- `qgear-ai` real package structure.
- AI provider interface.
- `none` provider default.
- Optional OpenAI provider via env.
- Prompt templates.
- JSON schema validation.
- AI request/response logging metadata.
- UI shows whether AI is enabled.
- No automatic external data sending.

Exit criteria:

- App works without AI key.
- AI calls are explicit user actions.
- AI output is draft-only.
- Tests cover no-provider mode and schema validation.

---

### v1.5 — AI Evidence Workbench

Goal: let user paste/upload source text and convert it into verified evidence.

Deliverables:

- Evidence workbench UI.
- Paste text area.
- Source metadata fields.
- AI extraction button if AI enabled.
- Manual extraction fallback.
- Evidence verification step.
- Persist verified evidence.
- Reject malformed/LOW-confidence action evidence.
- Link evidence to ticker and thesis.

Exit criteria:

- AI evidence does not affect decisions until verified.
- Verified evidence uses standard schema.
- User can see source, confidence, and disproof criteria.

---

### v1.6 — AI Earnings Review

Goal: make quarterly earnings the best workflow in the app.

Deliverables:

- Pre-earnings checklist.
- Post-earnings AI summarizer.
- Earnings evidence extraction.
- Thesis-change draft.
- User verification.
- Score-change explanation.
- Journal draft.
- Next metrics to monitor.

Exit criteria:

- User can review earnings end-to-end.
- Weakening evidence blocks buy/add.
- Strengthened thesis still requires valuation, technical, risk, freshness gates.

---

### v1.7 — Stock Workbench Redesign

Goal: make stock research clear and impressive.

Deliverables:

- New stock detail layout.
- Decision card.
- Evidence timeline.
- Thesis card.
- Valuation card.
- Earnings card.
- Technical/risk card.
- Portfolio impact card.
- AI assistant side panel.
- Journal trail.

Exit criteria:

- First screen answers state, reason, blockers, and next research task.
- Evidence is easy to inspect.
- UI is clean and non-cluttered.

---

### v1.8 — Valuation Underwriting Upgrade

Goal: make expected IRR more useful.

Deliverables:

- Better bear/base/bull editor.
- Revenue CAGR assumptions.
- Margin assumptions.
- FCF margin assumptions.
- Multiple assumptions.
- Dilution/buyback.
- Net cash/debt.
- Probability weights.
- IRR sensitivity table.
- Explain valuation blockers.

Exit criteria:

- “Great company but too expensive” is clearly shown.
- Valuation assumptions are editable and journalable.
- Valuation cannot create buy/add alone.

---

### v1.9 — Portfolio and Journal Intelligence

Goal: improve user behavior and portfolio discipline.

Deliverables:

- Portfolio risk dashboard.
- Exposure by AI layer.
- Position sizing simulator.
- Journal analytics.
- Mistake review.
- Process score.
- Decision outcome tracking.
- Review calendar.

Exit criteria:

- User can see concentration and process drift.
- Journal helps improve decisions.
- No brokerage execution.

---

### v2.0 — Polished AI-assisted local research OS

Goal: complete a polished local personal research OS.

Exit criteria:

- Clean impressive UI.
- Clear user flow.
- AI assistant is useful and safe.
- Evidence workbench works.
- Earnings workflow works.
- Valuation workflow works.
- Portfolio/journal workflow works.
- Reports are readable.
- CI passes.
- Docs are current.
- No auto-trading/margin/options.
- Demo mode works without keys.
- External providers are optional and explicit.
- User can use the app without reading code.

---

## 13. Definition of done for v2.0

v2.0 is done only when:

```text
1. A new user can open the app and understand the flow.
2. The UI feels clean, modern, and professional.
3. The app actually uses AI for research assistance when configured.
4. AI output is evidence-gated and user-verified.
5. The decision brain still blocks generic buy-the-dip behavior.
6. The app supports daily, weekly, monthly, quarterly, and annual review workflows.
7. All tests pass.
8. GitHub CI passes.
9. Docs are current.
10. Known limitations are honest.
```

---

## 14. Copywriting principles

Use user-friendly language.

Prefer:

```text
Why blocked
What changed
Evidence needed
Review next
No action justified today
Thesis strengthened
Valuation hurdle not met
Technical wait
Risk budget blocked
```

Avoid:

```text
Signal
Buy now
Sell now
Guaranteed return
AI says buy
Price target only
Oversold buy
```

---

## 15. Product personality

Q-GEAR should feel like:

```text
calm
professional
evidence-based
slightly aggressive but disciplined
clear
honest
local-first
research-oriented
```

Not:

```text
hype-driven
trader-ish
generic dashboard
messy spreadsheet
black-box AI
```
