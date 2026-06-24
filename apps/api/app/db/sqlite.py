from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.core.config import settings


def _connect() -> sqlite3.Connection:
    settings.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(settings.sqlite_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with _connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS app_settings (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                payload TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS theses (
                ticker TEXT PRIMARY KEY,
                statement TEXT NOT NULL,
                must_go_right TEXT NOT NULL,
                breaks_if TEXT NOT NULL,
                key_metrics TEXT NOT NULL,
                next_review_date TEXT NOT NULL,
                status TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS portfolio_positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                shares REAL NOT NULL,
                average_cost REAL NOT NULL,
                current_price REAL NOT NULL,
                status TEXT NOT NULL,
                thesis_status TEXT NOT NULL,
                next_review_date TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_date TEXT NOT NULL,
                ticker TEXT NOT NULL,
                action TEXT NOT NULL,
                price REAL NOT NULL,
                position_size_pct REAL NOT NULL,
                score REAL NOT NULL,
                evidence TEXT NOT NULL,
                thesis TEXT NOT NULL,
                invalidation_rule TEXT NOT NULL,
                expected_irr_pct REAL NOT NULL,
                future_review_date TEXT NOT NULL,
                later_outcome TEXT NOT NULL,
                decision_outcome TEXT NOT NULL DEFAULT '',
                mistake_category TEXT NOT NULL DEFAULT '',
                evidence_quality TEXT NOT NULL DEFAULT 'MEDIUM',
                followed_system INTEGER NOT NULL DEFAULT 1,
                later_review TEXT NOT NULL DEFAULT '',
                process_score REAL NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS evidence_objects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                claim TEXT NOT NULL,
                evidence TEXT NOT NULL,
                source TEXT NOT NULL,
                source_date TEXT NOT NULL,
                confidence TEXT NOT NULL,
                disproves_if TEXT NOT NULL,
                source_type TEXT NOT NULL DEFAULT 'MANUAL',
                verification_status TEXT NOT NULL DEFAULT 'USER_VERIFIED',
                source_url TEXT,
                retrieved_at TEXT,
                provider TEXT,
                accession_number TEXT,
                filing_date TEXT,
                period_end_date TEXT,
                related_type TEXT NOT NULL,
                related_id INTEGER,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS earnings_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                fiscal_period TEXT NOT NULL,
                report_date TEXT NOT NULL,
                revenue_surprise_pct REAL,
                eps_surprise_pct REAL,
                guidance_raised INTEGER NOT NULL,
                guidance_cut INTEGER NOT NULL,
                guidance_cut_structural INTEGER NOT NULL,
                revenue_growth_accelerated INTEGER NOT NULL,
                ai_evidence_improved INTEGER NOT NULL,
                segment_growth_improved INTEGER NOT NULL,
                margin_expanded INTEGER NOT NULL,
                margin_deteriorated INTEGER NOT NULL,
                fcf_improved INTEGER NOT NULL,
                fcf_deteriorated INTEGER NOT NULL,
                management_tone TEXT NOT NULL,
                thesis_status_change TEXT NOT NULL,
                score_change REAL NOT NULL,
                action_change TEXT NOT NULL,
                evidence_ids TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        _ensure_columns(
            connection,
            "journal_entries",
            {
                "decision_outcome": "TEXT NOT NULL DEFAULT ''",
                "mistake_category": "TEXT NOT NULL DEFAULT ''",
                "evidence_quality": "TEXT NOT NULL DEFAULT 'MEDIUM'",
                "followed_system": "INTEGER NOT NULL DEFAULT 1",
                "later_review": "TEXT NOT NULL DEFAULT ''",
                "process_score": "REAL NOT NULL DEFAULT 0",
            },
        )
        _ensure_columns(
            connection,
            "evidence_objects",
            {
                "source_type": "TEXT NOT NULL DEFAULT 'MANUAL'",
                "verification_status": "TEXT NOT NULL DEFAULT 'USER_VERIFIED'",
                "source_url": "TEXT",
                "retrieved_at": "TEXT",
                "provider": "TEXT",
                "accession_number": "TEXT",
                "filing_date": "TEXT",
                "period_end_date": "TEXT",
            },
        )


def _ensure_columns(connection: sqlite3.Connection, table: str, columns: dict[str, str]) -> None:
    existing = {row["name"] for row in connection.execute(f"PRAGMA table_info({table})").fetchall()}
    for name, definition in columns.items():
        if name not in existing:
            connection.execute(f"ALTER TABLE {table} ADD COLUMN {name} {definition}")


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def get_settings() -> dict[str, Any] | None:
    init_db()
    with _connect() as connection:
        row = connection.execute("SELECT payload FROM app_settings WHERE id = 1").fetchone()
    return json.loads(row["payload"]) if row else None


def save_settings(payload: dict[str, Any]) -> dict[str, Any]:
    init_db()
    timestamp = now_iso()
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO app_settings (id, payload, updated_at)
            VALUES (1, ?, ?)
            ON CONFLICT(id) DO UPDATE SET payload = excluded.payload, updated_at = excluded.updated_at
            """,
            (json.dumps(payload), timestamp),
        )
    return payload


def approve_thesis(
    ticker: str,
    statement: str,
    must_go_right: str,
    breaks_if: str,
    key_metrics: Iterable[str],
    next_review_date: str,
) -> dict[str, Any]:
    init_db()
    payload = {
        "ticker": ticker.upper(),
        "statement": statement,
        "must_go_right": must_go_right,
        "breaks_if": breaks_if,
        "key_metrics": list(key_metrics),
        "next_review_date": next_review_date,
        "status": "APPROVED",
        "updated_at": now_iso(),
    }
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO theses (ticker, statement, must_go_right, breaks_if, key_metrics, next_review_date, status, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(ticker) DO UPDATE SET
                statement = excluded.statement,
                must_go_right = excluded.must_go_right,
                breaks_if = excluded.breaks_if,
                key_metrics = excluded.key_metrics,
                next_review_date = excluded.next_review_date,
                status = excluded.status,
                updated_at = excluded.updated_at
            """,
            (
                payload["ticker"],
                statement,
                must_go_right,
                breaks_if,
                json.dumps(payload["key_metrics"]),
                next_review_date,
                "APPROVED",
                payload["updated_at"],
            ),
        )
    return payload


def get_thesis(ticker: str) -> dict[str, Any] | None:
    init_db()
    with _connect() as connection:
        row = connection.execute("SELECT * FROM theses WHERE ticker = ?", (ticker.upper(),)).fetchone()
    if not row:
        return None
    payload = dict(row)
    payload["key_metrics"] = json.loads(payload["key_metrics"])
    return payload


def list_positions() -> list[dict[str, Any]]:
    init_db()
    with _connect() as connection:
        rows = connection.execute("SELECT * FROM portfolio_positions ORDER BY ticker").fetchall()
    positions: list[dict[str, Any]] = []
    total_value = sum(row["shares"] * row["current_price"] for row in rows)
    for row in rows:
        market_value = row["shares"] * row["current_price"]
        positions.append(
            {
                **dict(row),
                "market_value": round(market_value, 2),
                "unrealized_pl": round((row["current_price"] - row["average_cost"]) * row["shares"], 2),
                "position_weight_pct": round((market_value / total_value * 100) if total_value else 0, 2),
            }
        )
    return positions


def add_position(payload: dict[str, Any]) -> dict[str, Any]:
    init_db()
    timestamp = now_iso()
    with _connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO portfolio_positions
              (ticker, shares, average_cost, current_price, status, thesis_status, next_review_date, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["ticker"].upper(),
                payload["shares"],
                payload["average_cost"],
                payload["current_price"],
                payload.get("status", "HOLD"),
                payload.get("thesis_status", "DRAFT"),
                payload.get("next_review_date", ""),
                timestamp,
                timestamp,
            ),
        )
        payload = {**payload, "id": cursor.lastrowid, "created_at": timestamp, "updated_at": timestamp}
    return payload


def list_journal_entries() -> list[dict[str, Any]]:
    init_db()
    with _connect() as connection:
        rows = connection.execute("SELECT * FROM journal_entries ORDER BY entry_date DESC, id DESC").fetchall()
    entries = []
    for row in rows:
        payload = dict(row)
        payload["followed_system"] = bool(payload.get("followed_system", 1))
        entries.append(payload)
    return entries


def add_journal_entry(payload: dict[str, Any]) -> dict[str, Any]:
    init_db()
    timestamp = now_iso()
    with _connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO journal_entries
              (entry_date, ticker, action, price, position_size_pct, score, evidence, thesis,
               invalidation_rule, expected_irr_pct, future_review_date, later_outcome,
               decision_outcome, mistake_category, evidence_quality, followed_system, later_review,
               process_score, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["entry_date"],
                payload["ticker"].upper(),
                payload["action"],
                payload["price"],
                payload["position_size_pct"],
                payload["score"],
                payload["evidence"],
                payload["thesis"],
                payload["invalidation_rule"],
                payload["expected_irr_pct"],
                payload["future_review_date"],
                payload.get("later_outcome", ""),
                payload.get("decision_outcome", ""),
                payload.get("mistake_category", ""),
                payload.get("evidence_quality", "MEDIUM"),
                1 if payload.get("followed_system", True) else 0,
                payload.get("later_review", ""),
                payload.get("process_score", 0),
                timestamp,
            ),
        )
    return {**payload, "id": cursor.lastrowid, "created_at": timestamp}


