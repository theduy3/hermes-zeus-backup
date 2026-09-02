---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-08-31
updated: 2026-08-31
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-08-31

## Summary

Hermes Agent v0.20.5 running on xAI Grok OAuth (SuperGrok/Premium+) with 7 profiles all gateway-connected. Gateway running manually (Docker foreground), not as a system service. 12 active cron jobs; 2 errored today. Model provider healthy; Nous Portal auth near expiry (22:44 UTC).

## What Ran Today

| Job | Schedule | Last Run | Status |
|-----|----------|----------|--------|
| daily-hermes-health-check | 09:00 daily | 2026-08-30 09:02 PDT | ✓ ok |
| weekday-hermes-recap | 18:00 Mon–Fri | 2026-08-31 18:01 EDT | ✓ ok |
| weekly-hermes-ops-review | Mon 09:15 | 2026-08-31 09:20 EDT | ✓ ok |
| nightly-hermes-github-backup | 00:00 daily | 2026-08-31 00:01 PDT | ✓ ok |
| Hermes profile gateway watchdog | every 30m | 2026-08-31 17:45 EDT | ✓ ok |
| Daily Tasks/Events Call Generator | 05:15 daily | 2026-08-29 05:15 PDT | ✓ ok |
| Callmebot: Catthew vehicle (Jun30/Dec30) | Jun/Dec 30 | — | scheduled |
| Callmebot: Catthew humidifier (Wed) | Wed 20:00/20:30 | 2026-08-26 | ✓ ok |

## Health Signals

**Green**
- Python 3.11.15, SQLite WAL, all required packages present
- SSL CA bundle valid; config version current (v39); no deprecated keys
- 7/7 profiles gateway-running: butter, catthew, charles, finance, thor, wiki, zeus
- MCP servers: 5/6 enabled (graphify-vault, graphify-vault-core, graphify-vault-sources, graphify-vault-daily, remarkable)
- Telegram, Matrix, Slack, Teams, iMessage, Home Assistant, A2A all configured

**Yellow**
- OpenAI Codex auth not logged in (no credentials stored)
- MiniMax OAuth not logged in
- No API keys in `~/.hermes/.env` — `hermes setup` pending
- Nous Portal access/refresh expiring 2026-08-31 22:44 UTC (today)
- `weekday-hermes-vault-summary` (2cf8e8f0) still running as of last check — may be stale

**Red**
- `graphify-daily-refresh` (5f86e306) died with SIGKILL at 03:30 PT — `graphify extract` OOM-killed across 7507 code files with 4 workers. Likely memory pressure; reduce `--max-workers` or split scan.
- `weekday-hermes-vault-summary` delivery failed: Telegram send timed out to `@theduynguyen` (8446251233). Retry logic or channel fallback needed.
- Gateway running manually, not installed as a system service — won't auto-restart on reboot.

## Next Actions

- [ ] Renew/re-authenticate Nous Portal before 22:44 UTC expiry if credits still needed
- [ ] Fix `graphify-daily-refresh`: reduce `--max-workers` from 4 → 1 or 2; check available RAM
- [ ] Diagnose `weekday-hermes-vault-summary` stuck execution (2cf8e8f0) — kill if zombie, then retry delivery or switch to fallback channel
- [ ] Run `hermes gateway install` to make gateway survive reboots
- [ ] Set GITHUB_TOKEN in `.env` to lift 60 req/hr rate limit on GitHub-dependent workflows
- [ ] Re-run `hermes update` — 1457 commits behind upstream

## Related Notes

- `[[Hermes Agent Setup and Operations]]`
- `[[Hermes Operations Dashboard]]`
- `[[Life OS]]` (central operating authority)
- `[[theduyvault Tasks]]` (task source of truth)
