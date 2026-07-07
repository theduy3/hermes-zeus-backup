---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-07
updated: 2026-07-07
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-07-07

## Summary
- Hermes is running in the local container as user `hermes` with home `/home/hermes`.
- Gateway is healthy and running manually under Docker/foreground supervision.
- Doctor reports no security advisories and a generally healthy install; main issues are missing optional API keys.
- Local summary target `/home/hermes/.hermes/daily-summaries/` was creatable and writable.

## What Ran Today
- Checked live Hermes status with `hermes status`.
- Ran diagnostics with `hermes doctor`.
- Reviewed schedules with `hermes cron list`.
- Checked MCP configuration with `hermes mcp list`.
- Confirmed gateway state with `hermes gateway status`.
- Active cron jobs: 7 active, 8 total.
- Recent job signals in cron list:
  - `daily-hermes-health-check`: last run 2026-07-06 09:01 PDT, ok; next run 2026-07-07 09:00 PDT.
  - `weekday-hermes-recap`: last run 2026-07-06 18:02 PDT, ok; next run 2026-07-07 18:00 PDT.
  - `weekly-hermes-ops-review`: last run 2026-07-06 09:18 PDT, ok; next run 2026-07-13 09:15 PDT.
  - `weekday-hermes-vault-summary`: last run 2026-07-03 18:12 PDT, ok; next run 2026-07-07 18:10 PDT.
  - `nightly-hermes-github-backup`: last run 2026-07-06 14:44 PDT, ok; next run 2026-07-07 00:00 PDT.
  - `Hermes profile gateway watchdog`: last run 2026-07-06 17:43 PDT, ok; next run shown as 2026-07-06 18:13 PDT.
  - `Silent Vancouver return travel-context reset`: scheduled once for 2026-07-13 07:15 UTC.

## Health Signals
- Environment: Hermes Agent project at `/home/hermes/.hermes/hermes-agent`.
- Python: 3.11.15; virtual environment active; version files consistent at 0.17.0.
- Model/provider: `gpt-5.5` via OpenAI Codex OAuth; Codex auth logged in and refreshed 2026-07-07 01:00 UTC.
- Gateway: running with default plus profile gateways for `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, and `zeus`.
- Profiles: 7 named profiles found; all profile gateways reported running.
- MCP: no MCP servers configured in the default profile.
- Tool availability: core tools available; browser/computer-use and several external integrations are gated by missing dependencies or credentials.
- Disk: root overlay filesystem at 63% used, with about 37G available.
- Doctor issues to address:
  - No API key found in `~/.hermes/.env`.
  - Missing optional API keys limit full tool access.
- Doctor warnings:
  - Nous Portal, MiniMax OAuth, and xAI OAuth are not logged in.
  - `agent-browser` is not installed.
  - `web` and `x_search` toolsets are missing required API keys.

## Next Actions
- Configure optional API keys or OAuth providers only where needed for active workflows.
- Install `agent-browser` if browser or computer-use workflows are expected.
- Review the profile gateway watchdog schedule because its next-run timestamp appears stale relative to the current date.
- Add MCP servers only if default-profile workflows need Obsidian, browser, or other MCP-backed tools.
- Keep using the local container summary path when the vault is intentionally read-only or unavailable.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
