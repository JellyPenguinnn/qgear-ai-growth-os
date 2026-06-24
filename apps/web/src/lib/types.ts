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
  source_type?: string;
  verification_status?: string;
  source_url?: string | null;
  retrieved_at?: string | null;
  provider?: string | null;
  accession_number?: string | null;
  filing_date?: string | null;
  period_end_date?: string | null;
};

export type AIDraftResponse = {
  task: string;
  draft_status: "disabled" | "draft" | "rejected" | "error";
  provider_metadata: {
    provider: string;
    mode: string;
    model: string | null;
    status: string;
    draft_only: boolean;
    external_call_performed: boolean;
    error: string | null;
  };
  draft: Record<string, unknown>;
  evidence: EvidenceObject[];
  warnings: string[];
  validation_errors: string[];
  requires_user_verification: boolean;
  mutates_decision_state: boolean;
  disclaimer: string;
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

export type ValuationAssumptions = {
  revenue_cagr_pct: number;
  gross_margin_pct: number;
  operating_margin_pct: number;
  fcf_margin_pct: number;
  terminal_multiple: number;
  dilution_buyback_pct: number;
  net_cash_debt_per_share: number;
};

export type ValuationCase = {
  name: string;
  probability: number;
  current_price: number;
  target_price_3y: number;
  target_price_5y: number;
  notes: string;
  assumptions: ValuationAssumptions;
  evidence_refs: string[];
};

export type ValuationSummary = {
  cases: ValuationCase[];
  probability_weighted_irr_3y_pct: number;
  probability_weighted_irr_5y_pct: number;
  hurdle_irr_pct: number;
  clears_hurdle: boolean;
};

export type ValuationSensitivityCell = {
  terminal_multiple_delta_pct: number;
  fcf_margin_delta_pct: number;
  target_price_5y: number;
  expected_irr_5y_pct: number;
};

export type ValuationResponse = {
  ticker: string;
  company_name: string;
  mode: string;
  summary: ValuationSummary;
  case_irrs: Array<{
    name: string;
    irr_3y_pct: number;
    irr_5y_pct: number;
  }>;
  sensitivity_table: ValuationSensitivityCell[];
  valuation_notes: string[];
  evidence_links: string[];
  decision_gate: {
    valuation_clears_hurdle: boolean;
    hurdle_irr_pct: number;
    note: string;
  };
  trade_instruction: false;
};

export type UniverseResponse = {
  mode: string;
  not_recommendations: boolean;
  count: number;
  companies: DemoCompany[];
};

export type PortfolioSummary = {
  mode: string;
  manual_only: boolean;
  cash: number;
  cash_pct: number;
  total_equity: number;
  drawdown_pct: number;
  drawdown_mode: string;
  single_stock_concentration_pct: number;
  ai_layer_concentration: Record<string, number>;
  expected_portfolio_irr_pct: number;
  expected_irr_distribution: {
    min_pct: number;
    max_pct: number;
    weighted_pct: number;
    note: string;
  };
  benchmark_comparison: Array<{
    benchmark: string;
    status: string;
    total_return_pct: number | null;
    relative_return_pct: number | null;
    note: string;
  }>;
  benchmark_comparison_placeholders: Record<string, string>;
  concentration_risks: Array<{
    ticker: string | null;
    severity: string;
    message: string;
    trade_instruction: false;
  }>;
  blocked_adds: Array<{
    ticker: string;
    reason: string;
    state: string;
    trade_instruction: false;
  }>;
  review_calendar: Array<{
    ticker: string;
    next_review_date: string;
    status: string;
    thesis_status: string;
    review_type: string;
    trade_instruction: false;
  }>;
  as_of: string;
  risk_note: string;
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
    ai_layer?: string;
    expected_irr_base_pct?: number;
  }>;
};

export type ProviderStatusResponse = {
  mode: "demo" | "live" | string;
  live_network_required_for_tests: boolean;
  providers: Record<string, string>;
  ai: AIStatusResponse;
  safety: {
    auto_trading: string;
    margin: string;
    options: string;
    live_data_is_optional: boolean;
  };
};

