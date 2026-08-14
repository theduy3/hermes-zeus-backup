# Major earnings reminder tasks

Use when Duy asks to add or maintain reminders for major US stock-market earnings.

## User preference
- Duy wants major US earnings reminders in Obsidian/Zeus, refreshed at the beginning of each earnings season: January, April, July, and October.
- These are specific-time/fixed finance reminders, not Pomodoro work items.
- Keep reminder volume useful: prefer mega-cap/major watchlist names rather than every earnings calendar entry.

## Recommended task shape
Create one Markdown task per ticker/date under `/vault/Tasks/tasks/`:

```yaml
---
type: task
due_date: YYYY-MM-DD
due_time: "Before market open"   # or "After market close" / "Time not confirmed"
status: pending
time_block: fixed
estimated_minutes: 10
energy: low
priority: normal
company: finance
tags: [finance, stocks, earnings]
earnings_symbol: TSLA
earnings_session: "After market close"
earnings_fiscal_quarter: "Jun/2026"
source: nasdaq-earnings-calendar
---
# Earnings: TSLA — Tesla, Inc.

Date: YYYY-MM-DD
Time: After market close
Ticker: TSLA
Company: Tesla, Inc.
Fiscal quarter: Jun/2026
EPS forecast: $0.31

Reminder: check earnings preview, options/volatility, and post-earnings reaction.
```

## Current Zeus implementation
- Script: `/home/hermes/.hermes/profiles/zeus/scripts/fetch_major_earnings_reminders.py`
- Quarterly cron: `ccdc2300f9fe`, schedule `0 8 1 1,4,7,10 *`
- The script fetches Nasdaq earnings calendar rows for the next ~70 days and creates missing `/vault/Tasks/tasks/earnings-*.md` files idempotently.
- Default filter: explicit core ticker allowlist plus market cap threshold to avoid flooding.

## Verification
1. Dry-run importer:
   ```bash
   python3 /home/hermes/.hermes/profiles/zeus/scripts/fetch_major_earnings_reminders.py --dry-run
   ```
2. Spot-read a generated file and verify frontmatter includes `due_time`, `time_block: fixed`, `tags: [finance, stocks, earnings]`.
3. Run Zeus calendar sync dry-run; expected earnings tasks appear as created/unchanged on `theduy calendar`.
4. Generate a daily plan for an earnings date and confirm earnings appear under `Fixed`, not Pomodoro sections.

## Pitfalls
- Do not create these under Catthew or Kitty/Family calendar; these are Zeus/finance reminders.
- Do not feed earnings reminders into Pomodoro schedule reminders.
- Do not import every Nasdaq row; constrain to major names or Duy’s watchlist/major-market-cap filter.
