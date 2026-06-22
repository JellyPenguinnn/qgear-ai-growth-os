import { getJson } from "@/lib/api";

type DailyReport = {
  title: string;
  default_action: string;
  evidence_changes: Array<{
    ticker: string;
    state: string;
    reason: string;
    source?: string;
    source_date?: string;
    confidence?: string;
    disproves_if?: string;
  }>;
  top_alerts?: AlertItem[];
  alert_note?: string;
};

type WeeklyReport = {
  title: string;
  rankings: Array<{ rank: number; ticker: string; score: number; decision_state: string; ai_layer: string }>;
  note: string;
};

type AlertItem = {
  type: string;
  severity: string;
  ticker?: string | null;
  message: string;
  source: string;
  source_date: string;
  confidence: string;
  disproves_if: string;
  trade_instruction: boolean;
};

type AlertsResponse = {
  alerts: AlertItem[];
  note: string;
};

type MonthlyReport = {
  title: string;
  journal_analytics: {
    entry_count: number;
    evidence_backed_count: number;
    unresolved_outcome_count: number;
  };
  alerts: AlertItem[];
  review_prompts: string[];
};

type QuarterlyReport = {
  title: string;
  weakened_or_broken: Array<{ ticker: string; state: string }>;
  earnings_alerts: AlertItem[];
  review_prompts: string[];
};

type AnnualReport = {
  title: string;
  alert_rules: string[];
  benchmark_policy: string;
  backtest_note: string;
  audit_items: string[];
};

export default async function ReportsPage() {
  const [daily, weekly, alerts, monthly, quarterly, annual] = await Promise.all([
    getJson<DailyReport>("/reports/daily", {
      title: "Daily Brief",
      default_action: "No action justified today unless evidence changed.",
      evidence_changes: []
    }),
    getJson<WeeklyReport>("/reports/weekly", {
      title: "Weekly Ranking Report",
      rankings: [],
      note: "High score is not an action."
    }),
    getJson<AlertsResponse>("/alerts", {
      alerts: [],
      note: "Alerts are local review prompts only."
    }),
    getJson<MonthlyReport>("/reports/monthly", {
      title: "Monthly Portfolio Review",
      journal_analytics: { entry_count: 0, evidence_backed_count: 0, unresolved_outcome_count: 0 },
      alerts: [],
      review_prompts: []
    }),
    getJson<QuarterlyReport>("/reports/quarterly", {
      title: "Quarterly Earnings Review",
      weakened_or_broken: [],
      earnings_alerts: [],
      review_prompts: []
    }),
    getJson<AnnualReport>("/reports/annual", {
      title: "Annual Strategy Audit",
      alert_rules: [],
      benchmark_policy: "Compare against SPY, QQQ, XLK, and SMH.",
      backtest_note: "Backtests must avoid look-ahead bias.",
      audit_items: []
    })
  ]);

  return (
    <div className="page">
      <section className="section">
        <div className="section-header">
          <div>
            <h1>Reports</h1>
            <p className="muted">Daily, weekly, monthly, quarterly, and annual review structures for the local process.</p>
          </div>
        </div>
      </section>

      <section className="section grid cols-2">
        <div className="panel panel-body">
          <h2>{daily.title}</h2>
          <p>{daily.default_action}</p>
          {daily.evidence_changes.length ? (
            daily.evidence_changes.map((change) => (
              <p key={change.ticker}>
                <strong>{change.ticker}</strong>: {change.state.replaceAll("_", " ")} · {change.reason}
                {change.source ? (
                  <span className="muted">
                    {" "}
                    Source: {change.source}, {change.source_date}, {change.confidence}. Disproves if: {change.disproves_if}
                  </span>
                ) : null}
              </p>
            ))
          ) : (
            <p className="muted">No action-changing evidence in fallback mode.</p>
          )}
          <p className="muted">{daily.alert_note ?? alerts.note}</p>
        </div>
        <div className="panel panel-body">
          <h2>Alert Queue</h2>
          {(alerts.alerts.length ? alerts.alerts.slice(0, 5) : daily.top_alerts ?? []).map((alert) => (
            <p key={`${alert.type}-${alert.ticker ?? "portfolio"}`}>
              <span className={`badge ${alert.severity === "high" ? "danger" : alert.severity === "medium" ? "warn" : ""}`}>
                {alert.type.replaceAll("_", " ")}
              </span>{" "}
              <strong>{alert.ticker ?? "Portfolio"}</strong>: {alert.message}
              <span className="muted">
                {" "}
                Source: {alert.source}, {alert.source_date}, {alert.confidence}. Trade instruction:{" "}
                {alert.trade_instruction ? "yes" : "no"}.
              </span>
            </p>
          ))}
        </div>
      </section>

      <section className="section grid cols-3">
        <div className="panel panel-body">
          <h2>{monthly.title}</h2>
          <p>
            Journal entries: <strong>{monthly.journal_analytics.entry_count}</strong>
          </p>
          <p>
            Evidence-backed: <strong>{monthly.journal_analytics.evidence_backed_count}</strong>
          </p>
          <p>
            Unresolved outcomes: <strong>{monthly.journal_analytics.unresolved_outcome_count}</strong>
          </p>
          <p className="muted">{monthly.review_prompts[0] ?? "Review concentration, cash, drawdown, and journal discipline."}</p>
        </div>
        <div className="panel panel-body">
          <h2>{quarterly.title}</h2>
          <p>
            Weakened or broken theses: <strong>{quarterly.weakened_or_broken.length}</strong>
          </p>
          <p>
            Earnings risk alerts: <strong>{quarterly.earnings_alerts.length}</strong>
          </p>
          <p className="muted">{quarterly.review_prompts[0] ?? "Review earnings thesis changes and invalidation rules."}</p>
        </div>
        <div className="panel panel-body">
          <h2>{annual.title}</h2>
          <p>{annual.benchmark_policy}</p>
          <p className="muted">{annual.backtest_note}</p>
          <p>
            Alert rules tracked: <strong>{annual.alert_rules.length}</strong>
          </p>
        </div>
      </section>

      <section className="section">
        <div className="section-header">
          <h2>{weekly.title}</h2>
          <span className="badge">{weekly.note}</span>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Rank</th>
                <th>Ticker</th>
                <th>Score</th>
                <th>State</th>
                <th>AI layer</th>
              </tr>
            </thead>
            <tbody>
              {weekly.rankings.map((row) => (
                <tr key={row.ticker}>
                  <td>{row.rank}</td>
                  <td>{row.ticker}</td>
                  <td>{row.score.toFixed(1)}</td>
                  <td>{row.decision_state.replaceAll("_", " ")}</td>
                  <td>{row.ai_layer.replaceAll("_", " ")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
