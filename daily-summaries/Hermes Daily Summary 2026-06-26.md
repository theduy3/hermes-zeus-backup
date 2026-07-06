---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-06-26
updated: 2026-06-26
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
# Hermes Daily Summary 2026-06-26

## Summary
- Live operations check completed from the local container; the summary directory was created and write-tested successfully.
- Core Hermes is running on Python 3.11.15 with model `gpt-5.5` via OpenAI Codex auth.
- Gateway is running manually in Docker with default plus seven profile gateways active.
- Cron automation is active with 14 active jobs and 15 total jobs.
- Doctor reports 2 setup issues: missing API keys for broader provider/tool access.

## What Ran Today
- `date +%F` — returned `2026-06-26` for the local note date.
- `mkdir -p /home/hermes/.hermes/daily-summaries` plus `touch`/`rm` — write check succeeded.
- `hermes status --all` — succeeded; reported gateway running, Telegram configured, 14 active scheduled jobs, and 1 active session.
- `hermes doctor` — succeeded; found no active security advisories and 2 configuration issues related to missing API keys.
- `hermes cron list` — succeeded; listed active jobs including health checks, recaps, vault workflows, backups, wiki ingest/lint, and gateway watchdog.
- `hermes mcp list` — succeeded; no MCP servers are configured.
- `hermes gateway status` — succeeded; gateway is running manually with PIDs for default and profile gateways.

## Health Signals
- Security: no active security advisories; no suspicious MCP stdio commands.
- Runtime: Python 3.11.15, virtual environment active, version files consistent at 0.17.0.
- Auth: OpenAI Codex is logged in; Nous Portal, MiniMax OAuth, xAI OAuth, and Qwen OAuth are not logged in.
- API keys: `.env` exists but no API key was found; many API-key providers are not configured.
- Tooling: core tools are available; browser, computer_use, Discord, web, x_search, spotify, and several runtime-gated tools are unavailable or missing credentials/dependencies.
- Profiles: 7 profiles found and reported as gateway running: butter, catthew, charles, finance, thor, wiki, zeus.
- Cron: `weekday-hermes-vault-summary` last ran ok, but delivery previously failed with Telegram timeout / `send_path_degraded`.
- MCP: no MCP servers configured.
- Gateway: running manually, not installed as a system service in this container.

## Next Actions
- Configure API keys only if broader provider, web, browser, Discord, or X search access is needed.
- Watch the `weekday-hermes-vault-summary` delivery path; prior Telegram timeout may indicate intermittent delivery degradation.
- Decide whether the gateway should remain manually managed in Docker or be installed as a service for this environment.
- Add MCP servers only when a workflow requires them; current state is clean but empty.
- Ensure `/home/hermes/.hermes/daily-summaries/` is covered by any desired backup/sync process, since this task intentionally writes outside the read-only vault.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
