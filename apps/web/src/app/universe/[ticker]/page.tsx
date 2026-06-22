import Link from "next/link";
import { notFound } from "next/navigation";
import { StateBadge } from "@/components/StateBadge";
import { ThesisForm } from "@/components/ThesisForm";
import { getStockDetail } from "@/lib/api";

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

export default async function StockDetailPage({ params }: { params: Promise<{ ticker: string }> }) {
  const { ticker } = await params;
  const detail = await getStockDetail(ticker);
  if (!detail) {
    notFound();
  }
  const company = detail.company;
  const sizing = sizingForState(company.status);

  return (
    <div className="page">
      <section className="section">
        <div className="section-header">
          <div>
            <h1>
              {company.ticker} · {company.company_name}
            </h1>
            <p className="muted">
              {company.sector} · {company.industry} · {company.ai_layer.replaceAll("_", " ")}
            </p>
          </div>
          <StateBadge state={company.status} />
        </div>
      </section>

      <section className="section split">
        <div className="grid">
          <div className="panel panel-body">
            <h2>Stock Memo</h2>
            <p>{detail.business_summary}</p>
            <p>{detail.ai_thesis}</p>
            <p className="muted">Classification confidence: {company.classification_confidence}. Last reviewed: {company.last_reviewed}.</p>
          </div>
          <div className="panel panel-body">
            <h2>Evidence Table</h2>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Claim</th>
                    <th>Evidence</th>
                    <th>Source</th>
                    <th>Disproves if</th>
                  </tr>
                </thead>
                <tbody>
                  {detail.evidence_table.map((item) => (
                    <tr key={`${item.claim}-${item.source_date}`}>
                      <td>{item.claim}</td>
                      <td>{item.evidence}</td>
                      <td>
                        {item.source}
                        <br />
                        <span className="muted">
                          {item.source_date} · {item.confidence}
                        </span>
                      </td>
                      <td>{item.disproves_if}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          <div className="panel panel-body">
            <h2>Decision Reasons</h2>
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
          </div>
          <div className="panel panel-body">
            <h2>Thesis Approval</h2>
            {detail.approved_thesis ? (
              <div className="callout compact">
                <strong>Approved thesis:</strong> {detail.approved_thesis.statement}
                <br />
                <span className="muted">Invalidation: {detail.approved_thesis.breaks_if}</span>
              </div>
            ) : null}
            <ThesisForm ticker={company.ticker} />
          </div>
        </div>

        <aside className="grid">
          <div className="panel panel-body metric">
            <span>Q-GEAR score</span>
            <strong>{company.score.total.toFixed(1)}</strong>
            <span>Score alone never creates action</span>
          </div>
          <div className="panel panel-body">
            <h3>Scoring</h3>
            <p>AI relevance: {company.score.ai_relevance.toFixed(1)} / 12</p>
            <p>Business quality: {company.score.business_quality.toFixed(1)} / 18</p>
            <p>Acceleration: {company.score.revenue_earnings_acceleration.toFixed(1)} / 18</p>
            <p>Earnings: {company.score.earnings_guidance_revisions.toFixed(1)} / 17</p>
            <p>Valuation: {company.score.valuation_expected_irr.toFixed(1)} / 15</p>
            <p>Technical: {company.score.technical_trend.toFixed(1)} / 10</p>
            <p>Portfolio fit: {company.score.portfolio_fit.toFixed(1)} / 10</p>
          </div>
          <div className="panel panel-body">
            <h3>Financial Metrics</h3>
            <p>Revenue growth: {(detail.financial_metrics?.revenue_growth_pct ?? company.metrics.revenue_growth_pct).toFixed(1)}%</p>
            <p>Gross margin: {(detail.financial_metrics?.gross_margin_pct ?? company.metrics.gross_margin_pct).toFixed(1)}%</p>
            <p>FCF margin: {(detail.financial_metrics?.fcf_margin_pct ?? company.metrics.fcf_margin_pct).toFixed(1)}%</p>
            <p>Base expected IRR: {(detail.financial_metrics?.expected_irr_base_pct ?? company.metrics.expected_irr_base_pct).toFixed(1)}%</p>
          </div>
          <div className="panel panel-body">
            <h3>Valuation Zone</h3>
            <p>Bear IRR: {(detail.valuation_scenarios?.bear_case_irr_pct ?? company.metrics.expected_irr_base_pct - 8).toFixed(1)}%</p>
            <p>Base IRR: {(detail.valuation_scenarios?.base_case_irr_pct ?? company.metrics.expected_irr_base_pct).toFixed(1)}%</p>
            <p>Bull IRR: {(detail.valuation_scenarios?.bull_case_irr_pct ?? company.metrics.expected_irr_base_pct + 10).toFixed(1)}%</p>
            <p>Hurdle: {(detail.valuation_scenarios?.hurdle_irr_pct ?? 15).toFixed(1)}%</p>
            <p className="muted">Great business quality cannot override a valuation hurdle failure.</p>
          </div>
          <div className="panel panel-body">
            <h3>Latest Earnings</h3>
            <p>Thesis change: {detail.latest_earnings_analysis?.thesis_change ?? "UNCHANGED"}</p>
            <p>Guidance raised: {detail.latest_earnings_analysis?.guidance_raised ? "Yes" : "No"}</p>
            <p>AI evidence improved: {detail.latest_earnings_analysis?.ai_evidence_improved ? "Yes" : "No"}</p>
            <p>Margin expanded: {detail.latest_earnings_analysis?.margin_expanded ? "Yes" : "No"}</p>
            <p>FCF improved: {detail.latest_earnings_analysis?.fcf_improved ? "Yes" : "No"}</p>
          </div>
          <div className="panel panel-body">
            <h3>Technical State</h3>
            <p>{(detail.technical_state?.regime ?? company.metrics.technical_regime).replaceAll("_", " ")}</p>
            <p>Relative strength: {(detail.technical_state?.relative_strength_pct ?? 0).toFixed(1)}%</p>
            <p>Drawdown from high: {(detail.technical_state?.drawdown_from_high_pct ?? company.metrics.drawdown_from_high_pct).toFixed(1)}%</p>
          </div>
          <div className="panel panel-body">
            <h3>Journal Trail</h3>
            <p>{detail.journal_entries?.length ?? 0} local journal entries for this ticker.</p>
            <p className="muted">Journal entries are local records, not trade execution.</p>
          </div>
          <div className="panel panel-body">
            <h3>Position Sizing</h3>
            <p className={sizing.tone}>{detail.position_sizing.range_label || sizing.label}</p>
            <p>
              Max new money: ${detail.position_sizing.max_new_money.toLocaleString()} · target weight{" "}
              {detail.position_sizing.target_weight_pct.toFixed(1)}%
            </p>
            {detail.position_sizing.reasons.map((reason) => (
              <p className="muted" key={reason}>
                {reason}
              </p>
            ))}
            <p className="muted">Absolute single-stock cap: 15%. Price decline alone never increases allowed size.</p>
          </div>
          <Link className="button secondary" href="/journal">
            Log decision
          </Link>
        </aside>
      </section>
    </div>
  );
}
