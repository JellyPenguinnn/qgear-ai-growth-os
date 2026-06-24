import type { ReactNode } from "react";
import { StateBadge } from "./StateBadge";
import type { DecisionState, EvidenceObject } from "@/lib/types";

export function PageHeader({
  eyebrow,
  title,
  description,
  actions
}: {
  eyebrow?: string;
  title: string;
  description: string;
  actions?: ReactNode;
}) {
  return (
    <section className="section page-header">
      <div>
        {eyebrow ? <span className="eyebrow">{eyebrow}</span> : null}
        <h1>{title}</h1>
        <p className="muted">{description}</p>
      </div>
      {actions ? <div className="header-actions">{actions}</div> : null}
    </section>
  );
}

export function SectionCard({
  title,
  description,
  children,
  actions,
  className = ""
}: {
  title?: string;
  description?: string;
  children: ReactNode;
  actions?: ReactNode;
  className?: string;
}) {
  return (
    <section className={`section-card ${className}`}>
      {title || description || actions ? (
        <div className="card-header">
          <div>
            {title ? <h2>{title}</h2> : null}
            {description ? <p className="muted">{description}</p> : null}
          </div>
          {actions}
        </div>
      ) : null}
      {children}
    </section>
  );
}

export function MetricCard({
  label,
  value,
  detail,
  tone = "neutral"
}: {
  label: string;
  value: string | number;
  detail: string;
  tone?: "neutral" | "ok" | "warn" | "danger";
}) {
  return (
    <div className={`metric-card ${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </div>
  );
}

export function ProviderStatusBadge({ mode }: { mode: string }) {
  const label = mode.replaceAll("_", " ");
  const tone = mode === "live" ? "ok" : mode === "mixed" ? "warn" : "";
  return <span className={`provider-badge ${tone}`}>Data mode: {label}</span>;
}

export function EmptyState({ title, detail }: { title: string; detail: string }) {
  return (
    <div className="empty-state">
      <strong>{title}</strong>
      <span>{detail}</span>
    </div>
  );
}

export function BlockerList({ blockers, empty = "No hard blockers surfaced." }: { blockers: string[]; empty?: string }) {
  if (!blockers.length) {
    return <p className="ok-text">{empty}</p>;
  }
  return (
    <ul className="blocker-list">
      {blockers.map((blocker) => (
        <li key={blocker}>{blocker}</li>
      ))}
    </ul>
  );
}

export function HeroPanel({
  eyebrow,
  title,
  detail,
  children,
  actions
}: {
  eyebrow: string;
  title: string;
  detail: string;
  children?: ReactNode;
  actions?: ReactNode;
}) {
  return (
    <section className="hero-panel">
      <div>
        <span className="eyebrow">{eyebrow}</span>
        <h2>{title}</h2>
        <p>{detail}</p>
      </div>
      {children ? <div className="hero-panel-body">{children}</div> : null}
      {actions ? <div className="hero-panel-actions">{actions}</div> : null}
    </section>
  );
}

export function KeyValueGrid({ items }: { items: Array<{ label: string; value: ReactNode; detail?: ReactNode; tone?: "neutral" | "ok" | "warn" | "danger" | "review" }> }) {
  return (
    <div className="key-grid">
      {items.map((item) => (
        <div className={`key-item ${item.tone ?? "neutral"}`} key={item.label}>
          <span>{item.label}</span>
          <strong>{item.value}</strong>
          {item.detail ? <small>{item.detail}</small> : null}
        </div>
      ))}
    </div>
  );
}

export function StepList({ steps }: { steps: Array<{ title: string; detail: string; tone?: "neutral" | "ok" | "warn" | "danger" }> }) {
  return (
    <ol className="step-list">
      {steps.map((step, index) => (
        <li className={step.tone ?? "neutral"} key={step.title}>
          <span>{index + 1}</span>
          <strong>{step.title}</strong>
          <p>{step.detail}</p>
        </li>
      ))}
    </ol>
  );
}

export function DecisionCard({
  state,
  score,
  reasons,
  blockers,
  nextTask,
  maxNewMoney,
  evidenceQuality,
  nextReview
}: {
  state: DecisionState;
  score: number;
  reasons: string[];
  blockers: string[];
  nextTask: string;
  maxNewMoney: number;
  evidenceQuality?: string;
  nextReview?: string;
}) {
  return (
    <section className="decision-card">
      <div className="decision-card-main">
        <span className="eyebrow">Decision state</span>
        <div className="decision-title">
          <StateBadge state={state} />
          <strong>{score.toFixed(1)}</strong>
        </div>
        <p>{reasons[0] ?? "No action justified without fresh evidence and all gates clear."}</p>
        <small>Decision state is a research workflow result, not broker execution.</small>
      </div>
      <div className="decision-card-side">
        <span className="eyebrow">Blocked because</span>
        <BlockerList blockers={blockers} empty="No blocker, but journal discipline still applies." />
        <span className="eyebrow">Next research task</span>
        <p>{nextTask}</p>
        <div className="decision-facts">
          <span>
            <span className="eyebrow">Evidence quality</span>
            <p>{evidenceQuality ?? "Evidence quality not available."}</p>
          </span>
          <span>
            <span className="eyebrow">Next review</span>
            <p>{nextReview ?? "Set after thesis approval."}</p>
          </span>
          <span>
            <span className="eyebrow">Max new money</span>
            <p>${maxNewMoney.toLocaleString()}</p>
          </span>
        </div>
      </div>
    </section>
  );
}

export function EvidenceCard({ item }: { item: EvidenceObject }) {
  const tone = item.confidence === "HIGH" ? "ok" : item.confidence === "MEDIUM" ? "warn" : "danger";
  return (
    <article className={`evidence-card ${tone}`}>
      <div>
        <span className="eyebrow">Evidence</span>
        <h3>{item.claim}</h3>
        <p>{item.evidence}</p>
      </div>
      <dl>
        <div>
          <dt>Source</dt>
          <dd>{item.source}</dd>
        </div>
        <div>
          <dt>Date</dt>
          <dd>{item.source_date}</dd>
        </div>
        <div>
          <dt>Confidence</dt>
          <dd>{item.confidence}</dd>
        </div>
        {item.source_type ? (
          <div>
            <dt>Type</dt>
            <dd>{item.source_type.replaceAll("_", " ")}</dd>
          </div>
        ) : null}
        {item.verification_status ? (
          <div>
            <dt>Verification</dt>
            <dd>{item.verification_status.replaceAll("_", " ")}</dd>
          </div>
        ) : null}
        {item.provider ? (
          <div>
            <dt>Provider</dt>
            <dd>{item.provider}</dd>
          </div>
        ) : null}
        <div>
          <dt>Disproves if</dt>
          <dd>{item.disproves_if}</dd>
        </div>
      </dl>
    </article>
  );
}
