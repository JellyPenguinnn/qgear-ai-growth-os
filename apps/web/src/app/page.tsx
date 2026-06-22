import Link from "next/link";
import { StateBadge } from "@/components/StateBadge";
import { getPortfolio, getProviderStatus, getUniverse } from "@/lib/api";

export default async function DashboardPage() {
  const [universe, portfolio, providers] = await Promise.all([getUniverse(), getPortfolio(), getProviderStatus()]);
  const ranked = [...universe.companies].sort((a, b) => b.score.total - a.score.total).slice(0, 8);
  const actionAllowed = universe.companies.filter((company) => ["STARTER_ALLOWED", "ADD_ALLOWED"].includes(company.status));

  return (
    <div className="page">
      <section className="section">
        <div className="section-header">
          <div>
            <h1>Research Dashboard</h1>
            <p className="muted">Evidence-first AI infrastructure watchlist, decision gates, risk budget, and journal workflows.</p>
          </div>
          <Link className="button secondary" href="/settings">
            Onboarding settings
          </Link>
        </div>
        <div className="grid cols-4">
          <div className="panel panel-body metric">
            <span>Universe</span>
            <strong>{universe.count}</strong>
            <span>Demo tickers classified</span>
          </div>
          <div className="panel panel-body metric">
            <span>Total equity</span>
            <strong>${portfolio.total_equity.toLocaleString()}</strong>
            <span>Manual local portfolio</span>
          </div>
          <div className="panel panel-body metric">
            <span>Drawdown mode</span>
            <strong>{portfolio.drawdown_mode.replaceAll("_", " ")}</strong>
            <span>{portfolio.drawdown_pct.toFixed(1)}% current drawdown</span>
          </div>
          <div className="panel panel-body metric">
            <span>Action-changing evidence</span>
            <strong>{actionAllowed.length}</strong>
            <span>No action unless evidence changed</span>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="callout">
          <strong>Daily stance:</strong> No action justified today unless thesis, earnings, valuation, technical regime, evidence freshness, and risk budget all clear.
        </div>
      </section>

      <section className="section">
        <div className="section-header">
          <div>
            <h2>Data Provenance</h2>
            <p className="muted">Provider mode and safety status for local research data.</p>
          </div>
          <Link href="/reports" className="button secondary">
            Review reports
          </Link>
        </div>
        <div className="grid cols-4">
          <div className="panel panel-body metric">
            <span>Mode</span>
            <strong>{providers.mode.replaceAll("_", " ")}</strong>
            <span>Live data optional</span>
          </div>
          <div className="panel panel-body metric">
            <span>SEC filings</span>
            <strong>{providers.providers.filings ?? "not configured"}</strong>
            <span>Source metadata required</span>
          </div>
          <div className="panel panel-body metric">
            <span>Prices</span>
            <strong>{providers.providers.prices ?? "not configured"}</strong>
            <span>Mock snapshots in demo mode</span>
          </div>
          <div className="panel panel-body metric">
            <span>Safety</span>
            <strong>{providers.safety.auto_trading}</strong>
            <span>Auto-trading, margin, and options disabled</span>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-header">
          <h2>Top Demo Rankings</h2>
          <Link href="/universe" className="button secondary">
            Open screener
          </Link>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Ticker</th>
                <th>Layer</th>
                <th>Score</th>
                <th>State</th>
                <th>Evidence summary</th>
              </tr>
            </thead>
            <tbody>
              {ranked.map((company) => (
                <tr key={company.ticker}>
                  <td>
                    <Link href={`/universe/${company.ticker}`}>
                      <strong>{company.ticker}</strong>
                    </Link>
                  </td>
                  <td>{company.ai_layer.replaceAll("_", " ")}</td>
                  <td>{company.score.total.toFixed(1)}</td>
                  <td>
                    <StateBadge state={company.status} />
                  </td>
                  <td>{company.evidence_summary}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
