# Q-GEAR UI/UX v2.1 Specification

## 1. Purpose

v2.0 made the app more polished, but v2.1 should make it easier, clearer, and more professional for real use.

UI/UX must serve the Q-GEAR brain. The interface should make the decision process understandable without encouraging overtrading.

---

## 2. UX north star

When the user opens the app, they should immediately understand:

```text
What should I review today?
Which stocks are blocked and why?
Which data is live vs demo?
Which evidence is verified?
What evidence is missing?
What is the next research task?
What is my portfolio risk mode?
```

The app should feel like:

```text
professional research cockpit
calm daily review desk
evidence tracker
portfolio risk monitor
AI-assisted research assistant
```

It should not feel like:

```text
trading signal board
messy spreadsheet
AI hype dashboard
developer demo app
```

---

## 3. Navigation structure

Recommended primary navigation:

```text
Today
Pipeline
Evidence
Universe
Earnings
Portfolio
Journal
Reports
Data Health
Settings
```

If this feels too crowded, group Data Health under Settings but keep it easy to access from Today and Stock Workbench.

---

## 4. Today page priorities

Today should prioritize:

```text
1. Data health issues
2. Review queue
3. Thesis/evidence/valuation/technical blockers
4. Portfolio risk mode
5. Upcoming review tasks
6. Research rankings last
```

Do not make rankings look like buy recommendations.

Required cards:

```text
Daily stance
Data health summary
Review queue
Portfolio risk mode
Provider mode
Top blockers
Research priority only
```

Default message:

```text
No action justified today unless evidence changed and every hard gate clears.
```

---

## 5. Data Health page

Create `/data-health` or `/settings/data`.

Purpose: show live/demo/mixed data status clearly.

Sections:

```text
Overall mode
SEC EDGAR status
Price provider status
Benchmark provider status
FRED status
EIA status
AI status
Last successful refresh
Last errors
Missing keys
Cache status
What is live vs demo
What data can support action
What data is review-only
```

Example copy:

```text
Demo evidence is useful for workflow testing but cannot support live-mode buy/add decisions.
```

---

## 6. Stock Workbench improvements

The first visible area must answer:

```text
Decision state:
Why:
Blocked because:
Data quality:
Evidence quality:
Next research task:
Max new money:
```

Recommended layout:

```text
Header
  ticker, company, AI layer, provider/data mode

Decision card
  state, allowed?, blockers, reasons, next task

Data quality card
  source quality score, evidence coverage, missing inputs, live/demo badges

Evidence timeline
  verified sources, AI drafts, manual sources, SEC filings, earnings releases

Thesis card
  approved thesis, invalidation rule, next review

Earnings card
  latest thesis change, guidance, margin, FCF, AI evidence

Valuation card
  bear/base/bull, weighted IRR, hurdle, sensitivity

Technical/risk card
  50/150/200 DMA, relative strength, drawdown, source date

Portfolio impact
  current weight, max add, concentration, cash buffer

AI assistant
  explicit draft-only buttons

Journal trail
  historical decisions and outcomes
```

---

## 7. Evidence Workbench improvements

Evidence Workbench should be step-based:

```text
Step 1: Choose ticker and source type
Step 2: Paste or enter source text
Step 3: AI extract draft or manual entry
Step 4: User verifies claim/evidence/source/date/confidence/disproof
Step 5: Save verified evidence
Step 6: See where this evidence appears in Stock Workbench
```

Make it visually obvious:

```text
AI draft is not verified.
LOW confidence cannot support action.
Missing source date blocks action.
Price-only evidence is rejected.
```

---

## 8. Earnings Review improvements

Earnings should be a guided workflow:

```text
Before earnings
  what must go right
  what would break thesis
  expected key metrics
  current valuation hurdle

After earnings
  paste release/transcript
  extract evidence
  classify thesis change
  update valuation assumptions
  generate journal draft
  schedule next review
```

The UI must clearly show:

```text
STRENGTHENED does not automatically mean buy/add.
WEAKENED or BROKEN blocks buy/add.
All gates still apply.
```

---

## 9. Portfolio and Journal improvements

Portfolio should show:

```text
cash and cash percentage
single-stock concentration
AI-layer exposure
expected IRR distribution
benchmark placeholders/live comparison
blocked adds
review calendar
risk mode
```

Journal should show:

```text
decision quality
followed system?
evidence quality
mistake category
outcome
later review due
process score
```

This should help improve behavior, not encourage trading.

---

## 10. Visual design guidelines

Use a clean premium style:

```text
calm colors
strong typography hierarchy
consistent spacing
subtle borders
professional cards
state badges
clear warning/error styles
responsive layout
```

Avoid:

```text
too many tables
dense technical jargon
default unstyled forms
color chaos
large walls of text
buttons that look like trade buttons
```

---

## 11. Component guidelines

Useful reusable components:

```text
AppShell
TopNav
PageHeader
SectionCard
DecisionCard
DataQualityCard
EvidenceTimeline
ProviderStatusBadge
MetricCard
BlockerList
ReviewQueue
EmptyState
LoadingState
ErrorState
SourceBadge
LiveDemoBadge
```

---

## 12. Copywriting rules

Use:

```text
Review
Evidence
Blocked because
Next research task
No action justified today
Draft only
User verified
Provider verified
Live data optional
```

Avoid:

```text
Buy now
Sell now
Signal
Guaranteed
AI says
Hot stock
Oversold buy
```

---

## 13. Accessibility and usability

Add or preserve:

```text
semantic HTML
clear labels
keyboard-accessible forms
visible focus states
reasonable color contrast
responsive layout
plain-language errors
aria-live for form status where useful
```

---

## 14. UX acceptance tests

Before v2.1 is complete, manually or via route smoke verify:

```text
Today shows data health and review queue first.
Pipeline cards show next task and blockers.
Stock Workbench shows data/evidence quality.
Evidence Workbench makes verification step clear.
Earnings workflow explains that strengthened evidence is not automatic buy/add.
Portfolio page shows concentration and blocked adds.
Journal page shows behavior/process analytics.
Data Health page shows provider statuses and missing keys.
Settings explains AI/external data behavior clearly.
```

If browser visual smoke cannot run, document blocker honestly.

