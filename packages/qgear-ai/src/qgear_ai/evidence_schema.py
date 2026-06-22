from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ClaimConfidence(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass(frozen=True)
class AiClaim:
    claim: str
    evidence: str
    source: str
    source_date: str
    confidence: ClaimConfidence
    disproves_if: str


REQUIRED_JSON_SCHEMA = {
    "type": "object",
    "required": ["claim", "evidence", "source", "source_date", "confidence", "disproves_if"],
    "properties": {
        "claim": {"type": "string"},
        "evidence": {"type": "string"},
        "source": {"type": "string"},
        "source_date": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
        "confidence": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH"]},
        "disproves_if": {"type": "string"},
    },
}
