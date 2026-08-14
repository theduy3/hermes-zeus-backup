---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-16
updated: 2026-07-16
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-07-16

## Summary
- Daily Hermes operations summary generated from live container checks.
- Local write target was verified writable before writing: `/home/hermes/.hermes/daily-summaries/`.
- Hermes gateway is running; scheduled jobs are active.
- Doctor completed and reported 3 configuration issues to address.

## What Ran Today
- Created/overwrote this local container note for 2026-07-16.
- Ran `hermes status` successfully.
- Ran `hermes doctor` successfully.
- Ran `hermes cron list` successfully.
- Ran `hermes mcp list` successfully.
- Ran `hermes gateway status` successfully.
- Active scheduled jobs reported:
  - `daily-hermes-health-check` — last run 2026-07-15 09:01:58 -07:00, ok; next run 2026-07-16 09:00 -07:00.
  - `weekday-hermes-recap` — last run 2026-07-15 18:02:19 -07:00, ok; next run 2026-07-16 18:00 -07:00.
  - `weekly-hermes-ops-review` — last run 2026-07-13 09:18:57 -07:00, ok; next run 2026-07-20 09:15 -07:00.
  - `weekday-hermes-vault-summary` — last run 2026-07-14 18:12:16 -07:00, ok; next run 2026-07-16 18:10 -07:00.
  - `nightly-hermes-github-backup` — last run 2026-07-15 00:03:30 -07:00, ok; next run 2026-07-16 00:00 -07:00.
  - `Hermes profile gateway watchdog` — last run 2026-07-15 17:47:03 -07:00, ok; next run 2026-07-15 18:17:03 -07:00.

## Health Signals
- Environment: project path `/home/hermes/.hermes/hermes-agent`; Python 3.11.15; model `gpt-5.5`; provider OpenAI Codex.
- Authentication: OpenAI Codex is logged in; Nous Portal, Qwen OAuth, MiniMax OAuth, xAI OAuth, and listed API-key providers are not configured.
- Gateway: running in Docker foreground/manual mode with PIDs `74, 41, 47, 52, 56, 61, 67, 71`.
- Messaging: Telegram is configured; other listed messaging platforms are not configured.
- Sessions: 1 active session reported.
- Scheduled jobs: 6 active, 7 total.
- Doctor security checks: no active security advisories and no suspicious MCP stdio commands.
- Doctor environment checks: Python, virtual environment, version files, SSL CA bundle, required packages, directory structure, and command installation passed.
- Doctor warnings/issues:
  - No API key found in `~/.hermes/.env`.
  - Config version outdated: v32 → v33.
  - Browser/computer-use/web/x_search and several optional tools are unavailable due to missing system dependencies or API keys.
  - No GitHub token configured for Skills Hub higher rate limits.
- MCP: no MCP servers are configured.
- Profiles: 7 profile gateways reported running: `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, `zeus`.

## Next Actions
- Run `hermes doctor --fix` or `hermes setup` to migrate config from v32 to v33.
- Configure API keys in `~/.hermes/.env` if web, x_search, browser-dependent, or provider-specific tools are needed.
- Add MCP servers with `hermes mcp add ...` only if MCP integrations are required.
- Consider installing the gateway as a service if manual foreground Docker management is not desired.
- Continue monitoring scheduled jobs, especially `weekday-hermes-vault-summary` and `nightly-hermes-github-backup`.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
