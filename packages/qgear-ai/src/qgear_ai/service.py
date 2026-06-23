from __future__ import annotations

from typing import Any

from qgear_ai.models import AIProviderMetadata, AIProviderMode, AIServiceResponse, AITask, DraftStatus
from qgear_ai.providers import AIProvider, NoopAIProvider
from qgear_ai.validator import validate_ai_payload

DISABLED_WARNING = "AI provider is disabled. Enable QGEAR_AI_PROVIDER=openai and explicitly submit source text to request a draft."
VERIFY_WARNING = "AI output is draft-only. The user must verify source, confidence, and disproof criteria before saving evidence."
LOW_CONFIDENCE_WARNING = "LOW-confidence AI evidence cannot support action-changing decisions."


class AIResearchService:
    def __init__(self, provider: AIProvider | None = None) -> None:
        self.provider = provider or NoopAIProvider()

    def status(self) -> dict[str, Any]:
        metadata = self.provider.status()
        return {
            "provider_metadata": metadata.as_dict(),
            "ai_enabled": metadata.mode != AIProviderMode.NONE and metadata.status == "configured",
            "requires_explicit_request": True,
            "requires_external_ai_acknowledgement": metadata.mode == AIProviderMode.OPENAI,
            "draft_only": True,
            "mutates_decision_state": False,
            "external_upload_policy": "No local portfolio, journal, thesis, or source text is sent externally unless the user submits it in a specific AI request.",
        }

    def run(
        self,
        task: AITask,
        payload: dict[str, Any],
        *,
        external_ai_acknowledged: bool = False,
        fake_provider_payload: dict[str, Any] | None = None,
    ) -> AIServiceResponse:
        metadata = self.provider.status()
        if metadata.mode == AIProviderMode.NONE:
            return AIServiceResponse(
                task=task,
                draft_status=DraftStatus.DISABLED,
                provider_metadata=metadata,
                warnings=(DISABLED_WARNING,),
            )

        if metadata.mode == AIProviderMode.OPENAI and not external_ai_acknowledged:
            return AIServiceResponse(
                task=task,
                draft_status=DraftStatus.REJECTED,
                provider_metadata=AIProviderMetadata(
                    provider=metadata.provider,
                    mode=metadata.mode,
                    model=metadata.model,
                    status="external_ack_required",
                    draft_only=True,
                    external_call_performed=False,
                    error="Set external_ai_acknowledged=true before sending supplied text to the configured AI provider.",
                ),
                warnings=("External AI acknowledgement is required before any provider call.",),
                validation_errors=("external_ai_acknowledged is required for OpenAI mode.",),
            )

        if metadata.status != "configured":
            return AIServiceResponse(
                task=task,
                draft_status=DraftStatus.ERROR,
                provider_metadata=metadata,
                warnings=("AI provider is not configured for this request.",),
                validation_errors=tuple(filter(None, (metadata.error,))),
            )

        provider_result = (
            self.provider.complete_json(task, payload)
            if fake_provider_payload is None
            else type("_FakeResult", (), {"parsed": fake_provider_payload, "metadata": metadata})()
        )
        parsed, evidence, errors = validate_ai_payload(task, provider_result.parsed)
        if errors or parsed is None:
            return AIServiceResponse(
                task=task,
                draft_status=DraftStatus.REJECTED,
                provider_metadata=provider_result.metadata,
                warnings=(VERIFY_WARNING,),
                validation_errors=errors,
            )

        warnings = [VERIFY_WARNING]
        if any(item.confidence.value == "LOW" for item in evidence):
            warnings.append(LOW_CONFIDENCE_WARNING)

        return AIServiceResponse(
            task=task,
            draft_status=DraftStatus.DRAFT,
            provider_metadata=provider_result.metadata,
            draft=parsed,
            evidence=evidence,
            warnings=tuple(warnings),
        )
