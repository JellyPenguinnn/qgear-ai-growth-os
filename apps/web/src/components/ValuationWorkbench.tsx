"use client";

import { useMemo, useState } from "react";
import type { AIStatusResponse, ValuationCase, ValuationResponse } from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

function cloneCases(cases: ValuationCase[]) {
  return cases.map((caseItem) => ({
    ...caseItem,
    assumptions: { ...caseItem.assumptions },
    evidence_refs: [...caseItem.evidence_refs]
  }));
}

function updateNumber(value: string) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

export function ValuationWorkbench({ initial, aiStatus }: { initial: ValuationResponse; aiStatus: AIStatusResponse }) {
  const [valuation, setValuation] = useState(initial);
  const [cases, setCases] = useState(() => cloneCases(initial.summary.cases));
  const [hurdle, setHurdle] = useState(initial.summary.hurdle_irr_pct);
  const [status, setStatus] = useState<string | null>(null);

  const probabilityTotal = useMemo(() => cases.reduce((total, caseItem) => total + caseItem.probability, 0), [cases]);

  function updateCase(index: number, updater: (caseItem: ValuationCase) => ValuationCase) {
    setCases((current) => current.map((caseItem, itemIndex) => (itemIndex === index ? updater(caseItem) : caseItem)));
  }

  async function recalculate() {
    setStatus("Calculating draft valuation...");
    try {
      const response = await fetch(`${API_URL}/valuation/${initial.ticker}/calculate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticker: initial.ticker,
          hurdle_irr_pct: hurdle,
          cases
        })
      });
      const payload = await response.json();
      if (!response.ok) {
        setStatus(payload.detail ?? `Calculation failed with HTTP ${response.status}.`);
        return;
      }
      setValuation(payload as ValuationResponse);
      setCases(cloneCases((payload as ValuationResponse).summary.cases));
      setStatus("Draft valuation recalculated. Review evidence before using it in a decision.");
    } catch {
      setStatus("Could not reach the local valuation API. Existing demo assumptions remain visible.");
    }
  }

  return (
    <div className="valuation-workbench">
      <div className="valuation-hero">
        <div>
          <span className="eyebrow">Probability-weighted IRR</span>
          <strong>{valuation.summary.probability_weighted_irr_5y_pct.toFixed(1)}%</strong>
          <p className="muted">5Y weighted IRR vs {valuation.summary.hurdle_irr_pct.toFixed(1)}% hurdle.</p>
        </div>
        <div>
          <span className="eyebrow">Valuation gate</span>
          <strong className={valuation.summary.clears_hurdle ? "ok-text" : "warn-text"}>
            {valuation.summary.clears_hurdle ? "Clears hurdle" : "Below hurdle"}
          </strong>
          <p className="muted">This can support or block action, never create buy/add by itself.</p>
        </div>
        <div className="field">
          <label htmlFor={`${initial.ticker}-hurdle`}>Hurdle IRR %</label>
          <input id={`${initial.ticker}-hurdle`} type="number" value={hurdle} onChange={(event) => setHurdle(updateNumber(event.target.value))} />
        </div>
      </div>

      <div className="table-wrap compact-table">
        <table>
          <thead>
            <tr>
              <th>Case</th>
              <th>Probability</th>
              <th>3Y target</th>
              <th>5Y target</th>
              <th>Revenue CAGR</th>
              <th>FCF margin</th>
              <th>Terminal multiple</th>
              <th>5Y IRR</th>
            </tr>
          </thead>
          <tbody>
            {cases.map((caseItem, index) => {
              const irr = valuation.case_irrs.find((item) => item.name === caseItem.name);
              return (
                <tr key={caseItem.name}>
                  <td>
                    <strong>{caseItem.name}</strong>
                    <p className="muted">{caseItem.notes}</p>
                  </td>
                  <td>
                    <input
                      aria-label={`${caseItem.name} probability`}
                      type="number"
                      step="0.01"
                      value={caseItem.probability}
                      onChange={(event) => updateCase(index, (item) => ({ ...item, probability: updateNumber(event.target.value) }))}
                    />
                  </td>
                  <td>
                    <input
                      aria-label={`${caseItem.name} 3 year target`}
                      type="number"
                      value={caseItem.target_price_3y}
                      onChange={(event) => updateCase(index, (item) => ({ ...item, target_price_3y: updateNumber(event.target.value) }))}
                    />
                  </td>
                  <td>
                    <input
                      aria-label={`${caseItem.name} 5 year target`}
                      type="number"
                      value={caseItem.target_price_5y}
                      onChange={(event) => updateCase(index, (item) => ({ ...item, target_price_5y: updateNumber(event.target.value) }))}
                    />
                  </td>
                  <td>
                    <input
                      aria-label={`${caseItem.name} revenue CAGR`}
                      type="number"
                      value={caseItem.assumptions.revenue_cagr_pct}
                      onChange={(event) =>
                        updateCase(index, (item) => ({
                          ...item,
                          assumptions: { ...item.assumptions, revenue_cagr_pct: updateNumber(event.target.value) }
                        }))
                      }
                    />
                  </td>
                  <td>
                    <input
                      aria-label={`${caseItem.name} FCF margin`}
                      type="number"
                      value={caseItem.assumptions.fcf_margin_pct}
                      onChange={(event) =>
                        updateCase(index, (item) => ({
                          ...item,
                          assumptions: { ...item.assumptions, fcf_margin_pct: updateNumber(event.target.value) }
                        }))
                      }
                    />
                  </td>
                  <td>
                    <input
                      aria-label={`${caseItem.name} terminal multiple`}
                      type="number"
                      value={caseItem.assumptions.terminal_multiple}
                      onChange={(event) =>
                        updateCase(index, (item) => ({
                          ...item,
                          assumptions: { ...item.assumptions, terminal_multiple: updateNumber(event.target.value) }
                        }))
                      }
                    />
                  </td>
                  <td>{irr ? `${irr.irr_5y_pct.toFixed(1)}%` : "Recalculate"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="valuation-actions">
        <p className={Math.abs(probabilityTotal - 1) <= 0.001 ? "ok-text" : "warn-text"}>Probability total: {probabilityTotal.toFixed(2)}</p>
        <button className="button" type="button" onClick={recalculate}>
          Recalculate draft valuation
        </button>
        <button className="button secondary" type="button" disabled={!aiStatus.ai_enabled}>
          {aiStatus.ai_enabled ? "Draft valuation explanation with AI" : "AI valuation explainer disabled"}
        </button>
      </div>
      {status ? <p className="muted">{status}</p> : null}

      <div className="grid cols-2">
        <div>
          <h3>Sensitivity Table</h3>
          <div className="table-wrap compact-table">
            <table>
              <thead>
                <tr>
                  <th>Multiple delta</th>
                  <th>FCF margin delta</th>
                  <th>5Y target</th>
                  <th>5Y IRR</th>
                </tr>
              </thead>
              <tbody>
                {valuation.sensitivity_table.map((cell) => (
                  <tr key={`${cell.terminal_multiple_delta_pct}-${cell.fcf_margin_delta_pct}`}>
                    <td>{cell.terminal_multiple_delta_pct.toFixed(0)}%</td>
                    <td>{cell.fcf_margin_delta_pct.toFixed(0)}%</td>
                    <td>${cell.target_price_5y.toFixed(2)}</td>
                    <td>{cell.expected_irr_5y_pct.toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        <div className="valuation-notes">
          <h3>Notes and Evidence</h3>
          {valuation.valuation_notes.map((note) => (
            <p key={note}>{note}</p>
          ))}
          <div className="flag-row">
            {valuation.evidence_links.map((link) => (
              <span className="badge" key={link}>
                {link}
              </span>
            ))}
          </div>
          <p className="muted">{valuation.decision_gate.note}</p>
        </div>
      </div>
    </div>
  );
}
