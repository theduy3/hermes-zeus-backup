---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-14
updated: 2026-07-14
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
# Hermes Daily Summary 2026-07-14

## Summary
- Hermes is running on Python 3.11.15 with config version v32 and model `gpt-5.5` via OpenAI Codex auth.
- Gateway is active in manual/docker foreground mode with the default profile and seven named profile gateways running.
- Scheduled automation is active: 6 active jobs, 7 total jobs reported by status; `hermes cron list` shows 6 active scheduled jobs.
- Doctor found 2 configuration issues, both related to missing API keys for full tool/provider access.

## What Ran Today
- `hermes status` confirmed environment, profile, gateway, scheduled jobs, and session status.
- `hermes doctor` checked security advisories, MCP commands, Python environment, SSL, packages, config, auth, directories, tools, profiles, and Skills Hub.
- `hermes cron list` enumerated active recurring jobs:
  - `daily-hermes-health-check` — active; last run OK on 2026-07-13; next run 2026-07-14 09:00 -07:00.
  - `weekday-hermes-recap` — active; last run OK on 2026-07-13; next run 2026-07-14 18:00 -07:00.
  - `weekly-hermes-ops-review` — active; last run OK on 2026-07-13; next run 2026-07-20 09:15 -07:00.
  - `weekday-hermes-vault-summary` — active with `obsidian` skill; last run OK on 2026-07-10; next run 2026-07-14 18:10 -07:00.
  - `nightly-hermes-github-backup` — active; last run OK on 2026-07-13; next run 2026-07-14 00:00 -07:00.
  - `Hermes profile gateway watchdog` — active script job; last run OK on 2026-07-13; next run 2026-07-13 18:15 -07:00.
- `hermes mcp list` reported no MCP servers configured.
- `hermes gateway status` confirmed the gateway and profile gateways are running.

## Health Signals
- Positive:
  - No active security advisories.
  - No suspicious MCP stdio commands.
  - Python virtual environment, Hermes version files, SSL CA bundle, required packages, directory structure, command installation, GitHub token, and Skills Hub lock file are healthy.
  - Gateway is running for default plus profiles: `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, and `zeus`.
  - Built-in memory provider is active and state database is present.
- Warnings / gaps:
  - No API key found in `~/.hermes/.env`; OpenAI Codex auth is logged in, but most API-key providers are not configured.
  - Nous Portal, MiniMax OAuth, xAI OAuth, and Qwen OAuth are not logged in/configured.
  - Browser, browser-cdp, computer_use, discord, homeassistant, spotify, web, x_search, video_gen, and yuanbao tools are unavailable or missing dependencies/keys.
  - `agent-browser` is not installed.
  - No MCP servers are configured.
  - Gateway is running manually rather than as a system service.

## Next Actions
- Configure required API keys with `hermes setup` if broader provider/tool access is needed.
- Install or repair browser tooling (`agent-browser`) if browser/computer-use workflows should be available.
- Add MCP servers only if a concrete workflow needs them; current state is clean but empty.
- Consider installing the gateway as a service if persistent host-managed startup is preferred.
- Review whether `weekday-hermes-vault-summary` should keep using the local container summary target or be updated once vault mounts/permissions are intentionally available.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
