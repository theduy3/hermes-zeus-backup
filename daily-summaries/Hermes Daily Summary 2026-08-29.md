---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-08-29
updated: 2026-08-29
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-08-29

## 1. Summary

Hermes Agent is operational. The gateway and all 7 named profiles (butter, catthew, charles, finance, thor, wiki, zeus) are running on grok-4.5 via xAI OAuth. 12 of 15 scheduled cron jobs are active. One persistent delivery failure (Telegram timeout) and one graphify daily-refresh crash are the active issues.

## 2. What Ran Today

- `daily-hermes-health-check` — completed at 09:01 PDT, ok
- `weekday-hermes-recap` — completed at 18:01 PDT, ok
- `nightly-hermes-github-backup` — completed at 00:03 PDT, ok
- `Hermes profile gateway watchdog` — completed at 18:10 PDT, ok
- `graphify-daily-refresh` — FAILED (SIGKILL during AST extraction, 3 consecutive failures)
- `weekday-hermes-vault-summary` — currently running (started 18:11 PDT); last run ok but **Telegram delivery failed** (Timed out, target telegram:8446251233)

## 3. Health Signals

### OK
- Gateway running (manual/foreground, PID 3637441 + workers); all 7 profiles healthy
- Python 3.11.15, venv active, SQLite WAL mode
- xAI OAuth logged in (refreshed 2026-08-28 21:00 UTC)
- Nous Portal logged in (access expires 2026-08-29 02:00 UTC — refresh arriving today)
- Config v39, no deprecated keys
- state.db: 13,163 sessions, 77,698 messages, WAL 4.0 MB
- Messaging: Telegram, Discord, Slack, Matrix, Mattermost, iMessage, Home Assistant, Microsoft Teams, A2A — all configured
- MCP servers: graphify-vault (×4), remarkable — all enabled

### Warnings
- **No API keys in ~/.hermes/.env** — `hermes setup` recommended
- **OpenAI Codex** not logged in (optional; only needed if importing Codex tokens)
- **MiniMax OAuth** not logged in
- **Nous Portal credits** — no paid credits; managed web/image/TTS/STT/browser/Modal tools unavailable
- **GITHUB_TOKEN** not set → 60 req/hr rate limit on GitHub MCP

### Failed / Degraded
- **graphify-daily-refresh** (cron `5a9aa5056402`): SIGKILL at 3/2801 AST extraction. 66 source files produced zero nodes. Likely OOM or resource limit; re-run will retry empties.
- **Telegram delivery** (cron `67d44bd30291`): `send_path_degraded` — timed out targeting telegram:8446251233. Affects `weekday-hermes-vault-summary`. Previous runs ok; may be transient network issue.

### Unavailable Tools (system dependencies not met)
browser-cdp, browser-use, computer_use, discord (no token), feishu_doc, feishu_drive, homeassistant, image_gen, spotify, hermes-yuanbao

## 4. Next Actions

- [ ] `hermes setup` — add API keys to ~/.hermes/.env (OpenRouter at minimum for web tools; credits on Nous Portal for managed tools)
- [ ] Investigate graphify-daily-refresh SIGKILL: check `dmesg` / container memory limits; consider lowering `--max-workers` or running extract sequentially
- [ ] Re-test Telegram delivery: send a test message to telegram:8446251233; if persistent, check network/firewall or Telegram Bot API health
- [ ] Refresh Nous Portal auth before 2026-08-29 02:00 UTC expiry (or verify auto-refresh fires in time)
- [ ] Review `weekday-hermes-vault-summary` execution `fccc2dfef38440c49d67e35bafbd3491` once complete

## 5. Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[Cron Job Troubleshooting]]
- [[Telegram Integration]]
