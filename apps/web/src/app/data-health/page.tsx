import Link from "next/link";
import { HeroPanel, KeyValueGrid, MetricCard, PageHeader, SectionCard } from "@/components/ui";
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

      <HeroPanel
        eyebrow="Before research"
        title={`${health.mode.replaceAll("_", " ")} data mode`}
        detail="Data health improves confidence in the research record. It does not create buy/add permission or override the decision engine."
        actions={
          <Link className="button secondary" href="/settings">
            Configure providers
          </Link>
        }
      >
        <KeyValueGrid
          items={[
            {
              label: "SEC",
              value: health.provider_status.providers.company_facts ?? "not configured",
              detail: "Filings and company facts",
              tone: health.provider_status.providers.company_facts === "live" ? "ok" : "neutral"
            },
            {
              label: "Prices",
              value: health.provider_status.providers.price_history ?? "not configured",
              detail: "Technical confirmation only",
              tone: health.provider_status.providers.price_history === "live" ? "ok" : "neutral"
            },
            {
              label: "AI",
              value: health.provider_status.ai.provider_metadata.status,
              detail: "Draft-only explicit requests",
              tone: health.provider_status.ai.ai_enabled ? "review" : "neutral"
            },
            {
              label: "Missing keys",
              value: missingKeys.length,
              detail: "Optional; demo mode still works",
              tone: missingKeys.length ? "warn" : "ok"
            }
          ]}
        />
      </HeroPanel>

      <section className="section">
        <div className="grid cols-4">
          <MetricCard label="Mode" value={health.mode.replaceAll("_", " ")} detail="Demo mode runs without keys" />
          <MetricCard label="SEC" value={health.provider_status.providers.company_facts ?? "not configured"} detail="Filings and companyfacts" />
          <MetricCard label="Price history" value={health.provider_status.providers.price_history ?? "not configured"} detail="Technical/risk only" />
          <MetricCard label="AI" value={health.provider_status.ai.provider_metadata.status} detail="Draft-only and explicit" />
        </div>
      </section>

      <SectionCard title="Provider Sections" description="These statuses are research context, not trade instructions.">
        <div className="provider-grid">
          {health.sections.map((section) => (
            <article className="provider-tile" key={section.name}>
              <div className="provider-tile-header">
                <span>
                  <strong>{section.name}</strong>
                  <small>{section.status}</small>
                </span>
                <span className={section.can_support_action ? "badge ok" : "badge warn"}>
                  {section.can_support_action ? "Can support gates" : "Review only"}
                </span>
              </div>
              <p className="muted">{section.note}</p>
            </article>
          ))}
        </div>
      </SectionCard>

      <SectionCard title="Repair Queue" description="Use this as setup guidance. Missing optional data should not crash the app.">
        {missingKeys.length ? (
          <div className="provider-grid">
            {missingKeys.map(([name, value]) => (
              <article className="provider-tile" key={name}>
                <div className="provider-tile-header">
                  <span>
                    <strong>{name.replaceAll("_", " ")}</strong>
                    <small>Optional configuration</small>
                  </span>
                  <span className="badge warn">Missing</span>
                </div>
                <p>{value}</p>
                <small className="muted">Add this only if you want live/provider-assisted research. Demo mode remains valid for local testing.</small>
              </article>
            ))}
          </div>
        ) : (
          <div className="callout ok">
            <strong>No missing optional provider keys reported.</strong> Continue to the research pipeline and still verify source metadata before decisions.
          </div>
        )}
      </SectionCard>

      <SectionCard title="Provider Details" description="Raw section statuses remain available for audit and debugging.">
        <div className="status-list">
          {health.sections.map((section) => (
            <article className="status-row" key={`${section.name}-detail`}>
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
