---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-09-01
updated: 2026-09-01
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-09-01

## Summary

Hermes Agent is operational with 7 profiles and a running gateway. Today's activity centered on a scheduled cron job that generated this summary. All core services are healthy; 3 issues flagged by `hermes doctor` are below.

## What Ran Today

- **daily-hermes-health-check** — `e83470683a90` — completed at 09:02 AM EDT (ok)
- **weekday-hermes-recap** — `c9c38ab77915` — completed at 06:02 PM EDT (ok)
- **weekday-hermes-vault-summary** — `67d44bd30291` — running (started 06:13 PM)
- **Hermes profile gateway watchdog** — `96f28d228fb9` — last check 05:46 PM EDT (ok)
- **Daily Tasks/Events Call Generator (Zeus+Catthew)** — `5a9aa5056402` — completed at 05:15 AM EDT (ok)
- **graphify-daily-refresh** — `5a9aa5056402` — failed (SIGKILL at 03:30 AM, see Health Signals)

## Health Signals

### Green
- Gateway: running (PID 2946481, multiple workers) — manually started, not as system service
- All 7 profiles online: butter, catthew, charles, finance, thor, wiki, zeus (all grok-4.5)
- xAI OAuth: logged in, refreshed 21:00 UTC
- Nous Portal: logged in, access expires 2026-09-01 22:48 UTC
- SQLite DBs: WAL mode, healthy (state.db 700.9 MB, 13,177 sessions)
- Python 3.11.15, venv active, all required packages present
- 12 of 15 scheduled jobs active

### Yellow — Action Recommended
- **No API keys in `~/.hermes/.env`** — `hermes setup` recommended
- **OpenAI Codex not authenticated** — optional; only needed to import existing Codex tokens
- **MiniMax OAuth not logged in** — optional provider
- **Nous Portal has no paid credits** — managed web/image/TTS/STT/browser/Modal tools unavailable
- **npm vulnerabilities**: agent-browser (1 high), web workspace (2 total — 1 high, 1 moderate; build-tool advisory)

### Red — Failed
- **graphify-daily-refresh** (`5a9aa5056402`): last run failed with SIGKILL (OOM likely — 7507 code files scanned). Next run: 2026-09-02 03:30 AM EDT. Needs investigation: reduce `--max-workers`, check memory limits, or exclude large subtrees.

## Next Actions

1. **graphify refresh failure**: check container memory limits; reduce `--max-workers` from 4 to 1 or 2; consider `--exclude` for large subtrees in `graphify_refresh.py`
2. **Nous Portal credits**: add credits at https://portal.nousresearch.com/billing to restore managed tool access
3. **npm audits**: `cd /home/hermes/.hermes/hermes-agent && npm audit fix --workspaces=false` (optional — build-tool advisories, not runtime)
4. **API keys**: run `hermes setup` to configure keys if managed tools are needed
5. **Gateway as service**: consider `hermes gateway install` for auto-restart on reboot

## Related Notes

- `[[Hermes Agent Setup and Operations]]`
- `[[Hermes Operations Dashboard]]`
- `~/.hermes/cron/jobs.json` — full cron job definitions
- `~/.hermes/logs/` — execution logs
