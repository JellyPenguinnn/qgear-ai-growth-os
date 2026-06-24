import { fallbackPortfolio, fallbackUniverse } from "./demo-data";
import type {
  DecisionState,
  DataHealthResponse,
  DataQualityResponse,
  DemoCompany,
  PipelineItem,
  PipelineResponse,
  PortfolioSummary,
  ProviderStatusResponse,
  StockDetail,
  TodayResponse,
  UniverseResponse,
  ValuationResponse
} from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

const fallbackAIStatus = {
  provider_metadata: {
    provider: "noop",
    mode: "none",
    model: null,
    status: "disabled",
    draft_only: true,
    external_call_performed: false,
    error: null
  },
  ai_enabled: false,
  requires_explicit_request: true,
  requires_external_ai_acknowledgement: false,
  draft_only: true,
  mutates_decision_state: false,
  external_upload_policy: "No local portfolio, journal, thesis, or source text is sent externally unless the user submits it in a specific AI request."
};

export async function getJson<T>(path: string, fallback: T): Promise<T> {
  try {
    const response = await fetch(`${API_URL}${path}`, { cache: "no-store" });
    if (!response.ok) {
      return fallback;
    }
    return (await response.json()) as T;
  } catch {
    return fallback;
  }
}

export async function getUniverse(): Promise<UniverseResponse> {
  return getJson<UniverseResponse>("/universe", fallbackUniverse);
}

function fallbackPipelineItem(company: DemoCompany): PipelineItem {
  const fallbackActionState = ["STARTER_ALLOWED", "ADD_ALLOWED"].includes(company.status);
  return {
    ticker: company.ticker,
    company_name: company.company_name,
    ai_layer: company.ai_layer,
    score: company.score.total,
    decision_state: fallbackActionState ? "WATCHLIST" : company.status,
    action_allowed: false,
    trade_instruction: false,
    primary_reason: "Frontend fallback data is review-only; API/core gate verification is required.",
    primary_blocker: fallbackActionState ? "Fallback mode cannot confirm approved thesis, invalidation rule, fresh evidence, valuation, technical regime, and risk budget." : company.decision?.blocked_reasons?.[0] ?? "",
    reasons: ["Frontend fallback data is research-only and cannot create action permission."],
    blockers: fallbackActionState
      ? ["API/core decision context is required before any starter/add state can be treated as actionable."]
      : company.decision?.blocked_reasons ?? [],
    review_flags: fallbackActionState ? ["API_CONTEXT_REQUIRED", "JOURNAL_REVIEW_REQUIRED"] : company.decision?.blocked_reasons?.length ? ["REVIEW_REQUIRED"] : [],
    next_task: "Reconnect the API or review the stock workbench before changing any decision state.",
    evidence_summary: company.evidence_summary,
    evidence: {
      claim: "AI relevance requires measurable business evidence.",
      evidence: company.evidence_summary,
      source: "Q-GEAR frontend fallback demo data",
      source_date: company.last_reviewed,
      confidence: company.classification_confidence,
      disproves_if: "Future filings, earnings releases, segment data, guidance, or margins contradict the claim."
    },
    source_metadata: {
      source: "Q-GEAR frontend fallback demo data",
      source_date: company.last_reviewed,
      confidence: company.classification_confidence,
      disproves_if: "Future filings, earnings releases, segment data, guidance, or margins contradict the claim."
    },
    last_reviewed: company.last_reviewed
  };
}

function buildFallbackPipeline(): PipelineResponse {
  const items = fallbackUniverse.companies.map(fallbackPipelineItem);
  const stateOrder: DecisionState[] = [
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
    "NO_ACTION"
  ];
  const states = stateOrder.map((state) => ({
    state,
    label: state.replaceAll("_", " ").toLowerCase().replace(/\b\w/g, (letter) => letter.toUpperCase()),
    description: "Fallback grouping from local demo data. API/core context is required for gate-level interpretation.",
    count: items.filter((item) => item.decision_state === state).length,
    items: items.filter((item) => item.decision_state === state)
  }));
  const reviewQueue = items.filter((item) => item.blockers.length || item.review_flags.length).slice(0, 8);

  return {
    mode: "frontend_fallback",
    as_of: "2026-06-22",
    default_stance: "No action justified today unless evidence changed and every hard gate clears.",
    not_trade_instructions: true,
    summary: {
      total: items.length,
      review_queue_count: reviewQueue.length,
      action_allowed_count: 0,
      blocked_count: items.filter((item) => item.blockers.length).length
    },
    states,
    review_queue: reviewQueue
  };
}

