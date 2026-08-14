---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-08-11
updated: 2026-08-11
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary — 2026-08-11

## Summary
- Hermes is operational: default gateway and all seven profile gateways are running.
- OpenAI Codex authentication is active; the configured model is `gpt-5.5`.
- Doctor found no active security advisories and no suspicious MCP stdio commands.

## What Ran Today
- Seven scheduled jobs are active (eight total).
- The daily health check, weekday recap, weekly operations review, nightly GitHub backup, and profile gateway watchdog last completed successfully.
- `weekday-hermes-vault-summary` is currently running.
- `graphify-daily-refresh` last failed: `graphify extract` was terminated with `SIGKILL` during the Hermes code extraction.

## Health Signals
- Gateway: running (default plus butter, catthew, charles, finance, thor, wiki, and zeus profiles).
- MCP: five Graphify MCP servers are enabled.
- Python environment, required packages, configuration version, SSL bundle, and Hermes directory structure passed doctor checks.
- Warnings: no API key in `.env`; OpenAI Codex OAuth remains logged in.
- Optional `agent-browser` is not installed.
- Multiple cron deliveries report Telegram `Unauthorized` despite successful job execution.

## Next Actions
- Restore Telegram authorization so scheduled-job delivery succeeds.
- Investigate the Graphify extraction `SIGKILL`; reduce extraction resource use or inspect container limits before the next refresh.
- Configure only required OpenAI API credentials if API-key-based tools are needed; Codex OAuth is currently functional.
- Install `agent-browser` only if browser automation is required.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
