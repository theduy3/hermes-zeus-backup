---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-31
updated: 2026-07-31
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
# Hermes Daily Summary 2026-07-31

## Summary
- Live check ran Fri Jul 31 01:11:30 UTC 2026 in the local container as `uid=1500(hermes)` with home `/home/hermes`.
- Hermes Agent v0.19.0 is installed from git at `/home/hermes/.hermes/hermes-agent`; update available: 1614 commits behind.
- Default profile uses model `gpt-5.5` via `OpenAI Codex`; gateway is running with PIDs `97, 51, 59, 69, 76, 78, 86, 93`.
- Scheduled jobs: 7 active, 8 total; one visible failure: `graphify-daily-refresh` timed out after 3600s on its last run.

## What Ran Today
- ✓ **daily-hermes-health-check** — `0 9 * * *`; next `2026-07-31T09:00:00-07:00`; last `2026-07-30T09:02:55.776481-07:00 ok`.
- ✓ **weekday-hermes-recap** — `0 18 * * 1-5`; next `2026-07-31T18:00:00-07:00`; last `2026-07-30T18:02:50.510794-07:00 ok`.
- ✓ **weekly-hermes-ops-review** — `15 9 * * 1`; next `2026-08-03T09:15:00-07:00`; last `2026-07-27T09:18:48.129464-07:00 ok`.
- ✓ **weekday-hermes-vault-summary** — `10 18 * * 1-5`; next `2026-07-31T18:10:00-07:00`; last `2026-07-29T18:13:43.930260-07:00 ok`; current execution shown as running.
- ✓ **nightly-hermes-github-backup** — `0 0 * * *`; next `2026-07-31T00:00:00-07:00`; last `2026-07-30T00:01:23.563434-07:00 ok`.
- ✓ **Hermes profile gateway watchdog** — every 30m; last `2026-07-30T17:44:24.129815-07:00 ok`.
- ✗ **graphify-daily-refresh** — `30 3 * * *`; last `2026-07-30T04:30:43.731734-07:00 error: Script timed out after 3600s`.

## Health Signals
- **Good (✓):** `hermes status`, `hermes doctor`, `hermes cron list`, `hermes mcp list`, and `hermes gateway status` all executed.
- **Good (✓):** Gateway running manually, not as a system service; all listed profiles have running gateway PIDs: butter, catthew, charles, finance, thor, wiki, zeus.
- **Good (✓):** Doctor reports no active security advisories, no suspicious MCP stdio commands, Python 3.11.15, SQLite 3.53.1, venv active, config v33 up to date.
- **Good (✓):** MCP servers enabled: graphify-hermes, graphify-vault, graphify-vault-core, graphify-vault-sources, graphify-vault-daily.
- **Good (✓):** Local summary directory writable: `/home/hermes/.hermes/daily-summaries/`.
- **Good (✓):** Disk: `/home/hermes/.hermes` on `/dev/sda4` is 72% used, 29G free.
- **Warning (⚠):** No API key found in `~/.hermes/.env`; OpenAI Codex auth is logged in and current model/provider still works.
- **Warning (⚠):** Doctor found 4 issues: configure API keys, web workspace has 8 high npm vulnerabilities, ui-tui workspace has 7 high npm vulnerabilities, configure missing API keys for full tool access.
- **Warning (⚠):** Tool availability gaps: browser/computer-use/web/x_search and several platform tools are unavailable due to missing system deps or API keys.
- **Warning (⚠):** Recent logs include dependency-check warnings and a Telegram reconnect warning: `updater.stop() timed out ... forcing drain and restart`.

## Next Actions
- **Immediate:** Investigate `graphify-daily-refresh` timeout and decide whether to raise timeout, split the job, or reduce refresh scope.
- **Immediate:** Check whether `weekday-hermes-vault-summary` is genuinely still running or stale from execution `149afb4cb84442a28624ef6a3ff53a23`.
- **Today:** Run `hermes update` when safe; current install is 1614 commits behind upstream.
- **This week:** Address doctor warnings for workspace npm vulnerabilities and missing optional API keys only if those tools are needed.
- **This week:** Review Telegram reconnect warnings if message delivery becomes unreliable.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[AI Agent Tooling MOC]]
