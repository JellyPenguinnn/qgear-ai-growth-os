Title: FRED Series Observations API Provider Note
Author/organisation: Federal Reserve Bank of St. Louis
URL or citation: https://fred.stlouisfed.org/docs/api/fred/series_observations.html
Date accessed: 2026-06-22

Summary:
The FRED `fred/series/observations` endpoint returns observations or data values for an economic data series. The documented JSON response includes observation dates and values, and requests use `series_id`, `api_key`, and `file_type=json`.

How it affects Q-GEAR:
FRED can support macro context, interest-rate backdrop, liquidity indicators, and benchmark humility notes. Macro data should inform risk context only; it must not override thesis, earnings, valuation, evidence freshness, or portfolio risk gates.

Implementation consequence:
The FRED provider should remain optional behind `FRED_API_KEY`, return provider metadata when the key is missing, and preserve observation dates/source timestamps when implemented.

Limitations:
FRED is a macro data source, not company-specific evidence. v0.2 keeps FRED as a metadata-safe placeholder and does not require live FRED access for tests.
