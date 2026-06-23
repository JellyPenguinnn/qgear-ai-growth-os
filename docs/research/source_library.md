# Research Source Library

This is the canonical starting point for Q-GEAR source notes.

The original bibliography is preserved at `docs/QGEAR_RESEARCH_SOURCE_LIBRARY.md`. New source-specific notes should live in this `docs/research/` directory using the project template:

```text
Title:
Author/organisation:
URL or citation:
Date accessed:
Summary:
How it affects Q-GEAR:
Implementation consequence:
Limitations:
```

## Current Notes

- `sec-edgar-provider.md`
- `fred-api-provider.md`
- `eia-api-provider.md`
- `TODO_sources.md`

## Migration Queue

Status key:

- `TODO`: source note still needs migration.
- `BLOCKED`: needs live web/source verification before changing strategy logic.
- `DONE`: source note exists in `docs/research/`.

Migrate the source-library topics from `docs/QGEAR_RESEARCH_SOURCE_LIBRARY.md` into individual notes before changing strategy logic:

- `TODO`: Bessembinder wealth concentration.
- `TODO`: Quality Minus Junk / quality-growth factor.
- `TODO`: Novy-Marx gross profitability.
- `TODO`: Earnings acceleration and post-earnings-announcement drift.
- `TODO`: Momentum/trend and relative strength.
- `TODO`: SPIVA benchmark humility.
- `TODO`: AI infrastructure demand, power, data-center, and semiconductor supply-chain sources.

Do not change scoring weights, hard gates, or research-backed strategy rules based on these topics until the corresponding notes are migrated or explicitly marked as unverified TODOs.
