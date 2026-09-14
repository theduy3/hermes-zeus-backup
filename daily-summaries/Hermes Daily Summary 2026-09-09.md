---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-09-09

## Summary

Hermes gateway is running and healthy. 12 of 13 scheduled jobs active. Two delivery failures today (Telegram), one job currently running (vault summary), one job failed (graphify refresh — likely OOM kill). Nous Portal credentials expire at 23:00 UTC today; refresh needed to keep managed tools working.

## What Ran Today

- **daily-hermes-health-check** — ok, ran 09:01 EDT
- **weekday-hermes-recap** — execution ok, **delivery failed** (TelegramUnauthorized on target 8446251233)
- **nightly-hermes-github-backup** — ok, ran 00:01 EDT
- **Hermes profile gateway watchdog** — ok, last 18:06 EDT
- **Daily Tasks/Events Call Generator (Zeus+Catthew)** — ok, ran 05:15 EDT
- **graphify-daily-refresh** — **failed** (exit code -9, OOM kill); 46 source files produced zero nodes
- **weekday-hermes-vault-summary** — currently running (last run timed out on output length)
- Call reminders (Catthew vehicle/humidifier) — idle pending schedule

## Health Signals

- **Gateway**: ✓ running (PIDs 118, 70, 78, 85, 94, 100, 107, 117), foreground docker, not system service
- **Telegram**: ⚠ Bot token `8748253752:***` rejected by server — invalid or revoked; needs new token from @BotFather
- **Nous Portal**: ✓ logged in, but **no paid credits** — managed web/image/TTS/STT/browser/Modal tools unavailable
- **xAI OAuth**: ✓ logged in, refreshed 16:21 UTC
- **OpenAI Codex**: ✗ not logged in
- **Model**: gpt-5.5 via ChatGPT/Codex subscription
- **MCP servers**: 5 enabled (graphify-vault, graphify-vault-core, graphify-vault-sources, graphify-vault-daily, remarkable), 1 disabled (graphify-hermes)
- **Active sessions**: 0

## Next Actions

- [ ] Renew Nous Portal billing/credits before 23:00 UTC expiry to restore managed tools
- [ ] Refresh Hermes model config after billing update (`hermes model`)
- [ ] Fix Telegram bot token (invalid token — get new one from @BotFather, update `TELEGRAM_BOT_TOKEN`)
- [ ] Investigate graphify-daily-refresh OOM (exit -9) — raise memory limit or reduce `--max-workers`
- [ ] Check weekday-hermes-vault-summary output length issue — may need to split or truncate

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[Telegram Bot Configuration]]
- [[Graphify Configuration]]
