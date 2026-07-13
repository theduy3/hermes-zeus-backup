# 2026-07-07 Daily Recap Pattern

Session-specific lessons from a cron-heavy daily recap run.

## What mattered

- The live UTC date had already rolled to 2026-07-08, while the user's local reporting day was still 2026-07-07 in Montreal/EDT. The recap had to use the local reporting day, not UTC.
- `hermes cron list` on the default profile showed only default jobs; named profiles (`wiki`, `zeus`, `thor`, `catthew`, `charles`, etc.) held most of the day's output. A complete recap required scanning `~/.hermes/profiles/*/cron/output/*/YYYY-MM-DD_*.md` and checking each profile's `hermes --profile <profile> cron list`.
- A final re-scan changed the output count from 200 to 201 because a near-current no-agent watchdog output appeared while aggregating. Re-scan deltas can be silent/no-agent files, but counts should still be updated before finalizing.
- No-agent/script cron outputs often have only a markdown header with `**Status:** silent (empty output)` and no `## Response`; these are successful no-alert runs when job status is OK.
- Travel/timezone sync events may be in interactive/session history, not cron outputs. Include them in the recap when they materially changed all-profile scheduling context.

## Useful aggregation fields

For a concise daily report, classify files into:

- substantive `## Response`
- `## Error`
- `[SILENT]` response
- no-agent `Status: silent (empty output)`
- empty response sections

Then summarize high-volume silent monitoring as aggregate health, not as individual activity.
