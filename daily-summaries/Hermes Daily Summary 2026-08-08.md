---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-08-08
updated: 2026-08-08
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary — 2026-08-08

## Summary
- Hermes is operational on OpenAI Codex (`gpt-5.5`); default gateway and seven profile gateways are running.
- Doctor found no active security advisories and reports a consistent Hermes `0.19.1` environment.
- One scheduled Graphify refresh failed after its extraction process was killed (`SIGKILL`).

## What Ran Today
- `nightly-hermes-github-backup`: completed successfully at 00:00 PDT.
- `graphify-daily-refresh`: failed at 03:31 PDT during Hermes code extraction.
- `daily-hermes-health-check`: last completed successfully; next scheduled for 09:00 PDT.
- Gateway watchdog is active every 30 minutes.

## Health Signals
- Gateway: running manually in Docker; default plus butter, catthew, charles, finance, thor, wiki, and zeus profiles are up.
- MCP: five Graphify MCP servers are enabled.
- Cron: 7 active jobs of 8 total.
- Authentication: OpenAI Codex is logged in; no OpenAI API key is configured.
- Delivery: several cron jobs report Telegram delivery failures (`Unauthorized`).
- Diagnostics: 5 npm dependency vulnerabilities in web workspace and 3 in ui-tui workspace; `agent-browser` is not installed.

## Next Actions
- Investigate Graphify extraction `SIGKILL`; reduce extraction scope/workers or inspect memory limits before the next refresh.
- Repair the Telegram bot credentials/configuration used by cron delivery.
- Apply dependency lockfile updates for the reported npm vulnerabilities.
- Configure API keys only if API-key tools are needed beyond Codex OAuth.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
