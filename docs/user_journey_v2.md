# User Journey v2

Date: 2026-06-23

This journey describes how a non-technical local user should experience Q-GEAR v2.

## First Five Minutes

### Minute 0-1: Open Today

User sees:

- Local/demo mode status.
- Research-only disclaimer.
- Daily stance: “No action justified today unless evidence changed and all gates clear.”
- Portfolio risk mode.
- Top review queue.

User learns:

- The app is not a trading bot.
- The app starts with review discipline, not a buy list.

### Minute 1-2: Review The Queue

User sees review prompts such as:

- Thesis review due.
- Earnings review due.
- Evidence stale.
- Technical broken.
- Valuation hurdle failed.
- Concentration risk.
- Drawdown risk.
- Provider/source issue.

User action:

- Opens the highest-priority review item.

### Minute 2-3: Open Pipeline

User sees:

- Stocks grouped by Q-GEAR state.
- Research candidates and watchlist separated from actionable states.
- Starter/add allowed items shown as gated states, not commands.
- Blockers visible on each card.

User learns:

- High score is not the same as permission to act.
- Most names require more evidence, better valuation, technical stabilisation, or portfolio room.

### Minute 3-4: Open A Stock Workbench

First viewport answers:

```text
State:
Why:
Blocked because:
Evidence quality:
Next review:
Max new money:
```

User sees:

- Decision card.
- Thesis/invalidation rule.
- Evidence timeline.
- Valuation hurdle.
- Technical/risk status.
- Portfolio impact.
- Journal trail.

User action:

- Updates thesis, reviews evidence, or records `NO_ACTION` if gates do not clear.

### Minute 4-5: Journal The Decision

User records:

- Decision state.
- Evidence.
- Source and source date.
- Confidence.
- Invalidation rule.
- Expected IRR.
- Position size or `0%`.
- Future review date.

User learns:

- The journal is the audit trail.
- “No action justified today” is a valid outcome.

## Daily Journey

1. Open Today.
2. Check review queue.
3. Review provider/source status.
4. Open only items with changed evidence or stale review dates.
5. Journal `NO_ACTION` if nothing clears all gates.

Default outcome:

```text
No action justified today.
```

## Weekly Journey

1. Open Reports.
2. Read weekly ranking.
3. Open Pipeline.
4. Move research candidates only when evidence improves.
5. Review blocked high-quality names.

Allowed interpretation:

- Ranking helps prioritize research.

Disallowed interpretation:

- Ranking is not a buy list.

## Earnings Journey

Before earnings:

- Confirm thesis.
- Confirm invalidation rule.
- List metrics that must go right.
- List what would break the thesis.

After earnings:

- Paste or manually enter source evidence.
- Verify evidence object fields.
- Classify thesis strengthened, unchanged, weakened, or broken.
- Recheck valuation, technical, freshness, and risk gates.
- Draft journal entry.

Key rule:

- Earnings can strengthen evidence, but cannot bypass valuation, technical, freshness, or portfolio risk gates.

## Monthly Journey

1. Open Portfolio.
2. Review cash buffer, drawdown mode, concentration, and AI-layer exposure.
3. Review blocked adds and trim candidates.
4. Compare against SPY, QQQ, XLK, and SMH placeholders or configured data.
5. Open Journal and review process quality.

## Quarterly Journey

1. Open Earnings.
2. Review all stocks with new earnings evidence.
3. Update thesis status.
4. Update valuation cases.
5. Refresh review dates.
6. Journal decisions and non-decisions.

## Annual Journey

1. Open annual strategy audit.
2. Compare performance and drawdown against benchmarks.
3. Review journal outcomes.
4. Identify process mistakes.
5. Reassess scoring weights and research rules only after source-backed review.

## Failure States To Handle Gracefully

- API unavailable: app remains readable in demo/fallback mode and does not claim actions are allowed without backend context.
- AI disabled: manual workflow remains fully usable.
- Live provider unavailable: provider status shows unavailable; no route crashes.
- Evidence malformed or LOW confidence: evidence can be stored as reference/draft but cannot support action-changing decisions.
- Price down with no new evidence: add is blocked.
