---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-08-12
updated: 2026-08-12
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary — 2026-08-12

## Summary
- Hermes gateway and all seven named profile gateways are running.
- OpenAI Codex authentication is active; Telegram is configured.
- No active security advisories were reported.

## What Ran Today
- `daily-hermes-health-check`: previous run completed successfully; Telegram delivery failed as Unauthorized.
- `weekday-hermes-vault-summary`: current execution is running; prior delivery failed as Unauthorized.
- `graphify-daily-refresh`: most recent run failed after `graphify extract` was terminated with SIGKILL.
- Seven of eight scheduled jobs are active; the profile gateway watchdog last completed successfully.

## Health Signals
- `hermes doctor`: Python environment, required packages, SSL, SQLite, and core directory structure are healthy.
- Gateway is running manually in Docker; default plus butter, catthew, charles, finance, thor, wiki, and zeus are up.
- MCP: five Graphify servers are enabled.
- Warnings: config requires migration from v33 to v34; no API key in `.env`; browser tooling is not installed.
- Delivery failures persist for several cron jobs because Telegram returns Unauthorized.

## Next Actions
- Repair Telegram credentials or destination configuration, then verify cron delivery.
- Run `hermes doctor --fix` or `hermes setup` to migrate config v33 → v34.
- Investigate Graphify refresh SIGKILL; reduce extraction load or inspect container memory limits.
- Install `agent-browser` only if browser automation is needed.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[Hermes Daily Summary — 2026-08-11]]
