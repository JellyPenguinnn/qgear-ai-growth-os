"use client";

export default function Error({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <div className="page">
      <section className="section page-header">
        <div>
          <span className="eyebrow">Recovery</span>
          <h1>Workspace Could Not Load</h1>
          <p className="muted">The local research page hit an error. No decision state was changed.</p>
        </div>
      </section>
      <section className="section-card">
        <div className="callout danger compact">
          <strong>Review needed.</strong> Check that the API is running and that demo/provider data is available.
        </div>
        <p className="muted">{error.message || "Unknown local UI error."}</p>
        <button className="button" type="button" onClick={reset}>
          Retry page
        </button>
      </section>
    </div>
  );
}
