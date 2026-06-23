from __future__ import annotations

from fastapi import APIRouter

from app.core.config import settings
from app.schemas.requests import (
    AIDecisionExplainRequest,
    AIEarningsSummaryRequest,
    AIEvidenceExtractionRequest,
    AIThesisUpdateRequest,
)
from qgear_ai.models import AITask
from qgear_ai.providers import build_ai_provider
from qgear_ai.service import AIResearchService

router = APIRouter(prefix="/ai", tags=["ai"])


def build_ai_service() -> AIResearchService:
    provider = build_ai_provider(
        settings.ai_provider,
        api_key=settings.openai_api_key,
        model=settings.ai_model,
    )
    return AIResearchService(provider)


def _payload_without_ack(payload) -> dict:
    return payload.model_dump(exclude={"external_ai_acknowledged"})


@router.get("/status")
def ai_status() -> dict:
    return build_ai_service().status()


@router.post("/evidence/extract")
def extract_evidence(payload: AIEvidenceExtractionRequest) -> dict:
    response = build_ai_service().run(
        AITask.EVIDENCE_EXTRACTION,
        _payload_without_ack(payload),
        external_ai_acknowledged=payload.external_ai_acknowledged,
    )
    return response.as_dict()


@router.post("/earnings/summarize")
def summarize_earnings(payload: AIEarningsSummaryRequest) -> dict:
    response = build_ai_service().run(
        AITask.EARNINGS_SUMMARY,
        _payload_without_ack(payload),
        external_ai_acknowledged=payload.external_ai_acknowledged,
    )
    return response.as_dict()


@router.post("/thesis/update")
def update_thesis(payload: AIThesisUpdateRequest) -> dict:
    response = build_ai_service().run(
        AITask.THESIS_UPDATE,
        _payload_without_ack(payload),
        external_ai_acknowledged=payload.external_ai_acknowledged,
    )
    return response.as_dict()


@router.post("/decision/explain")
def explain_decision(payload: AIDecisionExplainRequest) -> dict:
    response = build_ai_service().run(
        AITask.DECISION_EXPLANATION,
        _payload_without_ack(payload),
        external_ai_acknowledged=payload.external_ai_acknowledged,
    )
    return response.as_dict()