function buildFallbackToday(): TodayResponse {
  const pipeline = buildFallbackPipeline();
  return {
    mode: "frontend_fallback",
    as_of: pipeline.as_of,
    title: "Today",
    default_stance: pipeline.default_stance,
    stance_reason: "Fallback mode cannot verify core gates. Treat every item as a research prompt until the API is available.",
    not_trade_instructions: true,
    metrics: {
      universe_count: fallbackUniverse.count,
      review_queue_count: pipeline.summary.review_queue_count,
      action_allowed_count: 0,
      blocked_count: pipeline.summary.blocked_count,
      drawdown_pct: fallbackPortfolio.drawdown_pct,
      drawdown_mode: fallbackPortfolio.drawdown_mode,
      total_equity: fallbackPortfolio.total_equity
    },
    review_queue: pipeline.review_queue,
    pipeline_snapshot: pipeline.states
      .filter((state) => state.count > 0)
      .map((state) => ({ state: state.state, label: state.label, count: state.count, description: state.description })),
    top_rankings: [...fallbackUniverse.companies]
      .sort((a, b) => b.score.total - a.score.total)
      .slice(0, 8)
      .map((company) => ({
        ticker: company.ticker,
        company_name: company.company_name,
        ai_layer: company.ai_layer,
        score: company.score.total,
        decision_state: ["STARTER_ALLOWED", "ADD_ALLOWED"].includes(company.status) ? "WATCHLIST" : company.status,
        primary_reason: "Fallback demo ranking only. High score is not an action.",
        primary_blocker: "API/core gate verification is unavailable.",
        trade_instruction: false
      })),
    alerts: [
      {
        type: "API_CONTEXT_REQUIRED",
        severity: "medium",
        message: "Frontend fallback mode is active; review prompts are not trade instructions.",
        trade_instruction: false
      }
    ],
    provider_status: {
      mode: "frontend_fallback",
      live_network_required_for_tests: false,
      providers: {
        company_facts: "frontend fallback",
        filings: "frontend fallback",
        prices: "frontend fallback",
        benchmarks: "frontend fallback"
      },
      ai: fallbackAIStatus,
      safety: {
        auto_trading: "disabled",
        margin: "disabled",
        options: "disabled_in_mvp",
        live_data_is_optional: true
      }
    },
    safety: {
      auto_trading: "disabled",
      margin: "disabled",
      options: "disabled_in_mvp",
      daily_stance: "review_only"
    }
  };
}

export async function getToday(): Promise<TodayResponse> {
  return getJson<TodayResponse>("/today", buildFallbackToday());
}

function buildFallbackDataHealth(): DataHealthResponse {
  const providerStatus = buildFallbackToday().provider_status;
  return {
    mode: "frontend_fallback",
    status: "review_only",
    provider_status: providerStatus,
    sections: [
      {
        name: "Frontend fallback",
        status: "API unavailable",
        can_support_action: false,
        note: "Fallback data cannot support action-changing decisions."
      }
    ],
    missing_keys: {},
    default_fred_series: ["FEDFUNDS", "DGS10", "DGS2", "CPIAUCSL", "UNRATE"],
    what_can_support_action: ["Reconnect the local API and verify provider/user evidence before action-changing decisions."],
    review_only_data: ["Frontend fallback data", "AI drafts", "Price-only context"],
    not_trade_instruction: true
  };
}

export async function getDataHealth(): Promise<DataHealthResponse> {
  return getJson<DataHealthResponse>("/data/health", buildFallbackDataHealth());
}

export async function getDataQuality(ticker: string): Promise<DataQualityResponse | null> {
  const fallbackCompany = fallbackUniverse.companies.find((company) => company.ticker === ticker.toUpperCase()) ?? null;
  if (!fallbackCompany) {
    return null;
  }
  return getJson<DataQualityResponse>(`/data/quality/${ticker}`, {
    ticker: fallbackCompany.ticker,
    status: "frontend_fallback",
    data_quality: {
      ticker: fallbackCompany.ticker,
      mode: "frontend_fallback",
      financial_data_status: "missing",
      price_data_status: "missing",
      filing_data_status: "missing",
      earnings_data_status: "demo",
      valuation_data_status: "demo",
      technical_data_status: "demo",
      source_quality_score: 0,
      evidence_coverage_score: 0,
      missing_required_inputs: ["api_context"],
      stale_inputs: [],
      provider_errors: ["Local API unavailable."]
    },
    can_support_action_in_live_mode: false,
    reason: "Frontend fallback data cannot support action-changing decisions.",
    source_metadata: null,
    not_trade_instruction: true
  });
}

export async function getPipeline(): Promise<PipelineResponse> {
  return getJson<PipelineResponse>("/pipeline", buildFallbackPipeline());
}

