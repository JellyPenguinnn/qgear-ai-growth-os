from __future__ import annotations

from app.core.config import settings


def init_duckdb() -> dict[str, str]:
    settings.duckdb_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import duckdb
    except ImportError:
        return {
            "status": "unavailable",
            "reason": "duckdb is not installed; install API dependencies to enable analytics tables.",
        }

    with duckdb.connect(str(settings.duckdb_path)) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS scoring_snapshots (
                snapshot_date DATE,
                ticker VARCHAR,
                score DOUBLE,
                decision_state VARCHAR,
                ai_layer VARCHAR
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS benchmark_snapshots (
                snapshot_date DATE,
                benchmark VARCHAR,
                close DOUBLE,
                total_return_index DOUBLE
            )
            """
        )
    return {"status": "ready"}
