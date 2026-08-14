---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-30
updated: 2026-07-30
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
# Hermes Daily Summary 2026-07-30

## Summary
- Local container operations snapshot generated from live Hermes state.
- Core Hermes CLI, doctor, cron, MCP, and gateway checks completed.
- Gateway is running; OpenAI Codex auth is logged in; scheduled jobs are mostly healthy.
- Main issue today: `graphify-daily-refresh` failed with SIGKILL during `graphify extract`.

## What Ran Today
- `hermes status` — OK.
- `hermes doctor` — OK, with 3 advisory issues reported.
- `hermes cron list` — OK; listed 7 active jobs, 8 total.
- `hermes mcp list` — OK; Graphify MCP servers enabled.
- `hermes gateway status` — OK; default and profile gateways running.

## Health Signals
- **Environment**
  - Project: `/home/hermes/.hermes/hermes-agent`.
  - Python: 3.11.15.
  - Model/provider: `gpt-5.5` via OpenAI Codex.
  - `.env` exists, but no API keys detected.
- **Authentication**
  - OpenAI Codex logged in via `/home/hermes/.hermes/auth.json`.
  - Nous Portal, MiniMax OAuth, and xAI OAuth not logged in.
- **Doctor**
  - No active security advisories.
  - No suspicious MCP stdio commands.
  - Version files consistent at 0.19.0.
  - Tool availability mostly healthy; browser/computer-use/web/x_search unavailable due to missing dependencies or keys.
  - Doctor advisories: configure API keys, resolve ui-tui npm vulnerabilities, configure missing API keys for full tool access.
- **Cron**
  - `daily-hermes-health-check` last run OK on 2026-07-29.
  - `weekday-hermes-recap` last run OK on 2026-07-29.
  - `weekly-hermes-ops-review` last run OK on 2026-07-27.
  - `weekday-hermes-vault-summary` currently shows running execution `a5faf7d1381441c0829b0c8e1d5322b9`.
  - `nightly-hermes-github-backup` last run OK on 2026-07-29.
  - `Hermes profile gateway watchdog` last run OK on 2026-07-29.
  - `graphify-daily-refresh` last run failed on 2026-07-29: `graphify extract` was killed by SIGKILL.
- **MCP**
  - Enabled: `graphify-hermes`, `graphify-vault`, `graphify-vault-core`, `graphify-vault-sources`, `graphify-vault-daily`.
- **Gateway**
  - Gateway running manually, not as a system service.
  - Default gateway PIDs include 97, 51, 59, 69, 76, 78, 86, 93.
  - Profile gateways running: butter, catthew, charles, finance, thor, wiki, zeus.

## Next Actions
- Investigate `graphify-daily-refresh` SIGKILL; likely resource pressure during full extraction.
- Consider reducing Graphify extraction workers below 4 or adding memory/swap before next scheduled refresh.
- Review `weekday-hermes-vault-summary` if it remains running longer than expected.
- Optionally run `hermes doctor --fix` for auto-fixable doctor advisories.
- Leave non-OpenAI providers unconfigured unless the user explicitly changes provider preferences.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
