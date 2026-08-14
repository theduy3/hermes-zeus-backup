---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-08-13
updated: 2026-08-13
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-08-13

## Summary

Hermes Agent is operational in a Docker container. Gateway is running with 8 profiles (default, butter, catthew, charles, finance, thor, wiki, zeus). 7 cron jobs active; 2 flagged with issues. No API keys configured — model calls use provider free tiers.

## What Ran Today

- **daily-hermes-health-check** — completed (09:00 ET)
- **weekday-hermes-recap** — completed (18:01 ET)
- **Hermes profile gateway watchdog** — completed (17:46 ET)
- **weekday-hermes-vault-summary** — currently running (18:10 ET)
- **graphify-daily-refresh** — errored (06:33 ET, see Health Signals)
- **nightly-hermes-github-backup** — failed (03:00 ET, see Health Signals)

## Health Signals

### Operational (green)
- No active security advisories
- Python 3.11.15, venv active, all required packages present
- SQLite databases in WAL journal mode
- Gateway running (PID 138816), all 8 profiles healthy
- MCP servers: 5 graphify instances all enabled

### Warnings
- ⚠ No API key in `~/.hermes/.env` — models rely on provider free tiers; rate limits may apply
- Model: `tencent/hy3:free` via Nous Portal

### Failures
- **nightly-hermes-github-backup** — failed at 03:00 ET. Investigate backup script; delivery target is `origin`
- **graphify-daily-refresh** — SIGKILL during `graphify extract` on hermes-agent codebase. Worker pool processes terminated abruptly across 2000+ TypeScript/Electron source files. May be resource-related (OOM) or worker timeout. Re-run may recover; persistent failures warrant investigation.

## Next Actions

- [ ] Check nightly-github-backup logs to determine failure cause
- [ ] Re-run graphify-daily-refresh or check system resources (memory pressure) if OOM suspected
- [ ] Consider adding OpenAI API key to `.env` if free-tier rate limits become problematic

## Related Notes

- `[[Hermes Agent Setup and Operations]]`
- `[[Hermes Operations Dashboard]]`
- Cron job details: `hermes cron list`
- Gateway health: `hermes gateway status`
