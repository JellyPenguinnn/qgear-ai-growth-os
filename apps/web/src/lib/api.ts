import { fallbackPortfolio, fallbackUniverse } from "./demo-data";
import type { DemoCompany, PortfolioSummary, ProviderStatusResponse, StockDetail, UniverseResponse } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

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
  const fallback: StockDetail = {
    company: fallbackCompany,
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
      state: fallbackCompany.status,
      score_total: fallbackCompany.score.total,
      reasons: fallbackCompany.decision?.reasons ?? [],
      blocked_reasons: fallbackCompany.decision?.blocked_reasons ?? [],
      drawdown_mode: "NORMAL",
      action_allowed: ["STARTER_ALLOWED", "ADD_ALLOWED"].includes(fallbackCompany.status)
    },
    position_sizing: {
      state: fallbackCompany.status,
      target_weight_pct: fallbackCompany.status === "STARTER_ALLOWED" ? 5 : fallbackCompany.status === "ADD_ALLOWED" ? 8 : 0,
      max_new_money: fallbackCompany.status === "STARTER_ALLOWED" ? 500 : fallbackCompany.status === "ADD_ALLOWED" ? 800 : 0,
      range_label: fallbackCompany.status === "STARTER_ALLOWED" ? "Starter: 2.5-5%" : fallbackCompany.status === "ADD_ALLOWED" ? "Normal: 5-8%" : "Research only: 0%",
      reasons: ["Fallback sizing is illustrative; API/core sizing is used when available."],
      drawdown_mode: "NORMAL"
    },
    invalidation_rule: ""
  };

  return getJson<StockDetail>(`/universe/${ticker}`, fallback);
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
    safety: {
      auto_trading: "disabled",
      margin: "disabled",
      options: "disabled_in_mvp",
      live_data_is_optional: true
    }
  });
}

export { API_URL };
