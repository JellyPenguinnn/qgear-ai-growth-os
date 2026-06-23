from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator

Benchmark = Literal["SPY", "QQQ", "XLK", "SMH"]
Currency = Literal["USD", "SGD", "MYR"]
Country = Literal["Singapore", "Malaysia", "Other"]
RiskStyle = Literal["CONSERVATIVE", "BALANCED", "AGGRESSIVE"]
BrokerMode = Literal["manual"]
DecisionAction = Literal[
    "REJECTED",
    "RESEARCH_CANDIDATE",
    "WATCHLIST",
    "APPROVED_THESIS",
    "APPROVED_VALUATION_ZONE",
    "TECHNICAL_WAIT",
    "STARTER_ALLOWED",
    "ADD_ALLOWED",
    "HOLD",
    "TRIM_CANDIDATE",
    "EXIT_THESIS_BROKEN",
    "BLOCKED_BY_RISK",
    "NO_ACTION",
]
ThesisStatus = Literal["NOT_STARTED", "DRAFT", "APPROVED", "NEEDS_REVIEW", "BROKEN"]
Confidence = Literal["LOW", "MEDIUM", "HIGH"]
MistakeCategory = Literal[
    "NONE",
    "THESIS_DRIFT",
    "EVIDENCE_GAP",
    "VALUATION_ERROR",
    "RISK_BUDGET_BREAK",
    "POSITION_SIZING_ERROR",
    "PROCESS_SKIP",
    "OTHER",
]


class OnboardingSettingsRequest(BaseModel):
    starting_capital: float = Field(default=10_000, gt=0)
    base_currency: Currency = "USD"
    country: Country = "Singapore"
    risk_style: RiskStyle = "BALANCED"
    target_cagr_low_pct: float = Field(default=18, ge=0, le=100)
    target_cagr_high_pct: float = Field(default=22, ge=0, le=100)
    hard_drawdown_limit_pct: float = Field(default=35, ge=1, le=100)
    cash_buffer_pct: float = Field(default=15, ge=0, le=100)
    max_single_stock_pct: float = Field(default=15, gt=0, le=100)
    benchmarks: list[Benchmark] = Field(default_factory=lambda: ["SPY", "QQQ", "XLK", "SMH"])
    broker_mode: BrokerMode = "manual"
    margin_enabled: bool = False
    options_enabled: bool = False
    auto_trading_enabled: bool = False

    @field_validator("target_cagr_high_pct")
    @classmethod
    def high_target_must_clear_low(cls, value: float, info) -> float:
        low = info.data.get("target_cagr_low_pct")
        if low is not None and value < low:
            raise ValueError("target_cagr_high_pct must be greater than or equal to target_cagr_low_pct")
        return value


class ThesisApprovalRequest(BaseModel):
    statement: str = Field(min_length=10)
    must_go_right: str = Field(min_length=10)
    breaks_if: str = Field(min_length=10)
    key_metrics: list[str] = Field(min_length=1)
    next_review_date: str


class PortfolioPositionRequest(BaseModel):
    ticker: str = Field(min_length=1, max_length=10)
    shares: float = Field(gt=0)
    average_cost: float = Field(ge=0)
    current_price: float = Field(ge=0)
    status: DecisionAction = "HOLD"
    thesis_status: ThesisStatus = "DRAFT"
    next_review_date: str = ""


class JournalEntryRequest(BaseModel):
    entry_date: str
    ticker: str = Field(min_length=1, max_length=10)
    action: DecisionAction
    price: float = Field(ge=0)
    position_size_pct: float = Field(ge=0, le=100)
    score: float = Field(ge=0, le=100)
    evidence: str = Field(min_length=10)
    thesis: str = Field(min_length=10)
    invalidation_rule: str = Field(min_length=10)
    expected_irr_pct: float = Field(ge=-100, le=200)
    future_review_date: str
    later_outcome: str = ""
    decision_outcome: str = ""
    mistake_category: MistakeCategory = "NONE"
    evidence_quality: Confidence = "MEDIUM"
    followed_system: bool = True
    later_review: str = ""
    process_score: float = Field(default=0, ge=0, le=100)


