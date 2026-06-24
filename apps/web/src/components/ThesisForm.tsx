"use client";

import { FormEvent, useState } from "react";
import { API_URL } from "@/lib/api";

export function ThesisForm({ ticker }: { ticker: string }) {
  const [message, setMessage] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const payload = {
      statement: String(form.get("statement") ?? ""),
      must_go_right: String(form.get("must_go_right") ?? ""),
      breaks_if: String(form.get("breaks_if") ?? ""),
      key_metrics: String(form.get("key_metrics") ?? "")
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean),
      next_review_date: String(form.get("next_review_date") ?? "")
    };
    try {
      const response = await fetch(`${API_URL}/theses/${ticker}/approve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      setMessage(response.ok ? "Thesis approved locally." : "Could not save thesis. Check that the API is running.");
    } catch {
      setMessage("API unavailable. Thesis draft was not saved; no action state changes without backend confirmation.");
    }
  }

  return (
    <form onSubmit={submit}>
      <div className="form-grid">
        <div className="field wide">
          <label htmlFor="statement">Thesis statement</label>
          <textarea id="statement" name="statement" required placeholder="Evidence-based thesis, not price movement." />
          <small>Price movement alone is never evidence for a thesis.</small>
        </div>
        <div className="field wide">
          <label htmlFor="must_go_right">What must go right</label>
          <textarea id="must_go_right" name="must_go_right" required />
        </div>
        <div className="field wide">
          <label htmlFor="breaks_if">What would break thesis</label>
          <textarea id="breaks_if" name="breaks_if" required />
          <small>This invalidation rule is required before any starter/add state can clear.</small>
        </div>
        <div className="field">
          <label htmlFor="key_metrics">Key metrics to monitor</label>
          <input id="key_metrics" name="key_metrics" placeholder="Revenue growth, GM, FCF, backlog" required />
        </div>
        <div className="field">
          <label htmlFor="next_review_date">Next review date</label>
          <input id="next_review_date" name="next_review_date" type="date" required />
        </div>
      </div>
      <div className="button-row">
        <button className="button" type="submit">
          Approve thesis
        </button>
        <span className="form-help">Approval is local research state only; it does not create trade execution.</span>
      </div>
      {message ? (
        <span className="muted" role="status" aria-live="polite">
          {message}
        </span>
      ) : null}
    </form>
  );
}
