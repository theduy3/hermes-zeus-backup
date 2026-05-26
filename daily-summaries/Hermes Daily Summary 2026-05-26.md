---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-05-26
updated: 2026-05-26
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-05-26

## Summary

- Hermes default profile is running on Python 3.11.15 with model `gpt-5.5` via OpenAI Codex auth.
- Gateway is healthy and running in foreground Docker mode with PID 35.
- Doctor reports no active security advisories and core dependencies are installed.
- Main issues are configuration hygiene: outdated config version, missing API keys for optional providers/tools, and browser automation dependencies not installed.

## What Ran Today

- Active scheduled jobs: 10 active, 11 total.
- Recent successful jobs include `daily-hermes-health-check`, `weekday-hermes-recap`, `weekly-hermes-ops-review`, `nightly-hermes-github-backup`, `vault-today`, `vault-process`, `vault-wiki-lint`, and `vault-tonight`.
- `weekday-hermes-vault-summary` is active and last reported OK on 2026-05-22.
- `vault-wiki-ingest` last failed with `RuntimeError: HTTP 429: The usage limit has been reached`.

## Health Signals

- Gateway: running; default PID 35.
- Other profile gateways: `butter`, `catthew`, `charles`, `finance`, `thor`, and `zeus` are running.
- Auth: OpenAI Codex logged in; Google Gemini OAuth logged in; Nous Portal, MiniMax OAuth, and xAI OAuth are not logged in.
- MCP: no MCP servers configured.
- Tooling: terminal, cronjob, file, memory, skills, todo, session search, vision, TTS, image/video, Feishu, and delegation tools available.
- Degraded tools: browser/browser-cdp/computer-use unavailable because Playwright Chromium is not installed; web/x_search/MOA/Discord/Spotify/Yuanbao gated by missing dependencies or credentials.
- Disk: root overlay filesystem at 60% used, with 79G available.

## Next Actions

- Run `hermes doctor --fix` or `hermes setup` to migrate config from v23 to v24.
- Configure API keys only for providers/tools that are actually needed; current Codex auth is sufficient for this run.
- Install Playwright Chromium if browser automation is needed: `cd /home/hermes/.hermes/hermes-agent && npx playwright install --with-deps chromium`.
- Investigate `vault-wiki-ingest` HTTP 429 before the next scheduled ingest window.
- Add MCP servers only if the Obsidian or external-tool workflows need MCP access.

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
