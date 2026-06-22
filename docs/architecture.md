# Architecture

The repository is a local-first monorepo.

```text
apps/
  api/        FastAPI backend, SQLite state, DuckDB analytics setup
  web/        Next.js dashboard
packages/
  qgear-core/ Pure scoring, risk, and decision policy
  qgear-ingest/ Provider interfaces and respectful ingestion utilities
  qgear-ai/   Evidence schema and prompt helpers
data/
  demo/       Demo universe metadata
  sqlite/     Local app DB
  duckdb/     Local analytics DB
  cache/      Provider cache
docs/
prompts/
scripts/
tests/
```

Domain rules live in `packages/qgear-core`. The API adapts those rules into routes and local persistence. The frontend consumes the API and includes fallback demo data so the UI can render before the backend is started.

No trading execution layer exists.