export async function getCompany(ticker: string): Promise<DemoCompany | null> {
  const fallback = fallbackUniverse.companies.find((company) => company.ticker === ticker.toUpperCase()) ?? null;
  const detail = await getJson<{ company?: DemoCompany } | DemoCompany | null>(`/universe/${ticker}`, fallback);
  if (!detail) {
    return null;
  }
  if ("company" in detail && detail.company) {
    return detail.company;
  }
  return detail as DemoCompany;
}

export async function getStockDetail(ticker: string): Promise<StockDetail | null> {
  const fallbackCompany = fallbackUniverse.companies.find((company) => company.ticker === ticker.toUpperCase()) ?? null;
  if (!fallbackCompany) {
    return null;
  }
  const fallbackState: DecisionState = ["STARTER_ALLOWED", "ADD_ALLOWED"].includes(fallbackCompany.status) ? "WATCHLIST" : fallbackCompany.status;
  const fallbackBlockers = [
    "Frontend fallback mode cannot confirm an approved thesis.",
    "Frontend fallback mode cannot confirm an invalidation rule.",
    "API/core decision context is required before any starter/add state can be treated as actionable."
  ];
  const fallback: StockDetail = {
    company: {
      ...fallbackCompany,
      status: fallbackState,
      decision: {
        reasons: ["Fallback demo data is research-only; action permission requires API/core gate verification."],
        blocked_reasons: fallbackBlockers
      }
    },
    business_summary: `${fallbackCompany.company_name} is shown from frontend fallback demo data.`,
    ai_thesis: fallbackCompany.evidence_summary,
    evidence_table: [
      {
        claim: "AI relevance requires measurable business evidence.",
        evidence: fallbackCompany.evidence_summary,
        source: "Q-GEAR frontend fallback demo data",
        source_date: "2026-06-22",
        confidence: fallbackCompany.classification_confidence,
        disproves_if: "Future filings, segment data, guidance, or margins contradict the claim."
      }
    ],
    financial_metrics: {
      revenue_growth_pct: fallbackCompany.metrics.revenue_growth_pct,
      gross_margin_pct: fallbackCompany.metrics.gross_margin_pct,
      fcf_margin_pct: fallbackCompany.metrics.fcf_margin_pct,
      expected_irr_base_pct: fallbackCompany.metrics.expected_irr_base_pct
    },
    latest_earnings_analysis: {
      thesis_change: "UNCHANGED",
      guidance_raised: false,
      ai_evidence_improved: false,
      margin_expanded: false,
      fcf_improved: false
    },
    valuation_scenarios: {
      bear_case_irr_pct: fallbackCompany.metrics.expected_irr_base_pct - 8,
      base_case_irr_pct: fallbackCompany.metrics.expected_irr_base_pct,
      bull_case_irr_pct: fallbackCompany.metrics.expected_irr_base_pct + 10,
      hurdle_irr_pct: 15
    },
    technical_state: {
      regime: fallbackCompany.metrics.technical_regime,
      relative_strength_pct: 0,
      drawdown_from_high_pct: fallbackCompany.metrics.drawdown_from_high_pct
    },
    approved_thesis: null,
    journal_entries: [],
    decision_state: {
      ticker: fallbackCompany.ticker,
      state: fallbackState,
      score_total: fallbackCompany.score.total,
      reasons: ["Fallback demo data is research-only; action permission requires API/core gate verification."],
      blocked_reasons: fallbackBlockers,
      drawdown_mode: "NORMAL",
      action_allowed: false
    },
    position_sizing: {
      state: fallbackState,
      target_weight_pct: 0,
      max_new_money: 0,
      range_label: "Research only: 0%",
      reasons: ["Fallback mode blocks new money until API/core thesis, invalidation, evidence, valuation, technical, and risk gates are verified."],
      drawdown_mode: "NORMAL"
    },
    invalidation_rule: ""
  };

  return getJson<StockDetail>(`/universe/${ticker}`, fallback);
}

