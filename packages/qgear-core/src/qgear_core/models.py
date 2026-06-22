from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from qgear_core.enums import (
    AILayer,
    BaseCurrency,
    Confidence,
    Country,
    DecisionState,
    DrawdownMode,
    EarningsThesisChange,
    RiskStyle,
    TechnicalRegime,
    ThesisStatus,
)


@dataclass(frozen=True)
class Evidence:
    claim: str
    evidence: str
    source: str
    source_date: str
    confidence: Confidence
    disproves_if: str


@dataclass(frozen=True)
class Thesis:
    ticker: str
    statement: str
    must_go_right: str
    breaks_if: str
    key_metrics: tuple[str, ...]
    next_review_date: str
    status: ThesisStatus = ThesisStatus.DRAFT

    @property
    def is_approved(self) -> bool:
        return self.status == ThesisStatus.APPROVED and bool(self.breaks_if.strip())


@dataclass(frozen=True)
class StrategySettings:
    starting_capital: float = 10_000
    base_currency: BaseCurrency = BaseCurrency.USD
    country: Country = Country.SINGAPORE
    risk_style: RiskStyle = RiskStyle.BALANCED
    target_cagr_low_pct: float = 18
    target_cagr_high_pct: float = 22
    hard_drawdown_limit_pct: float = 35
    cash_buffer_pct: float = 15
    max_single_stock_pct: float = 15
    benchmarks: tuple[str, ...] = ("SPY", "QQQ", "XLK", "SMH")
    margin_enabled: bool = False
    options_enabled: bool = False
    auto_trading_enabled: bool = False


@dataclass(frozen=True)
class ScoreBreakdown:
    ai_relevance: float
    business_quality: float
    revenue_earnings_acceleration: float
    earnings_guidance_revisions: float
    valuation_expected_irr: float
    technical_trend: float
    portfolio_fit: float

    @property
    def total(self) -> float:
        return round(
            self.ai_relevance
            + self.business_quality
            + self.revenue_earnings_acceleration
            + self.earnings_guidance_revisions
            + self.valuation_expected_irr
            + self.technical_trend
            + self.portfolio_fit,
            2,
        )

    def as_dict(self) -> dict[str, float]:
        return {
            "ai_relevance": self.ai_relevance,
            "business_quality": self.business_quality,
            "revenue_earnings_acceleration": self.revenue_earnings_acceleration,
            "earnings_guidance_revisions": self.earnings_guidance_revisions,
            "valuation_expected_irr": self.valuation_expected_irr,
            "technical_trend": self.technical_trend,
            "portfolio_fit": self.portfolio_fit,
            "total": self.total,
        }


@dataclass(frozen=True)
class StockMetrics:
    ticker: str
    ai_layer: AILayer
    classification_confidence: Confidence
    revenue_growth_pct: float
    revenue_growth_acceleration_pct: float
    gross_margin_pct: float
    operating_margin_pct: float
    fcf_margin_pct: float
    net_debt_to_ebitda: float
    roic_pct: float
    expected_irr_base_pct: float
    relative_strength_pct: float
    drawdown_from_high_pct: float
    technical_regime: TechnicalRegime
    latest_earnings_change: EarningsThesisChange
    guidance_raised: bool = False
    ai_evidence_improved: bool = False
    margin_expanded: bool = False
    fcf_improved: bool = False
    red_flag_count: int = 0


@dataclass(frozen=True)
class PortfolioContext:
    total_equity: float = 10_000
    cash: float = 1_500
    portfolio_drawdown_pct: float = 0
    current_position_weight_pct: float = 0
    current_position_value: float = 0
    ai_layer_weight_pct: float = 0
    max_single_stock_pct: float = 15
    cash_buffer_pct: float = 15
    hard_drawdown_limit_pct: float = 35
    owned: bool = False

    @property
    def cash_pct(self) -> float:
        if self.total_equity <= 0:
            return 0
        return self.cash / self.total_equity * 100


@dataclass(frozen=True)
class DecisionInput:
    ticker: str
    score: ScoreBreakdown
    thesis_approved: bool
    invalidation_rule_present: bool
    ai_relevance_proven: bool
    latest_earnings_change: EarningsThesisChange
    expected_irr_base_pct: float
    hurdle_irr_pct: float
    technical_regime: TechnicalRegime
    evidence_age_days: int
    portfolio: PortfolioContext
    fresh_positive_evidence: bool
    price_change_pct: float = 0
    add_requested: bool = False
    guidance_cut_structural: bool = False
    margin_deterioration_unexplained: bool = False
    red_flags: tuple[str, ...] = field(default_factory=tuple)
    positive_evidence: tuple[Evidence, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class DecisionResult:
    ticker: str
    state: DecisionState
    score_total: float
    reasons: tuple[str, ...]
    blocked_reasons: tuple[str, ...] = field(default_factory=tuple)
    drawdown_mode: DrawdownMode = DrawdownMode.NORMAL
    action_allowed: bool = False

    @property
    def is_buy_or_add(self) -> bool:
        return self.state in {
            DecisionState.STARTER_ALLOWED,
            DecisionState.ADD_ALLOWED,
        }


@dataclass(frozen=True)
class PositionSizeRecommendation:
    state: DecisionState
    target_weight_pct: float
    max_new_money: float
    range_label: str
    reasons: tuple[str, ...]
    drawdown_mode: DrawdownMode


@dataclass(frozen=True)
class UniverseCompany:
    ticker: str
    company_name: str
    ai_layer: AILayer
    sector: str
    industry: str
    market_cap_usd_bn: float | None
    evidence_summary: str
    classification_confidence: Confidence
    status: DecisionState
    last_reviewed: str
    evidence: tuple[Evidence, ...]
    metrics: StockMetrics
    score: ScoreBreakdown
    decision: DecisionResult