def add_evidence_object(ticker: str, payload: dict[str, Any], *, related_type: str = "manual", related_id: int | None = None) -> dict[str, Any]:
    init_db()
    timestamp = now_iso()
    row = {
        "ticker": ticker.upper(),
        "claim": payload["claim"],
        "evidence": payload["evidence"],
        "source": payload["source"],
        "source_date": payload["source_date"],
        "confidence": payload["confidence"],
        "disproves_if": payload["disproves_if"],
        "source_type": payload.get("source_type", "MANUAL"),
        "verification_status": payload.get("verification_status", "USER_VERIFIED"),
        "source_url": payload.get("source_url"),
        "retrieved_at": payload.get("retrieved_at"),
        "provider": payload.get("provider"),
        "accession_number": payload.get("accession_number"),
        "filing_date": payload.get("filing_date"),
        "period_end_date": payload.get("period_end_date"),
        "related_type": related_type,
        "related_id": related_id,
        "created_at": timestamp,
    }
    with _connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO evidence_objects
              (ticker, claim, evidence, source, source_date, confidence, disproves_if,
               source_type, verification_status, source_url, retrieved_at, provider, accession_number,
               filing_date, period_end_date, related_type, related_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["ticker"],
                row["claim"],
                row["evidence"],
                row["source"],
                row["source_date"],
                row["confidence"],
                row["disproves_if"],
                row["source_type"],
                row["verification_status"],
                row["source_url"],
                row["retrieved_at"],
                row["provider"],
                row["accession_number"],
                row["filing_date"],
                row["period_end_date"],
                row["related_type"],
                row["related_id"],
                row["created_at"],
            ),
        )
    return {**row, "id": cursor.lastrowid}


