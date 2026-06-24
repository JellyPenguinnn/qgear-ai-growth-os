"use client";

import { FormEvent, useState } from "react";
import { API_URL } from "@/lib/api";

export function JournalForm() {
  const [message, setMessage] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const payload = {
      entry_date: String(form.get("entry_date")),
      ticker: String(form.get("ticker") ?? "").toUpperCase(),
      action: String(form.get("action")),
      price: Number(form.get("price")),
      position_size_pct: Number(form.get("position_size_pct")),
      score: Number(form.get("score")),
      evidence: String(form.get("evidence")),
      thesis: String(form.get("thesis")),
      invalidation_rule: String(form.get("invalidation_rule")),
      expected_irr_pct: Number(form.get("expected_irr_pct")),
      future_review_date: String(form.get("future_review_date")),
      later_outcome: String(form.get("later_outcome") ?? ""),
      decision_outcome: String(form.get("decision_outcome") ?? ""),
      mistake_category: String(form.get("mistake_category") ?? "NONE"),
      evidence_quality: String(form.get("evidence_quality") ?? "MEDIUM"),
      followed_system: form.get("followed_system") === "on",
      later_review: String(form.get("later_review") ?? ""),
      process_score: Number(form.get("process_score") ?? 0)
    };
    try {
      const response = await fetch(`${API_URL}/journal`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      setMessage(response.ok ? "Decision logged locally." : "Could not save journal entry. Check that the API is running.");
    } catch {
      setMessage("API unavailable. The journal form stayed local in your browser and was not saved.");
    }
  }

  return (
    <form onSubmit={submit}>
      <div className="form-grid">
        <div className="field">
          <label htmlFor="entry_date">Date</label>
          <input id="entry_date" name="entry_date" type="date" required />
        </div>
        <div className="field">
          <label htmlFor="ticker">Ticker</label>
          <input id="ticker" name="ticker" required />
        </div>
        <div className="field">
          <label htmlFor="action">Decision state</label>
          <select id="action" name="action">
            <option>NO_ACTION</option>
            <option>STARTER_ALLOWED</option>
            <option>ADD_ALLOWED</option>
            <option>HOLD</option>
            <option>TRIM_CANDIDATE</option>
            <option>EXIT_THESIS_BROKEN</option>
          </select>
          <small>This is a journaled state, not a broker instruction.</small>
        </div>
        <div className="field">
          <label htmlFor="price">Price</label>
          <input id="price" name="price" type="number" step="0.01" required />
        </div>
        <div className="field">
          <label htmlFor="position_size_pct">Position size</label>
          <input id="position_size_pct" name="position_size_pct" type="number" step="0.1" defaultValue="0" />
          <small>Use 0 for no-action, watchlist, or blocked decisions.</small>
        </div>
        <div className="field">
          <label htmlFor="score">Score</label>
          <input id="score" name="score" type="number" step="0.1" required />
        </div>
        <div className="field">
          <label htmlFor="expected_irr_pct">Expected IRR</label>
          <input id="expected_irr_pct" name="expected_irr_pct" type="number" step="0.1" required />
        </div>
        <div className="field">
          <label htmlFor="future_review_date">Future review date</label>
          <input id="future_review_date" name="future_review_date" type="date" required />
        </div>
        <div className="field">
          <label htmlFor="evidence_quality">Evidence quality</label>
          <select id="evidence_quality" name="evidence_quality" defaultValue="MEDIUM">
            <option>LOW</option>
            <option>MEDIUM</option>
            <option>HIGH</option>
          </select>
        </div>
        <div className="field">
          <label htmlFor="process_score">Process score</label>
          <input id="process_score" name="process_score" type="number" min="0" max="100" step="1" defaultValue="80" />
        </div>
        <div className="field">
          <label htmlFor="mistake_category">Mistake category</label>
          <select id="mistake_category" name="mistake_category" defaultValue="NONE">
            <option>NONE</option>
            <option>THESIS_DRIFT</option>
            <option>EVIDENCE_GAP</option>
            <option>VALUATION_ERROR</option>
            <option>RISK_BUDGET_BREAK</option>
            <option>POSITION_SIZING_ERROR</option>
            <option>PROCESS_SKIP</option>
            <option>OTHER</option>
          </select>
        </div>
        <label className="check-label">
          <input id="followed_system" name="followed_system" type="checkbox" defaultChecked />
          Followed Q-GEAR gates
        </label>
        <div className="field wide">
          <label htmlFor="evidence">Evidence and source</label>
          <textarea id="evidence" name="evidence" required />
          <small>Include source, date, confidence, and the claim it supports.</small>
        </div>
        <div className="field wide">
          <label htmlFor="thesis">Thesis</label>
          <textarea id="thesis" name="thesis" required />
        </div>
        <div className="field wide">
          <label htmlFor="invalidation_rule">Invalidation rule</label>
          <textarea id="invalidation_rule" name="invalidation_rule" required />
        </div>
        <div className="field wide">
          <label htmlFor="later_outcome">Later outcome</label>
          <textarea id="later_outcome" name="later_outcome" />
        </div>
        <div className="field wide">
          <label htmlFor="decision_outcome">Decision outcome</label>
          <textarea id="decision_outcome" name="decision_outcome" placeholder="Pending, worked, thesis weakened, avoided loss, process mistake..." />
        </div>
        <div className="field wide">
          <label htmlFor="later_review">Later review</label>
          <textarea id="later_review" name="later_review" placeholder="What should be checked after the future review date?" />
        </div>
      </div>
      <div className="button-row">
        <button className="button" type="submit">
          Log decision
        </button>
        <span className="form-help">No entry is saved until the local API confirms it.</span>
      </div>
      {message ? (
        <span className="muted" role="status" aria-live="polite">
          {message}
        </span>
      ) : null}
    </form>
  );
}
