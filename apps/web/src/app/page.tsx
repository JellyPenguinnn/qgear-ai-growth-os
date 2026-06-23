import Link from "next/link";
import type { Route } from "next";
import { StateBadge } from "@/components/StateBadge";
import { EmptyState, MetricCard, PageHeader, ProviderStatusBadge, SectionCard } from "@/components/ui";
import { getToday } from "@/lib/api";

export default async function TodayPage() {
  const today = await getToday();

  return (
    <div className="page">
      <PageHeader
        eyebrow="Today"
        title="No Action Unless Evidence Changed"
        description="A calm daily command center for review queues, evidence changes, provider status, and portfolio risk."
        actions={
          <>
            <ProviderStatusBadge mode={today.provider_status.mode} />
            <Link className="button secondary" href="/settings">
              Settings
            </Link>
          </>
        }
      />

      <section className="section">
        <div className="grid cols-4">
          <MetricCard label="Universe" value={today.metrics.universe_count} detail="Demo tickers classified" />
          <MetricCard label="Review queue" value={today.metrics.review_queue_count} detail="Start here today" tone="warn" />
          <MetricCard
            label="Drawdown mode"
            value={today.metrics.drawdown_mode.replaceAll("_", " ")}
            detail={`${today.metrics.drawdown_pct.toFixed(1)}% current drawdown`}
            tone={today.metrics.drawdown_mode === "NORMAL" ? "ok" : "warn"}
          />
          <MetricCard
            label="Gated action states"
            value={today.metrics.action_allowed_count}
            detail="Manual review only"
            tone={today.metrics.action_allowed_count ? "warn" : "neutral"}
          />
        </div>
      </section>

      <SectionCard title="Daily Stance" description="Default to discipline unless the evidence changed.">
        <div className="callout">
          <strong>{today.default_stance}</strong> {today.stance_reason}
        </div>
      </SectionCard>

      <section className="split">
        <SectionCard
          title="Review Queue"
          description="Evidence, thesis, valuation, technical, and portfolio-risk items to inspect before any decision changes."
          actions={
            <Link href={"/pipeline" as Route} className="button secondary">
              Pipeline
            </Link>
          }
        >
          {today.review_queue.length ? (
            <div className="review-list">
              {today.review_queue.map((item) => (
                <Link key={item.ticker} href={`/universe/${item.ticker}`} className="review-item">
                  <span>
                    <strong>{item.ticker}</strong>
                    <small>{item.company_name}</small>
                  </span>
                  <StateBadge state={item.decision_state} />
                  <p>{item.primary_blocker || item.next_task}</p>
                </Link>
              ))}
            </div>
          ) : (
            <EmptyState title="Queue clear" detail="No urgent review prompts in the current demo data." />
          )}
        </SectionCard>

        <SectionCard title="Pipeline Snapshot" description="Where the universe sits today.">
          <div className="metric-stack">
            {today.pipeline_snapshot.map((state) => (
              <Link href={"/pipeline" as Route} className="snapshot-row" key={state.state}>
                <span>
                  <strong>{state.label}</strong>
                  <small>{state.description}</small>
                </span>
                <span className="badge">{state.count}</span>
              </Link>
            ))}
          </div>
        </SectionCard>
      </section>

      <SectionCard title="Review Prompts" description="Alerts are review prompts only. They are never trade instructions.">
        {today.alerts.length ? (
          <div className="alert-grid">
            {today.alerts.map((alert) => (
              <article className={`alert-card ${alert.severity}`} key={`${alert.type}-${alert.ticker ?? "portfolio"}`}>
                <span className="eyebrow">{alert.type.replaceAll("_", " ")}</span>
                <h3>{alert.ticker ?? "Portfolio"}</h3>
                <p>{alert.message}</p>
                <small>Review prompt only: {String(alert.trade_instruction)}</small>
              </article>
            ))}
          </div>
        ) : (
          <EmptyState title="No alerts" detail="No local review prompts are present in the current demo data." />
        )}
      </SectionCard>

      <SectionCard title="Data Provenance" description="Provider mode and safety status for local research data.">
        <div className="grid cols-4">
          <MetricCard label="Mode" value={today.provider_status.mode.replaceAll("_", " ")} detail="Live data optional" />
          <MetricCard label="SEC filings" value={today.provider_status.providers.filings ?? "not configured"} detail="Source metadata required" />
          <MetricCard label="Prices" value={today.provider_status.providers.prices ?? "not configured"} detail="Mock snapshots in demo mode" />
          <MetricCard label="Safety" value={today.safety.auto_trading} detail="Auto-trading, margin, and options disabled" tone="ok" />
        </div>
      </SectionCard>

      <SectionCard
        title="Research Priority Only"
        description="Rankings help decide what to study. A high score does not override hard gates."
        actions={
          <Link href="/universe" className="button secondary">
            Universe screener
          </Link>
        }
      >
        <div className="ranking-grid">
          {today.top_rankings.map((item) => (
            <Link href={`/universe/${item.ticker}`} key={item.ticker} className="ranking-card">
              <span>
                <strong>{item.ticker}</strong>
                <small>{item.company_name}</small>
              </span>
              <StateBadge state={item.decision_state} />
              <p>{item.primary_blocker || item.primary_reason}</p>
              <strong>{item.score.toFixed(1)}</strong>
            </Link>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
