---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-06-18
updated: 2026-06-18
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-06-18

## Summary
- Daily operations check completed from live Hermes CLI state.
- Core Hermes is running on Python 3.11.15 with model `gpt-5.5` via OpenAI Codex auth.
- Gateway is running manually in Docker/foreground mode across default plus six named profiles.
- Main risks: outdated config version, missing optional API keys/tool credentials, no MCP servers, and one cron job with a recent auth failure.

## What Ran Today
- Checked `hermes status --all` successfully.
- Checked `hermes doctor` successfully.
- Checked `hermes cron list` successfully.
- Checked `hermes mcp list` successfully.
- Checked `hermes gateway status` successfully.

## Health Signals
- `hermes status --all`: environment OK; project at `/home/hermes/.hermes/hermes-agent`; `.env` exists; provider is OpenAI Codex.
- API/auth: OpenAI Codex is logged in; many API-key providers are not configured; Telegram is configured.
- Gateway: running manually with PIDs `59, 31, 36, 41, 47, 52, 56`.
- Profiles: `butter`, `catthew`, `charles`, `finance`, `thor`, and `zeus` gateways are running.
- Cron: 11 active jobs, 12 total jobs.
- Cron warning: `weekday-hermes-vault-summary` last run failed with `401 unauthorized_unknown` / authentication token parse error.
- Doctor: no security advisories; Python/package basics healthy; config version is outdated `v29 → v30`.
- Tool availability: core tools are available; browser, Discord, web, x_search, spotify, and several optional toolsets are missing credentials or dependencies.
- MCP: no MCP servers are configured.

## Next Actions
- Run `hermes doctor --fix` or `hermes setup` to migrate config from v29 to v30.
- Re-authenticate or inspect the credential path used by `weekday-hermes-vault-summary` after its `401 unauthorized_unknown` failure.
- Configure only the optional API keys/tool backends that are actually needed, especially web/search credentials if cron jobs depend on live web data.
- Add MCP servers only if current workflows need them; current state is explicitly `No MCP servers configured`.
- Keep monitoring gateway/manual Docker foreground mode and profile gateway PIDs.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
