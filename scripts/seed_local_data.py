from __future__ import annotations

import pathlib
import json
import sys
from datetime import date


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "qgear-core" / "src"))
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.db.analytics import init_duckdb  # noqa: E402
from app.db.sqlite import db_path, init_db  # noqa: E402
from qgear_core.demo import DEMO_UNIVERSE  # noqa: E402


def validate_demo_universe() -> list[str]:
    errors: list[str] = []
    tickers = [company.ticker for company in DEMO_UNIVERSE]
    duplicate_tickers = sorted({ticker for ticker in tickers if tickers.count(ticker) > 1})
    if duplicate_tickers:
        errors.append(f"Duplicate demo tickers: {', '.join(duplicate_tickers)}")

    seed_path = ROOT / "data" / "demo" / "seed_universe.json"
    seed_payload = json.loads(seed_path.read_text(encoding="utf-8"))
    seed_tickers = seed_payload.get("tickers", [])
    if sorted(seed_tickers) != sorted(tickers):
        errors.append("data/demo/seed_universe.json tickers do not match qgear_core.demo.DEMO_UNIVERSE")

    for company in DEMO_UNIVERSE:
        if not company.evidence:
            errors.append(f"{company.ticker} has no evidence objects")
        for item in company.evidence:
            for field_name in ("claim", "evidence", "source", "source_date", "confidence", "disproves_if"):
                if not getattr(item, field_name):
                    errors.append(f"{company.ticker} evidence missing {field_name}")
            try:
                date.fromisoformat(item.source_date)
            except ValueError:
                errors.append(f"{company.ticker} evidence has invalid source_date: {item.source_date}")
        if company.decision.is_buy_or_add and not company.decision.action_allowed:
            errors.append(f"{company.ticker} has buy/add state without action_allowed")
    return errors


if __name__ == "__main__":
    validation_errors = validate_demo_universe()
    if validation_errors:
        print("Demo universe validation failed:")
        for error in validation_errors:
            print(f"- {error}")
        raise SystemExit(1)

    init_db()
    duckdb_status = init_duckdb()
    print(f"SQLite ready: {db_path()}")
    print(f"DuckDB status: {duckdb_status}")
    print(f"Demo universe loaded in code: {len(DEMO_UNIVERSE)} tickers")
