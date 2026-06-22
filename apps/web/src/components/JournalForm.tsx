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
      later_outcome: String(form.get("later_outcome") ?? "")
    };
    const response = await fetch(`${API_URL}/journal`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    setMessage(response.ok ? "Decision logged locally." : "Could not save journal entry. Check that the API is running.");
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
          <label htmlFor="action">Action</label>
          <select id="action" name="action">
            <option>NO_ACTION</option>
            <option>STARTER_ALLOWED</option>
            <option>ADD_ALLOWED</option>
            <option>HOLD</option>
            <option>TRIM_CANDIDATE</option>
            <option>EXIT_THESIS_BROKEN</option>
          </select>
        </div>
        <div className="field">
          <label htmlFor="price">Price</label>
          <input id="price" name="price" type="number" step="0.01" required />
        </div>
        <div className="field">
          <label htmlFor="position_size_pct">Position size</label>
          <input id="position_size_pct" name="position_size_pct" type="number" step="0.1" defaultValue="0" />
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
        <div className="field wide">
          <label htmlFor="evidence">Evidence</label>
          <textarea id="evidence" name="evidence" required />
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
      </div>
      <div className="button-row">
        <button className="button" type="submit">
          Log decision
        </button>
        {message ? <span className="muted">{message}</span> : null}
      </div>
    </form>
  );
}
