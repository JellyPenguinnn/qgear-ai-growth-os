"use client";

import { FormEvent, useState } from "react";
import { API_URL } from "@/lib/api";
import type { AIDraftResponse, EvidenceObject } from "@/lib/types";

const blankEvidence: EvidenceObject = {
  claim: "",
  evidence: "",
  source: "",
  source_date: "",
  confidence: "MEDIUM",
  disproves_if: ""
};

function formValue(form: FormData, key: string) {
  return String(form.get(key) ?? "");
}

export function EvidenceWorkbenchForm({ aiEnabled }: { aiEnabled: boolean }) {
  const [message, setMessage] = useState("");
  const [draftMessage, setDraftMessage] = useState("");
  const [evidence, setEvidence] = useState<EvidenceObject>(blankEvidence);

  async function extractWithAI(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const sourceTitle = formValue(form, "source_title");
    const sourceDate = formValue(form, "source_date");
    const sourceDescription = formValue(form, "source_url_or_description");
    const payload = {
      ticker: formValue(form, "ticker").toUpperCase(),
      source_title: sourceTitle,
      source_type: formValue(form, "source_type"),
      source_date: sourceDate,
      source_url_or_description: sourceDescription,
      pasted_text: formValue(form, "pasted_text"),
      external_ai_acknowledged: form.get("external_ai_acknowledged") === "on"
    };

    try {
      const response = await fetch(`${API_URL}/ai/evidence/extract`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const body = (await response.json()) as AIDraftResponse;
      if (body.draft_status !== "draft" || !body.evidence.length) {
        setDraftMessage(
          [...body.warnings, ...body.validation_errors].join(" ") || "AI extraction did not produce a verified draft. Manual evidence entry remains available."
        );
        setEvidence((current) => ({
          ...current,
          source: current.source || sourceTitle || sourceDescription,
          source_date: current.source_date || sourceDate
        }));
        return;
      }
      setEvidence(body.evidence[0]);
      setDraftMessage("AI draft loaded into the verification fields. Review and edit before saving.");
    } catch {
      setDraftMessage("AI route unavailable. Manual evidence entry remains available.");
    }
  }

  async function saveVerifiedEvidence(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const ticker = formValue(form, "save_ticker").toUpperCase();
    const payload: EvidenceObject = {
      claim: formValue(form, "claim"),
      evidence: formValue(form, "evidence"),
      source: formValue(form, "source"),
      source_date: formValue(form, "source_date_verified"),
      confidence: formValue(form, "confidence") as EvidenceObject["confidence"],
      disproves_if: formValue(form, "disproves_if")
    };

    try {
      const response = await fetch(`${API_URL}/earnings/${ticker}/evidence`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!response.ok) {
        setMessage("Could not save evidence. Check ticker, ISO date, source, claim, and disproof fields.");
        return;
      }
      setMessage(`Verified evidence saved locally for ${ticker}. It will appear in the stock workbench evidence timeline.`);
    } catch {
      setMessage("API unavailable. Evidence was not saved.");
    }
  }

  return (
    <div className="split">
      <form onSubmit={extractWithAI}>
        <div className="form-grid">
          <div className="field">
            <label htmlFor="ticker">Ticker</label>
            <input id="ticker" name="ticker" defaultValue="NVDA" required />
          </div>
          <div className="field">
            <label htmlFor="source_date">Source date</label>
            <input id="source_date" name="source_date" type="date" required />
          </div>
          <div className="field">
            <label htmlFor="source_title">Source title</label>
            <input id="source_title" name="source_title" placeholder="Earnings release, filing, transcript excerpt" required />
          </div>
          <div className="field">
            <label htmlFor="source_type">Source type</label>
            <select id="source_type" name="source_type" defaultValue="earnings release">
              <option>earnings release</option>
              <option>SEC filing</option>
              <option>transcript excerpt</option>
              <option>manual note</option>
            </select>
          </div>
          <div className="field wide">
            <label htmlFor="source_url_or_description">Source URL or description</label>
            <input id="source_url_or_description" name="source_url_or_description" placeholder="URL, filing accession, or local source description" required />
          </div>
          <div className="field wide">
            <label htmlFor="pasted_text">Pasted source text</label>
            <textarea id="pasted_text" name="pasted_text" placeholder="Paste only the excerpt you want converted into evidence." required />
          </div>
          <label className="check-label wide">
            <input name="external_ai_acknowledged" type="checkbox" disabled={!aiEnabled} />
            <span>Allow this submitted text to be sent to the configured external AI provider</span>
          </label>
        </div>
        <div className="button-row">
          <button className="button" type="submit" disabled={!aiEnabled}>
            Extract evidence draft
          </button>
          <span className="badge">{aiEnabled ? "AI enabled" : "AI disabled"}</span>
          {draftMessage ? <span className="muted" aria-live="polite">{draftMessage}</span> : null}
        </div>
      </form>

      <form onSubmit={saveVerifiedEvidence}>
        <div className="form-grid">
          <div className="field">
            <label htmlFor="save_ticker">Save to ticker</label>
            <input id="save_ticker" name="save_ticker" defaultValue="NVDA" required />
          </div>
          <div className="field">
            <label htmlFor="source_date_verified">Verified source date</label>
            <input
              id="source_date_verified"
              name="source_date_verified"
              type="date"
              value={evidence.source_date}
              onChange={(event) => setEvidence({ ...evidence, source_date: event.target.value })}
              required
            />
          </div>
          <div className="field wide">
            <label htmlFor="claim">Verified claim</label>
            <input id="claim" name="claim" value={evidence.claim} onChange={(event) => setEvidence({ ...evidence, claim: event.target.value })} required />
          </div>
          <div className="field wide">
            <label htmlFor="evidence">Verified evidence detail</label>
            <textarea id="evidence" name="evidence" value={evidence.evidence} onChange={(event) => setEvidence({ ...evidence, evidence: event.target.value })} required />
          </div>
          <div className="field wide">
            <label htmlFor="source">Verified source</label>
            <input id="source" name="source" value={evidence.source} onChange={(event) => setEvidence({ ...evidence, source: event.target.value })} required />
          </div>
          <div className="field">
            <label htmlFor="confidence">Confidence</label>
            <select
              id="confidence"
              name="confidence"
              value={evidence.confidence}
              onChange={(event) => setEvidence({ ...evidence, confidence: event.target.value as EvidenceObject["confidence"] })}
            >
              <option>MEDIUM</option>
              <option>HIGH</option>
              <option>LOW</option>
            </select>
          </div>
          <div className="field wide">
            <label htmlFor="disproves_if">Disproves if</label>
            <textarea id="disproves_if" name="disproves_if" value={evidence.disproves_if} onChange={(event) => setEvidence({ ...evidence, disproves_if: event.target.value })} required />
          </div>
        </div>
        <div className="button-row">
          <button className="button" type="submit">
            Save verified evidence
          </button>
          <span className="badge">User verified</span>
          {evidence.confidence === "LOW" ? <span className="warn-text">LOW confidence cannot support action-changing decisions.</span> : null}
          {message ? <span className="muted" aria-live="polite">{message}</span> : null}
        </div>
      </form>
    </div>
  );
}
