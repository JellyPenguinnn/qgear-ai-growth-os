# Data Sources

v0.2 keeps mock/demo mode as the default and adds provider metadata foundations. Live provider integrations are intentionally modular and optional.

## Core Free Providers

- SEC EDGAR APIs for filings and XBRL company facts.
- FRED API for macro data.
- EIA API for electricity and energy data.

## Current v0.2 Provider Foundation

- Provider responses include `payload` plus `metadata`.
- Metadata includes provider name, status, source URL/name, retrieved timestamp, cache status, source/as-of dates when available, cache key, error, and demo/live mode.
- SEC provider supports company facts, submissions, and filing metadata behind custom User-Agent, cache, retry/backoff, and a request-rate cap of 10 requests/second or less.
- Price and benchmark provider interfaces use deterministic mock snapshots in demo mode.
- `/providers/status`, `/providers/filings/{cik}`, `/providers/company-facts/{cik}`, `/providers/prices`, and `/providers/benchmarks` expose provider state without requiring API keys.
- FRED and EIA remain safe metadata placeholders until live clients are implemented.

## Optional Providers

- Alpha Vantage
- Financial Modeling Prep
- Finnhub
- Nasdaq Data Link

## Experimental Fallback

`yfinance` may be added later only as an experimental fallback, not a mission-critical source.

## SEC Access Rules

The SEC provider requires:

- custom User-Agent configured by env,
- max 10 requests/second,
- local response cache,
- retry with backoff,
- no endpoint hammering.

Keys belong in `.env`; never hardcode API keys.

Provider source notes:

- `docs/research/sec-edgar-provider.md`
- `docs/research/fred-api-provider.md`
- `docs/research/eia-api-provider.md`
