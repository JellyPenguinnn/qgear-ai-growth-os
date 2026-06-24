import Link from "next/link";
import { notFound } from "next/navigation";
import { StateBadge } from "@/components/StateBadge";
import { StockAIAssistantPanel } from "@/components/StockAIAssistantPanel";
import { ThesisForm } from "@/components/ThesisForm";
import { ValuationWorkbench } from "@/components/ValuationWorkbench";
import { BlockerList, DecisionCard, EmptyState, EvidenceCard, MetricCard, PageHeader, SectionCard } from "@/components/ui";
import { getDataQuality, getProviderStatus, getStockDetail, getValuation } from "@/lib/api";

function sizingForState(state: string) {
  if (state === "STARTER_ALLOWED") {
    return { label: "Starter: 2.5-5%", amount: "$250-$500 on $10,000", tone: "ok-text" };
  }
  if (state === "ADD_ALLOWED") {
    return { label: "Normal add: 5-8%", amount: "$500-$800 on $10,000, capped by current weight", tone: "ok-text" };
  }
  if (state === "TRIM_CANDIDATE" || state === "BLOCKED_BY_RISK" || state === "EXIT_THESIS_BROKEN") {
    return { label: "Risk review: 0%", amount: "$0 new money", tone: "danger-text" };
  }
  return { label: "Research / wait: 0%", amount: "$0 new money until gates clear", tone: "warn-text" };
}

function evidenceQuality(items: { confidence: "LOW" | "MEDIUM" | "HIGH"; source_date: string }[]) {
  if (!items.length) {
    return "No verified evidence recorded.";
  }
  const high = items.filter((item) => item.confidence === "HIGH").length;
  const medium = items.filter((item) => item.confidence === "MEDIUM").length;
  const low = items.filter((item) => item.confidence === "LOW").length;
  const latest = [...items].sort((a, b) => b.source_date.localeCompare(a.source_date))[0]?.source_date;
  return `${high} high / ${medium} medium / ${low} low confidence; latest source ${latest}.`;
}