export type ProviderMetadata = {
  provider: string;
  status: string;
  source_url: string;
  source_name: string;
  retrieved_at: string;
  cached: boolean;
  source_date: string | null;
  as_of_date: string | null;
  cache_written_at: string | null;
  cache_key: string | null;
  error: string | null;
  mode: string | null;
};

export type DataQualityResponse = {
  ticker: string;
  status: string;
  data_quality: {
    ticker: string;
    mode: string;
    financial_data_status: string;
    price_data_status: string;
    filing_data_status: string;
    earnings_data_status: string;
    valuation_data_status: string;
    technical_data_status: string;
    source_quality_score: number;
    evidence_coverage_score: number;
    missing_required_inputs: string[];
    stale_inputs: string[];
    provider_errors: string[];
  };
  can_support_action_in_live_mode: boolean;
  reason: string;
  source_metadata: ProviderMetadata | null;
  not_trade_instruction: boolean;
};

export type DataHealthResponse = {
  mode: string;
  status: string;
  provider_status: ProviderStatusResponse;
  sections: Array<{
    name: string;
    status: string;
    can_support_action: boolean;
    note: string;
  }>;
  missing_keys: Record<string, string | null>;
  default_fred_series: string[];
  what_can_support_action: string[];
  review_only_data: string[];
  not_trade_instruction: boolean;
};

export type AIStatusResponse = {
  provider_metadata: {
    provider: string;
    mode: string;
    model: string | null;
    status: string;
    draft_only: boolean;
    external_call_performed: boolean;
    error: string | null;
  };
  ai_enabled: boolean;
  requires_explicit_request: boolean;
  requires_external_ai_acknowledgement: boolean;
  draft_only: boolean;
  mutates_decision_state: boolean;
  external_upload_policy: string;
};

export type SourceMetadata = {
  source: string;
  source_date: string;
  confidence: "LOW" | "MEDIUM" | "HIGH";
  disproves_if: string;
};

export type PipelineItem = {
  ticker: string;
  company_name: string;
  ai_layer: string;
  score: number;
  decision_state: DecisionState;
  action_allowed: boolean;
  trade_instruction: false;
  primary_reason: string;
  primary_blocker: string;
  reasons: string[];
  blockers: string[];
  review_flags: string[];
  next_task: string;
  evidence_summary: string;
  evidence: EvidenceObject;
  source_metadata: SourceMetadata;
  last_reviewed: string;
};

export type PipelineState = {
  state: DecisionState;
  label: string;
  description: string;
  count: number;
  items: PipelineItem[];
};

export type PipelineResponse = {
  mode: string;
  as_of: string;
  default_stance: string;
  not_trade_instructions: boolean;
  summary: {
    total: number;
    review_queue_count: number;
    action_allowed_count: number;
    blocked_count: number;
  };
  states: PipelineState[];
  review_queue: PipelineItem[];
};

export type TodayResponse = {
  mode: string;
  as_of: string;
  title: string;
  default_stance: string;
  stance_reason: string;
  not_trade_instructions: boolean;
  metrics: {
    universe_count: number;
    review_queue_count: number;
    action_allowed_count: number;
    blocked_count: number;
    drawdown_pct: number;
    drawdown_mode: string;
    total_equity: number;
  };
  review_queue: PipelineItem[];
  pipeline_snapshot: Array<{
    state: DecisionState;
    label: string;
    count: number;
    description: string;
  }>;
  top_rankings: Array<{
    ticker: string;
    company_name: string;
    ai_layer: string;
    score: number;
    decision_state: DecisionState;
    primary_reason: string;
    primary_blocker: string;
    trade_instruction: false;
  }>;
  alerts: Array<{
    type: string;
    severity: string;
    ticker?: string | null;
    message: string;
    trade_instruction: false;
  }>;
  provider_status: ProviderStatusResponse;
  safety: {
    auto_trading: string;
    margin: string;
    options: string;
    daily_stance: string;
  };
};
