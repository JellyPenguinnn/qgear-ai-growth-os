import { PositionForm } from "@/components/PositionForm";
import { StateBadge } from "@/components/StateBadge";
import { getPortfolio } from "@/lib/api";

export default async function PortfolioPage() {
  const portfolio = await getPortfolio();

  return (
    <div className="page">
      <section className="section">
        <div className="section-header">
          <div>
            <h1>Portfolio Risk</h1>
            <p className="muted">Manual local portfolio with concentration, drawdown mode, and benchmark placeholders.</p>
          </div>
          <StateBadge state={portfolio.drawdown_mode === "HARD_AUDIT" ? "BLOCKED_BY_RISK" : "HOLD"} />
        </div>
        <div className="grid cols-4">
          <div className="panel panel-body metric">
            <span>Cash</span>
            <strong>${portfolio.cash.toLocaleString()}</strong>
            <span>Default buffer target 10-20%</span>
          </div>
          <div className="panel panel-body metric">
            <span>Total equity</span>
            <strong>${portfolio.total_equity.toLocaleString()}</strong>
            <span>Manual holdings plus cash</span>
          </div>
          <div className="panel panel-body metric">
            <span>Drawdown</span>
            <strong>{portfolio.drawdown_pct.toFixed(1)}%</strong>
            <span>{portfolio.drawdown_mode.replaceAll("_", " ")}</span>
          </div>
          <div className="panel panel-body metric">
            <span>Single-stock concentration</span>
            <strong>{portfolio.single_stock_concentration_pct.toFixed(1)}%</strong>
            <span>Absolute cap 15%</span>
          </div>
        </div>
      </section>

      <section className="section split">
        <div>
          <div className="section-header">
            <h2>Positions</h2>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Ticker</th>
                  <th>Shares</th>
                  <th>Avg cost</th>
                  <th>Current</th>
                  <th>Market value</th>
                  <th>P/L</th>
                  <th>Weight</th>
                  <th>Status</th>
                  <th>Review</th>
                </tr>
              </thead>
              <tbody>
                {portfolio.positions.length ? (
                  portfolio.positions.map((position) => (
                    <tr key={position.id}>
                      <td>{position.ticker}</td>
                      <td>{position.shares}</td>
                      <td>${position.average_cost.toFixed(2)}</td>
                      <td>${position.current_price.toFixed(2)}</td>
                      <td>${position.market_value.toFixed(2)}</td>
                      <td className={position.unrealized_pl >= 0 ? "ok-text" : "danger-text"}>${position.unrealized_pl.toFixed(2)}</td>
                      <td>{position.position_weight_pct.toFixed(1)}%</td>
                      <td>{position.status}</td>
                      <td>{position.next_review_date}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={9}>No manual positions recorded yet.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
        <div className="panel panel-body">
          <h2>Record Position</h2>
          <PositionForm />
        </div>
      </section>
    </div>
  );
}
