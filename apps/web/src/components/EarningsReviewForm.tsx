"use client";

import { FormEvent, useState } from "react";
import { API_URL } from "@/lib/api";

export function EarningsReviewForm() {
  const [message, setMessage] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const ticker = String(form.get("ticker") ?? "").toUpperCase();
    const evidence = {
      claim: String(form.get("claim")),
      evidence: String(form.get("evidence")),
      source: String(form.get("source")),
      source_date: String(form.get("source_date")),
      confidence: String(form.get("confidence")),
      disproves_if: String(form.get("disproves_if"))
    };
    const payload = {
      fiscal_period: String(form.get("fiscal_period")),
      report_date: String(form.get("report_date")),
      revenue_surprise_pct: Number(form.get("revenue_surprise_pct") || 0),
      eps_surprise_pct: Number(form.get("eps_surprise_pct") || 0),
      guidance_raised: form.get("guidance_raised") === "on",
      guidance_cut: form.get("guidance_cut") === "on",
      guidance_cut_structural: form.get("guidance_cut_structural") === "on",
      revenue_growth_accelerated: form.get("revenue_growth_accelerated") === "on",
      ai_evidence_improved: form.get("ai_evidence_improved") === "on",
      segment_growth_improved: form.get("segment_growth_improved") === "on",
      margin_expanded: form.get("margin_expanded") === "on",
      margin_deteriorated: form.get("margin_deteriorated") === "on",
      fcf_improved: form.get("fcf_improved") === "on",
      fcf_deteriorated: form.get("fcf_deteriorated") === "on",
      management_tone: String(form.get("management_tone")),
      score_change: Number(form.get("score_change") || 0),
      action_change: "NO_ACTION",
      evidence: [evidence]
    };
    const response = await fetch(`${API_URL}/earnings/${ticker}/reviews`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (!response.ok) {
      setMessage("Could not save earnings review. Check the ticker, evidence fields, and API status.");
      return;
    }
    const body = (await response.json()) as { thesis_status_change?: string };
    setMessage(`Earnings review saved locally. Thesis status change: ${body.thesis_status_change ?? "UNCHANGED"}.`);
  }

  return (
    <form onSubmit={submit}>
      <div className="form-grid">
        <div className="field">
          <label htmlFor="ticker">Ticker</label>
          <input id="ticker" name="ticker" defaultValue="NVDA" required />
        </div>
        <div className="field">
          <label htmlFor="fiscal_period">Fiscal period</label>
          <input id="fiscal_period" name="fiscal_period" defaultValue="2026Q1" required />
        </div>
        <div className="field">
          <label htmlFor="report_date">Report date</label>
          <input id="report_date" name="report_date" type="date" required />
        </div>
        <div className="field">
          <label htmlFor="source_date">Source date</label>
          <input id="source_date" name="source_date" type="date" required />
        </div>
        <div className="field">
          <label htmlFor="revenue_surprise_pct">Revenue surprise %</label>
          <input id="revenue_surprise_pct" name="revenue_surprise_pct" type="number" step="0.1" defaultValue="0" />
        </div>
        <div className="field">
          <label htmlFor="eps_surprise_pct">EPS surprise %</label>
          <input id="eps_surprise_pct" name="eps_surprise_pct" type="number" step="0.1" defaultValue="0" />
        </div>
        <div className="field">
          <label htmlFor="score_change">Score change</label>
          <input id="score_change" name="score_change" type="number" step="0.1" defaultValue="0" />
        </div>
        <div className="field">
          <label htmlFor="confidence">Confidence</label>
          <select id="confidence" name="confidence" defaultValue="HIGH">
            <option>HIGH</option>
            <option>MEDIUM</option>
            <option>LOW</option>
          </select>
        </div>
        <div className="field wide checkbox-grid">
          {[
            ["guidance_raised", "Guidance raised"],
            ["guidance_cut", "Guidance cut"],
            ["guidance_cut_structural", "Structural cut"],
            ["revenue_growth_accelerated", "Revenue accelerated"],
            ["ai_evidence_improved", "AI evidence improved"],
            ["segment_growth_improved", "Segment growth improved"],
            ["margin_expanded", "Margin expanded"],
            ["margin_deteriorated", "Margin deteriorated"],
            ["fcf_improved", "FCF improved"],
            ["fcf_deteriorated", "FCF deteriorated"]
          ].map(([name, label]) => (
            <label key={name} className="check-label">
              <input name={name} type="checkbox" />
              <span>{label}</span>
            </label>
          ))}
        </div>
        <div className="field wide">
          <label htmlFor="claim">Evidence claim</label>
          <input id="claim" name="claim" defaultValue="AI demand became more measurable after earnings." required />
        </div>
        <div className="field wide">
          <label htmlFor="evidence">Evidence detail</label>
          <textarea id="evidence" name="evidence" defaultValue="Revenue growth, guidance, AI evidence, margin, or FCF changed." required />
        </div>
        <div className="field wide">
          <label htmlFor="source">Source</label>
          <input id="source" name="source" defaultValue="Manual earnings review" required />
        </div>
        <div className="field wide">
          <label htmlFor="management_tone">Management tone</label>
          <textarea id="management_tone" name="management_tone" defaultValue="Evidence reviewed manually; no automatic action." required />
        </div>
        <div className="field wide">
          <label htmlFor="disproves_if">Disproves if</label>
          <textarea id="disproves_if" name="disproves_if" defaultValue="Guidance is cut, AI demand slows, margins deteriorate, or free cash flow weakens." required />
        </div>
      </div>
      <div className="button-row">
        <button className="button" type="submit">
          Save earnings review
        </button>
        {message ? <span className="muted" aria-live="polite">{message}</span> : null}
      </div>
    </form>
  );
}
