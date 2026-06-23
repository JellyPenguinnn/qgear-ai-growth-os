from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - dependency exists in normal API installs
    load_dotenv = None

if load_dotenv:
    load_dotenv(ROOT / ".env")


@dataclass(frozen=True)
class ApiSettings:
    app_name: str = "Q-GEAR AI Growth OS"
    environment: str = os.getenv("QGEAR_ENV", "demo")
    sqlite_path: Path = Path(os.getenv("QGEAR_SQLITE_PATH", ROOT / "data" / "sqlite" / "qgear.db"))
    duckdb_path: Path = Path(os.getenv("QGEAR_DUCKDB_PATH", ROOT / "data" / "duckdb" / "qgear.duckdb"))
    cache_dir: Path = Path(os.getenv("QGEAR_CACHE_DIR", ROOT / "data" / "cache"))
    sec_user_agent: str = os.getenv(
        "SEC_USER_AGENT",
        "qgear-ai-growth-os personal research app contact@example.com",
    )
    sec_max_requests_per_second: int = int(os.getenv("SEC_MAX_REQUESTS_PER_SECOND", "10"))
    ai_provider: str = os.getenv("QGEAR_AI_PROVIDER", "none")
    ai_model: str | None = os.getenv("QGEAR_AI_MODEL")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    alpha_vantage_api_key: str | None = os.getenv("ALPHA_VANTAGE_API_KEY")
    fmp_api_key: str | None = os.getenv("FMP_API_KEY")
    finnhub_api_key: str | None = os.getenv("FINNHUB_API_KEY")
    fred_api_key: str | None = os.getenv("FRED_API_KEY")
    eia_api_key: str | None = os.getenv("EIA_API_KEY")


settings = ApiSettings()
