from __future__ import annotations

import json
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from typing import Any

from qgear_ai.models import AIProviderMetadata, AIProviderMode, AIProviderResult, AITask
from qgear_ai.prompts import build_prompt


class AIProvider(ABC):
    @abstractmethod
    def complete_json(self, task: AITask, payload: dict[str, Any]) -> AIProviderResult:
        raise NotImplementedError

    @abstractmethod
    def status(self) -> AIProviderMetadata:
        raise NotImplementedError


class NoopAIProvider(AIProvider):
    def __init__(self, model: str | None = None) -> None:
        self.model = model

    def status(self) -> AIProviderMetadata:
        return AIProviderMetadata(
            provider="noop",
            mode=AIProviderMode.NONE,
            model=self.model,
            status="disabled",
            draft_only=True,
            external_call_performed=False,
        )

    def complete_json(self, task: AITask, payload: dict[str, Any]) -> AIProviderResult:
        return AIProviderResult(parsed=None, raw_text="", metadata=self.status())


class OpenAIProvider(AIProvider):
    def __init__(self, *, api_key: str | None, model: str = "gpt-5.5") -> None:
        self.api_key = api_key
        self.model = model

    def status(self) -> AIProviderMetadata:
        if not self.api_key:
            return AIProviderMetadata(
                provider="openai",
                mode=AIProviderMode.OPENAI,
                model=self.model,
                status="missing_api_key",
                draft_only=True,
                external_call_performed=False,
                error="OPENAI_API_KEY is not configured.",
            )
        return AIProviderMetadata(
            provider="openai",
            mode=AIProviderMode.OPENAI,
            model=self.model,
            status="configured",
            draft_only=True,
            external_call_performed=False,
        )

    def complete_json(self, task: AITask, payload: dict[str, Any]) -> AIProviderResult:
        if not self.api_key:
            return AIProviderResult(parsed=None, raw_text="", metadata=self.status())

        request_payload = {
            "model": self.model,
            "input": build_prompt(task, payload),
            "text": {"format": {"type": "json_object"}},
        }
        request = urllib.request.Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps(request_payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            return AIProviderResult(
                parsed=None,
                raw_text="",
                metadata=AIProviderMetadata(
                    provider="openai",
                    mode=AIProviderMode.OPENAI,
                    model=self.model,
                    status="error",
                    draft_only=True,
                    external_call_performed=True,
                    error=str(exc),
                ),
            )

        raw_text = _extract_openai_text(body)
        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            return AIProviderResult(
                parsed=None,
                raw_text=raw_text,
                metadata=AIProviderMetadata(
                    provider="openai",
                    mode=AIProviderMode.OPENAI,
                    model=self.model,
                    status="malformed_json",
                    draft_only=True,
                    external_call_performed=True,
                    error=str(exc),
                ),
            )

        return AIProviderResult(
            parsed=parsed,
            raw_text=raw_text,
            metadata=AIProviderMetadata(
                provider="openai",
                mode=AIProviderMode.OPENAI,
                model=self.model,
                status="ok",
                draft_only=True,
                external_call_performed=True,
            ),
        )


def _extract_openai_text(response_body: dict[str, Any]) -> str:
    if isinstance(response_body.get("output_text"), str):
        return response_body["output_text"]

    chunks: list[str] = []
    for output in response_body.get("output", []):
        if not isinstance(output, dict):
            continue
        for content in output.get("content", []):
            if isinstance(content, dict) and isinstance(content.get("text"), str):
                chunks.append(content["text"])
    return "".join(chunks)


def build_ai_provider(mode: str, *, api_key: str | None = None, model: str | None = None) -> AIProvider:
    normalized = mode.lower()
    if normalized == AIProviderMode.OPENAI.value:
        return OpenAIProvider(api_key=api_key, model=model or "gpt-5.5")
    return NoopAIProvider(model=model)
