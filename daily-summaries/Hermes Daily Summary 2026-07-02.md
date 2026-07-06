---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-02
updated: 2026-07-02
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
# Hermes Daily Summary 2026-07-02

## Summary
- Hermes is running in the local container with project path `/home/hermes/.hermes/hermes-agent`.
- Active model/provider: `gpt-5.5` via OpenAI Codex OAuth.
- Gateway is healthy and running for the default profile plus 7 named profiles.
- Doctor found 2 configuration issues: missing API keys in `.env` / incomplete API-key setup.

## What Ran Today
- `hermes status` reported 10 active scheduled jobs and 11 total jobs.
- Recent/active jobs include daily health check, weekday recap, weekday vault summary, weekly ops review, nightly GitHub backup, and profile gateway watchdog.
- Travel-context reset jobs are scheduled for July 13 after the Quebec/Montreal trip.
- MCP check ran; no MCP servers are currently configured.

## Health Signals
- Gateway: running manually, not as a system service; PIDs include `65, 32, 37, 42, 47, 52, 57, 62`.
- Profiles: `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, and `zeus` all show gateways running.
- Python environment: OK on Python `3.11.15`; virtual environment active; version files consistent at `0.17.0`.
- Directory structure: OK; state database present with `12896` sessions.
- Disk: `/` overlay is `56%` used with `44G` available.
- Tool availability: core tools available; browser/computer-use/web/x_search and several integrations are gated by missing dependencies or API keys.
- Security: no active security advisories and no suspicious MCP stdio commands reported.

## Next Actions
- Run `hermes setup` when ready to configure missing API keys and unlock full tool access.
- Install `agent-browser` if browser or computer-use tools are needed in this container.
- Add MCP servers only if a current workflow needs them; `hermes mcp list` currently reports none configured.
- Consider installing the gateway as a service if manual foreground gateway management becomes unreliable.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
