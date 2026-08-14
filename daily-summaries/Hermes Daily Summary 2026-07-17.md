---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-17
updated: 2026-07-17
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
# Hermes Daily Summary 2026-07-17

## Summary
- Daily Hermes operations check completed from the local container on `Fri Jul 17 01:10:55 UTC 2026`.
- Note written to local container storage, not the read-only vault.
- Hermes gateway is running; default profile is on `gpt-5.5` via OpenAI Codex auth.
- Doctor found 2 configuration issues, both related to missing API keys/full tool access.

## What Ran Today
- `hermes status` completed successfully.
  - Project: `/home/hermes/.hermes/hermes-agent`
  - Python: `3.11.15`
  - `.env` file exists.
  - Gateway service is running under Docker/foreground.
  - Scheduled jobs: `6 active, 7 total`.
  - Active sessions: `1`.
- `hermes doctor` completed successfully.
  - No active security advisories.
  - Python environment, virtualenv, package checks, directory structure, command installation, and memory provider passed.
  - Profiles found: `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, `zeus`; all reported gateway running.
- `hermes cron list` completed successfully.
  - `daily-hermes-health-check`: last run `2026-07-16T09:01:06.466538-07:00`, ok; next run `2026-07-17T09:00:00-07:00`.
  - `weekday-hermes-recap`: last run `2026-07-16T18:01:52.514378-07:00`, ok; next run `2026-07-17T18:00:00-07:00`.
  - `weekly-hermes-ops-review`: last run `2026-07-13T09:18:57.950753-07:00`, ok; next run `2026-07-20T09:15:00-07:00`.
  - `weekday-hermes-vault-summary`: last run `2026-07-15T18:11:58.904270-07:00`, ok; next run `2026-07-17T18:10:00-07:00`.
  - `nightly-hermes-github-backup`: last run `2026-07-16T00:02:46.591907-07:00`, ok; next run `2026-07-17T00:00:00-07:00`.
  - `Hermes profile gateway watchdog`: last run `2026-07-16T17:48:13.970068-07:00`, ok; next run `2026-07-16T18:18:13.970068-07:00`.
- `hermes mcp list` completed successfully.
  - No MCP servers configured.
- `hermes gateway status` completed successfully.
  - Default gateway running with PIDs `74, 40, 46, 51, 55, 60, 65, 70`.
  - Other profile gateways running: `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, `zeus`.

## Health Signals
- Gateway: healthy; running manually, not as a system service.
- Doctor: mostly healthy, with warnings for missing API keys and unavailable optional tools.
- Auth: OpenAI Codex is logged in; Nous Portal, Qwen OAuth, MiniMax OAuth, and xAI OAuth are not logged in/configured.
- API keys: no API key found in `~/.hermes/.env`; many API-key providers are unset.
- Tool availability: core tools available, including terminal, file, memory, skills, delegation, session search, todo, TTS, video, and vision.
- Optional tool gaps: browser/computer-use dependencies, Discord token, web search API keys, X search key, Spotify, image/video generation, Home Assistant, and related integrations are unavailable.
- MCP: no servers configured.
- Disk: `/home/hermes` and `/tmp` are on overlay filesystem, `99G` total, `65G` used, `35G` available, `65%` usage.
- Security: no active security advisories; no suspicious MCP stdio commands.

## Next Actions
- Configure API keys with `hermes setup` if full web/API tool access is needed.
- Install or enable optional browser/computer-use dependencies only if those workflows are required.
- Add MCP servers only when a concrete integration needs them.
- Consider installing the gateway as a service if manual foreground operation becomes unreliable.
- Review cron timing because one listed next run (`Hermes profile gateway watchdog`) appears earlier than the live UTC check time, which may indicate scheduler display/timezone nuance or stale listing output.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
