# Q-GEAR AI Growth OS

[![CI](https://github.com/JellyPenguinnn/qgear-ai-growth-os/actions/workflows/ci.yml/badge.svg)](https://github.com/JellyPenguinnn/qgear-ai-growth-os/actions/workflows/ci.yml)

Q-GEAR AI Growth OS is a local, personal-use US equity research operating system for AI-era growth stocks. Q-GEAR means Quality, Growth, Earnings Acceleration, AI Infrastructure Relevance, and Risk Control.

The app is not an advisory product, not an auto-trader, and not a day-trading system. It is a local research, scoring, portfolio, and decision-journal tool.

> This tool is for personal research and educational use only. It does not provide licensed financial advice, tax advice, or legal advice. Final investment decisions are made by the user.

## What The Local Demo Includes

- Pure Python scoring, hard-gate decision policy, drawdown modes, and position sizing logic.
- FastAPI backend with demo universe, stock detail, settings, thesis approval, portfolio, journal, earnings lab, provider metadata, valuation, alerts, and report routes.
- SQLite app-state schema for settings, approved theses, manual positions, journal entries, structured evidence, and earnings reviews.
- Optional DuckDB analytics tables for scoring and benchmark snapshots.
- Next.js frontend with Today, Research Pipeline, Evidence Workbench, AI universe screener, stock detail, thesis form, portfolio tracker, journal, earnings lab, reports, and settings.
- Mock/demo seed universe for NVDA, AMD, AVGO, MRVL, TSM, ASML, AMAT, LRCX, KLAC, MU, SNDK, WDC, STX, ANET, CSCO, CIEN, MSFT, GOOGL, AMZN, META, ORCL, VRT, ETN, PWR, CEG, NRG, EQIX, DLR, PLTR, NOW, CRWD, DDOG, SNOW, and MDB.
- Provider foundation for SEC metadata, mock prices, benchmark snapshots, FRED/EIA placeholders, source provenance, and demo/live routing.
- Earnings/evidence engine, editable valuation underwriting workbench, probability-weighted IRR, portfolio/journal intelligence, fixture no-lookahead backtest skeleton, local alerts, and review-cycle reports.
- Optional AI provider foundation with disabled-by-default mode, draft-only AI routes, schema validation, explicit external-provider acknowledgement, and no automatic decision mutation.
- Tests for anti-buy-the-dip gates, thesis requirements, earnings weakening, weighted valuation hurdle, concentration cap, hard drawdown mode, portfolio/journal intelligence, provider metadata, AI draft safety, alerts, report routes, and no-lookahead validation.

## Local Setup

From the repo root:

```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -e packages/qgear-core -e packages/qgear-ingest -e packages/qgear-ai -e apps/api
python3 scripts/seed_local_data.py
```

Install frontend dependencies:

```bash
cd apps/web
npm install
```

## Run Locally

API:

```bash
source .venv/bin/activate
./scripts/dev_api.sh
```

Web:

```bash
./scripts/dev_web.sh
```

Open `http://localhost:3000`. The web app uses `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000` by default and falls back to frontend demo data if the API is not running.

## Tests

The core tests use Python `unittest`, so they can run without pytest:

```bash
python3 scripts/run_tests.py
python3 -m compileall packages apps/api scripts tests
python3 scripts/seed_local_data.py
```

If you install pytest, the same tests can also be collected by pytest with `PYTHONPATH=packages/qgear-core/src pytest`.

API smoke checks:

```bash
./scripts/dev_api.sh
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/today
curl http://127.0.0.1:8000/pipeline
curl http://127.0.0.1:8000/ai/status
curl http://127.0.0.1:8000/universe
curl http://127.0.0.1:8000/portfolio
curl http://127.0.0.1:8000/earnings
curl http://127.0.0.1:8000/reports/weekly
curl http://127.0.0.1:8000/providers/status
curl http://127.0.0.1:8000/alerts
curl http://127.0.0.1:8000/journal/analytics
curl http://127.0.0.1:8000/valuation/NVDA
curl -X POST http://127.0.0.1:8000/valuation/NVDA/calculate -H "Content-Type: application/json" -d '{...}'
```

Frontend checks after `npm install` or `npm ci`:

```bash
cd apps/web
npm run lint
npm run typecheck
npm run build
npm audit --omit=dev
```

## CI

GitHub Actions is configured in `.github/workflows/ci.yml`. It runs the Python/API checks, seed validation, frontend lint/typecheck/build, and production dependency audit. See `docs/ci.md` for the command matrix and current limitations.

If `npm install` fails because of registry/network errors, do not treat the frontend as verified. Record the command and error in `docs/iteration_log.md`.

## Decision Brain

The final action is based on:

```text
Action = Score + Hard Gates + Risk Budget + Evidence Freshness
```

The 100-point score uses:

- AI infrastructure relevance: 12
- Business quality: 18
- Revenue and earnings acceleration: 18
- Earnings report / guidance / revisions: 17
- Valuation and expected IRR: 15
- Technical trend / relative strength: 10
- Portfolio fit / risk control: 10

Score alone never creates a buy/add action. A lower price only improves valuation; it does not improve business quality, earnings quality, AI relevance, management execution, or balance-sheet strength.

The current scoring weights and cutoffs are deterministic MVP heuristics. The research base supports the broad pillars, but not the exact point values as proven alpha weights.

## Non-Negotiables

- No auto-trading.
- No margin.
- No options in the MVP.
- No buy/add without an approved thesis and invalidation rule.
- No averaging down without fresh positive fundamental evidence.
- Price movement alone is never evidence.
- Technical analysis is timing/risk confirmation only.

## Data Sources

The current local/demo system keeps mock/demo mode as the default and exposes provider metadata foundations:

- SEC EDGAR company facts, submissions, and filing metadata with custom User-Agent, caching, backoff, and <=10 requests/second.
- Mock daily price snapshots and benchmark snapshots for SPY, QQQ, XLK, and SMH.
- Provider response metadata including source URL, source/as-of dates when available, retrieved timestamp, cache status, provider status, and errors.
- Safe FRED and EIA placeholders that do not require API keys in demo mode.
- Optional AI draft provider mode. Default is `QGEAR_AI_PROVIDER=none`; set `QGEAR_AI_PROVIDER=openai`, `QGEAR_AI_MODEL`, and `OPENAI_API_KEY` only when you intentionally want explicit draft AI assistance.
- Optional Alpha Vantage, Financial Modeling Prep, Finnhub, Nasdaq Data Link, and experimental yfinance fallback later.

API keys belong in `.env`; no keys are hardcoded.
Keep `NEXT_PUBLIC_API_URL` pointed at localhost unless you intentionally accept sending local research, journal, and portfolio data to another API host.
AI routes are draft-only and require explicit user-submitted text. In OpenAI mode, each POST must acknowledge external AI use before any supplied text is sent.

## Known Limitations

- Demo data is realistic but mocked and should not be treated as live market data.
- Benchmark comparison uses demo snapshots until real market data ingestion is configured.
- Backtesting is a fixture/no-lookahead skeleton, not a validated historical performance study.
- Frontend dependencies require `npm install` or `npm ci`.
- API dependencies require local Python environment setup.
- Live SEC/FRED/EIA/price providers are optional; demo mode does not require API keys.
- Research notes are being migrated into `docs/research/` with the required source template; unverified source work remains clearly marked.
- Browser visual smoke may be unavailable if the in-app browser runtime fails to initialize; production route smoke was verified with the built Next server.
- No brokerage integration exists by design.
