---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-06-19
updated: 2026-06-19
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
# Hermes Daily Summary 2026-06-19

## Summary
- Daily Hermes operations check completed from the live container state.
- Core runtime is online: Hermes uses Python 3.11.15, model `gpt-5.5`, provider OpenAI Codex, and the gateway is running.
- Main issues to track: outdated config version, missing API keys for optional providers/tools, one `ui-tui` npm vulnerability, no MCP servers configured.

## What Ran Today
- `hermes status --all` → exit 0.
- `hermes doctor` → exit 0.
- `hermes cron list` → exit 0.
- `hermes mcp list` → exit 0.
- `hermes gateway status` → exit 0.

## Health Signals
- **Environment:** Project at `/home/hermes/.hermes/hermes-agent`; Python 3.11.15; `.env` exists; model `gpt-5.5`; provider OpenAI Codex.
- **Authentication:** OpenAI Codex is logged in; Nous Portal, Qwen OAuth, MiniMax OAuth, xAI OAuth, and API-key providers are not configured.
- **Doctor:** No active security advisories; Python, required packages, directories, command installation, built-in memory, and six profile gateways are healthy.
- **Doctor issues:** No API key in `~/.hermes/.env`; config version is outdated (`v29 → v30`); `ui-tui` workspace has one high npm vulnerability; some optional tools are unavailable due to missing credentials/system dependencies.
- **Cron:** 12 active jobs, 13 total; visible active jobs include health checks, weekday recaps, vault workflows, GitHub backup, profile gateway watchdog, and a scheduled travel timezone switch-back.
- **MCP:** No MCP servers configured.
- **Gateway:** Gateway is running manually, not as a system service; default plus `butter`, `catthew`, `charles`, `finance`, `thor`, and `zeus` profile processes are active.

## Next Actions
- Run `hermes doctor --fix` or `hermes setup` to migrate the config from v29 to v30.
- Decide whether optional API keys/tool credentials are needed; leave them unset if those providers/tools are intentionally unused.
- Address or accept the `ui-tui` workspace npm vulnerability based on whether that build tooling matters in this deployment.
- Add MCP servers only if current workflows need MCP integration.
- Consider installing the gateway as a service if manual foreground Docker supervision is not the desired steady state.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
