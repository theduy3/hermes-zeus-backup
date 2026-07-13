---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-10
updated: 2026-07-10
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
# Hermes Daily Summary 2026-07-10

## Summary
- Generated from live Hermes checks on 2026-07-10.
- Hermes is running on Python 3.11.15 with model `gpt-5.5` via OpenAI Codex auth.
- Gateway is running manually in Docker/foreground mode across the default profile and seven named profiles.
- Doctor found two configuration issues: missing API keys in `.env` and missing API keys for full tool access.

## What Ran Today
- Scheduled jobs: 7 active, 8 total.
- `daily-hermes-health-check`: last run 2026-07-09 09:01 - ok; next run 2026-07-10 09:00 PDT.
- `weekday-hermes-recap`: last run 2026-07-09 18:01 - ok; next run 2026-07-10 18:00 PDT.
- `weekday-hermes-vault-summary`: last run 2026-07-08 18:12 - ok; next run 2026-07-10 18:10 PDT; uses `obsidian` skill.
- `nightly-hermes-github-backup`: last run 2026-07-09 00:01 - ok; next run 2026-07-10 00:00 PDT.
- `weekly-hermes-ops-review`: last run 2026-07-06 09:18 - ok; next run 2026-07-13 09:15 EDT.
- `Hermes profile gateway watchdog`: last run 2026-07-09 18:02 - ok; runs every 30 minutes.
- `Silent Vancouver return travel-context reset`: one-shot scheduled for 2026-07-13 07:15 UTC.

## Health Signals
- `hermes status`: OK; `.env` exists; GitHub token configured; OpenAI Codex auth logged in; Telegram configured.
- `hermes doctor`: OK overall with warnings; no active security advisories; Python, venv, packages, config, directories, skills hub, and memory provider healthy.
- API keys: most direct provider API keys are not set; this limits full tool access but current model auth works through OpenAI Codex.
- Tool availability: core tools available; browser/computer-use and several third-party integrations are unavailable due to missing system dependencies or tokens.
- MCP: `hermes mcp list` reports no MCP servers configured.
- Gateway: running manually with PIDs 65, 32, 37, 42, 47, 52, 57, 62.
- Profiles: `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, and `zeus` gateways are all running.
- Disk: `/` overlay is 64% used with 36G available.

## Next Actions
- Run `hermes setup` when full provider/tool access is needed; doctor specifically flags missing API keys.
- Configure MCP servers only if an MCP-backed workflow is expected; current state has none configured.
- Consider installing/configuring browser/computer-use dependencies if GUI/browser automation is needed.
- Continue monitoring gateway watchdog and scheduled jobs; recent cron entries report successful last runs.
- Keep these generated daily summaries in `/home/hermes/.hermes/daily-summaries/` as requested, not in the read-only vault.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
