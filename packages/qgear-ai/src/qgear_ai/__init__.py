"""AI prompt, provider, and evidence helpers for Q-GEAR."""

from qgear_ai.models import (
    AIProviderMetadata,
    AIProviderMode,
    AIServiceResponse,
    AITask,
    AiEvidence,
    ClaimConfidence,
    DraftStatus,
)
from qgear_ai.providers import AIProvider, NoopAIProvider, OpenAIProvider, build_ai_provider
from qgear_ai.service import AIResearchService

__all__ = [
    "AIProvider",
    "AIProviderMetadata",
    "AIProviderMode",
    "AIResearchService",
    "AIServiceResponse",
    "AITask",
    "AiEvidence",
    "ClaimConfidence",
    "DraftStatus",
    "NoopAIProvider",
    "OpenAIProvider",
    "build_ai_provider",
]
