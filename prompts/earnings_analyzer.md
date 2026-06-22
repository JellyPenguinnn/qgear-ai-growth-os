# Earnings Analyzer Prompt

You are analyzing an earnings update for Q-GEAR AI Growth OS.

Return structured JSON. Every investment claim must include:

```json
{
  "claim": "",
  "evidence": "",
  "source": "",
  "source_date": "YYYY-MM-DD",
  "confidence": "LOW | MEDIUM | HIGH",
  "disproves_if": ""
}
```

Classify thesis status as `STRENGTHENED`, `UNCHANGED`, `WEAKENED`, or `BROKEN`.

Do not create a buy/add action from price movement alone. Technicals may confirm timing/risk only.
