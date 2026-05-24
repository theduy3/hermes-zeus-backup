---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-05-23
updated: 2026-05-23
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-05-23

## Summary
- Hermes is up and operational: gateway running, config loaded, and the main environment is healthy.
- Core scheduling is active with 10 jobs running out of 11 total.
- The main gaps are API/tooling coverage, DeepSeek key validity, and MCP server setup.

## What Ran Today
- Checked live Hermes status (`hermes status --all`): project path, model, provider, gateway, scheduled jobs, sessions.
- Ran health diagnostics (`hermes doctor`): config and environment mostly healthy, with a few auth/tooling warnings.
- Listed scheduled jobs (`hermes cron list`): daily, weekday, weekly, vault, and backup jobs are present and active.
- Listed MCP servers (`hermes mcp list`): no MCP servers are configured.
- Checked gateway state (`hermes gateway status`): main gateway is running, and profile gateways are up as well.

## Health Signals
- Good: Python 3.11.15, virtualenv active, config present, config version up to date, no active security advisories.
- Good: OpenAI Codex auth is logged in; Google Gemini OAuth is also logged in.
- Good: gateway is running manually with PID 36362; all listed profile gateways are running.
- Warning: DeepSeek connectivity check reported an invalid API key.
- Warning: web tool access is unavailable because required keys are missing.
- Warning: MCP is not configured at all.
- Warning: several optional providers/platforms remain unconfigured, including Discord and xAI OAuth.
- Warning: `weekly-hermes-ops-review` last run errored with a timeout and Telegram delivery authorization failure.

## Next Actions
- Fix or replace the DeepSeek API key so connectivity checks pass.
- Add at least one MCP server if any workflow depends on MCP-backed tools.
- Review the failed weekly ops review delivery path and Telegram auth.
- If web browsing is needed, configure one of the required web providers/keys.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[Hermes Daily Summary 2026-05-23]]
