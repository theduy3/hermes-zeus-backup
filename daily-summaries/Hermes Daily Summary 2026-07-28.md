---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-28
updated: 2026-07-28
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
# Hermes Daily Summary 2026-07-28

## Summary
- Live operations checks completed for Hermes status, doctor, cron, MCP, and gateway.
- Summary written to the local container path, not the read-only vault.
- Core gateway and all named profile gateways are running.
- Attention needed: doctor reports 4 issues; graphify daily refresh failed with SIGKILL; one vault-summary delivery previously failed via Telegram Bad Gateway/timeout.

## What Ran Today
- `hermes status` exited 0.
- `hermes doctor` exited 0.
- `hermes cron list` exited 0.
- `hermes mcp list` exited 0.
- `hermes gateway status` exited 0.

## Health Signals
- **Environment:** project `/home/hermes/.hermes/hermes-agent`; Python 3.11.15; model `gpt-5.5`; provider OpenAI Codex.
- **Auth:** OpenAI Codex logged in; no API keys configured in `.env`; Nous Portal, MiniMax OAuth, and xAI OAuth not logged in.
- **Gateway:** running with PIDs `97, 51, 59, 69, 76, 78, 86, 93`; profiles `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, and `zeus` all running.
- **Cron:** 7 active jobs, 8 total; recent completed jobs include health check, recap, weekly ops review, backup, and gateway watchdog.
- **Cron warning:** `weekday-hermes-vault-summary` shows a running execution from 2026-07-24 and delivery failure: Telegram Bad Gateway/timeout.
- **Cron error:** `graphify-daily-refresh` last run failed; `graphify extract` died with `SIGKILL: 9`.
- **MCP:** 5 enabled Graphify MCP servers: `graphify-hermes`, `graphify-vault`, `graphify-vault-core`, `graphify-vault-sources`, `graphify-vault-daily`.
- **Doctor issues:** missing API keys, web workspace npm vulnerabilities, ui-tui workspace npm vulnerabilities, missing API keys for full tool access.
- **Tool availability:** core tools are available; browser/computer-use/web/x_search and several integrations are gated by missing dependencies or keys.

## Next Actions
- Investigate `graphify-daily-refresh` SIGKILL; likely reduce `graphify extract --max-workers` or resource usage before next scheduled run.
- Inspect/clear stale `weekday-hermes-vault-summary` running execution and confirm Telegram delivery path is healthy.
- Run targeted dependency remediation or lockfile bump for web/ui-tui npm advisories when maintenance window is available.
- Keep OpenAI Codex auth as primary auth path; missing non-OpenAI providers are expected unless explicitly needed.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]

## Raw Command Output

### `hermes status`
```text
Environment: Project /home/hermes/.hermes/hermes-agent; Python 3.11.15; .env exists; Model gpt-5.5; Provider OpenAI Codex.
Auth: OpenAI Codex logged in; other providers not logged in/configured.
Gateway Service: running; docker foreground; PIDs 97, 51, 59, ...
Scheduled Jobs: 7 active, 8 total.
Sessions: 1 active session.
```

### `hermes doctor`
```text
Security advisories: no active advisories.
Python: 3.11.15; SQLite 3.53.1; virtualenv active; version files consistent 0.19.0.
Configuration: ~/.hermes/.env exists; no API key found; config v33 up to date.
Profiles: butter, catthew, charles, finance, thor, wiki, zeus gateways running.
Issues: configure API keys; web workspace has 8 npm vulnerabilities; ui-tui workspace has 7 npm vulnerabilities; configure missing API keys for full tool access.
```

### `hermes cron list`
```text
Active jobs: daily-hermes-health-check, weekday-hermes-recap, weekly-hermes-ops-review, weekday-hermes-vault-summary, nightly-hermes-github-backup, Hermes profile gateway watchdog, graphify-daily-refresh.
Recent ok: daily health check, weekday recap, weekly ops review, nightly backup, gateway watchdog.
Warning: weekday-hermes-vault-summary delivery failed via Telegram Bad Gateway/timeout and shows execution running from 2026-07-24.
Error: graphify-daily-refresh exited code 1; graphify extract died with SIGKILL: 9.
```

### `hermes mcp list`
```text
Enabled MCP servers: graphify-hermes, graphify-vault, graphify-vault-core, graphify-vault-sources, graphify-vault-daily.
```

### `hermes gateway status`
```text
Gateway running: PID 97, 51, 59, 69, 76, 78, 86, 93.
Other profiles running: butter, catthew, charles, finance, thor, wiki, zeus.
Running manually, not as a system service.
```
