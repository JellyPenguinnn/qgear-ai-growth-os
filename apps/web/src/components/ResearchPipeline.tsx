import Link from "next/link";
import { StateBadge } from "./StateBadge";
import { EmptyState } from "./ui";
import type { PipelineItem, PipelineState } from "@/lib/types";

function flagLabel(flag: string) {
  return flag.replaceAll("_", " ").toLowerCase().replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function PipelineCard({ item }: { item: PipelineItem }) {
  return (
    <Link href={`/universe/${item.ticker}`} className="pipeline-card">
      <div className="pipeline-card-top">
        <span>
          <strong>{item.ticker}</strong>
          <small>{item.company_name}</small>
        </span>
        <StateBadge state={item.decision_state} />
      </div>
      <div className="pipeline-card-score">
        <span>{item.ai_layer.replaceAll("_", " ")}</span>
        <strong>{item.score.toFixed(1)}</strong>
      </div>
      <p>{item.primary_reason}</p>
      {item.primary_blocker ? <p className="warn-text">{item.primary_blocker}</p> : null}
      <div className="pipeline-next">
        <span className="eyebrow">Next task</span>
        <p>{item.next_task}</p>
      </div>
      {item.review_flags.length ? (
        <div className="flag-row">
          {item.review_flags.slice(0, 3).map((flag) => (
            <span className="badge warn" key={`${item.ticker}-${flag}`}>
              {flagLabel(flag)}
            </span>
          ))}
        </div>
      ) : null}
      <dl className="source-strip">
        <div>
          <dt>Source</dt>
          <dd>{item.source_metadata.source}</dd>
        </div>
        <div>
          <dt>Date</dt>
          <dd>{item.source_metadata.source_date}</dd>
        </div>
        <div>
          <dt>Confidence</dt>
          <dd>{item.source_metadata.confidence}</dd>
        </div>
      </dl>
    </Link>
  );
}

export function ResearchPipeline({ states }: { states: PipelineState[] }) {
  const populated = states.filter((state) => state.count > 0);

  if (!states.length || !populated.length) {
    return <EmptyState title="Pipeline empty" detail="No companies are currently available in the local demo universe." />;
  }

  return (
    <div className="pipeline-board">
      {states.map((state) => (
        <section className="pipeline-column" key={state.state}>
          <div className="pipeline-column-header">
            <span>
              <strong>{state.label}</strong>
              <small>{state.description}</small>
            </span>
            <span className="badge">{state.count}</span>
          </div>
          <div className="pipeline-items">
            {state.items.length ? (
              state.items.map((item) => <PipelineCard key={item.ticker} item={item} />)
            ) : (
              <EmptyState title="No names here" detail="Nothing currently sits in this review state." />
            )}
          </div>
        </section>
      ))}
    </div>
  );
}
