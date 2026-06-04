---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-06-04
updated: 2026-06-04
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-06-04

## Summary

- Hermes is running on Linux with project path `/home/hermes/.hermes/hermes-agent`.
- Active model/provider: `gpt-5.5` via OpenAI Codex; OpenAI Codex auth is logged in.
- Gateway is healthy and running in foreground Docker/manual mode with PID `37`.
- Doctor found no active security advisories and confirmed core Python/package/install checks are OK.
- Main issues remain missing API keys for broader provider/tool coverage and missing Playwright Chromium for browser tools.

## What Ran Today

- `hermes status` reported `10 active` scheduled jobs out of `11 total` and `1` active session.
- Scheduled jobs are active for health checks, recaps, ops review, GitHub backup, vault processing, wiki ingest/lint, today, tonight, and vault summary.
- Most recent visible runs were OK; `weekday-hermes-vault-summary` last ran OK but had a Telegram delivery timeout.
- `hermes mcp list` reported no MCP servers configured.
- Gateway status checked successfully for default plus profiles: butter, catthew, charles, finance, thor, and zeus.

## Health Signals

- Gateway: running, PID `37`; other profile gateways also running.
- Python: `3.11.15`; virtual environment active.
- Config: `~/.hermes/config.yaml` exists and is up to date at config version `v24`.
- Memory/state: built-in memory active; state database present with `12581` sessions.
- Filesystem: `/home/hermes/.hermes` on `/dev/sda1`, `194G` total, `130G` used, `64G` available, `67%` usage.
- Logs footprint: `/home/hermes/.hermes/logs` is about `16M`.
- Tool availability: terminal, file, cronjob, delegation, memory, session_search, skills, todo, TTS, vision, video, Feishu, image generation, and code execution are available.
- Tool limitations: browser/browser-cdp/computer_use unavailable due to missing system dependency; web and x_search unavailable due to missing API keys; Discord unavailable due to missing bot token.
- Auth: OpenAI Codex and Google Gemini OAuth are logged in; Nous Portal, MiniMax OAuth, and xAI OAuth are not logged in.

## Next Actions

- Run `hermes setup` to configure missing API keys if broader web/provider/tool access is needed.
- Install Playwright Chromium from the Hermes agent project if browser tools are required: `cd /home/hermes/.hermes/hermes-agent && npx playwright install --with-deps chromium`.
- Review Telegram delivery reliability for `weekday-hermes-vault-summary` because the last listed run had a delivery timeout.
- Add MCP servers with `hermes mcp add ...` if Obsidian or other MCP-backed workflows should be available through MCP.
- Continue monitoring disk usage; current `67%` usage is acceptable but worth tracking.

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