class EvidenceObjectRequest(BaseModel):
    claim: str = Field(min_length=10)
    evidence: str = Field(min_length=10)
    source: str = Field(min_length=3)
    source_date: str
    confidence: Confidence
    disproves_if: str = Field(min_length=10)

    @field_validator("source_date")
    @classmethod
    def source_date_must_be_iso(cls, value: str) -> str:
        date.fromisoformat(value)
        return value


class EarningsReviewRequest(BaseModel):
    fiscal_period: str = Field(min_length=2, max_length=20)
    report_date: str
    revenue_surprise_pct: float | None = Field(default=None, ge=-100, le=500)
    eps_surprise_pct: float | None = Field(default=None, ge=-500, le=500)
    guidance_raised: bool = False
    guidance_cut: bool = False
    guidance_cut_structural: bool = False
    revenue_growth_accelerated: bool = False
    ai_evidence_improved: bool = False
    segment_growth_improved: bool = False
    margin_expanded: bool = False
    margin_deteriorated: bool = False
    fcf_improved: bool = False
    fcf_deteriorated: bool = False
    management_tone: str = Field(default="neutral", min_length=3)
    score_change: float = Field(default=0, ge=-100, le=100)
    action_change: DecisionAction = "NO_ACTION"
    evidence: list[EvidenceObjectRequest] = Field(default_factory=list)

    @field_validator("report_date")
    @classmethod
    def report_date_must_be_iso(cls, value: str) -> str:
        date.fromisoformat(value)
        return value


class AIBaseRequest(BaseModel):
    external_ai_acknowledged: bool = False


class AIEvidenceExtractionRequest(AIBaseRequest):
    ticker: str = Field(min_length=1, max_length=10)
    source_title: str = Field(min_length=3)
    source_type: str = Field(min_length=3)
    source_date: str
    source_url_or_description: str = Field(min_length=3)
    pasted_text: str = Field(min_length=20)

    @field_validator("source_date")
    @classmethod
    def ai_source_date_must_be_iso(cls, value: str) -> str:
        date.fromisoformat(value)
        return value


class AIEarningsSummaryRequest(AIBaseRequest):
    ticker: str = Field(min_length=1, max_length=10)
    fiscal_period: str = Field(min_length=2, max_length=20)
    report_date: str
    earnings_text: str = Field(min_length=20)
    existing_thesis: str = ""
    existing_evidence: list[EvidenceObjectRequest] = Field(default_factory=list)

    @field_validator("report_date")
    @classmethod
    def ai_report_date_must_be_iso(cls, value: str) -> str:
        date.fromisoformat(value)
        return value


class AIThesisUpdateRequest(AIBaseRequest):
    ticker: str = Field(min_length=1, max_length=10)
    existing_thesis: str = Field(min_length=3)
    evidence: list[EvidenceObjectRequest] = Field(default_factory=list)
    next_review_date: str

    @field_validator("next_review_date")
    @classmethod
    def ai_next_review_date_must_be_iso(cls, value: str) -> str:
        date.fromisoformat(value)
        return value


class AIDecisionExplainRequest(AIBaseRequest):
    ticker: str = Field(min_length=1, max_length=10)
    decision_state: DecisionAction
    score: float = Field(ge=0, le=100)
    reasons: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    evidence: list[EvidenceObjectRequest] = Field(default_factory=list)


class ValuationAssumptionsRequest(BaseModel):
    revenue_cagr_pct: float = Field(ge=-100, le=200)
    gross_margin_pct: float = Field(ge=-100, le=100)
    operating_margin_pct: float = Field(ge=-100, le=100)
    fcf_margin_pct: float = Field(ge=-100, le=100)
    terminal_multiple: float = Field(ge=0, le=200)
    dilution_buyback_pct: float = Field(ge=-100, le=100)
    net_cash_debt_per_share: float = Field(ge=-10000, le=10000)


class ValuationCaseRequest(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    probability: float = Field(ge=0, le=1)
    current_price: float = Field(gt=0)
    target_price_3y: float = Field(ge=0)
    target_price_5y: float = Field(ge=0)
    notes: str = Field(min_length=3)
    assumptions: ValuationAssumptionsRequest
    evidence_refs: list[str] = Field(default_factory=list)


class ValuationUnderwriteRequest(BaseModel):
    ticker: str = Field(min_length=1, max_length=10)
    hurdle_irr_pct: float = Field(default=15, ge=0, le=100)
    cases: list[ValuationCaseRequest] = Field(min_length=1)
