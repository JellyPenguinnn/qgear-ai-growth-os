# Q-GEAR v2.1 Professional Live Research Foundation

## 1. Purpose

This document defines the next major milestone after v2.0.

v2.0 created a polished local/demo AI-assisted research OS. v2.1 must make Q-GEAR more professional by strengthening the core decision brain and adding safe live-data foundations.

The priority order is:

```text
1. Core brain and strategy correctness
2. Evidence/source/data quality
3. Live SEC and price-data foundations
4. Clear UI/UX for live vs demo state
5. Robust tests, CI, and release verification
```

Do not treat v2.1 as a random feature sprint. Treat it as the transition from demo scaffold to professional local research infrastructure.

---

## 2. Current v2.0 baseline

Current v2.0 capabilities:

```text
Today page
Research Pipeline
Evidence Workbench
Stock Workbench
AI provider foundation
Draft-only AI routes
AI output validation
Editable valuation underwriting
Portfolio/journal intelligence
Reports
GitHub Actions CI workflow file
Local test/build/smoke verification documented
```

Current v2.0 limitations:

```text
Most stock/financial data is still demo or mock.
SEC live behavior is not fully verified.
FRED/EIA are placeholders.
Price and benchmark data are mock.
Backtesting is fixture-only.
Valuation is still mostly demo/draft.
UI is cleaner but still needs stronger live/demo clarity and less cognitive load.
Browser visual smoke remains unverified due environment blocker.
```

---

## 3. v2.1 goal

v2.1 should deliver:

```text
Professional live-data-capable local research OS
+ stronger deterministic Q-GEAR brain
+ source/evidence/data-quality gates
+ live SEC financial foundation
+ optional live price/benchmark provider
+ technical engine from price history
+ FRED/EIA macro and energy context foundation
+ data-health UI
+ clearer onboarding and stock-workbench data quality
+ full test and release verification
```

v2.1 should **not** add:

```text
auto-trading
broker execution
margin
options-by-default
day-trading workflows
price-only buy-the-dip signals
ungrounded AI recommendations
silent external upload of user data
```

---

## 4. v2.1 product principles

### 4.1 Evidence first

Every important claim must be backed by a structured source. The app should make it obvious whether evidence is:

```text
demo/manual/AI draft/user verified/provider verified/SEC filing/earnings release/transcript/price provider/macro provider
```

### 4.2 Live data does not equal action

A live provider update can refresh data and improve confidence, but it cannot directly create a buy/add action. It only feeds the Q-GEAR gates.

### 4.3 AI is a research assistant

AI can extract, summarize, draft, and explain. AI cannot mutate decision state automatically.

### 4.4 Technical analysis is risk confirmation

Technical indicators must come from price data when available, but they remain timing/risk confirmation only.

### 4.5 UI should lower cognitive load

The user should not need to understand the codebase to know:

```text
What should I review?
Why is this blocked?
Which data is live vs demo?
Which evidence is verified?
What is missing before action can be considered?
```

---

## 5. v2.1 milestone map

### Milestone A — Baseline and CI reality check

Goal: verify current v2.0 state before modification.

Deliverables:

```text
Baseline test report
GitHub CI status reality check
Project status update
Iteration log update
```

Exit criteria:

```text
Baseline known.
No unverified success claims.
No code changed except docs if necessary.
```

---

### Milestone B — Core brain source-quality upgrade

Goal: strengthen Q-GEAR before trusting live data or AI evidence.

Deliverables:

```text
EvidenceSourceType
EvidenceVerificationStatus
EvidenceQuality / SourceQuality model
DataQualitySnapshot
DecisionInput integration
Hard-gate upgrades
Regression tests
```

Exit criteria:

```text
AI draft evidence cannot support buy/add.
Demo evidence cannot support live-mode buy/add.
Verified provider/manual evidence can support evidence gate.
Missing source type/date blocks action.
Low source/evidence quality blocks action.
qgear-core remains pure.
```

---

### Milestone C — Live SEC financial foundation

Goal: use SEC EDGAR as official financial truth source.

Deliverables:

```text
ticker to CIK map
SEC company facts parser
canonical financial metric snapshots
source metadata
local persistence
financial API routes
fixture-backed tests
```

Exit criteria:

```text
SEC fixture parses canonical financial metrics.
Source metadata and data-availability dates are retained.
Missing/malformed data returns structured errors.
Demo mode remains keyless.
```

---

### Milestone D — Price, benchmark, and technical engine

Goal: move technical state away from hardcoded demo values.

Deliverables:

```text
price provider interface
mock price history provider
optional Alpha Vantage provider
benchmark history for SPY, QQQ, XLK, SMH
technical indicator calculations
technical API routes
technical card live/demo metadata
fixture tests
```

Exit criteria:

```text
Moving averages and relative strength calculated from price history.
Technical regime is source-dated.
Technical alone cannot create buy/add.
```

---

### Milestone E — FRED/EIA macro and energy context

Goal: add macro and power-demand context without creating direct trade signals.

Deliverables:

```text
FRED provider implementation or safer placeholder
EIA provider implementation or safer placeholder
macro/energy snapshots
context API routes
UI context cards
fixture tests
```

Exit criteria:

```text
Macro/energy data is review context only.
Provider missing-key behavior is safe.
No action state mutation.
```

---

### Milestone F — Professional UI/UX live/demo clarity

Goal: make the product easier and more professional.

Deliverables:

```text
Data Health page
provider setup cards
onboarding improvements
live/demo badges on Stock Workbench
missing input indicators
better empty/loading/error states
UI smoke checks
```

Exit criteria:

```text
User can see data quality and provider status clearly.
Today prioritizes review queue and data health.
Stock Workbench shows why blocked and what data is missing.
```

---

### Milestone G — v2.1 release pass

Goal: verify everything works.

Deliverables:

```text
Full test run
Frontend build
API smoke
Built-route smoke
Docs update
Known limitations update
Commit-ready report
```

Exit criteria:

```text
All available local checks pass.
CI workflow remains valid.
No secrets tracked.
No non-negotiable weakened.
```

---

## 6. v2.1 definition of done

v2.1 is complete only when:

```text
1. Core brain includes source/evidence/data-quality gates.
2. Live SEC financial foundation exists with fixture tests.
3. Optional price provider and technical engine exist with fixture tests.
4. FRED/EIA provider behavior is safer and documented.
5. UI clearly distinguishes demo/live/mixed data.
6. Data Health page exists.
7. Demo mode works without keys.
8. Provider failures degrade gracefully.
9. AI remains draft-only and explicit.
10. No broker execution, auto-trading, margin, or options-by-default exist.
11. Python tests pass.
12. Frontend lint/typecheck/build pass.
13. API smoke passes.
14. Built-route smoke passes.
15. Docs and limitations are current.
```

---

## 7. Key design decision

The most important v2.1 architecture decision is the **truth pipeline**:

```text
source
→ provider response
→ normalized data
→ data quality snapshot
→ evidence object
→ evidence verification
→ financial / technical / valuation features
→ Q-GEAR hard gates
→ decision state
→ journal / review workflow
```

Do not bypass this pipeline.

