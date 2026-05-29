# Recurring sale checks

Session pattern: Sir asked to check the Save-On-Foods app/website under “1.49 Day Tuesday” and then clarified the routine cadence as “Every sunday.”

Reusable approach:

1. If the cadence is known and the source/task is clear, create a cron job immediately; do not wait for a full task-list style routine spec.
2. Schedule in Pacific time for household routines unless Sir says otherwise. Example used: `0 16 * * 0` = Sunday 9:00 AM PDT when the scheduler stores UTC-equivalent cron timing.
3. Make the cron prompt self-contained:
   - official page/source to check, e.g. `https://www.saveonfoods.com/dollar49day`
   - promotion names/aliases, e.g. “1.49 Day Tuesday” / “$1.49 Day Tuesday”
   - expected decision labels: `Active / Not active / Unable to verify`
   - requested evidence: sale dates, item examples, source URLs
   - fallback: if official site blocks automation, use web search and state the limitation plainly
   - guardrail: “Do not create or modify cron jobs.”
4. Confirm with the next run time, cadence, and job ID.

Pitfall: store sites may return Cloudflare 403 to direct terminal fetches. Do not encode “site is broken” as a rule; encode the resilient check pattern: official page first, web search fallback, transparent `Unable to verify` if blocked/app-only.
