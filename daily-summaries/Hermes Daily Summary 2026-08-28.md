---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-08-28
updated: 2026-08-28
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-08-28

## Summary

Hermes gateway is healthy with all 7 profiles running. Cron jobs executed normally yesterday; the weekday vault summary job is currently mid-run. No security advisories, no MCP anomalies, auth fully operational via Nous Portal + xAI OAuth.

## What Ran Today

**Cron jobs (all active, 6 jobs total):**

- `daily-hermes-health-check` — last run 2026-08-27 09:03 PDT, completed ok
- `weekday-hermes-recap` — last run 2026-08-27 18:04 PDT, completed ok
- `weekly-hermes-ops-review` — last run 2026-08-24, completed ok; next run 2026-08-31
- `weekday-hermes-vault-summary` — last run 2026-08-26, **currently running** (started 2026-08-26 18:12 EDT)
- `nightly-hermes-github-backup` — last run 2026-08-27 00:06 PDT, completed ok
- `Hermes profile gateway watchdog` — runs every 30 min, last ok at 18:07 PDT

**Current execution:** `weekday-hermes-vault-summary` (execution 8365445977114f50a81622ea76dfbec5) is mid-flight.

## Health Signals

- **Gateway:** ✓ Running, PID 3637441, manual mode (not system service)
- **Profiles (all 7):** ✓ butter, catthew, charles, finance, thor, wiki, zeus — all up
- **Doctor:** ✓ No security advisories, no MCP anomalies, Python 3.11.15, SQLite WAL healthy
- **Auth:** ✓ Nous Portal logged in (exp 2026-08-28 01:49 UTC); ✓ xAI OAuth logged in; ⚠ Codex auth not logged in (optional)
- **MCP Servers:**
  - ✓ graphify-vault (enabled)
  - ✓ graphify-vault-core (enabled)
  - ✓ graphify-vault-sources (enabled)
  - ✓ graphify-vault-daily (enabled)
  - ✓ remarkable (enabled)
  - ✗ graphify-hermes (disabled)
- **Model:** grok-4.5 via xAI Grok OAuth (SuperGrok / Premium+)
- **Config:** ✓ v39, no deprecated keys, no API keys in .env (uses OAuth providers)

## Next Actions

- None required — all systems nominal.
- Optional: `hermes gateway install` to run gateway as a system service instead of manual mode.

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[Daily Briefing 2026-08-28]] (if generated separately)
