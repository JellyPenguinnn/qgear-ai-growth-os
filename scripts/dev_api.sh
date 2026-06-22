#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="${PYTHONPATH:-}:packages/qgear-core/src:packages/qgear-ingest/src:packages/qgear-ai/src:apps/api"
python3 scripts/seed_local_data.py
uvicorn app.main:app --app-dir apps/api --reload --host 127.0.0.1 --port 8000
