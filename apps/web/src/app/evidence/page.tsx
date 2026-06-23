import { EvidenceWorkbenchForm } from "@/components/EvidenceWorkbenchForm";
import { MetricCard, PageHeader, ProviderStatusBadge, SectionCard } from "@/components/ui";
import { getProviderStatus } from "@/lib/api";

export default async function EvidenceWorkbenchPage() {
  const providerStatus = await getProviderStatus();
  const aiStatus = providerStatus.ai;

  return (
    <div className="page">
      <PageHeader
        eyebrow="Evidence Workbench"
        title="Verify Before Saving"
        description="Paste a source excerpt, optionally request an AI draft, then edit and save verified evidence into the local research record."
        actions={<ProviderStatusBadge mode={providerStatus.mode} />}
      />

      <section className="section">
        <div className="grid cols-4">
          <MetricCard label="AI provider" value={aiStatus.provider_metadata.mode} detail={aiStatus.ai_enabled ? "Explicit drafts available" : "Manual workflow active"} tone={aiStatus.ai_enabled ? "warn" : "ok"} />
          <MetricCard label="Draft only" value={aiStatus.draft_only ? "Yes" : "No"} detail="AI cannot save or mutate state" tone={aiStatus.draft_only ? "ok" : "danger"} />
          <MetricCard label="Verification" value="Required" detail="User edits before save" tone="warn" />
          <MetricCard label="LOW confidence" value="Blocked for action" detail="Research-only evidence" tone="warn" />
        </div>
      </section>

      <SectionCard title="Evidence Intake" description="AI extraction is optional. Manual verified evidence works when AI is disabled.">
        <div className="callout compact">
          Evidence can improve the research record, but it does not create a buy/add action by itself. Decision state still requires thesis, invalidation rule, valuation, technical confirmation, freshness, and risk budget.
        </div>
        <EvidenceWorkbenchForm aiEnabled={aiStatus.ai_enabled} />
      </SectionCard>
    </div>
  );
}
