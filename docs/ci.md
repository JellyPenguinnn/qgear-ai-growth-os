# Continuous Integration

Q-GEAR uses GitHub Actions for repository quality checks. The workflow lives at:

```text
.github/workflows/ci.yml
```

## Workflow Jobs

### Python And API

Runs on Ubuntu with Python 3.12:

```bash
python -m pip install --upgrade pip
pip install -e packages/qgear-core -e packages/qgear-ingest -e packages/qgear-ai -e apps/api
python scripts/run_tests.py
python -m compileall packages apps/api scripts tests
python scripts/seed_local_data.py
```

### Frontend

Runs on Ubuntu with Node 20:

```bash
cd apps/web
npm ci
npm run lint
npm run typecheck
npm run build
npm audit --omit=dev
```

## Local Equivalent

From the repository root:

```bash
python3 scripts/run_tests.py
python3 -m compileall packages apps/api scripts tests
python3 scripts/seed_local_data.py
```

Then:

```bash
cd apps/web
npm run lint
npm run typecheck
npm run build
npm audit --omit=dev
```

## Scope And Limits

The CI workflow verifies deterministic demo/local checks. It does not require API keys, live SEC/FRED/EIA access, broker integrations, margin, options, or auto-trading.

Current CI does not yet run full process-level API curl smoke checks, built Next route smoke, browser visual inspection, or live-provider verification. Those remain documented manual checks until a later hardening milestone adds reliable automation.
