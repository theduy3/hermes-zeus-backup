---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-06-27
updated: 2026-06-27
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-06-27

## Summary
- Hermes operational checks ran against live local state on 2026-06-27.
- Core Hermes CLI surfaces are responsive: status, doctor, cron list, MCP list, and gateway status all returned successfully.
- Gateway is running locally with all named profile gateways reporting active.
- Doctor reports two configuration issues: missing API keys in `~/.hermes/.env` and missing API keys for full tool access.

## What Ran Today
- `hermes status` completed successfully.
- `hermes doctor` completed successfully and surfaced configuration warnings.
- `hermes cron list` completed successfully and reported 15 active scheduled jobs.
- `hermes mcp list` completed successfully and reported no configured MCP servers.
- `hermes gateway status` completed successfully and confirmed the gateway is running manually, not as a system service.

## Health Signals
- Environment: Hermes Agent project at `/home/hermes/.hermes/hermes-agent`, Python 3.11.15, model `gpt-5.5`, provider `OpenAI Codex`.
- Auth: OpenAI Codex is logged in; Nous Portal, MiniMax OAuth, xAI OAuth, and Qwen OAuth are not logged in.
- API keys: no API key found in `~/.hermes/.env`; multiple provider/tool integrations remain unconfigured.
- Gateway: running with PIDs `64, 31, 37, 41, 46, 51, 56, 63`.
- Profiles: `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, and `zeus` gateways all report running.
- Cron: 15 active jobs, including health checks, recaps, vault workflows, GitHub backup, gateway watchdog, and travel-context reset jobs.
- MCP: no MCP servers configured.
- Doctor: no active security advisories; no suspicious MCP stdio commands; version files consistent at `0.17.0`; SSL and required packages are healthy.
- Tool availability warnings: browser/computer-use, Discord, Home Assistant, web, x_search, Yuanbao, Spotify, and video_gen have missing dependencies or credentials.

## Next Actions
- Configure API keys via `hermes setup` if broader provider/tool access is needed.
- Log in to Nous Portal, MiniMax OAuth, xAI OAuth, or Qwen OAuth only if those providers are expected to be used.
- Add MCP servers with `hermes mcp add` if Obsidian or other MCP-backed workflows should be available through Hermes.
- Consider installing the gateway as a service if manual gateway supervision is not desired.
- Continue monitoring scheduled jobs, especially vault workflows and the profile gateway watchdog.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
