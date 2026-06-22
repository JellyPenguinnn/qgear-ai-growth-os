from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.db.sqlite import add_earnings_review, add_evidence_object, list_earnings_reviews, list_evidence_objects
from app.schemas.requests import EarningsReviewRequest, EvidenceObjectRequest
from app.serializers import to_jsonable
from qgear_core.earnings import EarningsReview, classify_earnings_review
from qgear_core.enums import Confidence
from qgear_core.demo import DEMO_UNIVERSE, get_company
from qgear_core.models import Evidence

router = APIRouter(prefix="/earnings", tags=["earnings"])


@router.get("")
def earnings_lab() -> dict:
    stored_reviews = list_earnings_reviews()
    return {
        "checklist": [
            "Confirm revenue and EPS beat/miss.",
            "Compare guidance to prior expectations.",
            "Check AI-related segment, backlog, RPO, order, or customer evidence.",
            "Review gross margin, operating margin, and FCF trend.",
            "Classify thesis status change before action.",
        ],
        "demo_events": [
            {
                "ticker": company.ticker,
                "company_name": company.company_name,
                "thesis_status_change": company.metrics.latest_earnings_change.value,
                "score": company.score.total,
                "action_change": company.status.value,
            }
            for company in DEMO_UNIVERSE[:12]
        ],
        "stored_review_count": len(stored_reviews),
    }


@router.get("/{ticker}")
def ticker_earnings(ticker: str) -> dict:
    company = get_company(ticker)
    if not company:
        raise HTTPException(status_code=404, detail="Ticker not found in demo universe")
    evidence_objects = list_evidence_objects(company.ticker)
    reviews = list_earnings_reviews(company.ticker)
    return to_jsonable(
        {
            "ticker": company.ticker,
            "pre_earnings_checklist": [
                "What evidence would strengthen the thesis?",
                "What would break the thesis?",
                "What valuation hurdle must still clear after the report?",
            ],
            "post_earnings_analysis": {
                "revenue_growth_pct": company.metrics.revenue_growth_pct,
                "guidance_raised": company.metrics.guidance_raised,
                "ai_evidence_improved": company.metrics.ai_evidence_improved,
                "margin_expanded": company.metrics.margin_expanded,
                "fcf_improved": company.metrics.fcf_improved,
                "management_tone": "demo placeholder",
                "thesis_status_change": company.metrics.latest_earnings_change,
                "score": company.score,
                "action": company.decision,
            },
            "stored_evidence": evidence_objects,
            "stored_reviews": reviews,
        }
    )


@router.get("/{ticker}/evidence")
def ticker_evidence(ticker: str) -> dict:
    company = get_company(ticker)
    if not company:
        raise HTTPException(status_code=404, detail="Ticker not found in demo universe")
    return {"ticker": company.ticker, "evidence": list_evidence_objects(company.ticker)}


@router.post("/{ticker}/evidence")
def create_ticker_evidence(ticker: str, payload: EvidenceObjectRequest) -> dict:
    company = get_company(ticker)
    if not company:
        raise HTTPException(status_code=404, detail="Ticker not found in demo universe")
    evidence = add_evidence_object(company.ticker, payload.model_dump(), related_type="manual")
    return {"ticker": company.ticker, "evidence": evidence}


@router.get("/{ticker}/reviews")
def ticker_reviews(ticker: str) -> dict:
    company = get_company(ticker)
    if not company:
        raise HTTPException(status_code=404, detail="Ticker not found in demo universe")
    return {"ticker": company.ticker, "reviews": list_earnings_reviews(company.ticker)}


@router.post("/{ticker}/reviews")
def create_earnings_review(ticker: str, payload: EarningsReviewRequest) -> dict:
    company = get_company(ticker)
    if not company:
        raise HTTPException(status_code=404, detail="Ticker not found in demo universe")

    evidence_rows = [
        add_evidence_object(company.ticker, item.model_dump(), related_type="earnings_review")
        for item in payload.evidence
    ]
    evidence_items = tuple(
        Evidence(
            claim=item.claim,
            evidence=item.evidence,
            source=item.source,
            source_date=item.source_date,
            confidence=Confidence(item.confidence),
            disproves_if=item.disproves_if,
        )
        for item in payload.evidence
    )
    review_input = EarningsReview(
        ticker=company.ticker,
        fiscal_period=payload.fiscal_period,
        report_date=payload.report_date,
        revenue_surprise_pct=payload.revenue_surprise_pct,
        eps_surprise_pct=payload.eps_surprise_pct,
        guidance_raised=payload.guidance_raised,
        guidance_cut=payload.guidance_cut,
        guidance_cut_structural=payload.guidance_cut_structural,
        revenue_growth_accelerated=payload.revenue_growth_accelerated,
        ai_evidence_improved=payload.ai_evidence_improved,
        segment_growth_improved=payload.segment_growth_improved,
        margin_expanded=payload.margin_expanded,
        margin_deteriorated=payload.margin_deteriorated,
        fcf_improved=payload.fcf_improved,
        fcf_deteriorated=payload.fcf_deteriorated,
        management_tone=payload.management_tone,
        evidence=evidence_items,
    )
    thesis_change = classify_earnings_review(review_input)
    review = add_earnings_review(
        {**payload.model_dump(exclude={"evidence"}), "ticker": company.ticker},
        thesis_status_change=thesis_change.value,
        evidence_ids=[row["id"] for row in evidence_rows],
    )
    return to_jsonable(
        {
            "ticker": company.ticker,
            "thesis_status_change": thesis_change,
            "review": review,
            "evidence": evidence_rows,
            "buy_add_note": "Earnings evidence does not create a buy/add action without thesis, invalidation, valuation, technical, freshness, and risk gates.",
        }
    )
