---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-08-06
updated: 2026-08-06
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary — 2026-08-06

## Summary
- Hermes is operational on OpenAI Codex (`gpt-5.5`); gateway and seven profile gateways are running.
- Doctor found no active security advisories and verified the Python environment, configuration, certificates, and required packages.
- Main operational concerns: repeated Telegram delivery failures and yesterday's failed Graphify refresh.

## What Ran Today
- `hermes status`: gateway running; 7 active scheduled jobs of 8 total; 1 active session.
- `hermes doctor`: completed with 5 non-blocking issues reported.
- `hermes cron list`: confirmed daily health, weekday recap, ops review, vault summary, backup, watchdog, and Graphify refresh schedules.
- `hermes mcp list`: five Graphify MCP servers enabled.
- `hermes gateway status`: default gateway plus butter, catthew, charles, finance, thor, wiki, and zeus gateways running.

## Health Signals
- Healthy: no security advisories; MCP stdio commands clean; virtual environment and configuration version (`0.19.1`) consistent.
- Healthy: OpenAI Codex authentication is active; Telegram is configured.
- Warning: no API key in `.env`; OpenAI Codex OAuth remains usable.
- Warning: `agent-browser` is not installed; browser/web/UI workspace dependency audits report high-severity build-tool vulnerabilities.
- Warning: several completed cron runs could not deliver to Telegram (`Unauthorized`); the vault-summary run previously reported `Bad Gateway`.
- Failure: `graphify-daily-refresh` last ran 2026-08-05 and exited 1 after `graphify extract` was killed by `SIGKILL` during AST extraction.

## Next Actions
- Repair Telegram credentials/delivery configuration for origin-delivered cron reports.
- Investigate Graphify extraction resource limits; retry with fewer workers or reduced extraction scope.
- Install/configure browser tooling only if browser automation is required; remediate reported npm dependency advisories.
- Add required API keys only where OAuth does not cover the intended integration.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[Graphify]]
- [[Scheduled Jobs]]
