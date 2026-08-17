---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-08-14
updated: 2026-08-14
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-08-14

## Summary

Hermes Agent is **operational** with 7 Telegram profiles running under a manual gateway (not a system service). The primary model is `gpt-5.5` via OpenAI Codex, authenticated via Nous Portal (xAI OAuth also active). All 7 profile gateways are healthy. Five of six delivery-bound cron jobs are failing delivery to Telegram (Unauthorized on `telegram:8446251233`) — a credential/token issue, not a runtime problem. One cron job (`weekday-hermes-vault-summary`) is currently running. The `graphify-daily-refresh` job errored last night.

## What Ran Today

- **daily-hermes-health-check** (09:02) — completed, delivery failed (Telegram Unauthorized)
- **weekday-hermes-recap** (18:00) — completed, delivery failed (Telegram Unauthorized)
- **nightly-hermes-github-backup** (00:10) — completed, delivery failed (Telegram Unauthorized)
- **graphify-daily-refresh** (03:31) — **errored** (exit 1): 57 source files produced zero nodes; re-run will retry
- **Hermes profile gateway watchdog** (17:50) — completed OK

**Currently running:**
- `weekday-hermes-vault-summary` (started 2026-08-13T18:11, still running as of this report)

## Health Signals

### Green
- Gateway: 7/7 profiles up (butter, catthew, charles, finance, thor, wiki, zeus)
- Python env: 3.11.15, venv active, all required packages present
- SQLite: WAL mode, state.db 688 MB / 13,086 sessions / 75,002 messages — healthy
- SSL CA bundle: valid
- Security: no active advisories, no suspicious MCP commands
- xAI OAuth: logged in and refreshed at 22:10 UTC
- Nous Portal: logged in (access expires 23:10 UTC today — same as this report time)

### Yellow
- **Config version outdated** (v33 → v34) — new settings available, not yet applied
- **No API key in `~/.hermes/.env`** — `.env` exists but empty of keys
- **OpenAI Codex not logged in** — primary model is gpt-5.5 but Codex auth is missing; running via Nous Portal inference instead
- **MiniMax OAuth not logged in**
- **Nous Portal credits: none usable** — managed web/image/TTS/STT/browser/Modal tools unavailable; add credits at portal.nousresearch.com/billing

### Red
- **Telegram delivery failing on 5/6 delivery-bound jobs** — all return `Unauthorized (target telegram:8446251233)`. The bot token for that chat ID is likely expired or revoked. This affects: daily-hermes-health-check, weekday-hermes-recap, nightly-hermes-github-backup, and any other job delivering to that target. The `weekday-hermes-vault-summary` job also lists `Deliver: origin` — verify if it also hits this failure path.
- **graphify-daily-refresh errored** — 57 source files empty; may be transient (retries empties) or indicate stale source data

## Next Actions

1. **Renew Nous Portal access** — access expires 2026-08-14 23:10 UTC; if this report is being read after that, re-auth with `hermes auth` or refresh billing at portal.nousresearch.com/billing
2. **Fix Telegram bot token** for chat `8446251233` — token appears unauthorized across all delivery-bound jobs; update in config or regenerate via BotFather
3. **Apply config v34 update** — run `hermes config migrate` or manually review new settings
4. **Re-run graphify-daily-refresh** — the 57 zero-node sources may clear on retry; if persistent, investigate source file health
5. **Add API keys to `~/.hermes/.env`** if any key-based providers are intended (currently all API-key providers show ✗ not configured)

## Related Notes

- `[[Hermes Agent Setup and Operations]]`
- `[[Hermes Operations Dashboard]]`
- `[[Hermes Profile Gateway Watchdog]]`
- `[[Telegram Delivery Troubleshooting]]`
