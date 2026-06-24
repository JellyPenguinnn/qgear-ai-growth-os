import Link from "next/link";
import { MetricCard, PageHeader, SectionCard } from "@/components/ui";
import { getDataHealth } from "@/lib/api";

export default async function DataHealthPage() {
  const health = await getDataHealth();
  const missingKeys = Object.entries(health.missing_keys).filter(([, value]) => value);

  return (
    <div className="page">
      <PageHeader
        eyebrow="Data Health"
        title="Live, Demo, And Review-Only Data"
        description="Provider status, source quality, missing keys, and which data can support Q-GEAR gates."
        actions={
          <>
            <Link className="button secondary" href="/settings">
              Settings
            </Link>
            <Link className="button secondary" href="/">
              Today
            </Link>
          </>
        }
      />

      <section className="section">
        <div className="grid cols-4">
          <MetricCard label="Mode" value={health.mode.replaceAll("_", " ")} detail="Demo mode runs without keys" />
          <MetricCard label="SEC" value={health.provider_status.providers.company_facts ?? "not configured"} detail="Filings and companyfacts" />
          <MetricCard label="Price history" value={health.provider_status.providers.price_history ?? "not configured"} detail="Technical/risk only" />
          <MetricCard label="AI" value={health.provider_status.ai.provider_metadata.status} detail="Draft-only and explicit" />
        </div>
      </section>

      <SectionCard title="Provider Sections" description="These statuses are research context, not trade instructions.">
        <div className="status-list">
          {health.sections.map((section) => (
            <article className="status-row" key={section.name}>
              <span>
                <strong>{section.name}</strong>
                <small>{section.status}</small>
                <small>{section.note}</small>
              </span>
              <span className={section.can_support_action ? "badge ok" : "badge warn"}>
                {section.can_support_action ? "Can support gates" : "Review only"}
              </span>
            </article>
          ))}
        </div>
      </SectionCard>

      <section className="split">
        <SectionCard title="What Can Support Action Gates" description="Only as one input after thesis, valuation, technical, freshness, and risk checks clear.">
          <ul className="plain-list">
            {health.what_can_support_action.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </SectionCard>

        <SectionCard title="Review-Only Data" description="These inputs may trigger review, but cannot create buy/add permission.">
          <ul className="plain-list">
            {health.review_only_data.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </SectionCard>
      </section>

      <section className="split">
        <SectionCard title="Missing Optional Keys" description="Demo mode works without these keys. Missing keys should not crash the app.">
          {missingKeys.length ? (
            <div className="flag-row">
              {missingKeys.map(([name, value]) => (
                <span className="badge warn" key={name}>
                  {value}
                </span>
              ))}
            </div>
          ) : (
            <p className="ok-text">No missing optional provider keys reported by the local API.</p>
          )}
        </SectionCard>

        <SectionCard title="Macro Series" description="FRED context is review-only and never creates action permission.">
          <div className="flag-row">
            {health.default_fred_series.map((series) => (
              <span className="badge" key={series}>
                {series}
              </span>
            ))}
          </div>
        </SectionCard>
      </section>

      <SectionCard title="Safety Boundary">
        <div className="callout">
          <strong>No auto-trading, no margin, no options-by-default.</strong> Data health improves research quality. It does not execute trades, create investment advice, or override the Q-GEAR hard gates.
        </div>
      </SectionCard>
    </div>
  );
}
