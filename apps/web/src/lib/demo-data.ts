import type { DemoCompany, PortfolioSummary, UniverseResponse } from "./types";

const score = (
  total: number,
  status: DemoCompany["status"],
  technical = "STABILISING",
  expectedIrr = 16,
  revenueGrowth = 18,
  grossMargin = 55,
  fcfMargin = 20
): Pick<DemoCompany, "score" | "metrics" | "status"> => ({
  status,
  score: {
    ai_relevance: Math.round(total * 0.12 * 10) / 10,
    business_quality: Math.round(total * 0.18 * 10) / 10,
    revenue_earnings_acceleration: Math.round(total * 0.18 * 10) / 10,
    earnings_guidance_revisions: Math.round(total * 0.17 * 10) / 10,
    valuation_expected_irr: Math.round(total * 0.15 * 10) / 10,
    technical_trend: Math.round(total * 0.1 * 10) / 10,
    portfolio_fit: Math.round(total * 0.1 * 10) / 10,
    total
  },
  metrics: {
    revenue_growth_pct: revenueGrowth,
    gross_margin_pct: grossMargin,
    fcf_margin_pct: fcfMargin,
    drawdown_from_high_pct: technical === "BROKEN" ? 42 : 14,
    expected_irr_base_pct: expectedIrr,
    technical_regime: technical
  }
});

const company = (
  ticker: string,
  company_name: string,
  ai_layer: string,
  sector: string,
  industry: string,
  market_cap_usd_bn: number | null,
  evidence_summary: string,
  classification_confidence: DemoCompany["classification_confidence"],
  statusPack: Pick<DemoCompany, "score" | "metrics" | "status">
): DemoCompany => ({
  ticker,
  company_name,
  ai_layer,
  sector,
  industry,
  market_cap_usd_bn,
  evidence_summary,
  classification_confidence,
  last_reviewed: "2026-06-22",
  ...statusPack,
  decision: {
    reasons: ["Demo mode: score is descriptive; hard gates and risk budget decide action."],
    blocked_reasons: []
  }
});

