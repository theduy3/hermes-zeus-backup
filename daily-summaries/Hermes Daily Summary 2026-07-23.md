---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-23
updated: 2026-07-23
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-07-23

## Summary
- Hermes default profile is running on Python 3.11.15 with model `gpt-5.5` via OpenAI Codex.
- Gateway is running manually in Docker/foreground mode.
- Doctor reports no security advisories and no active MCP servers.
- Main issues: missing API keys in `~/.hermes/.env`; several optional tool integrations unavailable.

## What Ran Today
- Active cron jobs: 6 active, 7 total.
- `daily-hermes-health-check`: last run 2026-07-22 09:01 PDT, ok; next 2026-07-23 09:00 PDT.
- `weekday-hermes-recap`: last run 2026-07-22 18:03 PDT, ok; next 2026-07-23 18:00 PDT.
- `weekly-hermes-ops-review`: last run 2026-07-20 09:18 PDT, ok; next 2026-07-27 09:15 PDT.
- `weekday-hermes-vault-summary`: currently running; next 2026-07-23 18:10 PDT.
- `nightly-hermes-github-backup`: last run 2026-07-22 00:01 PDT, ok; next 2026-07-23 00:00 PDT.
- `Hermes profile gateway watchdog`: last run 2026-07-22 18:03 PDT, ok; next 2026-07-22 18:33 PDT.

## Health Signals
- Security advisories: none active.
- Python environment: healthy; virtualenv active; Hermes version files consistent at 0.19.0.
- Required packages: present.
- Config: `~/.hermes/config.yaml` exists and is up to date at v33.
- Auth: OpenAI Codex logged in; Nous Portal, MiniMax OAuth, and xAI OAuth not logged in.
- Gateway: running with PIDs 75, 42, 48, 53, 57, 63, 68, 74.
- Profiles: butter, catthew, charles, finance, thor, wiki, and zeus gateways all running.
- MCP: no MCP servers configured.
- Tool gaps: browser/computer-use/image/video/Spotify/web/x_search and Discord-related integrations unavailable due to missing dependencies or credentials.

## Next Actions
- Decide whether missing API keys are expected for this OpenAI-Codex-only setup; if not, run `hermes setup`.
- Review the currently running `weekday-hermes-vault-summary` execution if it remains active unexpectedly.
- Configure MCP servers only if needed; current state is intentionally empty.
- Keep profile gateway watchdog active to maintain named profile gateways.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
