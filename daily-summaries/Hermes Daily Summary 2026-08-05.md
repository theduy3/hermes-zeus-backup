---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-08-05
updated: 2026-08-05
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary — 2026-08-05

## Summary
- Hermes is running with OpenAI Codex authentication and model `gpt-5.5`.
- Default gateway and seven named-profile gateways are running.
- Doctor reported no active security advisories; five operational follow-ups remain.

## What Ran Today
- `daily-hermes-health-check`: last run completed successfully; Telegram delivery failed as unauthorized.
- `weekday-hermes-recap`: last run completed successfully; Telegram delivery failed as unauthorized.
- `weekday-hermes-vault-summary`: currently running; prior delivery status shows Telegram unauthorized.
- `nightly-hermes-github-backup`: last run completed successfully; Telegram delivery failed as unauthorized.
- Profile gateway watchdog: last run completed successfully.
- `graphify-daily-refresh`: failed after `graphify extract` was terminated with SIGKILL during a forced Hermes code scan.

## Health Signals
- Python environment, virtual environment, required packages, SSL certificates, config version, and SQLite checks passed.
- OpenAI Codex authentication is active; no OpenAI API key is configured in `.env`.
- Five Graphify MCP servers are enabled.
- Browser tooling is not installed; npm dependency audits report build-tool vulnerabilities in browser, web, and ui-tui workspaces.
- All observed cron delivery failures are Telegram `Unauthorized` errors.

## Next Actions
- Refresh or replace the Telegram bot credentials used for cron delivery.
- Investigate the Graphify extraction SIGKILL; reduce worker/resource pressure or avoid a forced full scan.
- Install `agent-browser` if browser automation is required.
- Review and remediate reported npm dependency vulnerabilities.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[Graphify]]
- [[Telegram]]