export default async function StockDetailPage({ params }: { params: Promise<{ ticker: string }> }) {
  const { ticker } = await params;
  const [detail, providerStatus, valuation, dataQuality] = await Promise.all([
    getStockDetail(ticker),
    getProviderStatus(),
    getValuation(ticker),
    getDataQuality(ticker)
  ]);
  if (!detail) {
    notFound();
  }
  const company = detail.company;
  const sizing = sizingForState(detail.decision_state.state);
  const blockers = detail.decision_state.blocked_reasons;
  const nextReview = detail.approved_thesis?.next_review_date ?? "Not set until thesis approval.";
  const quality = evidenceQuality(detail.evidence_table);
  const nextTask = blockers.length
    ? "Resolve the first blocker with sourced evidence before changing state."
    : detail.decision_state.action_allowed
      ? "Journal the evidence and confirm position sizing before any manual action outside the app."
      : "Refresh thesis, evidence, valuation, technical state, and portfolio risk budget.";

  return (
    <div className="page">
      <PageHeader
        eyebrow="Stock Workbench"
        title={`${company.ticker} · ${company.company_name}`}
        description={`${company.sector} · ${company.industry} · ${company.ai_layer.replaceAll("_", " ")}`}
        actions={
          <>
            <StateBadge state={detail.decision_state.state} />
            <Link className="button secondary" href="/evidence">
              Add evidence
            </Link>
            <Link className="button secondary" href="/journal">
              Log decision
            </Link>
          </>
        }
      />

      <DecisionCard
        state={detail.decision_state.state}
        score={company.score.total}
        reasons={detail.decision_state.reasons}
        blockers={blockers}
        nextTask={nextTask}
        maxNewMoney={detail.position_sizing.max_new_money}
        evidenceQuality={quality}
        nextReview={nextReview}
      />

      <section className="workbench-summary" aria-label="Workbench summary">
        <MetricCard label="Evidence quality" value={quality.split(";")[0]} detail="MEDIUM/HIGH evidence is required for action-changing decisions" />
        <MetricCard label="Next review" value={nextReview} detail="Review dates keep the thesis from going stale" />
        <MetricCard
          label="Action permission"
          value={detail.decision_state.action_allowed ? "Allowed by gates" : "Blocked / wait"}
          detail="Score alone never creates action"
          tone={detail.decision_state.action_allowed ? "ok" : blockers.length ? "warn" : "neutral"}
        />
        <MetricCard
          label="Max new money"
          value={`$${detail.position_sizing.max_new_money.toLocaleString()}`}
          detail={`${detail.position_sizing.range_label || sizing.label}; not trade execution`}
          tone={detail.position_sizing.max_new_money > 0 ? "ok" : "warn"}
        />
      </section>

      <section className="section split">
        <div className="grid">
          <SectionCard title="Next Research Task" description="The workbench points to research work, not trade execution.">
            <div className="callout compact">
              <strong>{nextTask}</strong>
              <p className="muted">No action is justified unless thesis, invalidation, fresh evidence, valuation, technical regime, and risk budget all clear.</p>
            </div>
            <BlockerList blockers={blockers} empty="No hard blocker surfaced, but all Q-GEAR gates still need a journaled review." />
          </SectionCard>

          <SectionCard title="Stock Memo" description="Business context and AI-relevance thesis. Demo data is not a recommendation.">
            <p>{detail.business_summary}</p>
            <p>{detail.ai_thesis}</p>
            <p className="muted">Classification confidence: {company.classification_confidence}. Last reviewed: {company.last_reviewed}.</p>
          </SectionCard>

          <SectionCard title="Evidence Timeline" description="Action-changing claims require source, source date, confidence, and disproof criteria.">
            <div className="evidence-grid">
              {detail.evidence_table.map((item) => (
                <EvidenceCard key={`${item.claim}-${item.source_date}`} item={item} />
              ))}
            </div>
          </SectionCard>

          <SectionCard title="Reasons And Blockers" description="Score supports research priority, but hard gates decide state.">
            {(detail.decision_state.reasons.length ? detail.decision_state.reasons : ["No action justified without fresh evidence and risk budget."]).map((reason) => (
              <p key={reason}>{reason}</p>
            ))}
            {detail.decision_state.blocked_reasons.length ? (
              <>
                <h3>Blockers</h3>
                {detail.decision_state.blocked_reasons.map((reason) => (
                  <p className="warn-text" key={reason}>
                    {reason}
                  </p>
                ))}
              </>
            ) : null}
          </SectionCard>

          {valuation ? (
            <SectionCard title="Valuation Underwriting" description="Edit assumptions locally and recalculate without saving or changing state.">
              <ValuationWorkbench initial={valuation} aiStatus={providerStatus.ai} />
            </SectionCard>
          ) : (
            <SectionCard title="Valuation Zone">
              <p>Bear IRR: {(detail.valuation_scenarios?.bear_case_irr_pct ?? company.metrics.expected_irr_base_pct - 8).toFixed(1)}%</p>
              <p>Base IRR: {(detail.valuation_scenarios?.base_case_irr_pct ?? company.metrics.expected_irr_base_pct).toFixed(1)}%</p>
              <p>Bull IRR: {(detail.valuation_scenarios?.bull_case_irr_pct ?? company.metrics.expected_irr_base_pct + 10).toFixed(1)}%</p>
              <p>Hurdle: {(detail.valuation_scenarios?.hurdle_irr_pct ?? 15).toFixed(1)}%</p>
              <p className="muted">Great business quality cannot override a valuation hurdle failure.</p>
            </SectionCard>
          )}

          <SectionCard title="Thesis Card" description="A stock cannot become actionable without an approved thesis and invalidation rule.">
            {detail.approved_thesis ? (
              <div className="thesis-card">
                <p>
                  <strong>Status:</strong> {detail.approved_thesis.status}
                </p>
                <p>
                  <strong>Statement:</strong> {detail.approved_thesis.statement}
                </p>
                <p>
                  <strong>Must go right:</strong> {detail.approved_thesis.must_go_right}
                </p>
                <p>
                  <strong>Invalidation:</strong> {detail.approved_thesis.breaks_if || detail.invalidation_rule}
                </p>
                <p>
                  <strong>Next review:</strong> {detail.approved_thesis.next_review_date}
                </p>
                <div className="flag-row">
                  {detail.approved_thesis.key_metrics.map((metric) => (
                    <span className="badge" key={metric}>
                      {metric}
                    </span>
                  ))}
                </div>
              </div>
            ) : (
              <EmptyState title="No approved thesis yet" detail="Approve a thesis, invalidation rule, key metrics, and review date before any starter/add state can become actionable." />
            )}
            {detail.invalidation_rule && !detail.approved_thesis ? <p className="muted">Current invalidation rule: {detail.invalidation_rule}</p> : null}
            <ThesisForm ticker={company.ticker} />
          </SectionCard>

          <SectionCard title="AI Assistant Panel" description="Explicit draft-only assistance. AI output never changes state until the user verifies and saves evidence manually.">
            <StockAIAssistantPanel
              ticker={company.ticker}
              aiStatus={providerStatus.ai}
              decisionState={detail.decision_state.state}
              score={company.score.total}
              reasons={detail.decision_state.reasons}
              blockers={blockers}
              evidence={detail.evidence_table}
              existingThesis={detail.approved_thesis?.statement ?? detail.ai_thesis}
              nextReviewDate={detail.approved_thesis?.next_review_date ?? null}
            />
          </SectionCard>
        </div>

        <aside className="grid">
          <MetricCard label="Q-GEAR score" value={company.score.total.toFixed(1)} detail="Score alone never creates action" />
          <SectionCard title="Data Quality">
            {dataQuality ? (
              <>
                <div className="grid cols-2 compact">
                  <MetricCard label="Source quality" value={dataQuality.data_quality.source_quality_score} detail={dataQuality.data_quality.mode} />
                  <MetricCard label="Evidence coverage" value={dataQuality.data_quality.evidence_coverage_score} detail="Action support still requires all gates" />
                </div>
                <p>{dataQuality.reason}</p>
                <p>Financials: {dataQuality.data_quality.financial_data_status}</p>
                <p>Prices: {dataQuality.data_quality.price_data_status}</p>
                <p>Technical: {dataQuality.data_quality.technical_data_status}</p>
                {dataQuality.data_quality.missing_required_inputs.length ? (
                  <p className="warn-text">Missing: {dataQuality.data_quality.missing_required_inputs.join(", ")}</p>
                ) : null}
                {dataQuality.data_quality.provider_errors.length ? <p className="danger-text">Provider errors: {dataQuality.data_quality.provider_errors.join("; ")}</p> : null}
              </>
            ) : (
              <EmptyState title="No data quality available" detail="Reconnect the API to inspect source quality and provider metadata." />
            )}
            <Link className="button secondary" href="/data-health">
              Data Health
            </Link>
          </SectionCard>
          <SectionCard title="Scoring">
            <p>AI relevance: {company.score.ai_relevance.toFixed(1)} / 12</p>
            <p>Business quality: {company.score.business_quality.toFixed(1)} / 18</p>
            <p>Acceleration: {company.score.revenue_earnings_acceleration.toFixed(1)} / 18</p>
            <p>Earnings: {company.score.earnings_guidance_revisions.toFixed(1)} / 17</p>
            <p>Valuation: {company.score.valuation_expected_irr.toFixed(1)} / 15</p>
            <p>Technical: {company.score.technical_trend.toFixed(1)} / 10</p>
            <p>Portfolio fit: {company.score.portfolio_fit.toFixed(1)} / 10</p>
          </SectionCard>
          <SectionCard title="Financial Metrics">
            <p>Revenue growth: {(detail.financial_metrics?.revenue_growth_pct ?? company.metrics.revenue_growth_pct).toFixed(1)}%</p>
            <p>Gross margin: {(detail.financial_metrics?.gross_margin_pct ?? company.metrics.gross_margin_pct).toFixed(1)}%</p>
            <p>FCF margin: {(detail.financial_metrics?.fcf_margin_pct ?? company.metrics.fcf_margin_pct).toFixed(1)}%</p>
            <p>Base expected IRR: {(detail.financial_metrics?.expected_irr_base_pct ?? company.metrics.expected_irr_base_pct).toFixed(1)}%</p>
          </SectionCard>
          <SectionCard title="Latest Earnings">
            <p>Thesis change: {detail.latest_earnings_analysis?.thesis_change ?? "UNCHANGED"}</p>
            <p>Guidance raised: {detail.latest_earnings_analysis?.guidance_raised ? "Yes" : "No"}</p>
            <p>AI evidence improved: {detail.latest_earnings_analysis?.ai_evidence_improved ? "Yes" : "No"}</p>
            <p>Margin expanded: {detail.latest_earnings_analysis?.margin_expanded ? "Yes" : "No"}</p>
            <p>FCF improved: {detail.latest_earnings_analysis?.fcf_improved ? "Yes" : "No"}</p>
            <p className="muted">If thesis status weakens or breaks, starter/add is blocked regardless of score.</p>
          </SectionCard>

          <SectionCard title="Technical / Risk State">
            <p>{(detail.technical_state?.regime ?? company.metrics.technical_regime).replaceAll("_", " ")}</p>
            <p>Relative strength: {(detail.technical_state?.relative_strength_pct ?? 0).toFixed(1)}%</p>
            <p>Drawdown from high: {(detail.technical_state?.drawdown_from_high_pct ?? company.metrics.drawdown_from_high_pct).toFixed(1)}%</p>
            <p className="muted">Technicals confirm timing and risk only; they do not create the thesis.</p>
          </SectionCard>

          <SectionCard title="Portfolio Impact">
            <p className={sizing.tone}>{detail.position_sizing.range_label || sizing.label}</p>
            <p>
              Target weight: {detail.position_sizing.target_weight_pct.toFixed(1)}% · Max new money: $
              {detail.position_sizing.max_new_money.toLocaleString()}
            </p>
            <p>Drawdown mode: {detail.position_sizing.drawdown_mode}</p>
            {detail.position_sizing.reasons.map((reason) => (
              <p className="muted" key={reason}>
                {reason}
              </p>
            ))}
            <p className="muted">Absolute single-stock cap: 15%. Price decline alone never increases allowed size.</p>
          </SectionCard>

          <SectionCard title="Journal Trail">
            {detail.journal_entries?.length ? (
              <div className="journal-list">
                {detail.journal_entries.slice(0, 3).map((entry) => (
                  <article className="journal-mini" key={`${entry.action}-${entry.entry_date}-${entry.evidence}`}>
                    <strong>
                      {entry.action} · {entry.entry_date}
                    </strong>
                    <p>{entry.evidence}</p>
                  </article>
                ))}
              </div>
            ) : (
              <EmptyState title="No local journal trail yet" detail="Log the decision process before changing real-world position size." />
            )}
            <p className="muted">Journal entries are local records, not trade execution.</p>
          </SectionCard>

          <Link className="button secondary" href="/journal">
            Log decision
          </Link>
        </aside>
      </section>
    </div>
  );
}
