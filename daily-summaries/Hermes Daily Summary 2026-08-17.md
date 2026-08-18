---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-08-17
updated: 2026-08-17
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-08-17

## Summary

Hermes Agent is operational. Gateway is running manually (not as a system service) with all 7 profiles healthy. 5 MCP servers enabled and responding. A config version upgrade is available (v33 → v34). Two auth gaps remain open: OpenAI Codex not logged in, and no API keys in `.env`. One cron job is currently running (`weekday-hermes-vault-summary`). 4 of 6 active cron jobs have accumulated Telegram delivery failures against user `8446251233` — unauthorized across the board.

## What Ran Today

**Cron executions:**
- `daily-hermes-health-check` — 09:03 ET — completed, delivery failed (Telegram unauthorized)
- `weekday-hermes-recap` — 18:02 ET — completed, delivery failed (Telegram unauthorized)
- `weekly-hermes-ops-review` — 12:24 ET — completed, delivery failed (Telegram unauthorized)
- `weekday-hermes-vault-summary` — 18:10 ET (yesterday's slot, still running today) — **currently running** (execution `82b1bb4f…`)
- `nightly-hermes-github-backup` — scheduled 00:00 ET daily — no output shown yet

**Gateway:** All 7 profiles up — default, butter, catthew, charles, finance, thor, wiki, zeus.

## Health Signals

| Area | Status | Note |
|---|---|---|
| Gateway | ✓ Healthy | PID 116+, all profiles green |
| MCP servers | ✓ 5/5 enabled | graphify-hermes, graphify-vault, graphify-vault-core, graphify-vault-sources, graphify-vault-daily |
| Python env | ✓ Healthy | 3.11.15, venv active, all required packages present |
| SQLite DBs | ✓ WAL mode | state.db 688 MB, cron/executions.db 1.1 MB |
| SSL/CA | ✓ Valid | No certificate issues |
| Config version | ⚠ Outdated | v33 → v34 available; run `hermes config upgrade` |
| OpenAI Codex auth | ⚠ Not logged in | No Codex credentials; run `hermes auth` |
| `.env` API keys | ⚠ Empty | No API keys present in `~/.hermes/.env` |
| Nous Portal auth | ✓ Logged in | Expires **2026-08-17 22:44 UTC** — expires tonight |
| Telegram delivery | ✗ Failing | 4/6 active jobs unauthorized for user `8446251233` — token likely revoked or user blocked |
| Disk usage | ⚠ 76% | `/home/hermes/.hermes` on `/dev/sda4` (25G free of 99G) |
| Logs | Growing | agent.log 1.2 MB today; errors.log 1.3 MB today |

## Next Actions

1. **[Auth] Renew Nous Portal token** — access expires tonight at 22:44 UTC. Run `hermes auth` before expiry or Hermes falls back to no auth tomorrow.
2. **[Config] Upgrade config.yaml** — v33 → v34. Run `hermes config upgrade` to pick up new settings.
3. **[Telegram] Investigate delivery failures** — all 4 failing jobs target `telegram:8446251233` with "Unauthorized". Likely causes: token revoked, user blocked the bot, or phone number changed. Re-authenticate the Telegram integration or update the target user ID.
4. **[Auth] OpenAI Codex login** — optional but recommended if Codex models are in use. Run `hermes auth`.
5. **[Disk] Monitor `/dev/sda4`** — at 76% with log rotation in place (agent.log.1–3 present). No action needed yet; review if > 85%.

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[Telegram Integration Troubleshooting]] *(if exists)*
