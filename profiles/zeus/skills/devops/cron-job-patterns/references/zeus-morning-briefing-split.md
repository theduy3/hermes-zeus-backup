# Zeus Morning Briefing Split Pattern

Use when a daily briefing is doing too much or the user asks for tasks separately.

## Pattern

Create/maintain two cron jobs:

1. **Info-only briefing**
   - Schedule: main morning time, e.g. `15 6 * * *`
   - Content: header/date, family schedule context, stocks, headlines, weather, horoscope
   - Explicitly forbid tasks, reminders, overdue items, checkboxes, and action lists

2. **Tasks-only briefing**
   - Schedule: 1-3 minutes after info job, e.g. `17 6 * * *`
   - Content: Obsidian tasks, Catthew/family chores, Finance Advisor due/overdue jobs, Investment Strategist due/overdue jobs, timezone/travel trigger if relevant
   - Format every actionable item as `☐ item text`
   - Omit empty sections

## Cross-profile task sources

- Catthew output: latest file in `/home/hermes/.hermes/profiles/catthew/cron/output/<job_id>/`
- Finance Advisor: `/home/hermes/.hermes/profiles/finance/cron/jobs.json`
- Investment Strategist / Charles: `/home/hermes/.hermes/profiles/charles/cron/jobs.json`

For `jobs.json`, include enabled jobs due today in the user's timezone and overdue one-shot jobs that have not completed. Missing `jobs.json` means no due items, not an error.

## User readability preferences captured

- Strip Obsidian wiki-link brackets and markdown syntax in Telegram output.
- Do not dump raw `[[...]]` links; convert to clean display text.
- Use `☐` checkbox lines for task/reminder messages.
- Keep info and task briefings separate when requested.
