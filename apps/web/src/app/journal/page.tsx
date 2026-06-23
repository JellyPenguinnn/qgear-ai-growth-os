import { JournalForm } from "@/components/JournalForm";
import { EmptyState, MetricCard, PageHeader, SectionCard } from "@/components/ui";
import { getJson } from "@/lib/api";

type JournalResponse = {
  entries: Array<{
    id: number;
    entry_date: string;
    ticker: string;
    action: string;
    price: number;
    position_size_pct: number;
    score: number;
    evidence: string;
    thesis: string;
    invalidation_rule: string;
    expected_irr_pct: number;
    future_review_date: string;
    later_outcome: string;
    decision_outcome: string;
    mistake_category: string;
    evidence_quality: string;
    followed_system: boolean;
    later_review: string;
    process_score: number;
  }>;
};

type JournalAnalytics = {
  entry_count: number;
  action_counts: Record<string, number>;
  evidence_backed_count: number;
  unresolved_outcome_count: number;
  outcome_counts: Record<string, number>;
  mistake_counts: Record<string, number>;
  evidence_quality_counts: Record<string, number>;
  followed_system_rate_pct: number;
  average_process_score: number;
  unresolved_later_review_count: number;
  process_note: string;
};

export default async function JournalPage() {
  const [journal, analytics] = await Promise.all([
    getJson<JournalResponse>("/journal", { entries: [] }),
    getJson<JournalAnalytics>("/journal/analytics", {
      entry_count: 0,
      action_counts: {},
      evidence_backed_count: 0,
      unresolved_outcome_count: 0,
      outcome_counts: {},
      mistake_counts: {},
      evidence_quality_counts: {},
      followed_system_rate_pct: 0,
      average_process_score: 0,
      unresolved_later_review_count: 0,
      process_note: "Analytics unavailable in fallback mode."
    })
  ]);

  return (
    <div className="page">
      <PageHeader
        eyebrow="Journal"
        title="Decision Journal"
        description="Record evidence, thesis, invalidation rule, expected IRR, position size, and future review. No action is a valid entry."
        actions={<span className="badge">{journal.entries.length} entries</span>}
      />

      <section className="section">
        <div className="grid cols-4">
          <MetricCard label="Evidence-backed" value={analytics.evidence_backed_count} detail={`${analytics.entry_count} total entries`} />
          <MetricCard label="Followed system" value={`${analytics.followed_system_rate_pct.toFixed(1)}%`} detail="Self-reviewed process discipline" tone={analytics.followed_system_rate_pct >= 80 ? "ok" : "warn"} />
          <MetricCard label="Avg process score" value={analytics.average_process_score.toFixed(1)} detail="0-100 self-review" tone={analytics.average_process_score >= 75 ? "ok" : "warn"} />
          <MetricCard label="Unresolved reviews" value={analytics.unresolved_later_review_count} detail="Needs later outcome review" tone={analytics.unresolved_later_review_count ? "warn" : "neutral"} />
        </div>
      </section>

      <section className="section split">
        <SectionCard title="Log Decision" description="Journal the process. STARTER_ALLOWED and ADD_ALLOWED are decision states, not broker commands.">
          <JournalForm />
        </SectionCard>
        <div>
          <SectionCard title="Process Analytics" description={analytics.process_note}>
            <div className="grid cols-3">
              <div>
                <h3>Action Mix</h3>
                {Object.entries(analytics.action_counts).length ? (
                  Object.entries(analytics.action_counts).map(([action, count]) => (
                    <p key={action}>
                      {action}: {count}
                    </p>
                  ))
                ) : (
                  <p className="muted">No journal entries yet.</p>
                )}
              </div>
              <div>
                <h3>Evidence Quality</h3>
                {Object.entries(analytics.evidence_quality_counts).length ? (
                  Object.entries(analytics.evidence_quality_counts).map(([quality, count]) => (
                    <p key={quality}>
                      {quality}: {count}
                    </p>
                  ))
                ) : (
                  <p className="muted">No evidence quality tags yet.</p>
                )}
              </div>
              <div>
                <h3>Mistakes</h3>
                {Object.entries(analytics.mistake_counts).length ? (
                  Object.entries(analytics.mistake_counts).map(([mistake, count]) => (
                    <p key={mistake}>
                      {mistake.replaceAll("_", " ")}: {count}
                    </p>
                  ))
                ) : (
                  <p className="muted">No mistake categories recorded.</p>
                )}
              </div>
            </div>
          </SectionCard>

          <SectionCard title="Recent Entries" description="Local audit trail for decisions and non-decisions.">
            {journal.entries.length ? (
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Ticker</th>
                      <th>State</th>
                      <th>Score</th>
                      <th>Expected IRR</th>
                      <th>Process</th>
                      <th>Quality</th>
                      <th>Review</th>
                      <th>Evidence</th>
                    </tr>
                  </thead>
                  <tbody>
                    {journal.entries.map((entry) => (
                    <tr key={entry.id}>
                      <td>{entry.entry_date}</td>
                      <td>{entry.ticker}</td>
                      <td>{entry.action}</td>
                      <td>{entry.score.toFixed(1)}</td>
                      <td>{entry.expected_irr_pct.toFixed(1)}%</td>
                      <td>{entry.followed_system ? "Followed" : "Missed"} · {entry.process_score.toFixed(0)}</td>
                      <td>{entry.evidence_quality}</td>
                      <td>{entry.future_review_date}</td>
                      <td>{entry.evidence}</td>
                    </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <EmptyState title="No journal entries yet" detail="Start with a NO_ACTION entry when no evidence changed." />
            )}
          </SectionCard>
        </div>
      </section>
    </div>
  );
}
