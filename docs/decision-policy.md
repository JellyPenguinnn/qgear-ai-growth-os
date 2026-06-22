# Decision Policy

Decision states:

- `REJECTED`
- `RESEARCH_CANDIDATE`
- `WATCHLIST`
- `APPROVED_THESIS`
- `APPROVED_VALUATION_ZONE`
- `TECHNICAL_WAIT`
- `STARTER_ALLOWED`
- `ADD_ALLOWED`
- `HOLD`
- `TRIM_CANDIDATE`
- `EXIT_THESIS_BROKEN`
- `BLOCKED_BY_RISK`
- `NO_ACTION`

## Hard Gates

- No approved thesis: no buy/add.
- No invalidation rule: no buy/add.
- AI relevance weak or unproven: reject.
- Latest earnings weakened thesis: no buy/add.
- Valuation below hurdle: watch/hold.
- Technical trend broken: technical wait unless thesis is broken.
- Concentration cap would be breached: hold or trim candidate.
- Evidence stale: watch/hold.
- Price dropped but no fresh positive evidence: add blocked.
- Portfolio drawdown >=35%: hard audit and normal risk-taking blocked.
- Fresh positive evidence must be represented by structured evidence objects with claim, evidence, source, source date, confidence, and what would disprove it.

## Valid Buy/Add Evidence

Valid evidence can include accelerated revenue growth, measurable AI demand, improved segment/RPO/backlog/order data, margin expansion, FCF improvement, raised guidance, supportive valuation, stabilising technicals, and available portfolio risk budget.
