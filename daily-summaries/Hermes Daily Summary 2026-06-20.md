---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-06-20
updated: 2026-06-20
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-06-20

## Summary
- Hermes is running on Python 3.11.15 with model `gpt-5.5` via OpenAI Codex auth.
- Gateway is healthy and running manually in Docker foreground mode.
- Doctor completed successfully but reports 4 action items: missing API keys, outdated config version, one UI TUI npm vulnerability, and incomplete provider setup.
- Scheduler shows 12 active jobs and 13 total jobs.

## What Ran Today
- Checked live Hermes status with `hermes status`.
- Ran diagnostics with `hermes doctor`.
- Reviewed scheduled automation with `hermes cron list`.
- Checked MCP configuration with `hermes mcp list`.
- Verified gateway runtime with `hermes gateway status`.
- Confirmed local summary output directory is writable: `/home/hermes/.hermes/daily-summaries/`.

## Health Signals
- Gateway: running, PID set includes default plus profile gateways.
- Profiles: `butter`, `catthew`, `charles`, `finance`, `thor`, and `zeus` gateways are running.
- Auth: OpenAI Codex is logged in; Google Gemini OAuth is logged in per doctor output.
- API keys: no API keys found in `~/.hermes/.env`; several optional providers/tools are unavailable because keys are missing.
- Config: doctor reports config version outdated from v29 to v30.
- MCP: no MCP servers configured.
- Disk: root overlay filesystem is 68% used with about 64G available.
- Security: no active security advisories and no suspicious MCP stdio commands.

## Next Actions
- Run `hermes doctor --fix` or `hermes setup` to migrate config from v29 to v30.
- Configure desired API keys if web, browser-adjacent, X search, Discord, or other optional tools are needed.
- Review the UI TUI lockfile/vulnerability item when doing the next maintenance pass.
- Add MCP servers only if an active workflow needs them; current state is clean but unconfigured.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
