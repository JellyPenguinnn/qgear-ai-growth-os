from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AIProviderMode(str, Enum):
    NONE = "none"
    OPENAI = "openai"


class AITask(str, Enum):
    EVIDENCE_EXTRACTION = "evidence_extraction"
    EARNINGS_SUMMARY = "earnings_summary"
    THESIS_UPDATE = "thesis_update"
    RISK_EXTRACTION = "risk_extraction"
    DECISION_EXPLANATION = "decision_explanation"
    PORTFOLIO_REVIEW = "portfolio_review"


class DraftStatus(str, Enum):
    DISABLED = "disabled"
    DRAFT = "draft"
    REJECTED = "rejected"
    ERROR = "error"


class ClaimConfidence(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass(frozen=True)
class AiEvidence:
    claim: str
    evidence: str
    source: str
    source_date: str
    confidence: ClaimConfidence
    disproves_if: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "claim": self.claim,
            "evidence": self.evidence,
            "source": self.source,
            "source_date": self.source_date,
            "confidence": self.confidence.value,
            "disproves_if": self.disproves_if,
        }


@dataclass(frozen=True)
class AIProviderMetadata:
    provider: str
    mode: AIProviderMode
    model: str | None
    status: str
    draft_only: bool = True
    external_call_performed: bool = False
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "mode": self.mode.value,
            "model": self.model,
            "status": self.status,
            "draft_only": self.draft_only,
            "external_call_performed": self.external_call_performed,
            "error": self.error,
        }


@dataclass(frozen=True)
class AIProviderResult:
    parsed: dict[str, Any] | None
    raw_text: str
    metadata: AIProviderMetadata


@dataclass(frozen=True)
class AIServiceResponse:
    task: AITask
    draft_status: DraftStatus
    provider_metadata: AIProviderMetadata
    draft: dict[str, Any] = field(default_factory=dict)
    evidence: tuple[AiEvidence, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    validation_errors: tuple[str, ...] = field(default_factory=tuple)
    requires_user_verification: bool = True
    mutates_decision_state: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "task": self.task.value,
            "draft_status": self.draft_status.value,
            "provider_metadata": self.provider_metadata.as_dict(),
            "draft": self.draft,
            "evidence": [item.as_dict() for item in self.evidence],
            "warnings": list(self.warnings),
            "validation_errors": list(self.validation_errors),
            "requires_user_verification": self.requires_user_verification,
            "mutates_decision_state": self.mutates_decision_state,
            "disclaimer": "AI output is draft research assistance only and does not change Q-GEAR decision state until the user verifies evidence.",
        }
