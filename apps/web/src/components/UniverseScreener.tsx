"use client";

import { useState } from "react";
import type { Route } from "next";
import Link from "next/link";
import { StateBadge } from "./StateBadge";
import { EmptyState, SectionCard } from "./ui";
import type { DemoCompany } from "@/lib/types";

export function UniverseScreener({ companies }: { companies: DemoCompany[] }) {
  const [layer, setLayer] = useState("ALL");
  const [state, setState] = useState("ALL");
  const [minScore, setMinScore] = useState(0);
  const [minGrowth, setMinGrowth] = useState(-100);
  const [minGrossMargin, setMinGrossMargin] = useState(0);
  const [maxDrawdown, setMaxDrawdown] = useState(100);

  const layers = Array.from(new Set(companies.map((company) => company.ai_layer))).sort();
  const states = Array.from(new Set(companies.map((company) => company.status))).sort();

  const filtered = companies.filter((company) => {
    if (layer !== "ALL" && company.ai_layer !== layer) return false;
    if (state !== "ALL" && company.status !== state) return false;
    if (company.score.total < minScore) return false;
    if (company.metrics.revenue_growth_pct < minGrowth) return false;
    if (company.metrics.gross_margin_pct < minGrossMargin) return false;
    if (company.metrics.drawdown_from_high_pct > maxDrawdown) return false;
    return true;
  });

  return (
    <SectionCard title="Screener" description="Use filters to prioritize research. A filtered list is not a buy list.">
      <div className="filters">
        <div className="field">
          <label htmlFor="layer">AI layer</label>
          <select id="layer" value={layer} onChange={(event) => setLayer(event.target.value)}>
            <option value="ALL">All layers</option>
            {layers.map((item) => (
              <option key={item} value={item}>
                {item.replaceAll("_", " ")}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label htmlFor="state">Decision state</label>
          <select id="state" value={state} onChange={(event) => setState(event.target.value)}>
            <option value="ALL">All states</option>
            {states.map((item) => (
              <option key={item} value={item}>
                {item.replaceAll("_", " ")}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label htmlFor="score">Min quality score</label>
          <input id="score" type="number" min="0" max="100" value={minScore} onChange={(event) => setMinScore(Number(event.target.value))} />
        </div>
        <div className="field">
          <label htmlFor="growth">Min revenue growth</label>
          <input id="growth" type="number" value={minGrowth} onChange={(event) => setMinGrowth(Number(event.target.value))} />
        </div>
        <div className="field">
          <label htmlFor="margin">Min gross margin</label>
          <input id="margin" type="number" value={minGrossMargin} onChange={(event) => setMinGrossMargin(Number(event.target.value))} />
        </div>
        <div className="field">
          <label htmlFor="drawdown">Max drawdown</label>
          <input id="drawdown" type="number" min="0" max="100" value={maxDrawdown} onChange={(event) => setMaxDrawdown(Number(event.target.value))} />
        </div>
      </div>

      {filtered.length ? (
        <>
          <div className="callout compact">
            <strong>{filtered.length} names match.</strong> Open a workbench to inspect blockers, source metadata, thesis status, valuation, technical state, and portfolio impact.
          </div>
          <div className="entity-grid">
            {filtered.map((company) => {
              const blocker = company.decision?.blocked_reasons?.[0];
              const reason = blocker ?? company.decision?.reasons?.[0] ?? "Review thesis and evidence.";
              return (
                <Link href={`/universe/${company.ticker}` as Route} className="entity-card" key={company.ticker}>
                  <div className="entity-card-header">
                    <span>
                      <strong>{company.ticker}</strong>
                      <small>{company.company_name}</small>
                    </span>
                    <StateBadge state={company.status} />
                  </div>
                  <p>{reason}</p>
                  <div className="entity-card-metrics">
                    <div className="mini-stat">
                      <span>Score</span>
                      <strong>{company.score.total.toFixed(1)}</strong>
                    </div>
                    <div className="mini-stat">
                      <span>Growth</span>
                      <strong>{company.metrics.revenue_growth_pct.toFixed(1)}%</strong>
                    </div>
                    <div className="mini-stat">
                      <span>Drawdown</span>
                      <strong>{company.metrics.drawdown_from_high_pct.toFixed(1)}%</strong>
                    </div>
                  </div>
                  <p className="muted">{company.ai_layer.replaceAll("_", " ")}</p>
                  <p className="muted">{company.evidence_summary}</p>
                </Link>
              );
            })}
          </div>
        </>
      ) : (
        <EmptyState title="No names match these filters" detail="Relax one filter or return to all states before making research conclusions." />
      )}
    </SectionCard>
  );
}
