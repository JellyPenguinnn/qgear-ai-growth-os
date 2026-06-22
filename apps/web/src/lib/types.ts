export type DecisionState =
  | "REJECTED"
  | "RESEARCH_CANDIDATE"
  | "WATCHLIST"
  | "APPROVED_THESIS"
  | "APPROVED_VALUATION_ZONE"
  | "TECHNICAL_WAIT"
  | "STARTER_ALLOWED"
  | "ADD_ALLOWED"
  | "HOLD"
  | "TRIM_CANDIDATE"
  | "EXIT_THESIS_BROKEN"
  | "BLOCKED_BY_RISK"
  | "NO_ACTION";

export type DemoCompany = {
  ticker: string;
  company_name: string;
  ai_layer: string;
  sector: string;
  industry: string;
  market_cap_usd_bn: number | null;
  evidence_summary: string;
  classification_confidence: "LOW" | "MEDIUM" | "HIGH";
  status: DecisionState;
  last_reviewed: string;
  score: {
    ai_relevance: number;
    business_quality: number;
    revenue_earnings_acceleration: number;
    earnings_guidance_revisions: number;
    valuation_expected_irr: number;
    technical_trend: number;
    portfolio_fit: number;
    total: number;
  };
  metrics: {
    revenue_growth_pct: number;
    gross_margin_pct: number;
    fcf_margin_pct: number;
    drawdown_from_high_pct: number;
    expected_irr_base_pct: number;
    technical_regime: string;
  };
  decision?: {
    reasons: string[];
    blocked_reasons: string[];
  };
  evidence?: EvidenceObject[];
};

export type EvidenceObject = {
  claim: string;
  evidence: string;
  source: string;
  source_date: string;
  confidence: "LOW" | "MEDIUM" | "HIGH";
  disproves_if: string;
};

export type DecisionResult = {
  ticker: string;
  state: DecisionState;
  score_total: number;
  reasons: string[];
  blocked_reasons: string[];
  drawdown_mode: string;
  action_allowed: boolean;
};

export type PositionSizing = {
  state: DecisionState;
  target_weight_pct: number;
  max_new_money: number;
  range_label: string;
  reasons: string[];
  drawdown_mode: string;
};

export type StockDetail = {
  company: DemoCompany;
  business_summary: string;
  ai_thesis: string;
  evidence_table: EvidenceObject[];
  financial_metrics?: Record<string, number>;
  latest_earnings_analysis?: {
    thesis_change: string;
    guidance_raised: boolean;
    ai_evidence_improved: boolean;
    margin_expanded: boolean;
    fcf_improved: boolean;
  };
  valuation_scenarios?: {
    bear_case_irr_pct: number;
    base_case_irr_pct: number;
    bull_case_irr_pct: number;
    hurdle_irr_pct: number;
  };
  technical_state?: {
    regime: string;
    relative_strength_pct: number;
    drawdown_from_high_pct: number;
  };
  approved_thesis?: {
    statement: string;
    must_go_right: string;
    breaks_if: string;
    key_metrics: string[];
    next_review_date: string;
    status: string;
  } | null;
  journal_entries?: Array<{ action: string; entry_date: string; evidence: string }>;
  decision_state: DecisionResult;
  position_sizing: PositionSizing;
  invalidation_rule: string;
};

export type UniverseResponse = {
  mode: string;
  not_recommendations: boolean;
  count: number;
  companies: DemoCompany[];
};

export type PortfolioSummary = {
  cash: number;
  total_equity: number;
  drawdown_pct: number;
  drawdown_mode: string;
  single_stock_concentration_pct: number;
  expected_portfolio_irr_pct: number;
  positions: Array<{
    id: number;
    ticker: string;
    shares: number;
    average_cost: number;
    current_price: number;
    market_value: number;
    unrealized_pl: number;
    position_weight_pct: number;
    status: string;
    thesis_status: string;
    next_review_date: string;
  }>;
};

export type ProviderStatusResponse = {
  mode: "demo" | "live" | string;
  live_network_required_for_tests: boolean;
  providers: Record<string, string>;
  safety: {
    auto_trading: string;
    margin: string;
    options: string;
    live_data_is_optional: boolean;
  };
};
