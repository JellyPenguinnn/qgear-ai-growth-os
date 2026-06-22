"use client";

import { useState } from "react";
import type { Route } from "next";
import Link from "next/link";
import { StateBadge } from "./StateBadge";
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
    <section className="section">
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

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Ticker</th>
              <th>Company</th>
              <th>AI layer</th>
              <th>Score</th>
              <th>State</th>
              <th>Growth</th>
              <th>GM</th>
              <th>FCF margin</th>
              <th>Drawdown</th>
              <th>Evidence</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((company) => (
              <tr key={company.ticker}>
                <td>
                  <Link href={`/universe/${company.ticker}` as Route}>
                    <strong>{company.ticker}</strong>
                  </Link>
                </td>
                <td>{company.company_name}</td>
                <td>{company.ai_layer.replaceAll("_", " ")}</td>
                <td>{company.score.total.toFixed(1)}</td>
                <td>
                  <StateBadge state={company.status} />
                </td>
                <td>{company.metrics.revenue_growth_pct.toFixed(1)}%</td>
                <td>{company.metrics.gross_margin_pct.toFixed(1)}%</td>
                <td>{company.metrics.fcf_margin_pct.toFixed(1)}%</td>
                <td>{company.metrics.drawdown_from_high_pct.toFixed(1)}%</td>
                <td>{company.evidence_summary}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
