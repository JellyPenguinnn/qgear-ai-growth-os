import { SettingsForm } from "@/components/SettingsForm";
import { MetricCard, PageHeader, SectionCard } from "@/components/ui";
import { getProviderStatus } from "@/lib/api";

export default async function SettingsPage() {
  const providerStatus = await getProviderStatus();
  const aiStatus = providerStatus.ai;

  return (
    <div className="page">
      <PageHeader
        eyebrow="Settings"
        title="Onboarding Settings"
        description="Set local research assumptions for a USD 10,000 Singapore/Malaysia-oriented portfolio."
      />

      <section className="section">
        <SectionCard title="Strategy Settings" description="These are personal research assumptions and risk controls, not performance promises.">
          <SettingsForm />
        </SectionCard>
      </section>

      <section className="section grid cols-3">
        <MetricCard label="Auto-trading" value="Disabled" detail="No broker execution layer" tone="ok" />
        <MetricCard label="Margin" value="Disabled" detail="No margin workflow" tone="ok" />
        <MetricCard label="Options" value="Disabled" detail="Disabled by default" tone="ok" />
      </section>

      <SectionCard title="AI Research Assistance" description="AI is optional, explicit, draft-only, and disabled by default.">
        <div className="grid cols-4">
          <MetricCard
            label="Provider"
            value={aiStatus.provider_metadata.mode}
            detail={aiStatus.ai_enabled ? "Configured for explicit requests" : "Disabled by default"}
            tone={aiStatus.ai_enabled ? "warn" : "ok"}
          />
          <MetricCard label="Draft only" value={aiStatus.draft_only ? "Yes" : "No"} detail="User verification required" tone={aiStatus.draft_only ? "ok" : "danger"} />
          <MetricCard
            label="External acknowledgement"
            value={aiStatus.requires_external_ai_acknowledgement ? "Required" : "Not active"}
            detail="Needed before sending text to OpenAI"
            tone="warn"
          />
          <MetricCard
            label="Decision mutation"
            value={aiStatus.mutates_decision_state ? "Possible" : "Never"}
            detail="AI routes do not write decisions"
            tone={aiStatus.mutates_decision_state ? "danger" : "ok"}
          />
        </div>
        <p className="muted compact">{aiStatus.external_upload_policy}</p>
      </SectionCard>

      <SectionCard title="Disclaimer">
        <div className="callout">
          This tool is for personal research and educational use only. It does not provide licensed financial advice, tax advice, or legal advice. Final investment decisions are made by the user.
        </div>
      </SectionCard>
    </div>
  );
}
