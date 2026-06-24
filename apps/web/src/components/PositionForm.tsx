"use client";

import { FormEvent, useState } from "react";
import { API_URL } from "@/lib/api";

export function PositionForm() {
  const [message, setMessage] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const payload = {
      ticker: String(form.get("ticker") ?? "").toUpperCase(),
      shares: Number(form.get("shares")),
      average_cost: Number(form.get("average_cost")),
      current_price: Number(form.get("current_price")),
      status: String(form.get("status") ?? "HOLD"),
      thesis_status: String(form.get("thesis_status") ?? "DRAFT"),
      next_review_date: String(form.get("next_review_date") ?? "")
    };
    try {
      const response = await fetch(`${API_URL}/portfolio/positions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      setMessage(response.ok ? "Position recorded locally." : "Could not record position. Check that the API is running.");
    } catch {
      setMessage("API unavailable. Manual portfolio read mode still works, but this position was not saved.");
    }
  }

  return (
    <form onSubmit={submit}>
      <div className="form-grid">
        <div className="field">
          <label htmlFor="ticker">Ticker</label>
          <input id="ticker" name="ticker" placeholder="NVDA" required />
        </div>
        <div className="field">
          <label htmlFor="shares">Shares</label>
          <input id="shares" name="shares" type="number" step="0.0001" required />
        </div>
        <div className="field">
          <label htmlFor="average_cost">Average cost</label>
          <input id="average_cost" name="average_cost" type="number" step="0.01" required />
        </div>
        <div className="field">
          <label htmlFor="current_price">Current price</label>
          <input id="current_price" name="current_price" type="number" step="0.01" required />
          <small>Used for local risk math only. It is not a live quote or order ticket.</small>
        </div>
        <div className="field">
          <label htmlFor="status">Status</label>
          <select id="status" name="status" defaultValue="HOLD">
            <option>HOLD</option>
            <option>WATCHLIST</option>
            <option>TRIM_CANDIDATE</option>
            <option>EXIT_THESIS_BROKEN</option>
          </select>
        </div>
        <div className="field">
          <label htmlFor="thesis_status">Thesis status</label>
          <select id="thesis_status" name="thesis_status" defaultValue="DRAFT">
            <option>DRAFT</option>
            <option>APPROVED</option>
            <option>NEEDS_REVIEW</option>
            <option>BROKEN</option>
          </select>
        </div>
        <div className="field">
          <label htmlFor="next_review_date">Next review date</label>
          <input id="next_review_date" name="next_review_date" type="date" />
        </div>
      </div>
      <div className="button-row">
        <button className="button" type="submit">
          Record position
        </button>
        <span className="form-help">Manual tracking only; no brokerage connection is created.</span>
      </div>
      {message ? (
        <span className="muted" role="status" aria-live="polite">
          {message}
        </span>
      ) : null}
    </form>
  );
}
