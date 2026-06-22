from __future__ import annotations

from qgear_core.decision import evaluate_decision
from qgear_core.enums import (
    AILayer,
    Confidence,
    DecisionState,
    EarningsThesisChange,
    TechnicalRegime,
)
from qgear_core.models import DecisionInput, Evidence, PortfolioContext, StockMetrics, UniverseCompany
from qgear_core.scoring import score_from_metrics

DEMO_LAST_REVIEWED = "2026-06-22"


def _evidence(ticker: str, claim: str, detail: str, confidence: Confidence) -> Evidence:
    return Evidence(
        claim=claim,
        evidence=f"Demo data for {ticker}: {detail}",
        source="Q-GEAR demo seed data",
        source_date=DEMO_LAST_REVIEWED,
        confidence=confidence,
        disproves_if="Future filings, earnings releases, segment data, or guidance contradict the claim.",
    )


def _company(
    ticker: str,
    company_name: str,
    ai_layer: AILayer,
    sector: str,
    industry: str,
    market_cap_usd_bn: float | None,
    evidence_summary: str,
    confidence: Confidence,
    revenue_growth_pct: float,
    revenue_growth_acceleration_pct: float,
    gross_margin_pct: float,
    operating_margin_pct: float,
    fcf_margin_pct: float,
    net_debt_to_ebitda: float,
    roic_pct: float,
    expected_irr_base_pct: float,
    relative_strength_pct: float,
    drawdown_from_high_pct: float,
    technical_regime: TechnicalRegime,
    latest_earnings_change: EarningsThesisChange,
    thesis_approved: bool,
    invalidation_rule_present: bool,
    fresh_positive_evidence: bool,
    owned: bool = False,
    current_weight_pct: float = 0,
    guidance_raised: bool = False,
    ai_evidence_improved: bool = False,
    margin_expanded: bool = False,
    fcf_improved: bool = False,
    evidence_age_days: int = 25,
    price_change_pct: float = 0,
    add_requested: bool = False,
    red_flag_count: int = 0,
) -> UniverseCompany:
    evidence_item = _evidence(
        ticker,
        "AI relevance requires measurable business evidence.",
        evidence_summary,
        confidence,
    )
    metrics = StockMetrics(
        ticker=ticker,
        ai_layer=ai_layer,
        classification_confidence=confidence,
        revenue_growth_pct=revenue_growth_pct,
        revenue_growth_acceleration_pct=revenue_growth_acceleration_pct,
        gross_margin_pct=gross_margin_pct,
        operating_margin_pct=operating_margin_pct,
        fcf_margin_pct=fcf_margin_pct,
        net_debt_to_ebitda=net_debt_to_ebitda,
        roic_pct=roic_pct,
        expected_irr_base_pct=expected_irr_base_pct,
        relative_strength_pct=relative_strength_pct,
        drawdown_from_high_pct=drawdown_from_high_pct,
        technical_regime=technical_regime,
        latest_earnings_change=latest_earnings_change,
        guidance_raised=guidance_raised,
        ai_evidence_improved=ai_evidence_improved,
        margin_expanded=margin_expanded,
        fcf_improved=fcf_improved,
        red_flag_count=red_flag_count,
    )
    portfolio_fit = max(4, min(10, 9 - current_weight_pct / 3 - red_flag_count))
    score = score_from_metrics(metrics, portfolio_fit_score=portfolio_fit)
    decision = evaluate_decision(
        DecisionInput(
            ticker=ticker,
            score=score,
            thesis_approved=thesis_approved,
            invalidation_rule_present=invalidation_rule_present,
            ai_relevance_proven=ai_layer != AILayer.NOT_RELEVANT and confidence != Confidence.LOW,
            latest_earnings_change=latest_earnings_change,
            expected_irr_base_pct=expected_irr_base_pct,
            hurdle_irr_pct=15,
            technical_regime=technical_regime,
            evidence_age_days=evidence_age_days,
            portfolio=PortfolioContext(
                total_equity=10_000,
                cash=2_000,
                portfolio_drawdown_pct=4,
                current_position_weight_pct=current_weight_pct,
                current_position_value=10_000 * current_weight_pct / 100,
                ai_layer_weight_pct=12,
                owned=owned,
            ),
            fresh_positive_evidence=fresh_positive_evidence,
            price_change_pct=price_change_pct,
            add_requested=add_requested,
            red_flags=tuple("Demo red flag pending review" for _ in range(red_flag_count)),
            positive_evidence=(evidence_item,) if fresh_positive_evidence else (),
        )
    )

    return UniverseCompany(
        ticker=ticker,
        company_name=company_name,
        ai_layer=ai_layer,
        sector=sector,
        industry=industry,
        market_cap_usd_bn=market_cap_usd_bn,
        evidence_summary=evidence_summary,
        classification_confidence=confidence,
        status=decision.state,
        last_reviewed=DEMO_LAST_REVIEWED,
        evidence=(evidence_item,),
        metrics=metrics,
        score=score,
        decision=decision,
    )


