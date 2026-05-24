---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-05-22
updated: 2026-05-22
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-05-22

## Summary
- Hermes is up and running with the gateway active and 12 profiles online.
- Core config and environment are healthy, but a few auth/tooling gaps remain.
- Scheduled automation is active, with a small number of job-specific failures to watch.

## What Ran Today
- Checked `hermes status --all` to confirm environment, auth, messaging, gateway, and job counts.
- Ran `hermes doctor` to validate config, packages, paths, tools, and connectivity.
- Reviewed `hermes cron list` for active schedules and recent run outcomes.
- Checked `hermes mcp list` and found no MCP servers configured.
- Verified `hermes gateway status` and confirmed the gateway is running manually.

## Health Signals
- Gateway: running, PID 55, manual foreground process.
- Profiles: 12 total; all shown as running.
- Scheduled jobs: 10 active, 11 total.
- Positive: config files present, venv active, core packages installed, no active security advisories.
- Watchouts:
  - DeepSeek connectivity check reported an invalid API key.
  - No MCP servers are configured.
  - `weekly-hermes-ops-review` last run hit a timeout and Telegram delivery failed with `Unauthorized`.
  - `vault-wiki-lint` last run failed due to missing Codex credentials.

## Next Actions
- Fix or replace the DeepSeek API key in `~/.hermes/.env`.
- Review the Telegram auth state behind the failing cron jobs.
- Re-authenticate Codex credentials for the `vault-wiki-lint` workflow.
- Add MCP servers if they are expected for this deployment.
- Re-run the affected cron jobs after the auth issues are resolved.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
