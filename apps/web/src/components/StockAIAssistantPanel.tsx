"use client";

import { useState } from "react";
import type { AIDraftResponse, AIStatusResponse, DecisionState, EvidenceObject } from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

type DraftView =
  | {
      label: string;
      response?: AIDraftResponse;
      localDraft?: string;
      error?: string;
    }
  | null;

function nextQuarterReviewDate() {
  const date = new Date();
  date.setDate(date.getDate() + 90);
  return date.toISOString().slice(0, 10);
}

async function postAiDraft(path: string, payload: Record<string, unknown>) {
  const response = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!response.ok) {
    throw new Error(`AI draft request failed with HTTP ${response.status}.`);
  }
  return (await response.json()) as AIDraftResponse;
}

export function StockAIAssistantPanel({
  ticker,
  aiStatus,
  decisionState,
  score,
  reasons,
  blockers,
  evidence,
  existingThesis,
  nextReviewDate
}: {
  ticker: string;
  aiStatus: AIStatusResponse;
  decisionState: DecisionState;
  score: number;
  reasons: string[];
  blockers: string[];
  evidence: EvidenceObject[];
  existingThesis: string;
  nextReviewDate?: string | null;
}) {
  const [acknowledged, setAcknowledged] = useState(false);
  const [loading, setLoading] = useState<string | null>(null);
  const [draft, setDraft] = useState<DraftView>(null);

  const aiEnabled = aiStatus.ai_enabled;
  const provider = aiStatus.provider_metadata.provider;

  async function runDecisionExplain() {
    if (!aiEnabled) {
      return;
    }
    if (aiStatus.requires_external_ai_acknowledgement && !acknowledged) {
      setDraft({ label: "Decision explanation", error: "Confirm explicit external AI acknowledgement before sending source text." });
      return;
    }
    setLoading("decision");
    try {
      const response = await postAiDraft("/ai/decision/explain", {
        ticker,
        decision_state: decisionState,
        score,
        reasons,
        blockers,
        evidence,
        external_ai_acknowledged: acknowledged
      });
      setDraft({ label: "Decision explanation", response });
    } catch (error) {
      setDraft({ label: "Decision explanation", error: error instanceof Error ? error.message : "AI draft request failed." });
    } finally {
      setLoading(null);
    }
  }

  async function runThesisUpdate() {
    if (!aiEnabled) {
      return;
    }
    if (aiStatus.requires_external_ai_acknowledgement && !acknowledged) {
      setDraft({ label: "Thesis update", error: "Confirm explicit external AI acknowledgement before sending thesis/evidence text." });
      return;
    }
    setLoading("thesis");
    try {
      const response = await postAiDraft("/ai/thesis/update", {
        ticker,
        existing_thesis: existingThesis || "No approved thesis exists yet.",
        evidence,
        next_review_date: nextReviewDate || nextQuarterReviewDate(),
        external_ai_acknowledged: acknowledged
      });
      setDraft({ label: "Thesis update", response });
    } catch (error) {
      setDraft({ label: "Thesis update", error: error instanceof Error ? error.message : "AI draft request failed." });
    } finally {
      setLoading(null);
    }
  }

  function createJournalDraft() {
    const firstReason = reasons[0] ?? "No verified action-changing evidence is available.";
    const firstBlocker = blockers[0] ?? "No hard blocker surfaced, but all Q-GEAR gates still need confirmation.";
    const topEvidence = evidence[0]?.claim ?? "No verified evidence selected.";
    setDraft({
      label: "Journal draft",
      localDraft: `Draft journal for ${ticker}: decision state ${decisionState}. Why: ${firstReason} Blocked because: ${firstBlocker} Evidence checked: ${topEvidence}. Confirm thesis, invalidation rule, expected IRR, technical regime, evidence freshness, and portfolio risk budget before any manual action outside Q-GEAR.`
    });
  }

  return (
    <div className="assistant-panel">
      <div className="assistant-status">
        <span className="eyebrow">AI assistant</span>
        <strong>{aiEnabled ? "Configured" : "Disabled"}</strong>
        <small>
          Provider: {provider}. Draft-only: {aiStatus.draft_only ? "yes" : "no"}. Decision mutation:{" "}
          {aiStatus.mutates_decision_state ? "possible" : "never automatic"}.
        </small>
      </div>
      <label className="check-label">
        <input
          type="checkbox"
          checked={acknowledged}
          onChange={(event) => setAcknowledged(event.target.checked)}
          disabled={!aiStatus.requires_external_ai_acknowledgement}
        />
        I explicitly choose to send ticker, decision state, score, reasons, blockers, verified evidence, current thesis,
        and next review date to the configured external AI provider for this draft only.
      </label>
      <div className="assistant-actions">
        <button className="button" type="button" onClick={runDecisionExplain} disabled={!aiEnabled || loading !== null}>
          {loading === "decision" ? "Drafting..." : aiEnabled ? "Explain decision with AI" : "AI disabled"}
        </button>
        <button className="button secondary" type="button" onClick={runThesisUpdate} disabled={!aiEnabled || loading !== null}>
          {loading === "thesis" ? "Drafting..." : aiEnabled ? "Draft thesis update with AI" : "AI disabled"}
        </button>
        <a className="button secondary" href={`/evidence?ticker=${ticker}`}>
          Extract evidence from pasted text
        </a>
        <button className="button secondary" type="button" onClick={createJournalDraft}>
          Create journal draft
        </button>
      </div>
      {!aiEnabled ? <p className="warn-text">AI drafting is disabled by default. Configure AI only when you explicitly want external draft assistance.</p> : null}
      <p className="muted">{aiStatus.external_upload_policy}</p>
      {draft ? (
        <div className="assistant-draft">
          <strong>{draft.label}</strong>
          {draft.error ? <p className="warn-text">{draft.error}</p> : null}
          {draft.localDraft ? <p>{draft.localDraft}</p> : null}
          {draft.response ? (
            <>
              <p className="muted">
                Status: {draft.response.draft_status}. User verification required:{" "}
                {draft.response.requires_user_verification ? "yes" : "no"}.
              </p>
              {draft.response.warnings.map((warning) => (
                <p className="warn-text" key={warning}>
                  {warning}
                </p>
              ))}
              {draft.response.validation_errors.map((error) => (
                <p className="danger-text" key={error}>
                  {error}
                </p>
              ))}
              <pre>{JSON.stringify(draft.response.draft, null, 2)}</pre>
            </>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
