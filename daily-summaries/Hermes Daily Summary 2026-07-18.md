---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-18
updated: 2026-07-18
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-07-18

## Summary

- Hermes Agent is running on Python 3.11.15 with model `gpt-5.5` via OpenAI Codex auth.
- Gateway is healthy and running manually in Docker foreground mode.
- Doctor reports no active security advisories and a consistent Hermes version state.
- Main operational gaps are missing API keys for expanded providers/tools and no configured MCP servers.

## What Ran Today

- Checked `hermes status`: environment, auth providers, gateway, jobs, and active sessions are visible.
- Checked `hermes doctor`: core Python environment, required packages, config files, command installation, and built-in tools are healthy.
- Checked `hermes cron list`: 6 active scheduled jobs are registered.
- Checked `hermes mcp list`: no MCP servers are configured.
- Checked `hermes gateway status`: default gateway and profile gateways are running.

## Health Signals

- ✅ Gateway running with PIDs reported for default plus profiles: butter, catthew, charles, finance, thor, wiki, and zeus.
- ✅ Scheduled jobs: 6 active, 7 total; recent listed jobs report last-run status `ok`.
- ✅ Directory structure, config version, local Hermes entry point, memory DB, and required packages pass doctor checks.
- ✅ OpenAI Codex auth is logged in and refreshed recently.
- ⚠️ No API keys are configured in `~/.hermes/.env`; doctor recommends running `hermes setup` for broader tool/provider access.
- ⚠️ Several optional tools are unavailable due to missing dependencies or tokens, including browser/computer-use, Discord, Spotify, web, x_search, image/video generation, and Home Assistant.
- ⚠️ No MCP servers are configured.
- ⚠️ Gateway is running manually, not installed as a system service.

## Next Actions

- Add required API keys through `hermes setup` if broader web/provider/tool access is needed.
- Configure MCP servers only if current workflows require MCP integrations.
- Consider installing the gateway as a service if persistence across restarts is important.
- Review optional tool dependencies and tokens before relying on browser, Discord, Spotify, web, or media generation workflows.
- Keep monitoring scheduled jobs for stale next-run timestamps or non-`ok` last-run states.

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
