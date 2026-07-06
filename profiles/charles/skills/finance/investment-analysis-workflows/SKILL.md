---
name: investment-analysis-workflows
description: "Use when analyzing investments or portfolio holdings: registered account reviews, cash/allocation tracking, individual stock theses, valuation, filings, market data, and portfolio-context risk."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [finance, investing, portfolio, stocks, valuation, brokerage]
    related_skills: []
---

# Investment Analysis Workflows

## Overview

This umbrella combines portfolio-level review and single-stock thesis workflows. Session-specific portfolio snapshots and thesis examples are preserved under `references/source-packages/`.

## When to Use

- Review registered investment account screenshots or cash-balance updates.
- Normalize holdings, cash, FX, allocation, and concentration.
- Build an evidence-backed thesis for an individual stock.
- Connect a single-stock idea to current portfolio exposure and risk.

## Workflow Map

1. Normalize current holdings/cash and note data freshness.
2. Gather current market data, filings, valuation, and sentiment evidence.
3. Analyze allocation impact, downside/upside, concentration, and deployment plan.
4. Separate user-provided holdings facts from market-derived assumptions.
5. For institutional 13F/13G work, fetch primary SEC EDGAR XML, parse `infoTable` rows, keep option rows separate from stock rows, and warn that 13F option `value` is not cash equity exposure. Compare against the prior filing for buy / hold / sell deltas before drawing conclusions.
6. For daily stock watchlist reports, group tickers by sector or practical investment theme before presenting tables. Add a terse Buy / Hold / Sell / Watch sentiment for each ticker with the reason in parentheses, then include short `Best opportunities today` and `Avoid / wait` sections. This is the user's preferred format for comparing and picking names from a long watchlist.

## Scheduled Weekly Portfolio Briefing Pattern

When producing the user's Sunday registered-portfolio briefing:

- Keep it concise, bullet-based, Telegram-friendly, and avoid tables.
- Use current tools for market prices, FX, news, and macro context; record data date and source.
- If Yahoo quote endpoints fail, use the Yahoo chart endpoint for prices/returns and Yahoo RSS for headlines. See `references/weekly-portfolio-briefing-data-notes.md`.
- Use known share counts and the freshest available cash/account snapshot; label stale cash/account values clearly.
- Convert USD holdings to CAD with current USD/CAD and state that values are estimates.
- Include: portfolio summary, holdings snapshot, biggest weekly movers/news, risk flags, and action watchlist.
- Separate facts from analysis/opinion. Only include thesis, risks, timeline, and confidence when suggesting an action.
- End with the required investment disclaimer.

## Daily Watchlist Report Pattern

When creating or updating recurring ticker reports from `/vault/System/Stock Watchlist.md`:

- Parse only the watchlist ticker section, not indicator sections.
- Preserve the user's watchlist order within each sector/theme group.
- Fetch price, daily % change, trailing P/E, forward P/E, market cap, sector/industry, analyst recommendation/target if available, and 52-week range.
- If vendor sector data is missing, classify manually into practical comparison groups such as Mega-cap AI / Platforms, Semiconductors, AI Infrastructure / Cloud, Data Centers / Power, Crypto Miners / Bitcoin Infrastructure, Consumer / Internet, ETFs / Funds, or Other / Unresolved.
- Use table columns: `Ticker`, `Price`, `Chg %`, `P/E`, `Fwd P/E`, `Mkt Cap`, `Sentiment`.
- Sentiment values must be `Buy`, `Hold`, `Sell`, or `Watch`; include a concise reason, e.g. `Hold (rich P/E)`, `Buy (reasonable Fwd P/E + target upside)`, `Sell (weak earnings + weak tape)`, `Watch (data missing)`.
- Prefer `Watch` for ETFs, missing data, highly speculative or unprofitable names, or names needing deeper research. Do not force a Buy/Sell call when evidence is thin.
- End investment judgments with the standard caveat that it is analysis, not financial advice.

## References

- `references/situational-awareness-13f-workflow.md` - SEC EDGAR parsing notes and latest Situational Awareness holdings workflow.

## Verification Checklist

- [ ] Data date and source recorded.
- [ ] Prices/FX/filings refreshed with tools when needed.
- [ ] Portfolio implications and uncertainty clearly stated.
