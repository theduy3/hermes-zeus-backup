---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-08-19
updated: 2026-08-19
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-08-19

## Summary

Hermes Agent is running on a Linux container as the `hermes` user. The gateway is active with 7 named profiles (butter, catthew, charles, finance, thor, wiki, zeus) plus the default. Authentication is via Nous Portal (logged in, expires tonight at 22:56 UTC). Model is qwen/qwen3.8-27b-free via the orcarouter provider. Seven cron jobs are scheduled; most hit Telegram delivery failures due to a revoked bot token.

## What Ran Today

**Cron jobs that executed on 2026-08-19:**

- `daily-hermes-health-check` (09:03) — completed, delivery failed (Telegram: Unauthorized)
- `weekday-hermes-recap` (18:02) — completed, delivery failed (Telegram: Timed out)
- `weekly-hermes-ops-review` — last ran 2026-08-17, delivery failed (Unauthorized)
- `weekday-hermes-vault-summary` — last ran 2026-08-18, currently running (scheduled 18:10)
- `nightly-hermes-github-backup` (00:04) — completed, delivery failed (Unauthorized)
- `Hermes profile gateway watchdog` (18:03) — completed, no delivery issues (script stdout)
- `graphify-daily-refresh` (03:31) — **failed** (SIGKILL during AST extraction, 2515 files processed before kill)

**Gateway profiles all healthy:** butter, catthew, charles, finance, thor, wiki, zeus — all PIDs reported active.

## Health Signals

| Area | Status | Notes |
|------|--------|-------|
| Security | ✓ Clean | No active advisories, no suspicious MCP commands |
| Python env | ✓ OK | 3.11.15, venv active, all required packages present |
| Config | ⚠ Warning | Model slug `qwen/qwen3.8-27b-free` with provider `orcarouter` — vendor-prefixed slug + aggregator provider mismatch flagged by doctor |
| Auth | ⚠ Partial | Nous Portal logged in (expires 2026-08-19 22:56 UTC); OpenAI Codex, MiniMax not logged in |
| .env | ⚠ Empty | No API keys in `~/.hermes/.env` |
| Telegram | ✗ Broken | Bot token `8748253752:***` rejected by Telegram — needs regeneration via @BotFather |
| Graphify MCP | ✓ 5 servers | graphify-hermes, graphify-vault, graphify-vault-core, graphify-vault-sources, graphify-vault-daily — all enabled |
| graphify-daily-refresh | ✗ Failed | SIGKILL at 2515/2515 AST files; 65 source files produced zero nodes (baseline.json, easy.json, hard.json, acp.json, gui.json +60 more) |

## Next Actions

- **Telegram bot token** — regenerate via @BotFather and update `TELEGRAM_BOT_TOKEN` in config; this is blocking delivery for 5 of 7 cron jobs
- **graphify-daily-refresh failure** — investigate SIGKILL (likely OOM during AST extraction of 6972 files); consider reducing `--max-workers` or splitting the scan; 65 empty-source files need review (#1666)
- **Nous Portal expiry** — auth expires tonight 22:56 UTC; re-auth before then if cron jobs depend on it
- **Model/provider mismatch** — doctor flag on qwen slug + orcarouter provider; verify this is intentional or update to a proper vendor prefix
- **OpenAI Codex auth** — not logged in; relevant if Codex-backed workflows are planned

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[Cron Job Delivery Failures]]
- [[Graphify Refresh Failure — 2026-08-19]]
