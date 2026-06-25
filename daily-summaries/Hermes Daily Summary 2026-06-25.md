---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-06-25
updated: 2026-06-25
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
# Hermes Daily Summary 2026-06-25

## Summary
- Generated from live Hermes operational checks on 2026-06-25.
- Hermes gateway is running and the default profile is active on `gpt-5.5` via OpenAI Codex auth.
- Doctor completed with two configuration issues: API keys are missing/not fully configured for full tool access.
- Cron scheduler reports 14 active jobs and 15 total scheduled jobs.

## What Ran Today
- `hermes status` → exit 0.
- `hermes doctor` → exit 0.
- `hermes cron list` → exit 0.
- `hermes mcp list` → exit 0.
- `hermes gateway status` → exit 0.

## Health Signals
- Status: project path `/home/hermes/.hermes/hermes-agent`; Python `3.11.15`; `.env` exists.
- Auth: OpenAI Codex is logged in; Nous Portal, Qwen OAuth, MiniMax OAuth, xAI OAuth are not logged in/configured.
- Gateway: running manually, not as a system service; PIDs include `63, 30, 36, 41, 45, 50, 60, 5190`.
- Profiles: `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, and `zeus` gateways are running.
- Doctor: security advisories clear; Python environment, version files, config version, memory, and profile checks passed.
- Doctor warnings: no API key found in `~/.hermes/.env`; missing keys limit tool availability (`web`, `x_search`, Discord, browser/CDP, and others).
- MCP: no MCP servers are configured.
- Cron: most recent listed recurring jobs show `ok`; `weekday-hermes-vault-summary` has a prior delivery warning: Telegram timed out with `send_path_degraded`.

## Next Actions
- Run `hermes setup` when full API-key-backed tool access is needed.
- Decide whether MCP servers should be configured; current state is intentionally empty or unconfigured.
- Monitor `weekday-hermes-vault-summary` delivery because its last listed run includes a Telegram timeout warning.
- Consider installing the gateway as a service if manual gateway management becomes unreliable.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
