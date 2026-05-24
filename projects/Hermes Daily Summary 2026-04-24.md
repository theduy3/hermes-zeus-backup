---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-04-24
updated: 2026-04-24
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-04-24

## Summary
- Hermes is running on model `gpt-5.5` via OpenAI Codex provider.
- Gateway is running manually in the foreground, not installed as a system service.
- Four scheduled jobs are active; one recent vault-summary run failed due to an idle timeout.
- No MCP servers are currently configured.

## What Ran Today
- Checked `hermes status`: environment configured with `.env`, project at `/home/hermes/.hermes/hermes-agent`, Python 3.11.15.
- Checked `hermes doctor`: core Python environment, packages, config, command installation, memory, and tool availability are mostly healthy.
- Checked `hermes cron list`: 4 active scheduled jobs found.
  - `daily-hermes-health-check`: last run OK; next run 2026-04-24 09:00 -07:00.
  - `weekday-hermes-recap`: last run OK; next run 2026-04-24 18:00 -07:00.
  - `weekly-hermes-ops-review`: last run OK; next run 2026-04-27 09:15 -07:00.
  - `weekday-hermes-vault-summary`: last run errored from idle timeout; next run 2026-04-24 18:10 +00:00.
- Checked `hermes mcp list`: no MCP servers configured.
- Checked `hermes gateway status`: gateway running with PID 7.

## Health Signals
- Healthy: OpenRouter API connectivity is OK.
- Healthy: OpenAI Codex auth is logged in.
- Healthy: Telegram is configured; gateway is running.
- Healthy: required packages and config version are present.
- Warning: Anthropic API key is configured but invalid during doctor check.
- Warning: Nous Portal and Google Gemini OAuth are not logged in.
- Warning: `codex` CLI is not found, despite OpenAI Codex auth being present.
- Warning: optional Docker dependency is not found.
- Warning: web tooling is limited by missing web API keys.
- Warning: profiles `3r`, `charlesbourg`, `maily`, and `ss` are present but missing config/env/alias.

## Next Actions
- Investigate the `weekday-hermes-vault-summary` timeout and reduce long non-streaming API waits if possible.
- Refresh or remove the invalid Anthropic API key.
- Install or expose the `codex` CLI if OpenAI Codex CLI workflows are expected.
- Decide whether the gateway should be installed as a persistent service.
- Configure MCP servers only if a concrete workflow needs them.
- Add missing web/search API keys if web tools are needed regularly.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[AI Agent Tooling MOC]]