function fallbackValuation(ticker: string): ValuationResponse | null {
  const company = fallbackUniverse.companies.find((item) => item.ticker === ticker.toUpperCase()) ?? null;
  if (!company) {
    return null;
  }
  const currentPrice = 100;
  const baseIrr = company.metrics.expected_irr_base_pct;
  const target = (irr: number, years: number) => Number((currentPrice * (1 + irr / 100) ** years).toFixed(2));
  const cases = [
    {
      name: "bear",
      probability: 0.25,
      current_price: currentPrice,
      target_price_3y: target(baseIrr - 8, 3),
      target_price_5y: target(baseIrr - 8, 5),
      notes: "Fallback bear case. API/core valuation should be used for decisions.",
      assumptions: {
        revenue_cagr_pct: company.metrics.revenue_growth_pct - 12,
        gross_margin_pct: company.metrics.gross_margin_pct - 4,
        operating_margin_pct: 0,
        fcf_margin_pct: company.metrics.fcf_margin_pct - 5,
        terminal_multiple: 18,
        dilution_buyback_pct: -2,
        net_cash_debt_per_share: 0
      },
      evidence_refs: ["Frontend fallback valuation"]
    },
    {
      name: "base",
      probability: 0.5,
      current_price: currentPrice,
      target_price_3y: target(baseIrr, 3),
      target_price_5y: target(baseIrr, 5),
      notes: "Fallback base case. Score alone never creates action.",
      assumptions: {
        revenue_cagr_pct: company.metrics.revenue_growth_pct,
        gross_margin_pct: company.metrics.gross_margin_pct,
        operating_margin_pct: 0,
        fcf_margin_pct: company.metrics.fcf_margin_pct,
        terminal_multiple: 25,
        dilution_buyback_pct: 0,
        net_cash_debt_per_share: 0
      },
      evidence_refs: ["Frontend fallback valuation"]
    },
    {
      name: "bull",
      probability: 0.25,
      current_price: currentPrice,
      target_price_3y: target(baseIrr + 8, 3),
      target_price_5y: target(baseIrr + 8, 5),
      notes: "Fallback bull case. Fresh evidence and risk gates still decide action.",
      assumptions: {
        revenue_cagr_pct: company.metrics.revenue_growth_pct + 8,
        gross_margin_pct: company.metrics.gross_margin_pct + 3,
        operating_margin_pct: 0,
        fcf_margin_pct: company.metrics.fcf_margin_pct + 4,
        terminal_multiple: 32,
        dilution_buyback_pct: 1,
        net_cash_debt_per_share: 0
      },
      evidence_refs: ["Frontend fallback valuation"]
    }
  ];
  return {
    ticker: company.ticker,
    company_name: company.company_name,
    mode: "frontend_fallback",
    summary: {
      cases,
      probability_weighted_irr_3y_pct: baseIrr,
      probability_weighted_irr_5y_pct: baseIrr,
      hurdle_irr_pct: 15,
      clears_hurdle: baseIrr >= 15
    },
    case_irrs: cases.map((caseItem) => ({ name: caseItem.name, irr_3y_pct: baseIrr, irr_5y_pct: baseIrr })),
    sensitivity_table: [
      { terminal_multiple_delta_pct: -20, fcf_margin_delta_pct: -3, target_price_5y: target(baseIrr - 4, 5), expected_irr_5y_pct: baseIrr - 4 },
      { terminal_multiple_delta_pct: 0, fcf_margin_delta_pct: 0, target_price_5y: target(baseIrr, 5), expected_irr_5y_pct: baseIrr },
      { terminal_multiple_delta_pct: 20, fcf_margin_delta_pct: 3, target_price_5y: target(baseIrr + 4, 5), expected_irr_5y_pct: baseIrr + 4 }
    ],
    valuation_notes: [
      "Frontend fallback valuation is review-only.",
      "Valuation can support or block action, but cannot create buy/add without thesis, evidence, technical, and risk gates."
    ],
    evidence_links: ["Frontend fallback valuation"],
    decision_gate: {
      valuation_clears_hurdle: baseIrr >= 15,
      hurdle_irr_pct: 15,
      note: "Valuation can support or block action, but cannot create buy/add without thesis, evidence, technical, and risk gates."
    },
    trade_instruction: false
  };
}

export async function getValuation(ticker: string): Promise<ValuationResponse | null> {
  const fallback = fallbackValuation(ticker);
  if (!fallback) {
    return null;
  }
  return getJson<ValuationResponse>(`/valuation/${ticker}`, fallback);
}

export async function getPortfolio(): Promise<PortfolioSummary> {
  return getJson<PortfolioSummary>("/portfolio", fallbackPortfolio);
}

export async function getProviderStatus(): Promise<ProviderStatusResponse> {
  return getJson<ProviderStatusResponse>("/providers/status", {
    mode: "frontend_fallback",
    live_network_required_for_tests: false,
    providers: {
      company_facts: "frontend fallback",
      filings: "frontend fallback",
      prices: "frontend fallback",
      benchmarks: "frontend fallback"
    },
    ai: fallbackAIStatus,
    safety: {
      auto_trading: "disabled",
      margin: "disabled",
      options: "disabled_in_mvp",
      live_data_is_optional: true
    }
  });
}

export { API_URL };
