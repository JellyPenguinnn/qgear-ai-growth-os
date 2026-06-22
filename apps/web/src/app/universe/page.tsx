import { UniverseScreener } from "@/components/UniverseScreener";
import { getUniverse } from "@/lib/api";

export default async function UniversePage() {
  const universe = await getUniverse();

  return (
    <div className="page">
      <section className="section">
        <div className="section-header">
          <div>
            <h1>AI Universe Screener</h1>
            <p className="muted">Filter by layer, score, decision state, margins, growth, and drawdown. Seed data is demo research data.</p>
          </div>
          <span className="badge">{universe.count} tickers</span>
        </div>
      </section>
      <UniverseScreener companies={universe.companies} />
    </div>
  );
}
