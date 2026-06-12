---
name: registered-portfolio-review
description: Track and review the user's registered investment accounts from brokerage screenshots and cash-balance updates; normalize holdings, cash, FX, allocation, concentration, and deployment-plan implications.
tags:
  - finance
  - investing
  - portfolio
  - rrsp
  - fhsa
  - questrade
  - wealthsimple
---

# Registered Portfolio Review

Use this skill when the user sends brokerage screenshots, cash balances, or holding updates for RRSP/RSP/FHSA/spousal RRSP accounts and expects the data to be captured and synthesized.

## Goals

- Extract holdings and cash accurately from screenshots.
- Normalize values across CAD and USD when possible.
- Compute account-level and total registered-portfolio allocation.
- Flag concentration risk, idle-cash risk, and obvious portfolio construction issues.
- Save compact durable portfolio snapshots to memory when the data is stable enough to matter in future sessions.
- Keep replies terse and ledger-like unless the user asks for a full recommendation.

## Workflow

1. **Extract the screenshot data**
   - Use vision when screenshots are provided.
   - Capture: account type, broker, total equity, cash, buying power, market value, ticker, shares, last price, average cost, open P&L, today's P&L, and currency.
   - If the screenshot shows both holdings and account summary, reconcile totals.

2. **Compute, do not eyeball**
   - Use a calculation tool for totals, percentages, FX implications, and allocation.
   - Derive implied USD/CAD only when the screenshot provides CAD total and USD components; label it as implied.
   - Validate: cash + market value should match total equity, allowing small rounding differences.

3. **Summarize in the user's preferred format**
   - Start with `Logged.` when the user is providing portfolio data.
   - Use bullets, not tables, especially on Telegram.
   - Keep it concise: account totals, holdings, allocation, and one clear risk observation.
   - Avoid long educational disclaimers in pure logging turns; include fuller advice caveats when making buy/sell recommendations.

4. **Update memory compactly**
   - Store a consolidated snapshot, not many separate verbose entries.
   - Include date, account totals, major cash balances, key holdings/share counts, and top concentration risks.
   - When memory is near full, replace older granular portfolio entries with one compressed portfolio snapshot.

5. **Risk read-through**
   - Separate facts from analysis.
   - Flag single-stock concentration across all registered accounts, not just within one account.
   - Also flag idle cash when cash is large relative to total portfolio.
   - Be careful not to overstate precision when some account values are inferred from screenshot components.

## Pitfalls

- Do not treat an account's holdings-only allocation as the full risk picture if there is large cash in the same account.
- Do not mix CAD and USD market values without explicit conversion or an implied FX rate.
- Do not save every temporary screenshot line to memory; compress into durable account-level facts.
- Do not recommend trades from screenshots alone unless current prices/news/valuation have been researched.

## References

- `references/2026-05-19-registered-portfolio-snapshot.md` — session-specific snapshot and calculation pattern from Wealthsimple RRSP, Questrade FHSA, Questrade Spousal RRSP, and Questrade RSP cash updates.
