import Link from "next/link";

export default function NotFound() {
  return (
    <div className="page">
      <section className="section page-header">
        <div>
          <span className="eyebrow">Not found</span>
          <h1>Research Page Not Available</h1>
          <p className="muted">The requested local workbench or route could not be found. No action is justified from a missing page.</p>
        </div>
      </section>
      <div className="empty-state">
        <strong>Return to the pipeline</strong>
        <span>Open an available demo ticker, review source metadata, and journal only verified decisions.</span>
        <Link className="button secondary" href="/pipeline">
          Open pipeline
        </Link>
      </div>
    </div>
  );
}
