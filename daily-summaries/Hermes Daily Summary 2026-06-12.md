---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-06-12
updated: 2026-06-12
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
# Hermes Daily Summary 2026-06-12

## Summary
- Generated from live Hermes operations checks on 2026-06-12.
- Local summary path is writable: `/home/hermes/.hermes/daily-summaries/`.
- Gateway is running and scheduled jobs are active.
- Doctor found 5 issues: missing API-key setup, outdated config version, and npm vulnerabilities in `web` and `ui-tui` workspaces.

## What Ran Today
- `daily-hermes-health-check` last ran 2026-06-12 09:00 EDT: ok.
- `weekday-hermes-recap` last ran 2026-06-12 18:02 EDT: ok.
- `nightly-hermes-github-backup` last ran 2026-06-12 05:01 EDT: ok.
- Vault jobs ran today: `vault-today`, `vault-process`, `vault-wiki-ingest`, `vault-wiki-lint`, and `vault-tonight`.
- Profile gateway watchdog last ran 2026-06-12 18:09 EDT: ok.
- Cron inventory reports 11 active jobs, 12 total.

## Health Signals
- `hermes status`: ok; project at `/home/hermes/.hermes/hermes-agent`, Python 3.11.15, model `gpt-5.5` via OpenAI Codex.
- `hermes status`: gateway running under docker/foreground with PID 4089.
- `hermes status`: Telegram configured; Discord/Slack/email/SMS and several other messaging platforms not configured.
- `hermes doctor`: Python environment, required packages, directory structure, command installation, skills hub, and built-in memory are healthy.
- `hermes doctor`: warnings for no API key in `.env`, config version outdated v27 → v29, missing optional provider auth, and npm audit issues.
- `hermes mcp list`: no MCP servers configured.
- `hermes gateway status`: default gateway running at PID 4089; profile gateways running for butter, catthew, charles, finance, thor, and zeus.

## Next Actions
- Run `hermes doctor --fix` or `hermes setup` to migrate config from v27 to v29.
- Add API keys in `~/.hermes/.env` if full provider/tool access is required beyond OpenAI Codex and configured OAuth providers.
- Review npm vulnerabilities: `cd /home/hermes/.hermes/hermes-agent && npm audit fix --workspace web` and `npm audit fix --workspace ui-tui`.
- Decide whether MCP servers should remain unconfigured; if not, add required servers with `hermes mcp add`.
- Continue monitoring cron jobs and profile gateway watchdog runs.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
