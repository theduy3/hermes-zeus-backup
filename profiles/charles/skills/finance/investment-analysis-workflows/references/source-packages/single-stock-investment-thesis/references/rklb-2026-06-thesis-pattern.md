# RKLB thesis workflow example - 2026-06

This reference captures the reusable research pattern from a Rocket Lab (RKLB) thesis build. Do not treat the numbers below as evergreen; re-fetch current data on future runs.

## Source stack used

1. **Sentiment pre-check**
   - `/last30days Rocket Lab` produced a useful but incomplete sentiment read.
   - Coverage was thin: Reddit + Hacker News only; X/Twitter and YouTube were not unlocked.
   - Useful community signals: RKLB treated as the public-market proxy for SpaceX/space infrastructure; investors were asking whether to buy now or wait for a dip; defense/Space Systems milestones dominated the serious bull case.

2. **Current quote**
   - Yahoo/Stooq failed or blocked in-session.
   - Nasdaq public endpoint worked:
     - `https://api.nasdaq.com/api/quote/RKLB/info?assetclass=stocks`
   - Captured price, premarket status, 52-week range, and timestamp.

3. **SEC primary data**
   - CIK used: `0001819994` for Rocket Lab Corp.
   - Submissions endpoint found latest filings:
     - `https://data.sec.gov/submissions/CIK0001819994.json`
   - Company facts endpoint provided revenue, gross profit, operating loss, net loss, cash, assets, liabilities, equity, and operating cash flow:
     - `https://data.sec.gov/api/xbrl/companyfacts/CIK0001819994.json`
   - Latest earnings release exhibit found via 8-K index and opened directly:
     - `.../000181999426000027/rklb-05072026ex991.htm`

4. **Math performed**
   - Market cap = price × share count.
   - TTM revenue = latest fiscal-year revenue + current quarter revenue - prior-year same-quarter revenue.
   - P/S = market cap / TTM revenue and market cap / annualized guided revenue.
   - Gross margin = gross profit / revenue.
   - Backlog/revenue = backlog / TTM revenue.
   - Liquidity = cash + current marketable securities + non-current marketable securities.

## Thesis shape that worked

- Lead with a blunt verdict: high-quality company, very demanding valuation.
- Separate facts from analysis.
- Make the core distinction: Rocket Lab is increasingly a Space Systems / defense space infrastructure company, not only a launch company.
- Treat Neutron as the key asymmetric upside and execution-risk swing factor.
- Highlight valuation compression risk when sales multiples are extreme.
- Tie recommended sizing to the user's existing concentration risk: speculative starter, not full position.

## Pitfall

If `/last30days` data is thin, do not stop there. Use it as sentiment only, then ground the thesis in primary filings and current quote data.