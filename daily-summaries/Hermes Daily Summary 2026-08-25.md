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

Hermes Agent is healthy and fully operational. Gateway running with 7 child profiles. 12 of 13 scheduled jobs active; the one inactive job appears to be a no-agent script that completed normally. All MCP servers enabled. One Telegram profile (`default`) and 6 other named profiles active. xAI OAuth and Nous Portal authenticated; OpenAI Codex not set up (non-blocking).

## What Ran Today

**Completed cron jobs (2026-08-25):**
- `daily-hermes-health-check` — 12:01 EDT, ok
- `weekday-hermes-recap` — 18:02 EDT, ok
- `weekly-hermes-ops-review` — ran 2026-08-24, ok
- `nightly-hermes-github-backup` — 03:02 EDT, ok
- `Hermes profile gateway watchdog` — 17:59 EDT, ok
- `graphify-daily-refresh` — 07:28 EDT, ok
- `Daily Tasks/Events Call Generator (Zeus+Catthew)` — 08:15 EDT, ok
- `weekday-hermes-vault-summary` — running as of this report (in progress)

Upcoming next runs: watchdog at 18:29 EDT, vault summary at 18:10 EDT, daily health at 09:00 EDT tomorrow.

## Health Signals

**Green:**
- Gateway: running (8 PIDs), all 7 profiles responsive
- MCP: graphify-vault (core/sources/daily) + remarkable all enabled; graphify-hermes disabled (intentional per policy)
- Python/DB: 3.11.15, SQLite WAL, state.db 691.8 MB, 13,138 sessions
- Auth: Nous Portal + xAI OAuth active; refreshable
- Telegram: configured and operational
- Skills Hub: 8 skills installed, lock OK

**Yellow (non-blocking):**
- No API keys in `~/.hermes/.env` — model runs via Nous Portal auth only
- OpenAI Codex not authenticated
- MiniMax OAuth not logged in
- graphify-hermes MCP disabled (by policy — default profile loads all 4 vault graphs)
- 2 npm workspace advisories (build-tool only, not runtime)
- Playwright Chromium not installed (browser_* tools hidden)

**No red signals.** No security advisories. No suspicious MCP commands.

## Next Actions

- `[ ]` Verify `weekday-hermes-vault-summary` completes successfully (in progress at report time)
- `[ ]` Consider setting OpenAI Codex auth if Codex-based models are desired
- `[ ]` Optional: install Playwright Chromium for browser tool access
- `[ ]` Optional: set GITHUB_TOKEN in `.env` to lift 60 req/hr GitHub rate limit

## Related Notes

- `[[Hermes Agent Setup and Operations]]`
- `[[Hermes Operations Dashboard]]`
- `[[Life OS State of Truth]]`
