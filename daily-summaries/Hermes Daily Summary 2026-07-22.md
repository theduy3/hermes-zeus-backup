---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-22
updated: 2026-07-22
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
# Hermes Daily Summary 2026-07-22

## Summary
- Hermes is running on model `gpt-5.5` via OpenAI Codex auth.
- Gateway is active in manual/docker foreground mode, with the default profile and seven named profile gateways running.
- Doctor reports no active security advisories and core Python/package/config checks are healthy.
- Main operational gaps are missing optional API keys, no MCP servers configured, browser/computer-use dependencies unavailable, and npm vulnerability warnings in web/TUI workspaces.

## What Ran Today
- `hermes status` checked environment, auth providers, gateway, scheduled jobs, and sessions.
- `hermes doctor` checked security, Python environment, configuration, packages, tools, profiles, and advisories.
- `hermes cron list` reported 6 active scheduled jobs out of 7 total.
- `hermes mcp list` reported no configured MCP servers.
- `hermes gateway status` confirmed the gateway and profile gateways are running.

## Health Signals
- ✅ Gateway running with PIDs: `74, 40, 51, 55, 970061, 1666095, 1813818, 1813819`.
- ✅ Profiles running: `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, `zeus`.
- ✅ Python 3.11.15, Hermes version files consistent at `0.18.2`, virtual environment active.
- ✅ Configuration version is current (`v33`); required directories, memories, logs, skills, and session DB exist.
- ✅ Scheduled jobs: 6 active; recent listed runs show `ok` for health check, recap, ops review, vault summary, backup, and watchdog.
- ⚠️ API keys are broadly unset; OpenAI Codex OAuth is logged in and active, but Nous Portal, MiniMax OAuth, xAI OAuth, and many API-key providers are not configured.
- ⚠️ MCP: no servers configured.
- ⚠️ Tool gaps: browser, browser-cdp, computer_use, Discord, Home Assistant, image/video generation, Spotify, web, and x_search unavailable due to missing dependencies or keys.
- ⚠️ Dependency warnings: web workspace and ui-tui workspace each show 2 high npm vulnerabilities in build-time tooling.

## Next Actions
- Configure only the API providers actually needed; avoid chasing unused optional-provider warnings.
- Add MCP servers if Obsidian or other local integrations are expected in this environment.
- Review the web and ui-tui lockfile/dependency updates to clear build-tool npm vulnerability warnings.
- If gateway should be durable outside this container foreground process, consider installing it as a service.
- Keep monitoring scheduled jobs, especially `weekday-hermes-vault-summary` and `nightly-hermes-github-backup`, for successful latest runs.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
