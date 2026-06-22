# Local Development

## Setup

```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -e packages/qgear-core -e packages/qgear-ingest -e packages/qgear-ai -e apps/api
python3 scripts/seed_local_data.py
```

```bash
cd apps/web
npm install
```

## Run

```bash
./scripts/dev_api.sh
```

```bash
./scripts/dev_web.sh
```

Web runs at `http://localhost:3000`. API runs at `http://127.0.0.1:8000`.

## Test

```bash
python3 scripts/run_tests.py
python3 -m compileall packages apps/api scripts tests
python3 scripts/seed_local_data.py
```

The test runner uses Python `unittest` and does not require pytest. Seed validation verifies the demo universe and local SQLite setup; DuckDB is optional and may report unavailable if the dependency is not installed in the active Python environment.

## API Smoke

```bash
./scripts/dev_api.sh
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/universe
curl http://127.0.0.1:8000/portfolio
curl http://127.0.0.1:8000/earnings
curl http://127.0.0.1:8000/reports/weekly
curl http://127.0.0.1:8000/providers/status
curl http://127.0.0.1:8000/providers/benchmarks
```

## Frontend Verification

```bash
cd apps/web
npm run lint
npm run typecheck
npm run build
npm audit --omit=dev
```

Use `npm ci` when `package-lock.json` is present and dependencies do not need to be changed.

Keep `NEXT_PUBLIC_API_URL` pointed at `http://127.0.0.1:8000` unless you intentionally accept sending local research, journal, and portfolio data to another API host.
