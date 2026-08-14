---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-25
updated: 2026-07-25
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-07-25

## Summary

- Hermes is running on Linux with Python 3.11.15 and Hermes Agent 0.19.0.
- Active model/provider: `gpt-5.5` via OpenAI Codex OAuth.
- Gateway is healthy and running manually inside Docker/container foreground mode.
- Cron scheduler shows 6 active jobs and 7 total jobs.
- No MCP servers are configured for the default profile.
- Doctor found 4 non-blocking issues: missing API keys, npm vulnerability advisories in web/ui-tui workspaces, and reduced tool access for unconfigured providers.

## What Ran Today

- Checked `hermes status`: environment, auth, gateway, sessions, and cron state loaded successfully.
- Checked `hermes doctor`: no active security advisories; Python, version files, config, directories, and built-in tools are healthy.
- Checked `hermes cron list`: scheduled jobs are visible and mostly reporting successful prior runs.
- Checked `hermes mcp list`: no MCP servers configured.
- Checked `hermes gateway status`: default gateway plus profile gateways are running.
- Checked disk/process health: `/home/hermes/.hermes` has 28G available on a 99G filesystem, 72% used.

## Health Signals

- Healthy: OpenAI Codex auth is logged in; `/home/hermes/.hermes/auth.json` exists and was refreshed 2026-07-17 UTC.
- Healthy: Telegram is configured; Discord, WhatsApp, Slack, email, and other messaging platforms are not configured.
- Healthy: gateway PID set includes default plus profiles `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, and `zeus`.
- Healthy: all 7 named profiles report gateway running on `gpt-5.5`.
- Healthy: required Python packages and core Hermes directories exist.
- Warning: no API key found in `~/.hermes/.env`; current operation relies on OAuth where available.
- Warning: Nous Portal, MiniMax OAuth, xAI OAuth, Qwen OAuth, and API-key providers are not logged in/configured.
- Warning: browser/computer-use/image/video/Spotify/web/x_search-style tools remain unavailable because dependencies or API keys are missing.
- Warning: web workspace has 8 high npm advisories and ui-tui workspace has 7 high npm advisories, described by doctor as build-tool/lockfile-related.
- Watch: `weekday-hermes-vault-summary` shows an older running execution ID `702609a2eae6408c8a2bd46845a6cf38`; review if it remains stuck.

## Next Actions

- Review whether the old `weekday-hermes-vault-summary` running execution is stale and cancel/restart if needed.
- Keep OpenAI Codex OAuth as primary auth; add API keys only if specific missing tools are needed.
- Run `hermes doctor --fix` only for safe automated repairs after confirming intended changes.
- Consider lockfile refresh/remediation for web and ui-tui npm advisories.
- Leave MCP unconfigured unless a current workflow requires a default-profile MCP server.

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
