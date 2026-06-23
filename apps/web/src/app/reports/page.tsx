import { EmptyState, MetricCard, PageHeader, SectionCard } from "@/components/ui";
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
    followed_system_rate_pct?: number;
    average_process_score?: number;
  };
  blocked_adds?: Array<{ ticker: string; reason: string; state: string; trade_instruction: false }>;
  review_calendar?: Array<{ ticker: string; next_review_date: string; thesis_status: string; status: string }>;
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
      blocked_adds: [],
      review_calendar: [],
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
      <PageHeader
        eyebrow="Reports"
        title="Review Cadence"
        description="Daily, weekly, monthly, quarterly, and annual reports for a local research process. Reports are not trading instructions."
      />

      <section className="section grid cols-2">
        <SectionCard title={daily.title} description="Usually says no action unless evidence changed.">
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
        </SectionCard>
        <SectionCard title="Alert Queue" description="Review prompts only. Open evidence before journaling any state change.">
          {(alerts.alerts.length ? alerts.alerts.slice(0, 5) : daily.top_alerts ?? []).map((alert) => (
            <p key={`${alert.type}-${alert.ticker ?? "portfolio"}`}>
              <span className={`badge ${alert.severity === "high" ? "danger" : alert.severity === "medium" ? "warn" : ""}`}>
                {alert.type.replaceAll("_", " ")}
              </span>{" "}
              <strong>{alert.ticker ?? "Portfolio"}</strong>: {alert.message}
              <span className="muted">
                {" "}
                Source: {alert.source}, {alert.source_date}, {alert.confidence}. Review prompt only.
              </span>
            </p>
          ))}
        </SectionCard>
      </section>

      <section className="section grid cols-3">
        <SectionCard title={monthly.title}>
          <div className="metric-stack">
            <MetricCard label="Journal entries" value={monthly.journal_analytics.entry_count} detail="Local records" />
            <MetricCard label="Evidence-backed" value={monthly.journal_analytics.evidence_backed_count} detail="Contains evidence text" />
            <MetricCard label="Unresolved outcomes" value={monthly.journal_analytics.unresolved_outcome_count} detail="Needs later review" />
          </div>
          <div className="review-list compact">
            {(monthly.review_prompts.length ? monthly.review_prompts : ["Review concentration, cash, drawdown, and journal discipline."]).map((prompt) => (
              <p key={prompt}>{prompt}</p>
            ))}
          </div>
          {(monthly.blocked_adds ?? []).slice(0, 3).map((item) => (
            <p className="warn-text" key={`${item.ticker}-${item.reason}`}>
              <strong>{item.ticker}</strong>: {item.reason}
            </p>
          ))}
          {(monthly.review_calendar ?? []).slice(0, 3).map((item) => (
            <p key={`${item.ticker}-${item.next_review_date}`}>
              <strong>{item.ticker}</strong> review: {item.next_review_date} · {item.thesis_status}
            </p>
          ))}
        </SectionCard>
        <SectionCard title={quarterly.title}>
          <div className="metric-stack">
            <MetricCard label="Weakened/broken" value={quarterly.weakened_or_broken.length} detail="Thesis review required" tone={quarterly.weakened_or_broken.length ? "warn" : "neutral"} />
            <MetricCard label="Earnings risk alerts" value={quarterly.earnings_alerts.length} detail="Review prompts" tone={quarterly.earnings_alerts.length ? "warn" : "neutral"} />
          </div>
          {(quarterly.review_prompts.length ? quarterly.review_prompts : ["Review earnings thesis changes and invalidation rules."]).map((prompt) => (
            <p key={prompt}>{prompt}</p>
          ))}
          {quarterly.weakened_or_broken.slice(0, 4).map((item) => (
            <p className="warn-text" key={item.ticker}>
              <strong>{item.ticker}</strong>: {item.state}
            </p>
          ))}
        </SectionCard>
        <SectionCard title={annual.title}>
          <p>{annual.benchmark_policy}</p>
          <p className="muted">{annual.backtest_note}</p>
          <p>
            Alert rules tracked: <strong>{annual.alert_rules.length}</strong>
          </p>
        </SectionCard>
      </section>

      <SectionCard title={weekly.title} description={weekly.note}>
        {weekly.rankings.length ? (
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
        ) : (
          <EmptyState title="No weekly ranking data" detail="Fallback mode has not loaded rankings from the API." />
        )}
      </SectionCard>
    </div>
  );
}
