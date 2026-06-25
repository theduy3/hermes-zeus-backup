---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-06-23
updated: 2026-06-23
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-06-23

## Summary

- Hermes is running in the local container as user `hermes` with home `/home/hermes`.
- Daily summary target `/home/hermes/.hermes/daily-summaries/` was created/tested writable before this note was written.
- Primary gateway is running in Docker/foreground mode; all named profile gateways reported running.
- `hermes doctor` found no security advisories and confirmed core environment health, with two configuration issues around missing API keys.

## What Ran Today

- Checked live local date: `2026-06-23`.
- Verified runtime identity: `uid=1500(hermes) gid=1500(hermes)`.
- Ran `hermes status`:
  - Project: `/home/hermes/.hermes/hermes-agent`.
  - Python: `3.11.15`.
  - Active model/provider: `gpt-5.5` via OpenAI Codex.
  - Gateway service: running.
  - Scheduled jobs: `14 active`, `15 total`.
  - Active sessions: `1`.
- Ran `hermes doctor`:
  - Python, virtualenv, version files, CA bundle, required packages, config, directory structure, command installation, memory provider, and skills hub are healthy.
  - OpenAI Codex auth is logged in; Google Gemini OAuth is logged in.
  - Nous Portal, MiniMax OAuth, and xAI OAuth are not logged in.
- Ran `hermes cron list`:
  - Active jobs include health checks, recaps, GitHub backup, vault workflows, wiki ingest/lint, tonight/today routines, profile gateway watchdog, and travel-context reset jobs.
  - Recent listed runs from 2026-06-22 generally reported `ok`.
- Ran `hermes mcp list`:
  - No MCP servers are currently configured.
- Ran `hermes gateway status`:
  - Main gateway and profile gateways are running manually, not as system services.

## Health Signals

- ✅ Gateway running with PIDs reported for default and profiles: `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, `zeus`.
- ✅ Doctor reports no active security advisories.
- ✅ Core Python and Hermes environment checks pass.
- ✅ Required packages are installed; optional Telegram and Discord Python packages are present.
- ✅ Disk has available space: `/home/hermes/.hermes` is 51% used with 49G available.
- ⚠️ No API key found in `~/.hermes/.env`; doctor recommends `hermes setup` for full API-key configuration.
- ⚠️ Several optional toolsets/providers are unavailable due to missing keys or system dependencies, including web search API keys, browser dependencies, Discord token, x_search key, and Spotify dependency.
- ⚠️ No MCP servers configured; this is acceptable if MCP integrations are not expected for this container.
- ⚠️ Gateway is running manually rather than as an installed service.

## Next Actions

- Consider running `hermes setup` if broader API-key-backed tools are needed.
- Decide whether to configure MCP servers; `hermes mcp add ...` is available if needed.
- Consider installing the gateway as a service if persistent process supervision is desired.
- Keep monitoring scheduled jobs, especially vault-related workflows, because cron containers may not inherit vault mounts.
- Maintain local daily summaries under `/home/hermes/.hermes/daily-summaries/` when the requirement is explicitly to avoid writing to the read-only vault.

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
