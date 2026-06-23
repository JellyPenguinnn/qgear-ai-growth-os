"use client";

import { FormEvent, useState } from "react";
import { API_URL } from "@/lib/api";
import type { AIDraftResponse } from "@/lib/types";

export function AIEarningsSummaryForm({ aiEnabled }: { aiEnabled: boolean }) {
  const [message, setMessage] = useState("");
  const [draft, setDraft] = useState<AIDraftResponse | null>(null);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const payload = {
      ticker: String(form.get("ticker") ?? "").toUpperCase(),
      fiscal_period: String(form.get("fiscal_period") ?? ""),
      report_date: String(form.get("report_date") ?? ""),
      earnings_text: String(form.get("earnings_text") ?? ""),
      existing_thesis: String(form.get("existing_thesis") ?? ""),
      existing_evidence: [],
      external_ai_acknowledged: form.get("external_ai_acknowledged") === "on"
    };

    try {
      const response = await fetch(`${API_URL}/ai/earnings/summarize`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const body = (await response.json()) as AIDraftResponse;
      setDraft(body);
      setMessage(
        body.draft_status === "draft"
          ? "AI draft generated. Verify every claim before saving evidence or journal notes."
          : [...body.warnings, ...body.validation_errors].join(" ") || "AI summary did not produce a draft."
      );
    } catch {
      setMessage("AI summary route unavailable. Use the manual earnings workflow.");
    }
  }

  return (
    <form onSubmit={submit}>
      <div className="form-grid">
        <div className="field">
          <label htmlFor="ai_ticker">Ticker</label>
          <input id="ai_ticker" name="ticker" defaultValue="NVDA" required />
        </div>
        <div className="field">
          <label htmlFor="ai_fiscal_period">Fiscal period</label>
          <input id="ai_fiscal_period" name="fiscal_period" defaultValue="2026Q1" required />
        </div>
        <div className="field">
          <label htmlFor="ai_report_date">Report date</label>
          <input id="ai_report_date" name="report_date" type="date" required />
        </div>
        <div className="field wide">
          <label htmlFor="existing_thesis">Existing thesis</label>
          <textarea id="existing_thesis" name="existing_thesis" placeholder="Paste current thesis and invalidation rule." />
        </div>
        <div className="field wide">
          <label htmlFor="earnings_text">Earnings release or transcript excerpt</label>
          <textarea id="earnings_text" name="earnings_text" placeholder="Paste the source text to summarize. Do not include private portfolio data unless you intend to send it." required />
        </div>
        <label className="check-label wide">
          <input name="external_ai_acknowledged" type="checkbox" disabled={!aiEnabled} />
          <span>Allow this submitted earnings text to be sent to the configured external AI provider</span>
        </label>
      </div>
      <div className="button-row">
        <button className="button" type="submit" disabled={!aiEnabled}>
          Summarize earnings draft
        </button>
        <span className="badge">{aiEnabled ? "AI enabled" : "AI disabled"}</span>
        {message ? <span className="muted" aria-live="polite">{message}</span> : null}
      </div>
      {draft ? (
        <div className="callout compact">
          <strong>Draft status:</strong> {draft.draft_status}
          <br />
          <span className="muted">{draft.disclaimer}</span>
          {draft.evidence.length ? <p>{draft.evidence.length} draft evidence object(s) require verification before saving.</p> : null}
        </div>
      ) : null}
    </form>
  );
}
