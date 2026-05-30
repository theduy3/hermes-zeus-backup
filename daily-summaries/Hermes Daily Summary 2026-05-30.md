---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-05-30
updated: 2026-05-30
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-05-30

## Summary

- Hermes is running on Python 3.11.15 with active profile `default` using model `gpt-5.5` via OpenAI Codex auth.
- Gateway is healthy and running in Docker/manual foreground mode with PID 37.
- Scheduler reports 10 active jobs out of 11 total.
- Doctor found 2 configuration issues, both related to missing API keys / incomplete provider setup.
- MCP has no servers configured.

## What Ran Today

- Live cron registry is available and lists 10 active jobs.
- Recent successful runs visible in cron state:
  - `daily-hermes-health-check` last ran ok at 2026-05-29 09:01 -07:00.
  - `nightly-hermes-github-backup` last ran ok at 2026-05-29 05:01 -07:00.
  - Vault automation jobs (`vault-today`, `vault-process`, `vault-wiki-ingest`, `vault-wiki-lint`, `vault-tonight`) show last successful runs on 2026-05-29.
  - Weekday recap jobs show successful weekday runs, with next weekday executions scheduled for 2026-06-01.
- Upcoming scheduled jobs include `vault-wiki-lint`, `vault-today`, `nightly-hermes-github-backup`, `daily-hermes-health-check`, and `vault-process`.

## Health Signals

- Positive:
  - Gateway status: running.
  - Python environment and required packages: healthy.
  - Core directory structure and state database: present.
  - Command installation: `~/.local/bin/hermes` points to the correct venv entry point.
  - OpenAI Codex auth: logged in; auth refreshed 2026-05-27 03:31:57 UTC.
  - Google Gemini OAuth: logged in.
  - Security advisories: none active.
- Warnings:
  - No API key found in `~/.hermes/.env`.
  - Several optional providers/toolsets are unavailable because credentials or system dependencies are missing.
  - Browser, browser-cdp, and computer-use tools are unavailable because Playwright Chromium is not installed.
  - Web and x_search toolsets are unavailable due to missing search/API credentials.
  - No MCP servers configured.

## Next Actions

- Run `hermes setup` when broader provider/API-key coverage is desired.
- Install Playwright Chromium if browser automation is needed: `cd /home/hermes/.hermes/hermes-agent && npx playwright install --with-deps chromium`.
- Add MCP servers only if upcoming workflows need them; current state is clean but empty.
- Continue monitoring cron runs for weekend vault automation and weekday recap jobs.

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
