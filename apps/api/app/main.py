from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.analytics import init_duckdb
from app.db.sqlite import init_db
from app.routers import ai, alerts, earnings, journal, pipeline, portfolio, providers, reports, settings as settings_router, theses, today, universe, valuation
from qgear_ai.providers import build_ai_provider
from qgear_ai.service import AIResearchService

DISCLAIMER = (
    "This tool is for personal research and educational use only. It does not provide licensed financial "
    "advice, tax advice, or legal advice. Final investment decisions are made by the user."
)


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(settings_router.router)
    app.include_router(ai.router)
    app.include_router(today.router)
    app.include_router(pipeline.router)
    app.include_router(alerts.router)
    app.include_router(universe.router)
    app.include_router(theses.router)
    app.include_router(portfolio.router)
    app.include_router(journal.router)
    app.include_router(earnings.router)
    app.include_router(providers.router)
    app.include_router(reports.router)
    app.include_router(valuation.router)

    @app.on_event("startup")
    def startup() -> None:
        init_db()
        init_duckdb()

    @app.get("/health")
    def health() -> dict:
        duckdb_status = init_duckdb()
        ai_status = AIResearchService(
            build_ai_provider(settings.ai_provider, api_key=settings.openai_api_key, model=settings.ai_model)
        ).status()
        return {
            "status": "ok",
            "mode": settings.environment,
            "sqlite": "ready",
            "duckdb": duckdb_status["status"],
            "providers": {
                "mode": settings.environment,
                "live_data_required": False,
            },
            "ai": ai_status,
            "auto_trading": "disabled",
            "margin": "disabled",
            "options": "disabled_in_mvp",
            "disclaimer": DISCLAIMER,
        }

    return app


app = create_app()
