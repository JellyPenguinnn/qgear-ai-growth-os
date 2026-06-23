from __future__ import annotations

from qgear_ai.models import AITask

EVIDENCE_OBJECT_SCHEMA = {
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

TASK_SCHEMAS = {
    AITask.EVIDENCE_EXTRACTION: {
        "type": "object",
        "required": ["summary", "evidence"],
        "properties": {
            "summary": {"type": "string"},
            "evidence": {"type": "array", "items": EVIDENCE_OBJECT_SCHEMA},
            "limits": {"type": "array", "items": {"type": "string"}},
        },
    },
    AITask.EARNINGS_SUMMARY: {
        "type": "object",
        "required": ["summary", "thesis_change_candidate", "evidence", "next_metrics_to_monitor"],
        "properties": {
            "summary": {"type": "string"},
            "revenue_eps_guidance_notes": {"type": "array", "items": {"type": "string"}},
            "ai_evidence_notes": {"type": "array", "items": {"type": "string"}},
            "margin_fcf_notes": {"type": "array", "items": {"type": "string"}},
            "risks": {"type": "array", "items": {"type": "string"}},
            "thesis_change_candidate": {"type": "string", "enum": ["STRENGTHENED", "UNCHANGED", "WEAKENED", "BROKEN"]},
            "evidence": {"type": "array", "items": EVIDENCE_OBJECT_SCHEMA},
            "next_metrics_to_monitor": {"type": "array", "items": {"type": "string"}},
        },
    },
    AITask.THESIS_UPDATE: {
        "type": "object",
        "required": [
            "thesis_statement",
            "what_must_go_right",
            "what_would_break_thesis",
            "key_metrics_to_monitor",
            "next_review_date",
            "evidence_objects",
            "confidence",
        ],
        "properties": {
            "thesis_statement": {"type": "string"},
            "what_must_go_right": {"type": "string"},
            "what_would_break_thesis": {"type": "string"},
            "key_metrics_to_monitor": {"type": "array", "items": {"type": "string"}},
            "next_review_date": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
            "evidence_objects": {"type": "array", "items": EVIDENCE_OBJECT_SCHEMA},
            "confidence": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH"]},
        },
    },
    AITask.RISK_EXTRACTION: {
        "type": "object",
        "required": ["risks", "evidence"],
        "properties": {
            "risks": {"type": "array", "items": {"type": "string"}},
            "evidence": {"type": "array", "items": EVIDENCE_OBJECT_SCHEMA},
        },
    },
    AITask.DECISION_EXPLANATION: {
        "type": "object",
        "required": ["explanation", "reasons", "blockers", "evidence", "confidence", "disproof_conditions"],
        "properties": {
            "explanation": {"type": "string"},
            "reasons": {"type": "array", "items": {"type": "string"}},
            "blockers": {"type": "array", "items": {"type": "string"}},
            "evidence": {"type": "array", "items": EVIDENCE_OBJECT_SCHEMA},
            "confidence": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH"]},
            "disproof_conditions": {"type": "array", "items": {"type": "string"}},
        },
    },
    AITask.PORTFOLIO_REVIEW: {
        "type": "object",
        "required": ["summary", "risk_observations", "review_prompts"],
        "properties": {
            "summary": {"type": "string"},
            "risk_observations": {"type": "array", "items": {"type": "string"}},
            "review_prompts": {"type": "array", "items": {"type": "string"}},
            "evidence": {"type": "array", "items": EVIDENCE_OBJECT_SCHEMA},
        },
    },
}
