---
name: single-stock-investment-thesis
description: Build evidence-backed investment theses for individual stocks using current market data, SEC filings, valuation math, sentiment checks, and the user's portfolio context.
tags:
  - finance
  - investing
  - stocks
  - valuation
  - sec-filings
---

# Single-Stock Investment Thesis

Use this skill when the user asks for a stock thesis, buy/sell view, watchlist review, entry point, or risk/reward analysis for a specific ticker.

## Output contract

Keep it direct and investment-oriented. Always include:

1. **Verdict** - buy / watchlist / starter / hold / avoid, with sizing if relevant.
2. **Facts** - current price, 52-week range, market cap, revenue, margin, cash/debt, guidance, and latest filing date where available.
3. **Thesis** - 3-5 reasons the investment could work.
4. **Risks** - valuation, execution, balance sheet, dilution, customer concentration, macro/FX/tax where relevant.
5. **Upside / downside scenario** - explicitly separate business quality from stock attractiveness.
6. **Portfolio action** - position size and entry/add zones, considering the user's current concentration and cash needs.
7. **Confidence** - separate confidence in the business thesis from confidence in the stock at today's price.
8. **Disclaimer** - analysis, not financial advice; consult a qualified advisor; past performance does not guarantee future results.

Use bullets rather than tables on Telegram.

## Research workflow

1. **Get current market data**
   - Use a live source, not memory. Yahoo may rate-limit or block; Nasdaq's public quote endpoint often works:
     - `https://api.nasdaq.com/api/quote/{TICKER}/info?assetclass=stocks`
   - Capture: last sale, pre/after-market status if shown, net change, 52-week range, timestamp.
   - If the quote source is delayed or premarket, label it clearly.

2. **Pull primary financials from filings**
   - For U.S. issuers, use SEC data APIs:
     - Submissions: `https://data.sec.gov/submissions/CIK{CIK10}.json`
     - Company facts: `https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK10}.json`
   - Use a descriptive User-Agent.
   - Prefer SEC/company-reported values over secondary sites for revenue, gross profit, net loss, cash, assets, liabilities, and shares.
   - Pull the latest 10-Q/10-K and recent 8-K earnings release when available.

3. **Find the latest earnings release details**
   - From the SEC submission index, open exhibit files such as `ex991.htm` when present.
   - Extract company-stated: revenue growth, gross margin, backlog, liquidity, guidance, segment notes, key contracts, and management commentary.
   - Treat press-release claims as company claims, not independent truth.

4. **Do valuation math with a tool**
   - Compute market cap from current price × relevant share count.
   - Compute P/S on TTM revenue and forward/annualized revenue where guidance is available.
   - Compute gross margin, YoY growth, cash/liquidity, net cash, backlog/revenue where relevant.
   - Do not do these calculations mentally.

5. **Optional sentiment layer**
   - If the user recently invoked `/last30days` or asks what people are saying, use the latest social research as a sentiment supplement.
   - Do not over-weight thin social data. If only Reddit/HN are available or X/YouTube are missing, label the sentiment read as incomplete.

6. **Integrate portfolio context**
   - Check known user context before recommending size. For this user, explicitly consider existing growth/tech concentration, NVDA exposure, cash drag, FX exposure, and near-term payment constraints when relevant.
   - For speculative/high-multiple stocks, default to starter sizing unless valuation is clearly favorable.

## Valuation framing

Separate company quality from stock attractiveness:

- A great company can be a poor buy if the multiple already prices in flawless execution.
- High-growth, loss-making companies need scenario analysis, not a single-point target.
- If sales multiples are extreme, say so plainly and anchor the downside to multiple compression.
- For capital-intensive companies, balance sheet and dilution risk matter even when revenue growth is strong.

## Common pitfalls

- Do not recommend a full position from a narrative alone. Verify filings and current price first.
- Do not use stale memory for current prices, market caps, or filing data.
- Do not let community hype substitute for primary financial data.
- Do not ignore the user's current portfolio concentration when suggesting a speculative stock.
- Do not bury the conclusion. The user prefers terse, actionable investment calls.

## References

- `references/rklb-2026-06-thesis-pattern.md` - Example workflow and source stack from building a Rocket Lab thesis using Nasdaq quote data, SEC companyfacts, SEC earnings-release exhibit, and `/last30days` sentiment.