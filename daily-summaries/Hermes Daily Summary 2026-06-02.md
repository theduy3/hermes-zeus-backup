---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-06-02
updated: 2026-06-02
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-06-02

## Summary

- Daily Hermes operations check completed from the local container.
- Summary note written to local Hermes storage, not the read-only vault.
- Live state was checked with `hermes status`, `hermes doctor`, `hermes cron list`, `hermes mcp list`, and `hermes gateway status`.

## What Ran Today

- `hermes status`: exit `0` (ok).
  - │                 ⚕ Hermes Agent Status                  │
  - Model:        gpt-5.5
  - Provider:     OpenAI Codex
  - ◆ Auth Providers
  - Error:      Qwen CLI credentials not found. Run 'qwen auth qwen-oauth' first.
- `hermes doctor`: exit `0` (ok).
  - │                 🩺 Hermes Doctor                        │
  - ✓ Croniter (cron expressions) (optional)
  - ◆ xAI Model Retirement (May 15, 2026)
  - ✓ No retired xAI models in config
  - ◆ Auth Providers
- `hermes cron list`: exit `0` (ok).
  - ┌─────────────────────────────────────────────────────────────────────────┐
  - │                         Scheduled Jobs                                  │
  - └─────────────────────────────────────────────────────────────────────────┘
- `hermes mcp list`: exit `0` (ok).
  - No MCP servers configured.
  - Add one with:
  - hermes mcp add <name> --url <endpoint>
  - hermes mcp add <name> --command <cmd> --args <args...>
- `hermes gateway status`: exit `0` (ok).
  - ✓ Gateway is running (PID: 37)
  - (Running manually, not as a system service)
  - hermes gateway install
  - sudo hermes gateway install --system
  - Other profiles:

## Health Signals

- `hermes status` completed successfully.
- `hermes doctor` completed successfully.
- `hermes cron list` completed successfully.
- `hermes mcp list` completed successfully.
- `hermes gateway status` completed successfully.

## Next Actions

- Monitor scheduled jobs for expected delivery and vault/container path behavior.
- Keep MCP/gateway checks in the daily loop to catch drift early.

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
