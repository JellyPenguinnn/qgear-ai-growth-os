# Information Architecture

Date: 2026-06-23

This document defines the v2 navigation and workflow architecture. It is a product map, not a promise that every route already exists.

## IA Principles

- Start with what needs review, not with rankings.
- Treat actions as gated decision states, not buy/sell signals.
- Keep evidence, source, confidence, and disproof criteria close to every claim.
- Keep AI assistance explicit, draft-only, and opt-in.
- Keep manual workflow fully usable when providers or AI are disabled.

## Primary Navigation

Recommended v2 top-level navigation:

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

## Route Map

### Today

Route: `/` initially, optional `/today` alias later.

Purpose:

- Answer “what matters now?”
- Default to “No action justified today” unless evidence changed and all gates clear.

Core modules:

- Daily stance.
- Review queue.
- Evidence changes.
- Top blockers.
- Provider/data status.
- Portfolio risk mode.
- Upcoming reviews.

### Pipeline

Route: `/pipeline` later; may be introduced as a section within `/universe` first.

Purpose:

- Show where each stock sits in the Q-GEAR process.

Columns:

- Research candidates.
- Watchlist.
- Approved thesis.
- Valuation zone.
- Technical wait.
- Starter allowed.
- Add allowed.
- Hold.
- Trim / exit review.

Card fields:

- Ticker.
- Company.
- State.
- Top reason.
- Top blocker.
- Next research task.
- Evidence age/source quality.

### Universe

Route: `/universe`.

Purpose:

- Searchable and filterable research universe.

Primary users:

- User screening new names.
- User comparing metrics across AI infrastructure layers.

Must include:

- AI layer.
- Score.
- decision state.
- evidence confidence.
- last reviewed date.
- blocker summary.

### Workbench

Route: `/universe/[ticker]` for now; optional `/workbench/[ticker]` alias later.

Purpose:

- Deep research and decision workspace for one stock.

First viewport must answer:

```text
State:
Why:
Blocked because:
Evidence quality:
Next review:
Max new money:
```

Required sections:

- Decision card.
- Reasons and blockers.
- Next research task.
- Evidence timeline.
- Thesis card.
- Earnings card.
- Valuation card.
- Technical/risk card.
- Portfolio impact card.
- Journal trail.
- AI assistant panel when AI foundation exists.

### Earnings

Route: `/earnings`.

Purpose:

- Quarterly evidence engine.

Workflow:

- Before earnings checklist.
- After earnings review.
- Source text/evidence capture.
- Thesis change classification.
- Decision blockers.
- Journal draft.

### Portfolio

Route: `/portfolio`.

Purpose:

- Manual portfolio and risk budget review.

Modules:

- Cash.
- Total equity.
- Drawdown mode.
- Position weights.
- AI-layer exposure.
- Benchmark comparison placeholders.
- Expected IRR distribution.
- Concentration risks.
- Blocked adds.
- Review calendar.

### Journal

Route: `/journal`.

Purpose:

- Audit trail and behavior-improvement system.

Modules:

- Decision records.
- Evidence quality.
- Invalidation rule.
- Expected IRR at decision date.
- Later outcome.
- Mistake category.
- Followed-system flag.
- Process score.

### Reports

Route: `/reports`.

Purpose:

- Recurring review cadence.

Reports:

- Daily brief.
- Weekly ranking.
- Monthly portfolio review.
- Quarterly earnings review.
- Annual strategy audit.

### Settings

Route: `/settings`.

Purpose:

- Local app configuration and safety defaults.

Modules:

- Starting capital.
- Base currency.
- Country.
- Risk style.
- CAGR objective.
- Drawdown limit.
- Cash buffer.
- Single-stock cap.
- Benchmarks.
- Provider status.
- AI provider status once implemented.
- Margin/options/auto-trading disabled state.

## Data Ownership

Frontend pages may render workflow summaries, but deterministic decision rules belong in `packages/qgear-core` and backend adapters. The frontend must not invent buy/add permission or override blockers.

## v1.2 Component Map

- `AppShell`
- `TopNav`
- `PageHeader`
- `MetricCard`
- `DecisionCard`
- `EvidenceCard`
- `BlockerList`
- `ReviewQueue`
- `StateBadge`
- `ProviderStatusBadge`
- `EmptyState`
- `SectionCard`

## v1.3 API Needs

Likely backend routes:

- `GET /today`
- `GET /pipeline`

Until those exist, frontend may compose from existing `/universe`, `/alerts`, `/portfolio`, `/reports/daily`, and `/providers/status`, but that should be treated as transitional.
