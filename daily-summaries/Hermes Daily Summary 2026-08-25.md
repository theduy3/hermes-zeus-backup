---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-08-25
updated: 2026-08-25
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-08-25

## Summary

Hermes Agent is operational with 7 active profiles under the gateway. The model is `tencent/hy3:free` via Nous Portal (auth valid through 2026-08-25 02:10 UTC — expires tonight). All 7 scheduled cron jobs are healthy with no failures. MCP stack is stable: 5 servers enabled, 1 disabled.

## What Ran Today

- **daily-hermes-health-check** — completed 2026-08-24 09:02 EDT, next at 2026-08-25 09:00 PDT
- **weekday-hermes-recap** — completed 2026-08-24 21:01 EDT, next at 2026-08-25 18:00 EDT
- **weekly-hermes-ops-review** — completed 2026-08-24 09:19 EDT, next 2026-08-31 (Monday)
- **weekday-hermes-vault-summary** — currently running (started 2026-08-21, still active as of this check)
- **nightly-hermes-github-backup** — completed 2026-08-24 00:04 PDT, next at 2026-08-25 00:00 PDT
- **Hermes profile gateway watchdog** — last health ping 2026-08-24 20:58 EDT, every 30 min

## Health Signals

- **Gateway:** Running (manual, not system service). PIDs: 2799855, 2388278, 2388285, 2388288, 2388291, 2388293, 2388294, 2895923.
- **Profiles online:** butter, catthew, charles, finance, thor, wiki, zeus — all responding.
- **Doctor:** Clean — no security advisories, no MCP anomalies, SQLite WAL healthy, all required packages present.
- **Auth:** Nous Portal logged in and valid. OpenAI Codex, MiniMax OAuth not logged in (non-blocking).
- **Config:** v37, no deprecated keys, .env exists but no API keys stored.
- **MCP servers:**
  - Enabled: graphify-vault, graphify-vault-core, graphify-vault-sources, graphify-vault-daily, remarkable
  - Disabled: graphify-hermes

## Next Actions

- **Nous Portal auth expires tonight** (2026-08-25 02:10 UTC / ~22:10 EDT) — re-auth before then or first job after expiry will fail.
- **graphify-hermes MCP disabled** — if Hermes-vault graph integration is needed, enable it via `hermes mcp enable graphify-hermes`.
- **Gateway not installed as system service** — runs manually. Consider `hermes gateway install` for persistence across reboots.
- **vault-summary cron still running** — monitor for completion; if stuck, investigate.

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[Profile Gateway Watchdog]]
- [[Nous Portal Auth]]
