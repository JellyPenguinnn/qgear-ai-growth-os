export default function Loading() {
  return (
    <div className="page">
      <section className="section page-header">
        <div>
          <span className="eyebrow">Loading</span>
          <h1>Preparing Research Workspace</h1>
          <p className="muted">Loading local demo or provider-backed data. No decision state changes are made while this screen loads.</p>
        </div>
      </section>
      <div className="grid cols-3">
        <div className="empty-state">
          <strong>Decision state</strong>
          <span>Waiting for local API data.</span>
        </div>
        <div className="empty-state">
          <strong>Evidence</strong>
          <span>Source metadata will appear when available.</span>
        </div>
        <div className="empty-state">
          <strong>Risk</strong>
          <span>Portfolio checks remain manual-review only.</span>
        </div>
      </div>
    </div>
  );
}
