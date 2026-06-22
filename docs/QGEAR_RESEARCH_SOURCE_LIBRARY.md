# Q-GEAR Research Source Library

This file gives Codex and the project a starting research bibliography. It is not a promise that these sources guarantee future returns. Every strategy rule must be implemented with caveats, tests, and benchmark comparison.

## 1. Wealth concentration and stock selection humility

### Hendrik Bessembinder — Do Stocks Outperform Treasury Bills?

- Source: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2900447
- Related ASU page: https://wpcarey.asu.edu/department-finance/faculty-research/do-stocks-outperform-treasury-bills
- Key idea: The best-performing small minority of stocks explains most net stock-market wealth creation. Many individual stocks underperform Treasury bills over their lifetimes.
- Q-GEAR implication: The system should search for exceptional long-term compounders, not maintain a generic large list of average stocks. It must also benchmark honestly and avoid assuming stock picking is easy.
- Implementation: focused AI universe, quality/growth/earnings gates, decision journal, benchmark comparison, sell/avoid rules for broken theses.
- Limitation: Historical distribution of returns does not tell us which stocks will be future winners.

## 2. Quality and profitability

### AQR / Asness, Frazzini, Pedersen — Quality Minus Junk

- Source: https://www.aqr.com/Insights/Research/Working-Paper/Quality-Minus-Junk
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2312432
- Key idea: Quality companies can be defined using profitability, growth, safety, and payout/management characteristics. Quality-minus-junk factors have historically delivered significant risk-adjusted returns.
- Q-GEAR implication: Avoid low-quality AI hype. Prefer companies with real profitability, growth, safety, and management quality.
- Implementation: business-quality score, margin quality, balance-sheet score, dilution/SBC checks, ROIC/ROE/FCF trends.
- Limitation: Quality can become expensive. High-quality companies are not automatically good buys at any price.

### Robert Novy-Marx — The Other Side of Value: The Gross Profitability Premium

- Source: https://ideas.repec.org/a/eee/jfinec/v108y2013i1p1-28.html
- NBER related page: https://www.nber.org/papers/w15940
- Key idea: Gross profitability has strong power in explaining average returns; profitable firms have historically generated higher returns than unprofitable firms despite often higher valuation ratios.
- Q-GEAR implication: Revenue growth alone is not enough. Gross margin, operating margin, and profitability quality must matter.
- Implementation: gross margin trend, operating leverage, FCF margin, gross-profitability-style metrics when data supports them.
- Limitation: Profitability metrics can be sector-specific and must be compared carefully against peers.

## 3. Earnings acceleration and post-earnings evidence

### Bernard and Thomas — Post-Earnings-Announcement Drift

- Source: https://www.jstor.org/stable/2491062
- RePEc: https://ideas.repec.org/a/bla/joares/v27y1989ip1-36.html
- Key idea: Stock prices may underreact to earnings surprises, leading to drift after earnings announcements.
- Q-GEAR implication: Quarterly earnings should be the main thesis-update event. Reward credible revenue acceleration, margin expansion, raised guidance, and positive estimate revisions.
- Implementation: earnings analyzer, guidance extraction, thesis strengthened/unchanged/weakened/broken states, 1/5/20-day market reaction.
- Limitation: PEAD effects may vary by market, size, transaction costs, crowding, and data availability. Do not implement as a pure short-term trading rule.

## 4. Momentum, trend, and technical confirmation

### Jegadeesh and Titman — Returns to Buying Winners and Selling Losers

- Source: https://www.bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf
- Key idea: Buying prior winners and selling prior losers over 3- to 12-month periods historically produced positive returns.
- Q-GEAR implication: Relative strength and trend can be useful confirmation signals.
- Implementation: relative strength vs SPY/QQQ/XLK/SMH, price vs 50/150/200 DMA, volume and drawdown checks.
- Limitation: Momentum can crash. Do not use momentum as the thesis.

### AQR / Hurst, Ooi, Pedersen — A Century of Evidence on Trend-Following Investing

- Source: https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2993026
- Key idea: Time-series momentum/trend-following has delivered positive average returns across decades and markets.
- Q-GEAR implication: Technicals should control timing, sizing, and risk, especially when stocks are in broken trends.
- Implementation: technical regime engine, technical wait state, drawdown/risk modes.
- Limitation: Trend evidence is not company-specific fundamental evidence.

## 5. Active management humility and benchmarking

### S&P Dow Jones Indices — SPIVA U.S. Scorecard

- Source: https://www.spglobal.com/spdji/en/spiva/article/spiva-us/
- Key idea: Many active managers underperform benchmarks over time.
- Q-GEAR implication: The system must benchmark itself against SPY, QQQ, XLK, and SMH and honestly show whether it adds value.
- Implementation: benchmark module, performance attribution, annual strategy audit.
- Limitation: SPIVA concerns professional funds and indexes, but its lesson on difficulty and benchmark discipline is relevant.

## 6. AI infrastructure thesis

### Gartner AI spending and semiconductor forecasts

- AI spending source: https://www.gartner.com/en/newsroom/press-releases/2026-1-15-gartner-says-worldwide-ai-spending-will-total-2-point-5-trillion-dollars-in-2026
- Semiconductor source: https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026
- Key idea: AI spending and AI semiconductor demand are large enough to justify tracking the AI infrastructure stack.
- Q-GEAR implication: Include compute, memory, storage, networking, cloud, power/cooling, and software monetisation layers.
- Implementation: AI infrastructure causal map and universe classification.
- Limitation: Top-down growth forecasts do not automatically make every AI-related stock attractive.

### IEA — Data centres and electricity demand

- Source: https://www.iea.org/reports/energy-and-ai
- Key idea: AI/data-centre demand is increasingly relevant to electricity, power infrastructure, cooling, and grid investment.
- Q-GEAR implication: Track second-order AI infrastructure beneficiaries such as power, cooling, grid, and data-centre infrastructure.
- Implementation: AI layer classification beyond semiconductors; EIA/FRED/macro/energy data hooks.
- Limitation: Energy demand does not map one-to-one into stock returns.

## 7. Data-provider and implementation sources

### SEC EDGAR APIs

- Source: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- Access guidance: https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data
- Q-GEAR implication: Use SEC data as a primary source for filings and XBRL company facts. Respect rate limits, cache responses, and use a custom User-Agent.

### FRED API

- Source: https://fred.stlouisfed.org/docs/api/fred/
- Q-GEAR implication: Use FRED for macro context such as rates, inflation, and recession/liquidity indicators.

### EIA Open Data API

- Source: https://www.eia.gov/opendata/
- Q-GEAR implication: Use EIA data for electricity and energy context relevant to data-centre infrastructure.

## 8. Codex implementation sources

### OpenAI Codex AGENTS.md guide

- Source: https://developers.openai.com/codex/guides/agents-md
- Implementation implication: Keep project-level instructions in root `AGENTS.md`; use it as Codex’s persistent project contract.

### OpenAI Codex subagents

- Source: https://developers.openai.com/codex/subagents
- Implementation implication: For broad project work, explicitly ask Codex to spawn subagents for strategy, core, API, frontend, data ingestion, QA, security, and docs.

### OpenAI GPT-5.5 usage guidance

- Source: https://developers.openai.com/api/docs/guides/latest-model
- Implementation implication: Use outcome-first prompts with clear success criteria, allowed side effects, evidence rules, and verification expectations. Use high/xhigh reasoning for hardest long-running agentic tasks when worth the extra cost/latency.
