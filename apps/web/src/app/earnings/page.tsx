import { StateBadge } from "@/components/StateBadge";
import { EarningsReviewForm } from "@/components/EarningsReviewForm";
import { getJson } from "@/lib/api";

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
  const lab = await getJson<EarningsLabResponse>("/earnings", {
    checklist: [
      "Confirm revenue and EPS beat/miss.",
      "Compare guidance to prior expectations.",
      "Classify thesis status change before action."
    ],
    demo_events: []
  });

  return (
    <div className="page">
      <section className="section">
        <div className="section-header">
          <div>
            <h1>Earnings Lab</h1>
            <p className="muted">Pre-earnings checklists and post-earnings thesis classification. Earnings can strengthen, leave unchanged, weaken, or break a thesis.</p>
          </div>
        </div>
      </section>

      <section className="section grid cols-2">
        <div className="panel panel-body">
          <h2>Checklist</h2>
          {lab.checklist.map((item) => (
            <p key={item}>{item}</p>
          ))}
        </div>
        <div className="panel panel-body">
          <h2>Action Rules</h2>
          <p>Revenue acceleration, AI evidence, margin expansion, FCF improvement, and raised guidance may strengthen the thesis.</p>
          <p>Guidance cuts, unexplained margin deterioration, stale evidence, or broken technical regime block buy/add.</p>
          <p>Stored reviews: {lab.stored_review_count ?? 0}</p>
        </div>
      </section>

      <section className="section">
        <div className="section-header">
          <div>
            <h2>Manual Earnings Review</h2>
            <p className="muted">Record sourced evidence before any thesis or action change. The backend classifies thesis impact; buy/add still requires all hard gates.</p>
          </div>
        </div>
        <div className="panel panel-body">
          <EarningsReviewForm />
        </div>
      </section>

      <section className="section">
        <div className="section-header">
          <h2>Demo Earnings Events</h2>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Ticker</th>
                <th>Company</th>
                <th>Thesis change</th>
                <th>Score</th>
                <th>Action change</th>
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
      </section>
    </div>
  );
}
