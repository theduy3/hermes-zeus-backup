---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-08-18
updated: 2026-08-18
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-08-18

## Summary

Hermes Agent is operational with 7 active cron jobs and 5 MCP servers. Gateway running on PID 117 (docker, foreground). Model: qwen/qwen3.8-27b-free via orcarouter. Nous Portal auth active (expires 22:47 UTC). Telegram delivery failing across all jobs — token rejected by server. One cron job currently running (`weekday-hermes-vault-summary`), two completed today, one errored yesterday (graphify daily refresh, SIGKILL).

## What Ran Today

- **2026-08-18 09:02** — `daily-hermes-health-check` completed (ok). Delivery failed: Telegram timeout to `telegram:8446251233`.
- **2026-08-18 17:56** — `Hermes profile gateway watchdog` completed (ok). All 7 profile gateways verified running.
- **2026-08-18 18:01** — `weekday-hermes-recap` completed (ok). Delivery failed: Telegram timeout to `telegram:8446251233`.
- **2026-08-18 18:10** — `weekday-hermes-vault-summary` — **running** (in progress, triggered by this cron session).

## Health Signals

### ✅ Healthy
- Gateway service running (PID 117, 71, 79, 85, 96, 97, 106, 113)
- All 7 profile gateways up: butter, catthew, charles, finance, thor, wiki, zeus
- Python 3.11.15, SQLite WAL mode healthy, state.db 688 MB / 13,104 sessions
- 5 MCP servers enabled: graphify-hermes, graphify-vault, graphify-vault-core, graphify-vault-sources, graphify-vault-daily
- xAI OAuth logged in, refreshed 2026-08-18 22:10 UTC
- No active security advisories
- No suspicious MCP stdio commands

### ⚠️ Warnings
- **Telegram token rejected** — token `8748253752:***` rejected by Telegram server. All 6 delivery-dependent jobs failing. Generate new token via @BotFather and update `TELEGRAM_BOT_TOKEN`.
- **Nous Portal credits exhausted** — managed tools (web, image, TTS, STT, browser, Modal) unavailable. Add credits at https://portal.nousresearch.com/billing.
- **OpenAI Codex not logged in** — no Codex credentials stored. Run `hermes auth` to authenticate.
- **MiniMax OAuth not logged in** — CLI credentials not found.
- **No API keys in ~/.hermes/.env** — run `hermes setup` to configure.
- **Config mismatch** — `model.default` uses `qwen/qwen3.8-27b-free` (vendor-prefixed) but provider is `orcarouter`. Either set provider to `openrouter` or drop vendor prefix.

### ❌ Issues
- **graphify-daily-refresh** (cron `30 3 * * *`) errored yesterday: `graphify extract` killed by SIGKILL (OOM?) after processing 3536/3536 files. 65 source files produced zero nodes. Re-run may retry; if persistent, report file list (#1666).
- **npm vulnerabilities** — web workspace: 4 high; ui-tui workspace: 3 high. Build-tool advisories; clears via lockfile bump.
- **Playwright Chromium not installed** — browser_* tools hidden from agent. Install: `cd /home/hermes/.hermes/hermes-agent && npx playwright install --with-deps chromium`.

## Next Actions

1. **[Urgent] Fix Telegram token** — regenerate via @BotFather, update `TELEGRAM_BOT_TOKEN` in config. Unblocks 6 delivery-dependent cron jobs.
2. **[Info] Add Nous Portal credits** — or switch to alternative providers for managed tools.
3. **[Config] Resolve model/provider mismatch** — set `model.provider` to `openrouter` or change `model.default` to `qwen3.8-27b-free`.
4. **[Optional] Install Playwright Chromium** — if browser tools needed.
5. **[Monitoring] Watch graphify-daily-refresh** — check if next run (2026-08-19 03:30) succeeds or if SIGKILL recurs (possible memory pressure).
6. **[Optional] Run `hermes doctor --fix`** — to auto-fix what's possible.

## Related Notes

- `[[Hermes Agent Setup and Operations]]`
- `[[Hermes Operations Dashboard]]`
- Previous: `[[Hermes Daily Summary 2026-08-17]]`
