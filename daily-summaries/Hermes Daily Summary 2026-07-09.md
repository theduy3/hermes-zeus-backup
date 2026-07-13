---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-09
updated: 2026-07-09
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-07-09

## Summary
- Hermes is running on Python 3.11.15 with config version v32 and model `gpt-5.5` via OpenAI Codex auth.
- Gateway is healthy and running manually in Docker/foreground mode for the default profile and seven named profiles.
- Doctor reports no active security advisories and a valid Python/SSL/package baseline.
- Main issues are configuration gaps: no API keys in `~/.hermes/.env`, Nous Portal not logged in, and several optional tools/providers unavailable.

## What Ran Today
- `hermes status` completed successfully and reported 7 active scheduled jobs out of 8 total.
- `hermes doctor` completed successfully and found 2 issues to address, both related to missing API key configuration.
- `hermes cron list` completed successfully and showed active recurring jobs for health checks, recaps, vault summaries, GitHub backup, profile gateway watchdog, weekly ops review, and travel-context reset.
- `hermes mcp list` completed successfully and reported no MCP servers configured.
- `hermes gateway status` completed successfully and confirmed the gateway is running.

## Health Signals
- ✅ Gateway running: PIDs `65, 32, 37, 42, 47, 52, 57, 62`.
- ✅ Profiles running: `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, `zeus`.
- ✅ Version files consistent: Hermes `0.17.0`.
- ✅ Core command installation OK: venv entry point exists and `~/.local/bin/hermes` points to the correct target.
- ✅ Required Python packages present, including OpenAI SDK, Rich, python-dotenv, PyYAML, HTTPX, croniter, python-telegram-bot, and discord.py.
- ✅ Skills Hub OK with 8 hub-installed skills and authenticated GitHub API access.
- ⚠️ No API key found in `~/.hermes/.env`; doctor recommends running `hermes setup` for API key configuration.
- ⚠️ Nous Portal, MiniMax OAuth, xAI OAuth, Qwen OAuth, and most API-key providers are not logged in/configured.
- ⚠️ Browser/computer-use related tools are unavailable due to missing system dependency or `agent-browser` install.
- ⚠️ Web and X search tools are unavailable due to missing API keys.
- ℹ️ No MCP servers configured.

## Next Actions
- Run `hermes setup` when full provider/tool access is needed.
- Configure missing API keys in `~/.hermes/.env` if web search, x_search, browser, or external provider access should be enabled.
- Install `agent-browser` with npm if browser or computer-use workflows are required.
- Add MCP servers only if current workflows need Obsidian, filesystem, or external service MCP access.
- Consider installing the gateway as a service if manual Docker/foreground operation is not desired.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