export const demoCompanies: DemoCompany[] = [
  company("NVDA", "NVIDIA", "COMPUTE_ACCELERATORS", "Information Technology", "Semiconductors", 3200, "Data-center GPU demand and accelerated computing revenue are tracked as measurable AI evidence.", "HIGH", score(91, "STARTER_ALLOWED", "STABILISING", 17, 78, 76, 46)),
  company("AMD", "Advanced Micro Devices", "COMPUTE_ACCELERATORS", "Information Technology", "Semiconductors", 260, "Accelerator ramp evidence is monitored, with margin and guidance proof still required.", "MEDIUM", score(63, "WATCHLIST", "WEAKENING", 18, 18, 51, 19)),
  company("AVGO", "Broadcom", "CUSTOM_SILICON", "Information Technology", "Semiconductors", 740, "Custom AI silicon, networking, and infrastructure software cash generation support classification.", "HIGH", score(88, "STARTER_ALLOWED", "SUPPORTIVE", 16, 28, 68, 41)),
  company("MRVL", "Marvell Technology", "CUSTOM_SILICON", "Information Technology", "Semiconductors", 62, "Custom silicon and optical DSP exposure are positives, but broad cyclicality remains a watch item.", "MEDIUM", score(61, "RESEARCH_CANDIDATE", "STABILISING", 19, 6, 45, 10)),
  company("TSM", "Taiwan Semiconductor Manufacturing", "FOUNDRY", "Information Technology", "Semiconductors", 910, "Advanced-node foundry demand from AI accelerators and hyperscale silicon anchors relevance.", "HIGH", score(89, "STARTER_ALLOWED", "SUPPORTIVE", 18, 32, 57, 33)),
  company("ASML", "ASML Holding", "SEMICONDUCTOR_EQUIPMENT", "Information Technology", "Semiconductor Equipment", 395, "EUV lithography is a bottleneck for advanced-node capacity, with order timing risk.", "HIGH", score(72, "APPROVED_THESIS", "WEAKENING", 13, -2, 51, 28)),
  company("AMAT", "Applied Materials", "SEMICONDUCTOR_EQUIPMENT", "Information Technology", "Semiconductor Equipment", 170, "Deposition and process equipment support foundry and memory capacity buildout.", "HIGH", score(70, "WATCHLIST", "STABILISING", 15, 3, 48, 24)),
  company("LRCX", "Lam Research", "SEMICONDUCTOR_EQUIPMENT", "Information Technology", "Semiconductor Equipment", 120, "Etch and deposition tools link to memory and leading-edge logic capacity.", "HIGH", score(76, "WATCHLIST", "STABILISING", 16, 9, 47, 26)),
  company("KLAC", "KLA", "SEMICONDUCTOR_EQUIPMENT", "Information Technology", "Semiconductor Equipment", 105, "Inspection and process control are critical as advanced-node complexity increases.", "HIGH", score(79, "APPROVED_VALUATION_ZONE", "SUPPORTIVE", 14, 12, 60, 34)),
  company("MU", "Micron Technology", "MEMORY_HBM_DRAM", "Information Technology", "Memory", 165, "HBM and DRAM pricing recovery are tracked with strict cycle invalidation rules.", "HIGH", score(78, "ADD_ALLOWED", "STABILISING", 20, 61, 39, 18)),
  company("SNDK", "SanDisk", "STORAGE_NAND_SSD_HDD", "Information Technology", "Storage", 18, "NAND and enterprise SSD demand are tracked as AI storage beneficiaries in demo mode.", "MEDIUM", score(47, "TECHNICAL_WAIT", "BROKEN", 21, 16, 28, 8)),
  company("WDC", "Western Digital", "STORAGE_NAND_SSD_HDD", "Information Technology", "Storage", 26, "Enterprise HDD and NAND exposure may benefit from AI data growth, with cycle risk tracked.", "MEDIUM", score(62, "RESEARCH_CANDIDATE", "STABILISING", 19, 22, 31, 12)),
  company("STX", "Seagate Technology", "STORAGE_NAND_SSD_HDD", "Information Technology", "Storage", 23, "Nearline storage demand is a demo AI data growth proxy, not a direct thesis.", "MEDIUM", score(58, "RESEARCH_CANDIDATE", "WEAKENING", 15, 18, 34, 14)),
  company("ANET", "Arista Networks", "NETWORKING_OPTICAL", "Information Technology", "Communications Equipment", 120, "Cloud AI networking, high-speed switching, and hyperscale customer demand support classification.", "HIGH", score(71, "HOLD", "SUPPORTIVE", 15, 21, 65, 36)),
  company("CSCO", "Cisco Systems", "NETWORKING_OPTICAL", "Information Technology", "Communications Equipment", 190, "Networking exposure is broad, but AI evidence is less concentrated than specialist peers.", "MEDIUM", score(59, "RESEARCH_CANDIDATE", "WEAKENING", 11, 4, 64, 22)),
  company("CIEN", "Ciena", "NETWORKING_OPTICAL", "Information Technology", "Optical Networking", 10, "Optical transport demand is a secondary AI data-center/networking beneficiary.", "MEDIUM", score(61, "RESEARCH_CANDIDATE", "STABILISING", 17, 9, 43, 11)),
  company("MSFT", "Microsoft", "HYPERSCALE_CLOUD", "Information Technology", "Cloud and Software", 3300, "Azure AI, Copilot monetisation, and cloud infrastructure scale support AI relevance.", "HIGH", score(84, "HOLD", "SUPPORTIVE", 12, 17, 69, 32)),
  company("GOOGL", "Alphabet", "HYPERSCALE_CLOUD", "Communication Services", "Internet Services", 2300, "Cloud AI, TPU infrastructure, search monetisation, and model capability are monitored.", "HIGH", score(82, "STARTER_ALLOWED", "STABILISING", 16, 14, 58, 24)),
  company("AMZN", "Amazon", "HYPERSCALE_CLOUD", "Consumer Discretionary", "Cloud and E-commerce", 2100, "AWS AI services, Trainium/Inferentia, and retail operating leverage are tracked separately.", "HIGH", score(81, "STARTER_ALLOWED", "STABILISING", 18, 11, 49, 8)),
  company("META", "Meta Platforms", "HYPERSCALE_CLOUD", "Communication Services", "Social Platforms", 1500, "AI-driven ad ranking, compute spend, and open model strategy support classification.", "HIGH", score(80, "APPROVED_VALUATION_ZONE", "SUPPORTIVE", 13, 20, 82, 36)),
  company("ORCL", "Oracle", "HYPERSCALE_CLOUD", "Information Technology", "Cloud Infrastructure", 430, "OCI AI infrastructure demand and contracted backlog are demo evidence anchors.", "MEDIUM", score(66, "WATCHLIST", "STABILISING", 16, 11, 71, 28)),
  company("VRT", "Vertiv", "DATA_CENTER_POWER_COOLING", "Industrials", "Electrical and Thermal Infrastructure", 45, "Thermal management, power systems, backlog, and data-center customer demand support classification.", "HIGH", score(85, "STARTER_ALLOWED", "SUPPORTIVE", 21, 24, 37, 14)),
  company("ETN", "Eaton", "DATA_CENTER_POWER_COOLING", "Industrials", "Electrical Equipment", 130, "Electrical gear and data-center power exposure are tracked as infrastructure beneficiaries.", "HIGH", score(69, "WATCHLIST", "SUPPORTIVE", 12, 9, 38, 16)),
  company("PWR", "Quanta Services", "DATA_CENTER_POWER_COOLING", "Industrials", "Engineering and Construction", 42, "Grid, utility, and data-center electrical work create indirect AI infrastructure exposure.", "MEDIUM", score(62, "RESEARCH_CANDIDATE", "STABILISING", 16, 15, 15, 5)),
  company("CEG", "Constellation Energy", "DATA_CENTER_POWER_COOLING", "Utilities", "Nuclear Power", 92, "Low-carbon power demand from data centers is tracked, but contracts must be verified.", "MEDIUM", score(60, "RESEARCH_CANDIDATE", "SUPPORTIVE", 14, 6, 24, 12)),
  company("NRG", "NRG Energy", "DATA_CENTER_POWER_COOLING", "Utilities", "Independent Power", 17, "Power demand is relevant, though direct AI contract evidence is lower-confidence.", "MEDIUM", score(56, "RESEARCH_CANDIDATE", "STABILISING", 13, 5, 28, 10)),
  company("EQIX", "Equinix", "DATA_CENTER_REIT", "Real Estate", "Data Center REIT", 86, "Interconnection and data-center capacity are AI-adjacent, with REIT leverage tracked.", "MEDIUM", score(57, "WATCHLIST", "WEAKENING", 11, 7, 49, 11)),
  company("DLR", "Digital Realty", "DATA_CENTER_REIT", "Real Estate", "Data Center REIT", 50, "Data-center leasing demand is relevant, but balance-sheet and funding costs remain key risks.", "MEDIUM", score(54, "WATCHLIST", "WEAKENING", 12, 5, 57, 9)),
  company("PLTR", "Palantir", "AI_SOFTWARE", "Information Technology", "Analytics Software", 165, "AIP adoption, commercial growth, and operating leverage are tracked as software monetisation evidence.", "HIGH", score(79, "WATCHLIST", "SUPPORTIVE", 9, 30, 81, 29)),
  company("NOW", "ServiceNow", "AI_SOFTWARE", "Information Technology", "Workflow Software", 170, "GenAI workflow monetisation and subscription retention are monitored, but valuation hurdle matters.", "HIGH", score(74, "HOLD", "STABILISING", 10, 22, 79, 31)),
  company("CRWD", "CrowdStrike", "CYBERSECURITY", "Information Technology", "Cybersecurity", 92, "AI security workflows and platform consolidation support relevance; execution risk is tracked.", "MEDIUM", score(64, "WATCHLIST", "WEAKENING", 14, 27, 75, 32)),
  company("DDOG", "Datadog", "DATA_PLATFORM", "Information Technology", "Observability", 46, "Observability demand from cloud and AI workloads is plausible but needs measurable acceleration.", "MEDIUM", score(66, "WATCHLIST", "STABILISING", 18, 25, 80, 26)),
  company("SNOW", "Snowflake", "DATA_PLATFORM", "Information Technology", "Data Platform", 48, "Data cloud relevance is clear, but growth deceleration and valuation proof block action.", "MEDIUM", score(38, "RESEARCH_CANDIDATE", "BROKEN", 12, 26, 67, 24)),
  company("MDB", "MongoDB", "DATA_PLATFORM", "Information Technology", "Database Software", 18, "AI application data growth is plausible, but durable workload acceleration must be proven.", "MEDIUM", score(55, "RESEARCH_CANDIDATE", "WEAKENING", 16, 22, 74, 16))
];

export const fallbackUniverse: UniverseResponse = {
  mode: "frontend_fallback_demo",
  not_recommendations: true,
  count: demoCompanies.length,
  companies: demoCompanies
};

export const fallbackPortfolio: PortfolioSummary = {
  cash: 1500,
  total_equity: 10000,
  drawdown_pct: 4,
  drawdown_mode: "NORMAL",
  single_stock_concentration_pct: 0,
  expected_portfolio_irr_pct: 0,
  positions: []
};
