from __future__ import annotations

from datetime import date
from typing import Any

from qgear_ai.models import AITask, AiEvidence, ClaimConfidence
from qgear_ai.schemas import TASK_SCHEMAS

ACTION_STATE_FIELDS = {
    "action",
    "action_change",
    "decision_state",
    "final_action",
    "state",
    "trade_instruction",
}

PRICE_ONLY_TERMS = (
    "price dropped",
    "price fell",
    "share price fell",
    "stock is down",
    "stock fell",
    "down 20%",
    "down 25%",
    "dip",
    "cheap because price",
)


def _type_name(value: Any) -> str:
    return type(value).__name__


def _validate_string(value: Any, path: str, errors: list[str], *, allow_blank: bool = False) -> None:
    if not isinstance(value, str):
        errors.append(f"{path} must be a string, got {_type_name(value)}.")
        return
    if not allow_blank and not value.strip():
        errors.append(f"{path} must not be blank.")


def _validate_string_array(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{path} must be an array of strings.")
        return
    for index, item in enumerate(value):
        _validate_string(item, f"{path}[{index}]", errors)


def _validate_no_action_fields(payload: Any, errors: list[str], path: str = "$") -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in ACTION_STATE_FIELDS:
                errors.append(f"{path}.{key} is not allowed in AI drafts; AI must not create action-state mutations.")
            _validate_no_action_fields(value, errors, f"{path}.{key}")
    elif isinstance(payload, list):
        for index, item in enumerate(payload):
            _validate_no_action_fields(item, errors, f"{path}[{index}]")


def _looks_price_only(evidence: dict[str, Any]) -> bool:
    text = " ".join(str(evidence.get(field, "")) for field in ("claim", "evidence")).lower()
    has_price_language = any(term in text for term in PRICE_ONLY_TERMS)
    has_fundamental_language = any(
        term in text
        for term in (
            "revenue",
            "guidance",
            "margin",
            "free cash flow",
            "fcf",
            "backlog",
            "rpo",
            "orders",
            "segment",
            "customer",
            "earnings",
        )
    )
    return has_price_language and not has_fundamental_language


def _validate_evidence_object(value: Any, path: str, errors: list[str], *, action_supporting: bool) -> AiEvidence | None:
    if not isinstance(value, dict):
        errors.append(f"{path} must be an evidence object.")
        return None

    for required in ("claim", "evidence", "source", "source_date", "confidence", "disproves_if"):
        if required not in value:
            errors.append(f"{path}.{required} is required.")

    for key in ("claim", "evidence", "source", "source_date", "disproves_if"):
        if key in value:
            _validate_string(value[key], f"{path}.{key}", errors)

    parsed_date = value.get("source_date")
    if isinstance(parsed_date, str) and parsed_date.strip():
        try:
            date.fromisoformat(parsed_date)
        except ValueError:
            errors.append(f"{path}.source_date must be ISO format YYYY-MM-DD.")

    confidence = value.get("confidence")
    parsed_confidence: ClaimConfidence | None = None
    if confidence not in {item.value for item in ClaimConfidence}:
        errors.append(f"{path}.confidence must be LOW, MEDIUM, or HIGH.")
    else:
        parsed_confidence = ClaimConfidence(confidence)
        if action_supporting and parsed_confidence == ClaimConfidence.LOW:
            errors.append(f"{path}.confidence is LOW; action-supporting AI evidence must be at least MEDIUM before user verification.")

    source = str(value.get("source", "")).strip().lower()
    if source in {"unknown", "n/a", "none", "source not provided", "not provided"}:
        errors.append(f"{path}.source must identify a real supplied or manual source.")

    if _looks_price_only(value):
        errors.append(f"{path} appears to use price movement alone as evidence, which Q-GEAR rejects.")

    if errors or parsed_confidence is None:
        return None

    return AiEvidence(
        claim=value["claim"].strip(),
        evidence=value["evidence"].strip(),
        source=value["source"].strip(),
        source_date=value["source_date"].strip(),
        confidence=parsed_confidence,
        disproves_if=value["disproves_if"].strip(),
    )


def _validate_by_schema(payload: dict[str, Any], schema: dict[str, Any], errors: list[str], path: str = "$") -> None:
    for required in schema.get("required", ()):
        if required not in payload:
            errors.append(f"{path}.{required} is required.")

    properties = schema.get("properties", {})
    for key, expected in properties.items():
        if key not in payload:
            continue
        value = payload[key]
        expected_type = expected.get("type")
        child_path = f"{path}.{key}"
        if expected_type == "string":
            _validate_string(value, child_path, errors)
            if "enum" in expected and value not in expected["enum"]:
                errors.append(f"{child_path} must be one of {', '.join(expected['enum'])}.")
            if expected.get("pattern") == "^\\d{4}-\\d{2}-\\d{2}$" and isinstance(value, str):
                try:
                    date.fromisoformat(value)
                except ValueError:
                    errors.append(f"{child_path} must be ISO format YYYY-MM-DD.")
        elif expected_type == "array":
            items = expected.get("items", {})
            if not isinstance(value, list):
                errors.append(f"{child_path} must be an array.")
            elif items == {"type": "string"}:
                _validate_string_array(value, child_path, errors)
        elif expected_type == "object":
            if not isinstance(value, dict):
                errors.append(f"{child_path} must be an object.")


def validate_ai_payload(task: AITask, payload: Any, *, action_supporting: bool = True) -> tuple[dict[str, Any] | None, tuple[AiEvidence, ...], tuple[str, ...]]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return None, (), ("AI output must be a JSON object.",)

    _validate_no_action_fields(payload, errors)
    schema = TASK_SCHEMAS[task]
    _validate_by_schema(payload, schema, errors)

    evidence_keys = ("evidence", "evidence_objects")
    evidence_values: list[dict[str, Any]] = []
    for key in evidence_keys:
        if key in payload:
            if not isinstance(payload[key], list):
                errors.append(f"$.{key} must be an array.")
            else:
                evidence_values.extend(payload[key])

    evidence: list[AiEvidence] = []
    for index, value in enumerate(evidence_values):
        parsed = _validate_evidence_object(value, f"$.evidence[{index}]", errors, action_supporting=action_supporting)
        if parsed is not None:
            evidence.append(parsed)

    if errors:
        return None, (), tuple(errors)
    return payload, tuple(evidence), ()
