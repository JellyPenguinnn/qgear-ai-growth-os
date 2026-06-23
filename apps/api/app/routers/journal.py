from __future__ import annotations

from fastapi import APIRouter

from app.db.sqlite import add_journal_entry, list_journal_entries
from app.schemas.requests import JournalEntryRequest

router = APIRouter(prefix="/journal", tags=["journal"])


@router.get("")
def read_journal() -> dict:
    return {"entries": list_journal_entries()}


def build_journal_analytics() -> dict:
    entries = list_journal_entries()
    action_counts: dict[str, int] = {}
    mistake_counts: dict[str, int] = {}
    evidence_quality_counts: dict[str, int] = {}
    outcome_counts: dict[str, int] = {}
    evidence_backed = 0
    unresolved = 0
    unresolved_later_reviews = 0
    followed_count = 0
    process_score_total = 0.0
    for entry in entries:
        action = entry["action"]
        action_counts[action] = action_counts.get(action, 0) + 1
        mistake = entry.get("mistake_category") or "NONE"
        quality = entry.get("evidence_quality") or "MEDIUM"
        outcome = entry.get("decision_outcome") or "PENDING"
        mistake_counts[mistake] = mistake_counts.get(mistake, 0) + 1
        evidence_quality_counts[quality] = evidence_quality_counts.get(quality, 0) + 1
        outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1
        if entry["evidence"].strip() and entry["invalidation_rule"].strip():
            evidence_backed += 1
        if not entry.get("later_outcome"):
            unresolved += 1
        if not entry.get("later_review"):
            unresolved_later_reviews += 1
        if entry.get("followed_system"):
            followed_count += 1
        process_score_total += float(entry.get("process_score") or 0)
    entry_count = len(entries)
    return {
        "entry_count": entry_count,
        "action_counts": action_counts,
        "evidence_backed_count": evidence_backed,
        "unresolved_outcome_count": unresolved,
        "outcome_counts": outcome_counts,
        "mistake_counts": mistake_counts,
        "evidence_quality_counts": evidence_quality_counts,
        "followed_system_rate_pct": round((followed_count / entry_count * 100) if entry_count else 0, 2),
        "average_process_score": round((process_score_total / entry_count) if entry_count else 0, 2),
        "unresolved_later_review_count": unresolved_later_reviews,
        "process_note": "Analytics are local process review only; they are not trade instructions.",
    }


@router.get("/analytics")
def journal_analytics() -> dict:
    return build_journal_analytics()


@router.post("")
def create_journal_entry(payload: JournalEntryRequest) -> dict:
    return add_journal_entry(payload.model_dump())
