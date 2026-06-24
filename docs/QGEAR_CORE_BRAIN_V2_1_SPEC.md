# Q-GEAR Core Brain v2.1 Specification

## 1. Purpose

The core decision brain is the most important part of Q-GEAR.

v2.1 must strengthen the brain before expanding live data. Live data, AI, charts, and UI improvements are useful only if they feed the decision engine without weakening the hard gates.

The Q-GEAR brain must remain deterministic, testable, and independent of the frontend and live providers.

---

## 2. Existing brain to preserve

Existing formula:

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

Existing principles:

```text
Score alone never creates buy/add.
Price movement alone is never evidence.
Technical analysis is risk/timing confirmation only.
No buy/add without thesis and invalidation rule.
No add without fresh positive evidence.
Valuation can support or block action, but cannot create action alone.
AI output is draft-only until user verified.
```

---

## 3. New v2.1 core concepts

### 3.1 Evidence source type

Add an enum similar to:

```python
class EvidenceSourceType(str, Enum):
    DEMO = "DEMO"
    MANUAL = "MANUAL"
    AI_DRAFT = "AI_DRAFT"
    AI_USER_VERIFIED = "AI_USER_VERIFIED"
    SEC_FILING = "SEC_FILING"
    EARNINGS_RELEASE = "EARNINGS_RELEASE"
    TRANSCRIPT = "TRANSCRIPT"
    PRICE_PROVIDER = "PRICE_PROVIDER"
    MACRO_PROVIDER = "MACRO_PROVIDER"
    ENERGY_PROVIDER = "ENERGY_PROVIDER"
    OTHER = "OTHER"
```

### 3.2 Evidence verification status

Add an enum similar to:

```python
class EvidenceVerificationStatus(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    USER_VERIFIED = "USER_VERIFIED"
    PROVIDER_VERIFIED = "PROVIDER_VERIFIED"
    SYSTEM_VALIDATED = "SYSTEM_VALIDATED"
    REJECTED = "REJECTED"
```

### 3.3 Evidence quality

Add an enum similar to:

```python
class EvidenceQuality(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
```

Evidence quality should be derived from:

```text
source type
verification status
confidence
source date validity
source completeness
whether claim is action-changing
whether evidence is stale
whether source is demo/manual/provider/AI draft
```

---

## 4. Extended Evidence model

Extend the core Evidence object carefully. Preserve backwards compatibility where possible.

Suggested fields:

```python
@dataclass(frozen=True)
class Evidence:
    claim: str
    evidence: str
    source: str
    source_date: str
    confidence: Confidence
    disproves_if: str
    source_type: EvidenceSourceType = EvidenceSourceType.DEMO
    verification_status: EvidenceVerificationStatus = EvidenceVerificationStatus.UNVERIFIED
    source_url: str | None = None
    retrieved_at: str | None = None
    provider: str | None = None
    accession_number: str | None = None
    filing_date: str | None = None
    period_end_date: str | None = None
```

Rules:

```text
DEMO evidence supports demo workflows only.
AI_DRAFT cannot support buy/add.
AI_USER_VERIFIED may support evidence gate if confidence/source/date pass.
SEC_FILING and EARNINGS_RELEASE are high-quality if provider/source metadata is complete.
PRICE_PROVIDER evidence can support technical risk data, not fundamental thesis alone.
MACRO_PROVIDER and ENERGY_PROVIDER can support context only, not action alone.
```

---

## 5. Data quality snapshot

Add a pure core model like:

```python
@dataclass(frozen=True)
class DataQualitySnapshot:
    ticker: str
    mode: str  # demo | live | mixed
    financial_data_status: str
    price_data_status: str
    filing_data_status: str
    earnings_data_status: str
    valuation_data_status: str
    technical_data_status: str
    source_quality_score: float
    evidence_coverage_score: float
    missing_required_inputs: tuple[str, ...]
    stale_inputs: tuple[str, ...]
    provider_errors: tuple[str, ...]
```

This object should feed `DecisionInput` or a new decision context.

---

## 6. Source/evidence gate logic

Add pure helper functions:

```python
validate_action_evidence(evidence_items, mode) -> tuple[str, ...]
calculate_source_quality_score(evidence_items, provider_statuses) -> float
calculate_evidence_coverage_score(evidence_items, required_topics) -> float
is_evidence_action_supporting(evidence, mode) -> bool
```

Action-changing evidence must pass:

```text
has claim
has evidence detail
has source
has ISO source date
has disproof criteria
confidence is MEDIUM or HIGH
source_type is present
verification_status is USER_VERIFIED, PROVIDER_VERIFIED, or SYSTEM_VALIDATED
not AI_DRAFT
not LOW confidence
not price-only
not stale
```

Live mode adds stricter rule:

```text
In live mode, DEMO evidence cannot support buy/add.
```

Demo mode rule:

```text
DEMO evidence can demonstrate workflow states but must be labeled demo and not represented as live truth.
```

---

## 7. DecisionInput extension

Extend `DecisionInput` or add a companion context so the decision engine can see:

```text
data_quality_snapshot
source_quality_score
evidence_coverage_score
mode: demo | live | mixed
requires_live_data: bool
```

Do not break existing tests unnecessarily; adapt test helpers.

New hard gates:

```text
source_quality_score below threshold blocks buy/add
verified evidence coverage below threshold blocks buy/add
live mode with only demo evidence blocks buy/add
AI draft evidence blocks buy/add
provider failure for required data blocks action-changing live decision
```

---

## 8. Required source-quality tests

Add tests such as:

```text
AI_DRAFT evidence cannot support STARTER_ALLOWED.
AI_USER_VERIFIED evidence can support evidence gate but cannot override valuation/technical/risk gates.
DEMO evidence cannot support buy/add in live mode.
SEC_FILING evidence with source metadata can support evidence gate.
Missing source_type blocks action.
Missing source_date blocks action.
LOW confidence blocks action.
Price-only evidence blocks action.
Source quality below threshold blocks action.
Provider error blocks live action but not demo browsing.
Mixed mode produces caution/warning state.
```

---

## 9. Strategy integrity checks

Every future core change must preserve:

```text
No buy/add from score alone.
No buy/add from price drop alone.
No buy/add from AI draft alone.
No buy/add without thesis.
No buy/add without invalidation rule.
No buy/add when expected IRR below hurdle.
No buy/add when latest earnings weakens/breaks thesis.
No buy/add when technical trend is broken without stabilisation.
No buy/add when risk budget/cash/concentration blocks.
```

---

## 10. Implementation style

Keep this logic in `packages/qgear-core`.

Do not implement these gates only in:

```text
frontend components
FastAPI route conditionals
AI prompt wording
documentation only
```

The API and UI should explain the brain. They should not become the brain.

