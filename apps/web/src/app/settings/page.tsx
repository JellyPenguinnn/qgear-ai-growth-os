import { SettingsForm } from "@/components/SettingsForm";

export default function SettingsPage() {
  return (
    <div className="page">
      <section className="section">
        <div className="section-header">
          <div>
            <h1>Onboarding Settings</h1>
            <p className="muted">Set the local research assumptions for a USD 10,000 Singapore/Malaysia-oriented portfolio.</p>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="panel panel-body">
          <SettingsForm />
        </div>
      </section>

      <section className="section">
        <div className="callout">
          This tool is for personal research and educational use only. It does not provide licensed financial advice, tax advice, or legal advice. Final investment decisions are made by the user.
        </div>
      </section>
    </div>
  );
}
