from __future__ import annotations

import unittest

from qgear_ai.models import AIProviderMetadata, AIProviderMode, AIProviderResult, AITask, DraftStatus
from qgear_ai.providers import AIProvider, NoopAIProvider
from qgear_ai.service import AIResearchService


class FakeConfiguredProvider(AIProvider):
    def __init__(self, payload: dict | None) -> None:
        self.payload = payload

    def status(self) -> AIProviderMetadata:
        return AIProviderMetadata(
            provider="fake",
            mode=AIProviderMode.OPENAI,
            model="fake-model",
            status="configured",
            draft_only=True,
            external_call_performed=False,
        )

    def complete_json(self, task: AITask, payload: dict) -> AIProviderResult:
        return AIProviderResult(
            parsed=self.payload,
            raw_text="{}",
            metadata=AIProviderMetadata(
                provider="fake",
                mode=AIProviderMode.OPENAI,
                model="fake-model",
                status="ok",
                draft_only=True,
                external_call_performed=True,
            ),
        )


VALID_EVIDENCE_PAYLOAD = {
    "summary": "Draft evidence extracted from a user-supplied earnings excerpt.",
    "evidence": [
        {
            "claim": "AI-related demand became more measurable.",
            "evidence": "The supplied excerpt says revenue growth accelerated and guidance was raised.",
            "source": "Manual earnings excerpt",
            "source_date": "2026-06-22",
            "confidence": "MEDIUM",
            "disproves_if": "Future guidance is cut or AI demand metrics deteriorate.",
        }
    ],
}


class AIServiceTests(unittest.TestCase):
    def test_noop_provider_is_disabled_and_no_external_call(self) -> None:
        response = AIResearchService(NoopAIProvider()).run(AITask.EVIDENCE_EXTRACTION, {"ticker": "NVDA"})

        self.assertEqual(response.draft_status, DraftStatus.DISABLED)
        self.assertFalse(response.provider_metadata.external_call_performed)
        self.assertTrue(response.requires_user_verification)
        self.assertFalse(response.mutates_decision_state)

    def test_openai_mode_requires_external_acknowledgement(self) -> None:
        response = AIResearchService(FakeConfiguredProvider(VALID_EVIDENCE_PAYLOAD)).run(
            AITask.EVIDENCE_EXTRACTION,
            {"ticker": "NVDA", "pasted_text": "revenue growth accelerated"},
            external_ai_acknowledged=False,
        )

        self.assertEqual(response.draft_status, DraftStatus.REJECTED)
        self.assertFalse(response.provider_metadata.external_call_performed)
        self.assertIn("external_ai_acknowledged", response.validation_errors[0])

    def test_valid_draft_is_returned_but_cannot_mutate_decision_state(self) -> None:
        response = AIResearchService(FakeConfiguredProvider(VALID_EVIDENCE_PAYLOAD)).run(
            AITask.EVIDENCE_EXTRACTION,
            {"ticker": "NVDA", "pasted_text": "revenue growth accelerated"},
            external_ai_acknowledged=True,
        )

        self.assertEqual(response.draft_status, DraftStatus.DRAFT)
        self.assertEqual(len(response.evidence), 1)
        self.assertTrue(response.requires_user_verification)
        self.assertFalse(response.mutates_decision_state)

    def test_malformed_ai_output_is_rejected(self) -> None:
        response = AIResearchService(FakeConfiguredProvider({"summary": "missing evidence"})).run(
            AITask.EVIDENCE_EXTRACTION,
            {"ticker": "NVDA", "pasted_text": "revenue growth accelerated"},
            external_ai_acknowledged=True,
        )

        self.assertEqual(response.draft_status, DraftStatus.REJECTED)
        self.assertTrue(any("evidence" in error for error in response.validation_errors))

    def test_action_state_fields_are_rejected(self) -> None:
        payload = {
            **VALID_EVIDENCE_PAYLOAD,
            "decision_state": "ADD_ALLOWED",
        }
        response = AIResearchService(FakeConfiguredProvider(payload)).run(
            AITask.EVIDENCE_EXTRACTION,
            {"ticker": "NVDA", "pasted_text": "revenue growth accelerated"},
            external_ai_acknowledged=True,
        )

        self.assertEqual(response.draft_status, DraftStatus.REJECTED)
        self.assertTrue(any("not allowed" in error for error in response.validation_errors))

    def test_low_confidence_draft_warns_and_price_only_claim_is_rejected(self) -> None:
        low_confidence = {
            "summary": "Draft evidence.",
            "evidence": [
                {
                    "claim": "AI demand may be improving.",
                    "evidence": "The supplied excerpt gives limited detail.",
                    "source": "Manual source",
                    "source_date": "2026-06-22",
                    "confidence": "LOW",
                    "disproves_if": "Future source data does not confirm the claim.",
                }
            ],
        }
        low_response = AIResearchService(FakeConfiguredProvider(low_confidence)).run(
            AITask.EVIDENCE_EXTRACTION,
            {"ticker": "NVDA", "pasted_text": "limited detail"},
            external_ai_acknowledged=True,
        )
        self.assertEqual(low_response.draft_status, DraftStatus.REJECTED)
        self.assertTrue(any("LOW" in error for error in low_response.validation_errors))

        price_only = {
            "summary": "Draft evidence.",
            "evidence": [
                {
                    "claim": "The stock is down 20%, so it looks better.",
                    "evidence": "Price dropped and the dip looks attractive.",
                    "source": "Manual note",
                    "source_date": "2026-06-22",
                    "confidence": "MEDIUM",
                    "disproves_if": "Price recovers.",
                }
            ],
        }
        price_response = AIResearchService(FakeConfiguredProvider(price_only)).run(
            AITask.EVIDENCE_EXTRACTION,
            {"ticker": "NVDA", "pasted_text": "stock is down 20%"},
            external_ai_acknowledged=True,
        )
        self.assertEqual(price_response.draft_status, DraftStatus.REJECTED)
        self.assertTrue(any("price movement alone" in error for error in price_response.validation_errors))


if __name__ == "__main__":
    unittest.main()
