---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-08-20
updated: 2026-08-20
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-08-20

## Summary

Hermes Agent is operational: gateway running, all 7 profiles active, model/provider functional (Nous Portal). Primary operational issue: **Telegram bot token is invalid** — all scheduled jobs that deliver via Telegram are failing delivery. Graphify daily refresh hit a SIGKILL on the extract step.

## What Ran Today

- **daily-hermes-health-check** — completed ok (09:02 EDT); delivery failed (Telegram Unauthorized)
- **weekday-hermes-recap** — completed ok (18:01 EDT); delivery failed (Telegram Unauthorized)
- **weekday-hermes-vault-summary** — still running at time of check (last run 18:12 yesterday, ok)
- **nightly-hermes-github-backup** — completed ok (00:05 EDT); delivery failed (Telegram timed out)
- **Hermes profile gateway watchdog** — completed ok (17:43 EDT)
- **graphify-daily-refresh** — errored (SIGKILL during AST extraction); 65 source files produced zero nodes

## Health Signals

- ✅ Gateway: running (PIDs 117, 71, 79, 85, 96, 97, 106, 113); all profiles up
- ✅ Model/provider: tencent/hy3:free via Nous Portal; auth valid until 23:00 UTC today
- ✅ MCP servers: 6 enabled (graphify-hermes, graphify-vault × 4, remarkable)
- ✅ Cron: 7 active jobs, all either completed or running
- ⚠️ **Telegram**: bot token rejected by server — `@BotFather` new token needed; **all 4 telegram-delivery jobs affected** (daily-health-check, weekday-recap, weekly-ops-review, nightly-github-backup)
- ⚠️ **graphify-daily-refresh**: SIGKILL — possible OOM during AST extraction of 6972 code files; 65 source files skipped (zero nodes); re-run will retry
- ⚠️ `hermes doctor` — timed out at 30s (did not complete; may need longer timeout or background run)

## Next Actions

- [ ] **Regenerate Telegram bot token** via @BotFather; update `TELEGRAM_BOT_TOKEN` in config/env
- [ ] Re-run `hermes doctor` with a longer timeout or in background to clear diagnostics
- [ ] Investigate graphify SIGKILL: check available memory/ULimits; consider reducing `--max-workers` or splitting the extract
- [ ] Confirm graphify-zero-node files (baseline.json, easy.json, hard.json, acp.json, gui.json + 60 more) are expected or need source fixes

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[Telegram Bot Configuration]]
- [[Graphify Refresh Troubleshooting]]
