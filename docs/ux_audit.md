# UX Audit

Date: 2026-06-23

Scope: current v1.0 local/demo web app, audited against the v2 product direction in `docs/QGEAR_VISION_AND_PRODUCT_SPEC.md`.

## Summary

The v1.0 app is a solid developer-facing scaffold. It proves the domain model, API, persistence, demo universe, portfolio, journal, reports, and decision guardrails. It does not yet feel like a polished personal research OS.

The main UX issue is not missing data. It is hierarchy. Important concepts such as “what should I review today?”, “why is this blocked?”, “what evidence changed?”, and “what should I journal?” are present in pieces but not arranged as a guided workflow.

## Product Guardrails Preserved

The v2 redesign must preserve:

- No auto-trading.
- No margin.
- No options by default.
- No buy/add because price dropped.
- No averaging down without fresh positive fundamental evidence.
- No buy/add without approved thesis and invalidation rule.
- Technical analysis as timing/risk confirmation only.
- AI output as draft research assistance only.
- Evidence, source date, confidence, and disproof criteria for action-changing claims.

## Current Page Audit

### `/` Dashboard

What works:

- Shows portfolio summary, drawdown mode, provider status, and daily stance.
- Says “No action justified today” in the right spirit.
- Links to settings, reports, and screener.

Problems:

- The page is ranking-led instead of review-led.
- “Action-changing evidence” currently counts allowed states, which can confuse evidence changes with action permission.
- Missing review queue: thesis due, earnings due, stale evidence, technical break, valuation hurdle, concentration, drawdown, and provider/source issues.
- Top rankings table encourages scanning scores before blockers.

v2 direction:

- Redesign root as Today.
- Lead with stance, review queue, top blockers, evidence changes, and provider status.
- Keep rankings secondary.

### `/universe`

What works:

- Has the full demo universe.
- Filters by AI layer, score, decision state, and metrics.
- Links to stock detail.

Problems:

- Dense table is the primary experience.
- Research Pipeline is absent.
- Blockers and next review tasks are not visible without opening each stock.
- The UI feels like a generic screener, not a process board.

v2 direction:

- Add Pipeline as the primary workflow.
- Keep Universe as the searchable table.
- Group stocks by Q-GEAR decision state.
- Show one-line blocker and next research task per ticker.

### `/universe/[ticker]`

What works:

- Shows business summary, AI thesis, evidence, decision reasons/blockers, thesis form, score components, valuation, earnings, technicals, journal count, and sizing.
- Sizing copy correctly says price decline alone never increases allowed size.

Problems:

- The first screen does not answer state, why, blocked because, next review, evidence quality, and max new money in one place.
- Evidence is table-first rather than timeline/card-first.
- Thesis and invalidation are not visually central enough.
- AI assistant panel is absent.
- Fallback demo detail can display allowed states without approved thesis context; this must be hardened during UI work.

v2 direction:

- Rename conceptually to Stock Workbench.
- First viewport should be a decision card plus blockers and next research task.
- Evidence timeline and thesis card should be immediately visible.
- AI controls must be explicit and draft-only.

### `/earnings`

What works:

- Provides checklist and manual earnings review form.
- Stores structured evidence and reviews through API.
- Earnings classification is deterministic.

Problems:

- Workflow is not clearly split into before earnings and after earnings.
- Form defaults are optimistic, including a positive claim and HIGH confidence.
- No paste/source text path or verification step.
- No journal draft after review.

v2 direction:

- Make Earnings Review a guided workflow.
- Use neutral/blank defaults.
- Add source metadata and verification before evidence affects decisions.
- Generate journal draft only after user confirmation.

### `/portfolio`

What works:

- Shows local/manual positions, cash, equity, drawdown mode, concentration, and expected IRR placeholder.
- Manual position form exists.

Problems:

- Missing AI-layer exposure, benchmark comparison, positions by decision state, blocked adds, review calendar, and risk-mode explanation.
- Does not yet help the user see behavior or concentration risk at a glance.

v2 direction:

- Build Portfolio Risk around risk mode, concentration, cash buffer, AI-layer exposure, benchmark context, and blocked new money.
- Keep manual-only portfolio; no broker execution.

### `/journal`

What works:

- Captures decision date, ticker, action, price, size, score, evidence, thesis, invalidation rule, expected IRR, future review, and later outcome.
- Shows journal analytics through reports/API.

Problems:

- Action entry can look like a user-selected trading instruction instead of a recorded decision state.
- Evidence is free text rather than structured source/source date/confidence/disproof fields.
- Missing mistake category, process score, followed-system flag, and review workflow.

v2 direction:

- Reframe as Decision Journal.
- Emphasize process quality, evidence quality, later review, and whether the system was followed.
- Keep STARTER_ALLOWED/ADD_ALLOWED as decision states, not trade commands.

### `/reports`

What works:

- Daily, weekly, monthly, quarterly, and annual reports exist.
- Alerts are review prompts only.
- Reports include useful local/demo summaries.

Problems:

- Reports still feel like formatted API output.
- Alert queue belongs on Today as a daily workflow.
- Needs clearer cards and scan hierarchy.

v2 direction:

- Keep Reports for recurring cadence.
- Move urgent review prompts to Today.
- Make report sections readable and narrative-light.

### `/settings`

What works:

- Onboarding settings exist.
- Margin, options, and auto-trading are disabled.
- Benchmarks and cash/risk settings are visible.

Problems:

- Missing clear provider/data mode and AI safety state.
- Does not yet explain local-first privacy boundaries in the UI.

v2 direction:

- Add demo/live provider status.
- Add AI provider status once v1.4 is built.
- Keep safety defaults prominent.

## Cross-Cutting Issues

- Too table-heavy.
- Too many pages are generic panels rather than workflow cards.
- Provider/demo fallback status is not visible on every workflow.
- Evidence quality is visible but not visually prioritized.
- Empty states are limited.
- No active navigation state.
- No reusable decision/evidence/review queue component set yet.

## v1.2 Acceptance Criteria From This Audit

- App shell and navigation use v2 labels.
- Today answers what to review now.
- Pipeline board exists or is clearly staged.
- Stock detail starts with a decision card.
- Evidence appears as cards/timeline, not only table rows.
- Demo/live/provider status is visible in research workflows.
- No UI copy encourages trading signals.

## Deferred From v1.1

- Large UI rewrite.
- AI provider implementation.
- Evidence persistence schema changes.
- Browser screenshot verification.
