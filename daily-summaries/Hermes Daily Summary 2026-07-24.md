---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-24
updated: 2026-07-24
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-07-24

## Summary
- Live Hermes operations checks completed against current container state.
- Gateway is running for the default profile and all listed named profiles.
- Doctor found 2 configuration issues: missing API keys / full tool access API keys.
- Local summary target was writable: `/home/hermes/.hermes/daily-summaries/`.

## What Ran Today
- `date +%F` → `2026-07-24`.
- Writability check: created and removed `.hermes-write-test` successfully.
- `hermes status` → exit 0.
- `hermes doctor` → exit 0, with warnings/issues reported.
- `hermes cron list` → exit 0.
- `hermes mcp list` → exit 0.
- `hermes gateway status` → exit 0.

## Health Signals
- Environment: Hermes Agent project at `/home/hermes/.hermes/hermes-agent`; Python 3.11.15; model `gpt-5.5`; provider OpenAI Codex.
- Auth: OpenAI Codex logged in; Nous Portal, Qwen OAuth, MiniMax OAuth, and xAI OAuth not logged in.
- API keys: `.env` exists, but doctor reports no API key configured.
- Gateway: running manually, not as a system service.
- Profile gateways: `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, and `zeus` all reported running.
- Cron: 6 active jobs, 7 total; visible active jobs include health check, weekday recap, weekly ops review, vault summary, GitHub backup, and profile gateway watchdog.
- Cron anomaly: `weekday-hermes-vault-summary` shows last run `2026-07-22` OK but current execution still `running`.
- MCP: no MCP servers configured.
- Tool availability: core tools available; browser/computer-use/media/social integrations show missing dependencies or API keys.

## Next Actions
- Investigate the still-running `weekday-hermes-vault-summary` execution `8f4985e92023474d8b001fb5e4bb0141` if it remains stuck.
- Configure only desired OpenAI API keys if full tool access is needed; avoid enabling non-OpenAI providers unless explicitly requested.
- Decide whether the gateway should remain manual or be installed as a service.
- Add MCP servers only if required by active workflows.
- Continue monitoring profile gateway watchdog output for named-profile availability.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
