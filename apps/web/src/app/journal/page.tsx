import { JournalForm } from "@/components/JournalForm";
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
  }>;
};

export default async function JournalPage() {
  const journal = await getJson<JournalResponse>("/journal", { entries: [] });

  return (
    <div className="page">
      <section className="section">
        <div className="section-header">
          <div>
            <h1>Decision Journal</h1>
            <p className="muted">Every decision records action, evidence, thesis, invalidation rule, expected IRR, and review date.</p>
          </div>
          <span className="badge">{journal.entries.length} entries</span>
        </div>
      </section>

      <section className="section split">
        <div className="panel panel-body">
          <h2>Log Decision</h2>
          <JournalForm />
        </div>
        <div>
          <div className="section-header">
            <h2>Recent Entries</h2>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Ticker</th>
                  <th>Action</th>
                  <th>Score</th>
                  <th>Expected IRR</th>
                  <th>Review</th>
                  <th>Evidence</th>
                </tr>
              </thead>
              <tbody>
                {journal.entries.length ? (
                  journal.entries.map((entry) => (
                    <tr key={entry.id}>
                      <td>{entry.entry_date}</td>
                      <td>{entry.ticker}</td>
                      <td>{entry.action}</td>
                      <td>{entry.score.toFixed(1)}</td>
                      <td>{entry.expected_irr_pct.toFixed(1)}%</td>
                      <td>{entry.future_review_date}</td>
                      <td>{entry.evidence}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={7}>No journal entries yet.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  );
}
