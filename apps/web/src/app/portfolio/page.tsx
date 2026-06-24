import { PositionForm } from "@/components/PositionForm";
import { StateBadge } from "@/components/StateBadge";
import { EmptyState, MetricCard, PageHeader, SectionCard } from "@/components/ui";
import { getPortfolio, getProviderStatus } from "@/lib/api";

export default async function PortfolioPage() {
  const [portfolio, providerStatus] = await Promise.all([getPortfolio(), getProviderStatus()]);

  return (
    <div className="page">
      <PageHeader
        eyebrow="Portfolio"
        title="Portfolio Risk"
        description="Manual local portfolio with concentration, drawdown mode, cash buffer, and benchmark placeholders."
        actions={<StateBadge state={portfolio.drawdown_mode === "HARD_AUDIT" ? "BLOCKED_BY_RISK" : "HOLD"} />}
      />

      <section className="section">
        <div className="grid cols-4">
          <MetricCard label="Cash" value={`$${portfolio.cash.toLocaleString()}`} detail={`${portfolio.cash_pct.toFixed(1)}% cash; default buffer target 10-20%`} />
          <MetricCard label="Total equity" value={`$${portfolio.total_equity.toLocaleString()}`} detail="Manual holdings plus cash" />
          <MetricCard
            label="Drawdown"
            value={`${portfolio.drawdown_pct.toFixed(1)}%`}
            detail={portfolio.drawdown_mode.replaceAll("_", " ")}
            tone={portfolio.drawdown_mode === "NORMAL" ? "ok" : "warn"}
          />
          <MetricCard
            label="Single-stock concentration"
            value={`${portfolio.single_stock_concentration_pct.toFixed(1)}%`}
            detail="Absolute cap 15%"
            tone={portfolio.single_stock_concentration_pct >= 15 ? "danger" : "neutral"}
          />
          <MetricCard
            label="Weighted expected IRR"
            value={`${portfolio.expected_portfolio_irr_pct.toFixed(1)}%`}
            detail="Research assumption, not a promise"
            tone={portfolio.expected_portfolio_irr_pct >= 15 ? "ok" : "warn"}
          />
        </div>
      </section>

      <section className="section split">
        <div>
          <SectionCard title="Risk Dashboard" description={portfolio.risk_note}>
            <div className="grid cols-3">
              <div className="callout compact">
                <strong>Expected IRR distribution</strong>
                <p>
                  Min {portfolio.expected_irr_distribution.min_pct.toFixed(1)}% · Weighted{" "}
                  {portfolio.expected_irr_distribution.weighted_pct.toFixed(1)}% · Max{" "}
                  {portfolio.expected_irr_distribution.max_pct.toFixed(1)}%
                </p>
                <p className="muted">{portfolio.expected_irr_distribution.note}</p>
              </div>
              <div className="callout compact">
                <strong>AI-layer exposure</strong>
                {Object.keys(portfolio.ai_layer_concentration).length ? (
                  Object.entries(portfolio.ai_layer_concentration).map(([layer, weight]) => (
                    <p key={layer}>
                      {layer.replaceAll("_", " ")}: {weight.toFixed(1)}%
                    </p>
                  ))
                ) : (
                  <p className="muted">No layer concentration until positions are recorded.</p>
                )}
              </div>
              <div className="callout compact">
                <strong>Benchmark placeholders</strong>
                {portfolio.benchmark_comparison.map((benchmark) => (
                  <p key={benchmark.benchmark}>
                    {benchmark.benchmark}: {benchmark.status.replaceAll("_", " ")}
                  </p>
                ))}
              </div>
            </div>
          </SectionCard>

          <SectionCard title="Review Queue" description="Blocked adds and review dates are process prompts, never trade instructions.">
            <div className="grid cols-2">
              <div>
                <h3>Blocked Adds</h3>
                {portfolio.blocked_adds.length ? (
                  portfolio.blocked_adds.map((item) => (
                    <p className="warn-text" key={`${item.ticker}-${item.reason}`}>
                      <strong>{item.ticker}</strong>: {item.reason}
                    </p>
                  ))
                ) : (
                  <p className="muted">No blocked-add prompts from current manual positions.</p>
                )}
                {portfolio.concentration_risks.map((risk) => (
                  <p className={risk.severity === "high" ? "danger-text" : "warn-text"} key={`${risk.ticker ?? "portfolio"}-${risk.message}`}>
                    <strong>{risk.ticker ?? "Portfolio"}</strong>: {risk.message}
                  </p>
                ))}
              </div>
              <div>
                <h3>Review Calendar</h3>
                {portfolio.review_calendar.length ? (
                  portfolio.review_calendar.map((item) => (
                    <p key={`${item.ticker}-${item.next_review_date}`}>
                      <strong>{item.ticker}</strong>: {item.next_review_date} · {item.thesis_status}
                    </p>
                  ))
                ) : (
                  <p className="muted">No review dates recorded yet.</p>
                )}
              </div>
            </div>
          </SectionCard>

          <SectionCard title="AI Portfolio Review" description="Optional draft assistance only. No portfolio or journal data is sent automatically.">
            <div className="assistant-status">
              <span className="eyebrow">AI provider</span>
              <strong>{providerStatus.ai.ai_enabled ? "Configured" : "Disabled"}</strong>
              <small>
                Draft-only: {providerStatus.ai.draft_only ? "yes" : "no"} · Decision mutation:{" "}
                {providerStatus.ai.mutates_decision_state ? "possible" : "never automatic"}
              </small>
            </div>
            <p className="muted">{providerStatus.ai.external_upload_policy}</p>
            <button className="button secondary" type="button" disabled>
              {providerStatus.ai.ai_enabled ? "Portfolio AI draft requires explicit request" : "AI portfolio reviewer disabled"}
            </button>
          </SectionCard>

          <SectionCard title="Positions" description="Manual records only. This app does not execute trades.">
            {portfolio.positions.length ? (
              <div className="position-grid">
                {portfolio.positions.map((position) => (
                  <article className="position-card" key={position.id}>
                    <div className="position-card-header">
                      <span>
                        <strong>{position.ticker}</strong>
                        <small>
                          {position.status} · {position.thesis_status}
                        </small>
                      </span>
                      <span className={position.unrealized_pl >= 0 ? "badge ok" : "badge warn"}>
                        ${position.unrealized_pl.toFixed(2)}
                      </span>
                    </div>
                    <div className="position-card-metrics">
                      <div className="mini-stat">
                        <span>Weight</span>
                        <strong>{position.position_weight_pct.toFixed(1)}%</strong>
                      </div>
                      <div className="mini-stat">
                        <span>Value</span>
                        <strong>${position.market_value.toFixed(0)}</strong>
                      </div>
                      <div className="mini-stat">
                        <span>Review</span>
                        <strong>{position.next_review_date || "Not set"}</strong>
                      </div>
                    </div>
                    <p className="muted">
                      {position.shares} shares · avg ${position.average_cost.toFixed(2)} · current ${position.current_price.toFixed(2)}
                    </p>
                    <small className="muted">Manual record only. No brokerage execution exists here.</small>
                  </article>
                ))}
              </div>
            ) : (
              <EmptyState title="No manual positions recorded" detail="Add positions here only after trades are made outside Q-GEAR." />
            )}
          </SectionCard>
        </div>
        <SectionCard title="Record Position" description="Manual tracking only. No broker execution exists in Q-GEAR.">
          <PositionForm />
        </SectionCard>
      </section>
    </div>
  );
}
