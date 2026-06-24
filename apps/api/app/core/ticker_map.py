from __future__ import annotations

import json
from pathlib import Path

from app.core.config import ROOT

TICKER_CIK_MAP_PATH = ROOT / "data" / "demo" / "ticker_cik_map.json"


def load_ticker_cik_map(path: Path = TICKER_CIK_MAP_PATH) -> dict[str, str]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return {str(ticker).upper(): str(cik).zfill(10) for ticker, cik in payload.items()}


def ticker_cik(ticker: str) -> str | None:
    return load_ticker_cik_map().get(ticker.upper())