def list_evidence_objects(ticker: str | None = None) -> list[dict[str, Any]]:
    init_db()
    with _connect() as connection:
        if ticker:
            rows = connection.execute(
                "SELECT * FROM evidence_objects WHERE ticker = ? ORDER BY source_date DESC, id DESC",
                (ticker.upper(),),
            ).fetchall()
        else:
            rows = connection.execute("SELECT * FROM evidence_objects ORDER BY source_date DESC, id DESC").fetchall()
    return [dict(row) for row in rows]


def add_earnings_review(payload: dict[str, Any], *, thesis_status_change: str, evidence_ids: Iterable[int]) -> dict[str, Any]:
    init_db()
    timestamp = now_iso()
    bool_fields = (
        "guidance_raised",
        "guidance_cut",
        "guidance_cut_structural",
        "revenue_growth_accelerated",
        "ai_evidence_improved",
        "segment_growth_improved",
        "margin_expanded",
        "margin_deteriorated",
        "fcf_improved",
        "fcf_deteriorated",
    )
    row = {
        **payload,
        "ticker": payload["ticker"].upper(),
        "thesis_status_change": thesis_status_change,
        "evidence_ids": list(evidence_ids),
        "created_at": timestamp,
    }
    with _connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO earnings_reviews
              (ticker, fiscal_period, report_date, revenue_surprise_pct, eps_surprise_pct,
               guidance_raised, guidance_cut, guidance_cut_structural, revenue_growth_accelerated,
               ai_evidence_improved, segment_growth_improved, margin_expanded, margin_deteriorated,
               fcf_improved, fcf_deteriorated, management_tone, thesis_status_change,
               score_change, action_change, evidence_ids, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["ticker"],
                row["fiscal_period"],
                row["report_date"],
                row.get("revenue_surprise_pct"),
                row.get("eps_surprise_pct"),
                *(1 if row.get(field) else 0 for field in bool_fields),
                row["management_tone"],
                row["thesis_status_change"],
                row["score_change"],
                row["action_change"],
                json.dumps(row["evidence_ids"]),
                row["created_at"],
            ),
        )
    return {**row, "id": cursor.lastrowid}


def list_earnings_reviews(ticker: str | None = None) -> list[dict[str, Any]]:
    init_db()
    with _connect() as connection:
        if ticker:
            rows = connection.execute(
                "SELECT * FROM earnings_reviews WHERE ticker = ? ORDER BY report_date DESC, id DESC",
                (ticker.upper(),),
            ).fetchall()
        else:
            rows = connection.execute("SELECT * FROM earnings_reviews ORDER BY report_date DESC, id DESC").fetchall()
    reviews: list[dict[str, Any]] = []
    bool_fields = {
        "guidance_raised",
        "guidance_cut",
        "guidance_cut_structural",
        "revenue_growth_accelerated",
        "ai_evidence_improved",
        "segment_growth_improved",
        "margin_expanded",
        "margin_deteriorated",
        "fcf_improved",
        "fcf_deteriorated",
    }
    for row in rows:
        payload = dict(row)
        for field in bool_fields:
            payload[field] = bool(payload[field])
        payload["evidence_ids"] = json.loads(payload["evidence_ids"])
        reviews.append(payload)
    return reviews


def db_path() -> Path:
    return settings.sqlite_path
