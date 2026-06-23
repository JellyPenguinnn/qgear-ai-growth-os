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

## Today And Pipeline

```bash
curl http://127.0.0.1:8000/today
curl http://127.0.0.1:8000/pipeline
```

`/today` is the daily review command center. It returns the default no-action stance, portfolio/risk metrics, priority review queue, pipeline snapshot, alerts, provider status, and top research-priority names.

`/pipeline` is the research board grouped by Q-GEAR decision state. Each pipeline item includes:

```json
{
  "ticker": "NVDA",
  "decision_state": "STARTER_ALLOWED",
  "action_allowed": true,
  "trade_instruction": false,
  "primary_reason": "Thesis confirmed, valuation clears hurdle...",
  "primary_blocker": "",
  "review_flags": ["JOURNAL_REVIEW_REQUIRED"],
  "next_task": "Review the journal draft, position size, and evidence provenance before any manual decision.",
  "evidence": {
    "claim": "AI relevance requires measurable business evidence.",
    "evidence": "Demo data for NVDA: ...",
    "source": "Q-GEAR demo seed data",
    "source_date": "2026-06-22",
    "confidence": "HIGH",
    "disproves_if": "Future filings, earnings releases, segment data, or guidance contradict the claim."
  }
}
```

Pipeline states are workflow states, not trade instructions. Even `STARTER_ALLOWED` and `ADD_ALLOWED` require user review, journal discipline, and manual action outside the app.

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

Provider status also includes AI provider status. Default mode is disabled:

```json
{
  "ai": {
    "ai_enabled": false,
    "requires_explicit_request": true,
    "requires_external_ai_acknowledgement": false,
    "draft_only": true,
    "mutates_decision_state": false,
    "provider_metadata": {
      "provider": "noop",
      "mode": "none",
      "status": "disabled"
    }
  }
}
```

## AI Draft Routes

AI is optional and disabled by default. A configured API key alone does not enable AI; set `QGEAR_AI_PROVIDER=openai` intentionally.

```bash
curl http://127.0.0.1:8000/ai/status
```

Draft-only routes:

```bash
curl -X POST http://127.0.0.1:8000/ai/evidence/extract \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "NVDA",
    "source_title": "Manual earnings excerpt",
    "source_type": "earnings release",
    "source_date": "2026-06-22",
    "source_url_or_description": "User-pasted local excerpt",
    "pasted_text": "Revenue growth accelerated and guidance was raised in the supplied excerpt.",
    "external_ai_acknowledged": false
  }'
curl -X POST http://127.0.0.1:8000/ai/earnings/summarize -H "Content-Type: application/json" -d '{...}'
curl -X POST http://127.0.0.1:8000/ai/thesis/update -H "Content-Type: application/json" -d '{...}'
curl -X POST http://127.0.0.1:8000/ai/decision/explain -H "Content-Type: application/json" -d '{...}'
```

In default disabled mode, responses are safe drafts:

```json
{
  "task": "evidence_extraction",
  "draft_status": "disabled",
  "provider_metadata": {
    "provider": "noop",
    "mode": "none",
    "status": "disabled",
    "external_call_performed": false
  },
  "requires_user_verification": true,
  "mutates_decision_state": false
}
```

In `openai` mode, POST routes require `external_ai_acknowledged: true` before any supplied text is sent to the configured provider. AI routes never write theses, evidence, earnings reviews, journal entries, positions, or decision states.

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

Portfolio responses include local review-only analytics:

```json
{
  "manual_only": true,
  "cash_pct": 15.0,
  "ai_layer_concentration": {},
  "expected_irr_distribution": {
    "min_pct": 0,
    "max_pct": 0,
    "weighted_pct": 0,
    "note": "Expected IRR is a research assumption, not a promise."
  },
  "benchmark_comparison": [
    {
      "benchmark": "SPY",
      "status": "pending_local_market_data",
      "total_return_pct": null,
      "relative_return_pct": null
    }
  ],
  "concentration_risks": [],
  "blocked_adds": [],
  "review_calendar": []
}
```

`blocked_adds`, concentration risks, and review dates are review prompts only.

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
    "later_outcome": "",
    "decision_outcome": "PENDING",
    "mistake_category": "NONE",
    "evidence_quality": "HIGH",
    "followed_system": true,
    "later_review": "",
    "process_score": 92
  }'
```

Journal entries should record evidence and invalidation logic even when the action is `NO_ACTION`.

`/journal/analytics` summarizes local process discipline: action mix, evidence-backed entries, evidence quality counts, mistake counts, followed-system rate, average process score, unresolved outcomes, and unresolved later reviews. It is not a performance claim or trade signal.

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
curl -X POST http://127.0.0.1:8000/valuation/NVDA/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "NVDA",
    "hurdle_irr_pct": 15,
    "cases": [
      {
        "name": "bear",
        "probability": 0.25,
        "current_price": 100,
        "target_price_3y": 120,
        "target_price_5y": 140,
        "notes": "Bear case with weaker growth.",
        "assumptions": {
          "revenue_cagr_pct": 10,
          "gross_margin_pct": 55,
          "operating_margin_pct": 25,
          "fcf_margin_pct": 20,
          "terminal_multiple": 18,
          "dilution_buyback_pct": -1,
          "net_cash_debt_per_share": 0
        },
        "evidence_refs": ["verified evidence object or note"]
      },
      {
        "name": "base",
        "probability": 0.50,
        "current_price": 100,
        "target_price_3y": 150,
        "target_price_5y": 210,
        "notes": "Base case with evidence-backed assumptions.",
        "assumptions": {
          "revenue_cagr_pct": 18,
          "gross_margin_pct": 60,
          "operating_margin_pct": 32,
          "fcf_margin_pct": 28,
          "terminal_multiple": 25,
          "dilution_buyback_pct": 0,
          "net_cash_debt_per_share": 0
        },
        "evidence_refs": ["verified evidence object or note"]
      },
      {
        "name": "bull",
        "probability": 0.25,
        "current_price": 100,
        "target_price_3y": 190,
        "target_price_5y": 300,
        "notes": "Bull case with stronger growth and margins.",
        "assumptions": {
          "revenue_cagr_pct": 25,
          "gross_margin_pct": 63,
          "operating_margin_pct": 36,
          "fcf_margin_pct": 32,
          "terminal_multiple": 32,
          "dilution_buyback_pct": 1,
          "net_cash_debt_per_share": 0
        },
        "evidence_refs": ["verified evidence object or note"]
      }
    ]
  }'
curl http://127.0.0.1:8000/valuation/backtest/demo
```

Valuation responses include bear/base/bull cases, underwriting assumptions, case IRRs, 3-year and 5-year probability-weighted IRR, a sensitivity table, evidence references, notes, and the hurdle result. The calculate route is stateless and does not save assumptions or change decision state. Backtest responses are fixture-only and include no-lookahead validation status. They are research checks, not performance promises or trade instructions.
