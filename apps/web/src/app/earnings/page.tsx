import { AIEarningsSummaryForm } from "@/components/AIEarningsSummaryForm";
import { EarningsReviewForm } from "@/components/EarningsReviewForm";
import { StateBadge } from "@/components/StateBadge";
import { MetricCard, PageHeader, ProviderStatusBadge, SectionCard } from "@/components/ui";
import { getJson, getProviderStatus } from "@/lib/api";

type EarningsLabResponse = {
  checklist: string[];
  demo_events: Array<{
    ticker: string;
    company_name: string;
    thesis_status_change: string;
    score: number;
    action_change: string;
  }>;
  stored_review_count?: number;
};

export default async function EarningsPage() {
  const [lab, providerStatus] = await Promise.all([
    getJson<EarningsLabResponse>("/earnings", {
      checklist: [
        "Confirm revenue and EPS beat/miss.",
        "Compare guidance to prior expectations.",
        "Classify thesis status change before action."
      ],
      demo_events: []
    }),
    getProviderStatus()
  ]);
  const aiStatus = providerStatus.ai;
  const weakenedCount = lab.demo_events.filter((event) => ["WEAKENED", "BROKEN"].includes(event.thesis_status_change)).length;

  return (
    <div className="page">
      <PageHeader
        eyebrow="Earnings"
        title="Earnings Review Lab"
        description="A guided workflow for pre-earnings expectations, post-earnings evidence, thesis classification, blockers, and journal drafts."
        actions={<ProviderStatusBadge mode={providerStatus.mode} />}
      />

      <section className="section">
        <div className="grid cols-4">
          <MetricCard label="Stored reviews" value={lab.stored_review_count ?? 0} detail="Local/manual earnings records" />
          <MetricCard label="AI summary" value={aiStatus.ai_enabled ? "Available" : "Disabled"} detail="Draft-only, explicit request" tone={aiStatus.ai_enabled ? "warn" : "ok"} />
          <MetricCard label="Weak/Broken demos" value={weakenedCount} detail="Buy/add blocked until repaired" tone={weakenedCount ? "danger" : "ok"} />
          <MetricCard label="Journal draft" value="Manual" detail="Generated after review save" tone="warn" />
        </div>
      </section>

      <section className="section grid cols-2">
        <SectionCard title="Before Earnings" description="Define what evidence would matter before the report arrives.">
          {lab.checklist.map((item) => (
            <p key={item}>{item}</p>
          ))}
          <p className="muted">Write the invalidation rule before interpreting the report. Price movement after earnings is not thesis evidence.</p>
        </SectionCard>
        <SectionCard title="After Earnings" description="Classify thesis impact before thinking about sizing.">
          <p>Strengthening evidence can include accelerated revenue, measurable AI demand, raised guidance, margin expansion, or FCF improvement.</p>
          <p>Weakening evidence includes structural guidance cuts, unexplained margin deterioration, weakening AI demand, or stale source data.</p>
          <p className="warn-text">A strengthened thesis still requires valuation, technical confirmation, evidence freshness, and portfolio risk budget.</p>
        </SectionCard>
      </section>

      <SectionCard title="AI Earnings Draft" description="Optional. AI can summarize supplied text, but the user must verify every output before saving.">
        <AIEarningsSummaryForm aiEnabled={aiStatus.ai_enabled} />
      </SectionCard>

      <SectionCard
        title="Manual Post-Earnings Review"
        description="Save sourced evidence and deterministic thesis classification. This does not auto-save a journal entry or create buy/add permission."
      >
        <EarningsReviewForm />
      </SectionCard>

      <section className="section grid cols-2">
        <SectionCard title="Decision Blockers" description="Earnings status feeds the decision engine but cannot override hard gates.">
          <p>WEAKENED or BROKEN thesis status blocks starter/add actions.</p>
          <p>Fresh positive evidence must be structured with source, source date, confidence, and disproof criteria.</p>
          <p>LOW-confidence evidence can be tracked, but cannot support action-changing decisions.</p>
        </SectionCard>
        <SectionCard title="Journal Discipline" description="Record the process even when the correct action is no action.">
          <p>Journal the thesis status change, evidence, invalidation rule, expected IRR, next review date, and later outcome.</p>
          <p className="muted">The app drafts journal language after manual review save, but the user decides whether to save it.</p>
        </SectionCard>
      </section>

      <SectionCard title="Demo Earnings Context" description="Demo status is for workflow testing and not a recommendation.">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Ticker</th>
                <th>Company</th>
                <th>Thesis change</th>
                <th>Score</th>
                <th>Decision state</th>
              </tr>
            </thead>
            <tbody>
              {lab.demo_events.map((event) => (
                <tr key={event.ticker}>
                  <td>{event.ticker}</td>
                  <td>{event.company_name}</td>
                  <td>{event.thesis_status_change}</td>
                  <td>{event.score.toFixed(1)}</td>
                  <td>
                    <StateBadge state={event.action_change} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </SectionCard>
    </div>
  );
}
