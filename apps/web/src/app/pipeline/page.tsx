import Link from "next/link";
import { ResearchPipeline } from "@/components/ResearchPipeline";
import { StateBadge } from "@/components/StateBadge";
import { EmptyState, MetricCard, PageHeader, ProviderStatusBadge, SectionCard } from "@/components/ui";
import { getPipeline, getProviderStatus } from "@/lib/api";

export default async function PipelinePage() {
  const [pipeline, providers] = await Promise.all([getPipeline(), getProviderStatus()]);

  return (
    <div className="page">
      <PageHeader
        eyebrow="Research Pipeline"
        title="Review Before Action"
        description="A board for moving names from research to approved thesis, valuation zone, technical wait, hold, trim, or gated action states."
        actions={
          <>
            <ProviderStatusBadge mode={providers.mode} />
            <Link className="button secondary" href="/universe">
              Open screener
            </Link>
          </>
        }
      />

      <section className="section">
        <div className="grid cols-4">
          <MetricCard label="Universe" value={pipeline.summary.total} detail="Local demo names" />
          <MetricCard label="Review queue" value={pipeline.summary.review_queue_count} detail="Items needing attention" tone="warn" />
          <MetricCard label="Gated action states" value={pipeline.summary.action_allowed_count} detail="Still manual and journaled" tone={pipeline.summary.action_allowed_count ? "warn" : "neutral"} />
          <MetricCard label="Blocked" value={pipeline.summary.blocked_count} detail="Hard gate or risk blocker" tone={pipeline.summary.blocked_count ? "danger" : "ok"} />
        </div>
      </section>

      <SectionCard title="Default Stance" description="Pipeline states are research workflow states, not trading instructions.">
        <div className="callout">
          <strong>{pipeline.default_stance}</strong> Score, price movement, and technical movement alone cannot create buy/add permission.
        </div>
      </SectionCard>

      <SectionCard
        title="Priority Review Queue"
        description="Start here before opening the larger board."
        actions={
          <Link href="/" className="button secondary">
            Today
          </Link>
        }
      >
        {pipeline.review_queue.length ? (
          <div className="review-list">
            {pipeline.review_queue.slice(0, 8).map((item) => (
              <Link href={`/universe/${item.ticker}`} key={item.ticker} className="review-item">
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
          <EmptyState title="Queue clear" detail="No review prompts are present in the current demo data." />
        )}
      </SectionCard>

      <SectionCard title="Pipeline Board" description="Grouped by Q-GEAR decision state with reasons, blockers, next task, and evidence provenance.">
        <ResearchPipeline states={pipeline.states} />
      </SectionCard>
    </div>
  );
}
