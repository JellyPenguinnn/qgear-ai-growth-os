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
    evidence_backed = 0
    unresolved = 0
    for entry in entries:
        action = entry["action"]
        action_counts[action] = action_counts.get(action, 0) + 1
        if entry["evidence"].strip() and entry["invalidation_rule"].strip():
            evidence_backed += 1
        if not entry.get("later_outcome"):
            unresolved += 1
    return {
        "entry_count": len(entries),
        "action_counts": action_counts,
        "evidence_backed_count": evidence_backed,
        "unresolved_outcome_count": unresolved,
        "process_note": "Analytics are local process review only; they are not trade instructions.",
    }


@router.get("/analytics")
def journal_analytics() -> dict:
    return build_journal_analytics()


@router.post("")
def create_journal_entry(payload: JournalEntryRequest) -> dict:
    return add_journal_entry(payload.model_dump())