DEMO_UNIVERSE: tuple[UniverseCompany, ...] = (
    _company("NVDA", "NVIDIA", AILayer.COMPUTE_ACCELERATORS, "Information Technology", "Semiconductors", 3200, "Data-center GPU demand, accelerated computing platform revenue, and ecosystem lock-in are the demo evidence anchors.", Confidence.HIGH, 78, 28, 76, 64, 46, -0.4, 58, 17, 18, 12, TechnicalRegime.STABILISING, EarningsThesisChange.STRENGTHENED, True, True, True, guidance_raised=True, ai_evidence_improved=True, margin_expanded=True, fcf_improved=True),
    _company("AMD", "Advanced Micro Devices", AILayer.COMPUTE_ACCELERATORS, "Information Technology", "Semiconductors", 260, "Accelerator ramps and server CPU share are tracked, but demo evidence still requires margin and guidance confirmation.", Confidence.MEDIUM, 18, 7, 51, 10, 19, 0.8, 9, 18, 7, 26, TechnicalRegime.WEAKENING, EarningsThesisChange.UNCHANGED, False, False, False),
    _company("AVGO", "Broadcom", AILayer.CUSTOM_SILICON, "Information Technology", "Semiconductors", 740, "Custom AI silicon, networking, and infrastructure software cash generation support the classification.", Confidence.HIGH, 28, 9, 68, 43, 41, 1.4, 31, 16, 14, 10, TechnicalRegime.SUPPORTIVE, EarningsThesisChange.STRENGTHENED, True, True, True, guidance_raised=True, ai_evidence_improved=True, fcf_improved=True),
    _company("MRVL", "Marvell Technology", AILayer.CUSTOM_SILICON, "Information Technology", "Semiconductors", 62, "Custom silicon and optical DSP exposure are demo positives; broad cyclicality remains a watch item.", Confidence.MEDIUM, 6, 8, 45, 4, 10, 1.3, 5, 19, -3, 33, TechnicalRegime.STABILISING, EarningsThesisChange.UNCHANGED, False, False, False, ai_evidence_improved=True),
    _company("TSM", "Taiwan Semiconductor Manufacturing", AILayer.FOUNDRY, "Information Technology", "Semiconductors", 910, "Advanced-node foundry demand from AI accelerators and hyperscale silicon is the key evidence anchor.", Confidence.HIGH, 32, 11, 57, 47, 33, -0.2, 27, 18, 20, 8, TechnicalRegime.SUPPORTIVE, EarningsThesisChange.STRENGTHENED, True, True, True, guidance_raised=True, ai_evidence_improved=True, margin_expanded=True),
    _company("ASML", "ASML Holding", AILayer.SEMICONDUCTOR_EQUIPMENT, "Information Technology", "Semiconductor Equipment", 395, "EUV lithography is a bottleneck for advanced-node capacity, with order timing as the main demo risk.", Confidence.HIGH, -2, -4, 51, 31, 28, -0.6, 42, 13, -5, 24, TechnicalRegime.WEAKENING, EarningsThesisChange.UNCHANGED, True, True, False),
    _company("AMAT", "Applied Materials", AILayer.SEMICONDUCTOR_EQUIPMENT, "Information Technology", "Semiconductor Equipment", 170, "Deposition and process equipment support foundry and memory capacity buildout.", Confidence.HIGH, 3, 2, 48, 29, 24, -0.5, 33, 15, 4, 18, TechnicalRegime.STABILISING, EarningsThesisChange.UNCHANGED, False, False, False),
    _company("LRCX", "Lam Research", AILayer.SEMICONDUCTOR_EQUIPMENT, "Information Technology", "Semiconductor Equipment", 120, "Etch and deposition tools link to memory and leading-edge logic capacity.", Confidence.HIGH, 9, 8, 47, 31, 26, -0.4, 44, 16, 9, 16, TechnicalRegime.STABILISING, EarningsThesisChange.STRENGTHENED, False, False, True, ai_evidence_improved=True),
    _company("KLAC", "KLA", AILayer.SEMICONDUCTOR_EQUIPMENT, "Information Technology", "Semiconductor Equipment", 105, "Inspection and process control are critical as advanced-node complexity increases.", Confidence.HIGH, 12, 6, 60, 40, 34, -0.1, 54, 14, 8, 14, TechnicalRegime.SUPPORTIVE, EarningsThesisChange.UNCHANGED, True, True, False),
    _company("MU", "Micron Technology", AILayer.MEMORY_HBM_DRAM, "Information Technology", "Memory", 165, "HBM and DRAM pricing recovery are demo evidence anchors, but memory cyclicality requires strict invalidation rules.", Confidence.HIGH, 61, 30, 39, 22, 18, 0.5, 12, 20, 19, 11, TechnicalRegime.STABILISING, EarningsThesisChange.STRENGTHENED, True, True, True, owned=True, current_weight_pct=6, add_requested=True, guidance_raised=True, ai_evidence_improved=True, margin_expanded=True),
    _company("SNDK", "SanDisk", AILayer.STORAGE_NAND_SSD_HDD, "Information Technology", "Storage", 18, "NAND and enterprise SSD demand are tracked as AI storage beneficiaries in demo mode.", Confidence.MEDIUM, 16, 10, 28, 6, 8, 1.8, 6, 21, -4, 37, TechnicalRegime.BROKEN, EarningsThesisChange.UNCHANGED, False, False, False),
    _company("WDC", "Western Digital", AILayer.STORAGE_NAND_SSD_HDD, "Information Technology", "Storage", 26, "Enterprise HDD and NAND exposure may benefit from AI data growth, with cycle risk explicitly tracked.", Confidence.MEDIUM, 22, 14, 31, 9, 12, 1.6, 8, 19, 2, 30, TechnicalRegime.STABILISING, EarningsThesisChange.STRENGTHENED, False, False, True, ai_evidence_improved=True),
    _company("STX", "Seagate Technology", AILayer.STORAGE_NAND_SSD_HDD, "Information Technology", "Storage", 23, "Nearline storage demand is a demo AI data growth proxy, not a direct buy thesis.", Confidence.MEDIUM, 18, 12, 34, 13, 14, 1.7, 12, 15, 1, 22, TechnicalRegime.WEAKENING, EarningsThesisChange.UNCHANGED, False, False, False),
    _company("ANET", "Arista Networks", AILayer.NETWORKING_OPTICAL, "Information Technology", "Communications Equipment", 120, "Cloud AI networking, high-speed switching, and hyperscale customer demand support classification.", Confidence.HIGH, 21, 4, 65, 44, 36, -0.8, 38, 15, 16, 9, TechnicalRegime.SUPPORTIVE, EarningsThesisChange.STRENGTHENED, True, True, False, owned=True, current_weight_pct=14.5, add_requested=True, ai_evidence_improved=True, margin_expanded=True),
    _company("CSCO", "Cisco Systems", AILayer.NETWORKING_OPTICAL, "Information Technology", "Communications Equipment", 190, "Networking exposure is broad, but demo AI evidence is less concentrated than specialist peers.", Confidence.MEDIUM, 4, 1, 64, 28, 22, 1.2, 19, 11, -6, 17, TechnicalRegime.WEAKENING, EarningsThesisChange.UNCHANGED, False, False, False),
    _company("CIEN", "Ciena", AILayer.NETWORKING_OPTICAL, "Information Technology", "Optical Networking", 10, "Optical transport demand is a secondary AI data-center/networking beneficiary.", Confidence.MEDIUM, 9, 6, 43, 9, 11, 0.6, 8, 17, 5, 20, TechnicalRegime.STABILISING, EarningsThesisChange.UNCHANGED, False, False, False),
    _company("MSFT", "Microsoft", AILayer.HYPERSCALE_CLOUD, "Information Technology", "Cloud and Software", 3300, "Azure AI, Copilot monetisation, and cloud infrastructure scale support AI relevance.", Confidence.HIGH, 17, 2, 69, 45, 32, -0.7, 29, 12, 4, 8, TechnicalRegime.SUPPORTIVE, EarningsThesisChange.STRENGTHENED, True, True, False, guidance_raised=True, ai_evidence_improved=True),
    _company("GOOGL", "Alphabet", AILayer.HYPERSCALE_CLOUD, "Communication Services", "Internet Services", 2300, "Cloud AI, TPU infrastructure, search monetisation, and model capability are demo evidence anchors.", Confidence.HIGH, 14, 1, 58, 32, 24, -0.9, 25, 16, 8, 13, TechnicalRegime.STABILISING, EarningsThesisChange.STRENGTHENED, True, True, True, ai_evidence_improved=True, margin_expanded=True),
    _company("AMZN", "Amazon", AILayer.HYPERSCALE_CLOUD, "Consumer Discretionary", "Cloud and E-commerce", 2100, "AWS AI services, Trainium/Inferentia, and retail operating leverage are tracked separately.", Confidence.HIGH, 11, 2, 49, 11, 8, 0.7, 14, 18, 7, 10, TechnicalRegime.STABILISING, EarningsThesisChange.STRENGTHENED, True, True, True, ai_evidence_improved=True, margin_expanded=True, fcf_improved=True),
    _company("META", "Meta Platforms", AILayer.HYPERSCALE_CLOUD, "Communication Services", "Social Platforms", 1500, "AI-driven ad ranking, compute spend, and open model strategy support classification.", Confidence.HIGH, 20, 3, 82, 41, 36, -0.4, 31, 13, 10, 9, TechnicalRegime.SUPPORTIVE, EarningsThesisChange.UNCHANGED, True, True, False),
    _company("ORCL", "Oracle", AILayer.HYPERSCALE_CLOUD, "Information Technology", "Cloud Infrastructure", 430, "OCI AI infrastructure demand and contracted backlog are the demo evidence anchors.", Confidence.MEDIUM, 11, 3, 71, 32, 28, 3.6, 17, 16, 6, 18, TechnicalRegime.STABILISING, EarningsThesisChange.STRENGTHENED, False, False, True, ai_evidence_improved=True),
    _company("VRT", "Vertiv", AILayer.DATA_CENTER_POWER_COOLING, "Industrials", "Electrical and Thermal Infrastructure", 45, "Thermal management, power systems, backlog, and data-center customer demand support classification.", Confidence.HIGH, 24, 8, 37, 18, 14, 1.9, 18, 21, 18, 15, TechnicalRegime.SUPPORTIVE, EarningsThesisChange.STRENGTHENED, True, True, True, guidance_raised=True, ai_evidence_improved=True, margin_expanded=True),
    _company("ETN", "Eaton", AILayer.DATA_CENTER_POWER_COOLING, "Industrials", "Electrical Equipment", 130, "Electrical gear and data-center power exposure are tracked as infrastructure beneficiaries.", Confidence.HIGH, 9, 2, 38, 21, 16, 1.5, 19, 12, 5, 11, TechnicalRegime.SUPPORTIVE, EarningsThesisChange.UNCHANGED, False, False, False),
    _company("PWR", "Quanta Services", AILayer.DATA_CENTER_POWER_COOLING, "Industrials", "Engineering and Construction", 42, "Grid, utility, and data-center electrical work create indirect AI infrastructure exposure.", Confidence.MEDIUM, 15, 3, 15, 7, 5, 1.1, 10, 16, 7, 12, TechnicalRegime.STABILISING, EarningsThesisChange.UNCHANGED, False, False, False),
    _company("CEG", "Constellation Energy", AILayer.DATA_CENTER_POWER_COOLING, "Utilities", "Nuclear Power", 92, "Low-carbon power demand from data centers is tracked, but contracts and pricing must be verified.", Confidence.MEDIUM, 6, 2, 24, 15, 12, 1.3, 9, 14, 9, 9, TechnicalRegime.SUPPORTIVE, EarningsThesisChange.UNCHANGED, False, False, False),
    _company("NRG", "NRG Energy", AILayer.DATA_CENTER_POWER_COOLING, "Utilities", "Independent Power", 17, "Power demand is relevant, though demo confidence is lower without direct AI contract evidence.", Confidence.MEDIUM, 5, 1, 28, 13, 10, 2.4, 11, 13, 3, 15, TechnicalRegime.STABILISING, EarningsThesisChange.UNCHANGED, False, False, False),
    _company("EQIX", "Equinix", AILayer.DATA_CENTER_REIT, "Real Estate", "Data Center REIT", 86, "Interconnection and data-center capacity are AI-adjacent, with REIT leverage and capex tracked.", Confidence.MEDIUM, 7, 1, 49, 18, 11, 5.1, 6, 11, -2, 19, TechnicalRegime.WEAKENING, EarningsThesisChange.UNCHANGED, False, False, False),
    _company("DLR", "Digital Realty", AILayer.DATA_CENTER_REIT, "Real Estate", "Data Center REIT", 50, "Data-center leasing demand is relevant, but balance-sheet and funding costs remain key demo risks.", Confidence.MEDIUM, 5, 2, 57, 15, 9, 5.7, 5, 12, -1, 21, TechnicalRegime.WEAKENING, EarningsThesisChange.UNCHANGED, False, False, False),
    _company("PLTR", "Palantir", AILayer.AI_SOFTWARE, "Information Technology", "Analytics Software", 165, "AIP adoption, commercial growth, and operating leverage are tracked as software monetisation evidence.", Confidence.HIGH, 30, 8, 81, 16, 29, -1.0, 16, 9, 22, 6, TechnicalRegime.SUPPORTIVE, EarningsThesisChange.STRENGTHENED, True, True, False, guidance_raised=True, ai_evidence_improved=True, margin_expanded=True),
    _company("NOW", "ServiceNow", AILayer.AI_SOFTWARE, "Information Technology", "Workflow Software", 170, "GenAI workflow monetisation and subscription retention are monitored, but valuation hurdle matters.", Confidence.HIGH, 22, 1, 79, 28, 31, -0.7, 19, 10, 1, 14, TechnicalRegime.STABILISING, EarningsThesisChange.UNCHANGED, True, True, False),
    _company("CRWD", "CrowdStrike", AILayer.CYBERSECURITY, "Information Technology", "Cybersecurity", 92, "AI security workflows and platform consolidation support relevance; execution risk is tracked.", Confidence.MEDIUM, 27, 0, 75, 8, 32, -0.4, 11, 14, -4, 28, TechnicalRegime.WEAKENING, EarningsThesisChange.UNCHANGED, False, False, False),
    _company("DDOG", "Datadog", AILayer.DATA_PLATFORM, "Information Technology", "Observability", 46, "Observability demand from cloud and AI workloads is plausible but needs measurable acceleration.", Confidence.MEDIUM, 25, 3, 80, 9, 26, -0.5, 10, 18, 2, 25, TechnicalRegime.STABILISING, EarningsThesisChange.UNCHANGED, False, False, False),
    _company("SNOW", "Snowflake", AILayer.DATA_PLATFORM, "Information Technology", "Data Platform", 48, "Data cloud relevance is clear, but demo thesis is held back by growth deceleration and valuation proof.", Confidence.MEDIUM, 26, -6, 67, -3, 24, -0.8, 4, 12, -10, 45, TechnicalRegime.BROKEN, EarningsThesisChange.WEAKENED, False, False, False, price_change_pct=-25),
    _company("MDB", "MongoDB", AILayer.DATA_PLATFORM, "Information Technology", "Database Software", 18, "AI application data growth is plausible, but demo evidence requires durable workload acceleration.", Confidence.MEDIUM, 22, -4, 74, 5, 16, -0.6, 7, 16, -8, 40, TechnicalRegime.WEAKENING, EarningsThesisChange.UNCHANGED, False, False, False),
)


def get_company(ticker: str) -> UniverseCompany | None:
    normalized = ticker.upper()
    return next((company for company in DEMO_UNIVERSE if company.ticker == normalized), None)
