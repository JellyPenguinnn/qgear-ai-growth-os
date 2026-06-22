# API Examples

API defaults to `http://127.0.0.1:8000`.

## Health

```bash
curl http://127.0.0.1:8000/health
```

Expected shape:

```json
{
  "status": "ok",
  "mode": "demo",
  "sqlite": "ready",
  "duckdb": "ready | unavailable",
  "providers": {
    "mode": "demo",
    "live_data_required": false
  },
  "auto_trading": "disabled",
  "margin": "disabled",
  "options": "disabled_in_mvp",
  "disclaimer": "..."
}
```

Health output must not expose local filesystem paths.

## Universe

```bash
curl "http://127.0.0.1:8000/universe?min_score=75"
curl http://127.0.0.1:8000/universe/NVDA
```

The response is demo research data and not a recommendation.

## Provider Status And Metadata

```bash
curl http://127.0.0.1:8000/providers/status
curl http://127.0.0.1:8000/providers/filings/1045810?limit=5
curl http://127.0.0.1:8000/providers/company-facts/1045810
curl "http://127.0.0.1:8000/providers/prices?tickers=NVDA,MU,SPY"
curl http://127.0.0.1:8000/providers/benchmarks
```

Provider responses use a stable envelope:

```json
{
  "payload": {
    "filings": [
      {
        "accession_number": "0001045810-26-000001",
        "form": "10-Q",
        "filing_date": "2026-05-22",
        "report_date": "2026-04-30",
        "primary_document": "nvda-20260430.htm",
        "source_url": "local://demo/sec/submissions/0001045810"
      }
    ]
  },
  "metadata": {
    "provider": "mock",
    "status": "ok",
    "source_url": "local://demo/sec/filings",
    "source_name": "Q-GEAR demo filing metadata",
    "retrieved_at": "2026-06-22T00:00:00+00:00",
    "cached": true,
    "source_date": "2026-06-22",
    "as_of_date": "2026-06-22",
    "cache_written_at": null,
    "cache_key": "mock_filing_metadata_0001045810_5",
    "error": null,
    "mode": "demo"
  }
}
```

In demo mode these endpoints use local/mock data and require no API keys. In live mode, SEC responses remain behind cache/backoff/User-Agent controls and provider errors return metadata instead of crashing the app.

## Settings

```bash
curl -X POST http://127.0.0.1:8000/settings \
  -H "Content-Type: application/json" \
  -d '{
    "starting_capital": 10000,
    "base_currency": "USD",
    "country": "Singapore",
    "risk_style": "BALANCED",
    "target_cagr_low_pct": 18,
    "target_cagr_high_pct": 22,
    "hard_drawdown_limit_pct": 35,
    "cash_buffer_pct": 15,
    "max_single_stock_pct": 15,
    "benchmarks": ["SPY", "QQQ", "XLK", "SMH"],
    "broker_mode": "manual",
    "margin_enabled": false,
    "options_enabled": false,
    "auto_trading_enabled": false
  }'
```

The API forces margin, options, and auto-trading disabled.

## Thesis Approval

```bash
curl -X POST http://127.0.0.1:8000/theses/NVDA/approve \
  -H "Content-Type: application/json" \
  -d '{
    "statement": "Data-center accelerator demand remains measurable in revenue and margin evidence.",
    "must_go_right": "Revenue growth, margin quality, and AI demand evidence stay strong.",
    "breaks_if": "Guidance is structurally cut, margins deteriorate, or AI demand evidence weakens.",
    "key_metrics": ["data center revenue", "gross margin", "free cash flow"],
    "next_review_date": "2026-09-30"
  }'
```

## Portfolio

```bash
curl http://127.0.0.1:8000/portfolio
curl -X POST http://127.0.0.1:8000/portfolio/positions \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "NVDA",
    "shares": 1,
    "average_cost": 100,
    "current_price": 110,
    "status": "HOLD",
    "thesis_status": "APPROVED",
    "next_review_date": "2026-09-30"
  }'
```

Manual position recording is not trade execution.

## Journal

