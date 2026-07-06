# Weekly Portfolio Briefing Data Notes

Session-derived notes for scheduled registered-portfolio briefings.

## Data retrieval pattern that worked

- Yahoo Finance `v7/finance/quote` may return HTTP 401 in this environment.
- Yahoo Finance chart endpoint worked unauthenticated for prices and recent returns:
  - `https://query1.finance.yahoo.com/v8/finance/chart/{SYMBOL}?range=5d&interval=1d`
  - Use `range=10d` when a market holiday or sparse trading may hide the prior week.
  - Read `chart.result[0].meta` for `currency`, `regularMarketPrice`, and names.
  - Read `timestamp` + `indicators.quote[0].close` for last close and weekly move.
- Yahoo Finance RSS worked for quick news context:
  - `https://feeds.finance.yahoo.com/rss/2.0/headline?s={SYMBOL}&region=US&lang=en-US`
- Stooq CSV endpoints can present a JavaScript/browser-verification page or 404 from this environment; prefer Yahoo chart/RSS first for this briefing class.

## Portfolio estimation pattern

- Treat broker cash/account balances from old snapshots as stale unless newer memory/session data exists.
- Convert USD holdings to CAD using current `USDCAD=X` from the same chart endpoint.
- Clearly label values as estimates when using stale cash and latest market prices.
- If a ticker quote cannot be resolved, exclude it from estimated total and explicitly state that the total is understated if it has value.

## Presentation pattern for this user/job

- Scheduled Sunday briefings should be concise, bullet-based, Telegram-friendly, and avoid tables.
- Include: data date/source, portfolio summary, holdings snapshot, biggest movers/news, risk flags, action watchlist, and required disclaimer.
- Separate facts from analysis. Only include thesis/risks/timeline/confidence when recommending or suggesting an action.
