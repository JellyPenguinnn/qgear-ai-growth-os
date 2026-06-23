import { UniverseScreener } from "@/components/UniverseScreener";
import { PageHeader, ProviderStatusBadge } from "@/components/ui";
import { getProviderStatus, getUniverse } from "@/lib/api";

export default async function UniversePage() {
  const [universe, providers] = await Promise.all([getUniverse(), getProviderStatus()]);

  return (
    <div className="page">
      <PageHeader
        eyebrow="Universe"
        title="AI Infrastructure Research Universe"
        description="Filter by layer, score, state, margins, growth, and drawdown. Seed data is demo research data, not recommendations."
        actions={
          <>
            <ProviderStatusBadge mode={providers.mode} />
            <span className="badge">{universe.count} tickers</span>
          </>
        }
      />
      <UniverseScreener companies={universe.companies} />
    </div>
  );
}
