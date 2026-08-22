---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-08-21
updated: 2026-08-21
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-08-21

## Summary

Gateway running with 7 profiles, all healthy. 6 of 7 cron jobs completed OK today; 1 failed (graphify-daily-refresh, SIGKILL). No API keys configured — free-tier models in use across all profiles.

## What Ran Today

- **daily-hermes-health-check** — 09:03, completed OK
- **weekday-hermes-recap** — 18:03, completed OK
- **nightly-hermes-github-backup** — 00:02, completed OK
- **graphify-daily-refresh** — 03:30, **ERROR** (SIGKILL during AST extraction; 65 source files produced zero nodes)
- **Hermes profile gateway watchdog** — 17:54, completed OK

## Health Signals

### Green
- Gateway: ✓ running (PID 2387703+), not installed as system service
- 7 profiles all gateway-connected: butter, catthew, charles, finance, thor, wiki, zeus
- MCP servers: 5/6 enabled (graphify-vault ×4, remarkable)
- `.env` exists

### Yellow
- `graphify-hermes` MCP: disabled
- Gateway not installed as a system service (running manually)

### Red
- **graphify-daily-refresh** crashed with SIGKILL — likely OOM during full AST extraction of 6972 code files; 65 source files produced zero nodes
- Doctor flag: 3 issues — no API keys set (OpenRouter, OpenAI, etc.), 4 npm vulnerabilities in `web` workspace, 3 npm vulnerabilities in `ui-tui` workspace

## Next Actions

- [ ] Investigate graphify-daily-refresh OOM — consider reducing `--max-workers`, adding swap, or scoping the extract
- [ ] Decide on graphify-hermes MCP: re-enable or leave disabled
- [ ] Run `hermes doctor --fix` to address npm vulnerabilities if desired
- [ ] Consider `hermes gateway install` for system-service resilience

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[Cron Job: graphify-daily-refresh]]
