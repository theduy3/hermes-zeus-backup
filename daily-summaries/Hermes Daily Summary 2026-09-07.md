---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-09-07
updated: 2026-09-07
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-09-07

## Summary

Hermes Agent is healthy and operational. Gateway running with 7 profiles. 12 active cron jobs; 11 completed today, 1 in progress. No active sessions open. xAI OAuth and Nous Portal auth confirmed. MCP servers all enabled and stable.

## What Ran Today

- **daily-hermes-health-check** (09:05) — completed
- **weekday-hermes-recap** (18:01) — completed
- **weekly-hermes-ops-review** (09:29) — completed
- **weekday-hermes-vault-summary** (18:13) — running (in progress)
- **nightly-hermes-github-backup** (00:02) — completed
- **graphify-daily-refresh** (03:30) — failed (exit code -9, OOM kill suspected)
- **Gateway watchdog** (17:55) — completed; next at 18:25
- **Daily Tasks/Events Call Generator** (05:15) — completed

## Health Signals

- ✓ Gateway: 6 PIDs alive, all 7 profiles up (butter, catthew, charles, finance, thor, wiki, zeus)
- ✓ Python 3.11.15, venv active, state.db WAL healthy (703 MB, 78K messages, 13K sessions)
- ✓ SSL CA bundle valid, SQLite WAL mode on all DBs
- ✓ xAI OAuth refreshing; Nous Portal auth valid until 22:58 UTC
- ⚠ `graphify-daily-refresh` crashed (exit -9) — likely OOM; check container memory limits
- ⚠ No API keys in `.env` — OAuth-based providers working but API-key providers (OpenRouter, Gemini, etc.) unavailable
- ⚠ Browser tools (agent-browser, browser-cdp, browser-use) have unmet system deps — non-critical for current operations
- ⚠ 3 npm advisories in web workspace (build-time tooling only)

## Next Actions

- Investigate `graphify-daily-refresh` OOM kill — consider memory limit bump or restart
- Optionally add missing API keys to `.env` if API-key providers needed
- Run `npm audit fix` in `/home/hermes/.hermes/hermes-agent` if advisories are a concern

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[Weekly Hermes Ops Review]]
