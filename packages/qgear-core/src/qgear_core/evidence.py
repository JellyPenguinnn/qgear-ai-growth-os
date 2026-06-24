from __future__ import annotations

from datetime import date
from statistics import mean

from qgear_core.enums import Confidence, DataMode, EvidenceSourceType, EvidenceVerificationStatus
from qgear_core.models import Evidence

ACTION_SUPPORTING_VERIFICATION_STATUSES = {
    EvidenceVerificationStatus.USER_VERIFIED,
    EvidenceVerificationStatus.PROVIDER_VERIFIED,
    EvidenceVerificationStatus.SYSTEM_VALIDATED,
}
CONTEXT_ONLY_SOURCE_TYPES = {
    EvidenceSourceType.PRICE_PROVIDER,
    EvidenceSourceType.MACRO_PROVIDER,
    EvidenceSourceType.ENERGY_PROVIDER,
}
SOURCE_QUALITY_MINIMUM = 70
EVIDENCE_COVERAGE_MINIMUM = 70

_PRICE_TERMS = (
    "price",
    "dropped",
    "drop",
    "down",
    "fell",
    "fall",
    "cheaper",
    "cheap",
    "discount",
    "pullback",
    "oversold",
    "drawdown",
)
_FUNDAMENTAL_TERMS = (
    "revenue",
    "sales",
    "earnings",
    "eps",
    "guidance",
    "margin",
    "free cash flow",
    "fcf",
    "cash flow",
    "backlog",
    "rpo",
    "orders",
    "order",
    "segment",
    "customer",
    "customers",
    "demand",
    "profit",
    "operating income",
)


def _source_type_label(source_type: EvidenceSourceType | None) -> str:
    return source_type.value if source_type else "missing"


def _verification_label(status: EvidenceVerificationStatus | None) -> str:
    return status.value if status else "missing"


def evidence_looks_price_only(evidence: Evidence) -> bool:
    text = f"{evidence.claim} {evidence.evidence}".lower()
    has_price_term = any(term in text for term in _PRICE_TERMS)
    has_fundamental_term = any(term in text for term in _FUNDAMENTAL_TERMS)
    return has_price_term and not has_fundamental_term


def is_evidence_action_supporting(evidence: Evidence, mode: DataMode = DataMode.DEMO) -> bool:
    return not validate_action_evidence((evidence,), mode=mode)


def validate_action_evidence(evidence_items: tuple[Evidence, ...], mode: DataMode = DataMode.DEMO) -> tuple[str, ...]:
    if not evidence_items:
        return ("Fresh positive evidence must include a structured evidence object.",)

    errors: list[str] = []
    for index, evidence in enumerate(evidence_items, start=1):
        prefix = f"Positive evidence #{index}"
        if not evidence.claim.strip():
            errors.append(f"{prefix} is missing a claim.")
        if not evidence.evidence.strip():
            errors.append(f"{prefix} is missing evidence detail.")
        if not evidence.source.strip():
            errors.append(f"{prefix} is missing a source.")
        if not evidence.source_date.strip():
            errors.append(f"{prefix} is missing a source date.")
        else:
            try:
                date.fromisoformat(evidence.source_date)
            except ValueError:
                errors.append(f"{prefix} source date must be ISO format YYYY-MM-DD.")
        if evidence.confidence == Confidence.LOW:
            errors.append(f"{prefix} confidence is LOW; action-changing evidence must be at least MEDIUM confidence.")
        if not evidence.disproves_if.strip():
            errors.append(f"{prefix} is missing disproof criteria.")

        if evidence.source_type is None:
            errors.append(f"{prefix} is missing a source type.")
        elif evidence.source_type == EvidenceSourceType.AI_DRAFT:
            errors.append(f"{prefix} is AI_DRAFT; AI drafts require user verification before supporting buy/add.")
        elif evidence.source_type in CONTEXT_ONLY_SOURCE_TYPES:
            errors.append(
                f"{prefix} source type {_source_type_label(evidence.source_type)} is review context only and cannot support buy/add by itself."
            )
        elif mode == DataMode.LIVE and evidence.source_type == EvidenceSourceType.DEMO:
            errors.append(f"{prefix} is DEMO evidence; demo evidence cannot support live-mode buy/add decisions.")

        if evidence.verification_status is None:
            errors.append(f"{prefix} is missing verification status.")
        elif evidence.verification_status not in ACTION_SUPPORTING_VERIFICATION_STATUSES:
            errors.append(
                f"{prefix} verification status {_verification_label(evidence.verification_status)} cannot support buy/add."
            )

        if evidence_looks_price_only(evidence):
            errors.append(f"{prefix} appears price-only; price movement alone is insufficient evidence.")

    return tuple(errors)


def calculate_source_quality_score(
    evidence_items: tuple[Evidence, ...],
    provider_statuses: tuple[str, ...] = (),
) -> float:
    if not evidence_items:
        return 0

    scores = [_single_source_quality_score(evidence) for evidence in evidence_items]
    score = mean(scores)
    if provider_statuses:
        bad_statuses = [status for status in provider_statuses if status not in {"ok", "demo", "system_validated"}]
        score -= min(40, len(bad_statuses) * 15)
    return round(max(0, min(100, score)), 2)


def calculate_evidence_coverage_score(
    evidence_items: tuple[Evidence, ...],
    required_topics: tuple[str, ...] = (),
) -> float:
    if not evidence_items:
        return 0
    if not required_topics:
        return 100

    combined = "\n".join(f"{item.claim} {item.evidence}" for item in evidence_items).lower()
    covered = sum(1 for topic in required_topics if topic.lower() in combined)
    return round(covered / len(required_topics) * 100, 2)


def _single_source_quality_score(evidence: Evidence) -> float:
    source_score = {
        EvidenceSourceType.DEMO: 70,
        EvidenceSourceType.MANUAL: 70,
        EvidenceSourceType.AI_DRAFT: 20,
        EvidenceSourceType.AI_USER_VERIFIED: 75,
        EvidenceSourceType.SEC_FILING: 95,
        EvidenceSourceType.EARNINGS_RELEASE: 90,
        EvidenceSourceType.TRANSCRIPT: 85,
        EvidenceSourceType.PRICE_PROVIDER: 70,
        EvidenceSourceType.MACRO_PROVIDER: 60,
        EvidenceSourceType.ENERGY_PROVIDER: 60,
        EvidenceSourceType.OTHER: 60,
    }.get(evidence.source_type, 0)

    verification_score = {
        EvidenceVerificationStatus.UNVERIFIED: -30,
        EvidenceVerificationStatus.USER_VERIFIED: 5,
        EvidenceVerificationStatus.PROVIDER_VERIFIED: 10,
        EvidenceVerificationStatus.SYSTEM_VALIDATED: 5,
        EvidenceVerificationStatus.REJECTED: -80,
    }.get(evidence.verification_status, -40)

    score = source_score + verification_score
    if evidence.confidence == Confidence.LOW:
        score = min(score, 40)
    elif evidence.confidence == Confidence.MEDIUM:
        score = min(score, 80)
    if not evidence.source_date.strip():
        score = min(score, 35)
    if evidence_looks_price_only(evidence):
        score = min(score, 35)
    return max(0, min(100, score))
