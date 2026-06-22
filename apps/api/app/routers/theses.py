from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.db.sqlite import approve_thesis, get_thesis
from app.schemas.requests import ThesisApprovalRequest
from qgear_core.demo import get_company

router = APIRouter(prefix="/theses", tags=["theses"])


@router.get("/{ticker}")
def read_thesis(ticker: str) -> dict:
    thesis = get_thesis(ticker)
    if not thesis:
        raise HTTPException(status_code=404, detail="No approved local thesis found for ticker")
    return thesis


@router.post("/{ticker}/approve")
def approve_ticker_thesis(ticker: str, payload: ThesisApprovalRequest) -> dict:
    if not get_company(ticker):
        raise HTTPException(status_code=404, detail="Ticker not found in demo universe")
    return approve_thesis(
        ticker=ticker,
        statement=payload.statement,
        must_go_right=payload.must_go_right,
        breaks_if=payload.breaks_if,
        key_metrics=payload.key_metrics,
        next_review_date=payload.next_review_date,
    )