```bash
curl http://127.0.0.1:8000/journal/analytics
curl -X POST http://127.0.0.1:8000/journal \
  -H "Content-Type: application/json" \
  -d '{
    "entry_date": "2026-06-22",
    "ticker": "NVDA",
    "action": "NO_ACTION",
    "price": 110,
    "position_size_pct": 0,
    "score": 90,
    "evidence": "No new action-changing evidence today.",
    "thesis": "Approved thesis remains under review.",
    "invalidation_rule": "Guidance cut or margin deterioration would weaken thesis.",
    "expected_irr_pct": 16,
    "future_review_date": "2026-09-30",
    "later_outcome": ""
  }'
```

Journal entries should record evidence and invalidation logic even when the action is `NO_ACTION`.

`/journal/analytics` summarizes local process discipline: action mix, evidence-backed entries, and unresolved outcomes. It is not a performance claim or trade signal.

## Alerts

```bash
curl http://127.0.0.1:8000/alerts
```

Alerts are review prompts only. They include filing review, earnings thesis risk, stale evidence, technical break, concentration, drawdown, and thesis review date rules. Every alert has source metadata, confidence, and disproof criteria, and `trade_instruction` must remain `false`.

## Reports

```bash
curl http://127.0.0.1:8000/earnings
curl http://127.0.0.1:8000/earnings/NVDA
curl http://127.0.0.1:8000/earnings/NVDA/evidence
curl http://127.0.0.1:8000/earnings/NVDA/reviews
curl http://127.0.0.1:8000/reports/daily
curl http://127.0.0.1:8000/reports/weekly
curl http://127.0.0.1:8000/reports/monthly
curl http://127.0.0.1:8000/reports/quarterly
curl http://127.0.0.1:8000/reports/annual
```

Daily, monthly, quarterly, and annual reports include local review prompts, alert summaries, and journal analytics where applicable. Reports preserve the default stance that no action is justified unless fresh evidence changes the thesis and all gates clear.

## Earnings Evidence

```bash
curl -X POST http://127.0.0.1:8000/earnings/NVDA/evidence \
  -H "Content-Type: application/json" \
  -d '{
    "claim": "AI demand became more measurable after earnings.",
    "evidence": "Revenue growth accelerated, guidance was raised, and margins expanded.",
    "source": "Manual earnings review",
    "source_date": "2026-06-22",
    "confidence": "HIGH",
    "disproves_if": "Guidance is cut, AI demand slows, or margins deteriorate."
  }'
```

```bash
curl -X POST http://127.0.0.1:8000/earnings/NVDA/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "fiscal_period": "2026Q1",
    "report_date": "2026-06-22",
    "revenue_surprise_pct": 8,
    "eps_surprise_pct": 6,
    "guidance_raised": true,
    "revenue_growth_accelerated": true,
    "ai_evidence_improved": true,
    "margin_expanded": true,
    "fcf_improved": true,
    "management_tone": "constructive but evidence-gated",
    "score_change": 4,
    "action_change": "NO_ACTION",
    "evidence": [
      {
        "claim": "AI demand became more measurable after earnings.",
        "evidence": "Revenue growth accelerated, guidance was raised, and margins expanded.",
        "source": "Manual earnings review",
        "source_date": "2026-06-22",
        "confidence": "HIGH",
        "disproves_if": "Guidance is cut, AI demand slows, or margins deteriorate."
      }
    ]
  }'
```

The earnings review classifies thesis impact as `STRENGTHENED`, `UNCHANGED`, `WEAKENED`, or `BROKEN`. That classification is evidence input only; it does not create a buy/add action without thesis, invalidation, valuation, technical, freshness, and risk gates.

## Valuation And Backtest Fixtures

```bash
curl http://127.0.0.1:8000/valuation/NVDA
curl http://127.0.0.1:8000/valuation/PLTR
curl http://127.0.0.1:8000/valuation/backtest/demo
```

Valuation responses include bear/base/bull cases, 3-year and 5-year probability-weighted IRR, and the hurdle result. Backtest responses are fixture-only and include no-lookahead validation status. They are research checks, not performance promises or trade instructions.
