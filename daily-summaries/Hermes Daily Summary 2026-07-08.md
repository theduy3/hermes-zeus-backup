---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-08
updated: 2026-07-08
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
# Hermes Daily Summary 2026-07-08

## Summary
- Generated from live Hermes CLI checks on 2026-07-08.
- Local container target `/home/hermes/.hermes/daily-summaries/` was created/checked and is writable.
- Core runtime is up: Hermes status succeeds, doctor completes, and gateway is running.
- Main items to watch: missing API keys/tool dependencies, no MCP servers configured, and gateway is running manually rather than as a service.

## What Ran Today
- `date +%F` returned `2026-07-08` for the local date used in this note.
- Writability check succeeded for `/home/hermes/.hermes/daily-summaries/`.
- `hermes status` completed successfully.
  - Project: `/home/hermes/.hermes/hermes-agent`
  - Python: `3.11.15`
  - Model/provider: `gpt-5.5` via OpenAI Codex
  - Gateway service: running under Docker foreground manager
  - Scheduled jobs: `7 active, 8 total`
  - Active sessions: `2`
- `hermes doctor` completed successfully but reported 2 configuration issues.
  - No active security advisories.
  - Python environment, required packages, directories, command installation, profiles, and memory provider are healthy.
  - Issues: configure API keys / missing API keys for full tool access.
- `hermes cron list` completed successfully.
  - Active jobs shown: health check, weekday recap, weekly ops review, weekday vault summary, GitHub backup, profile gateway watchdog, and Vancouver travel-context reset.
  - Recent listed last runs are marked `ok`.
- `hermes mcp list` completed successfully.
  - No MCP servers configured.
- `hermes gateway status` completed successfully.
  - Default gateway and profile gateways are running.
  - Gateway is running manually, not as a system service.

## Health Signals
- **Gateway:** running with PIDs `65, 32, 37, 42, 47, 52, 57, 62`.
- **Profiles:** `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, and `zeus` gateways reported running.
- **Doctor security:** no active security advisories; no suspicious MCP stdio commands.
- **Doctor environment:** Python `3.11.15`, active venv, config version up to date.
- **Auth:** OpenAI Codex and GitHub are configured; Nous Portal, MiniMax OAuth, xAI OAuth, and several API-key providers are not configured.
- **Tools:** core tools available; browser/computer-use/social/media integrations are limited by missing dependencies or credentials.
- **MCP:** no servers configured.
- **Disk:** `/home/hermes` and `/tmp` are on overlay filesystem, `99G` total, `63G` used, `37G` available, `64%` used.

## Next Actions
- Configure missing API keys if full tool access is required.
- Add MCP servers only if workflows need MCP-backed integrations.
- Consider installing the gateway as a service if manual Docker foreground operation is not intended.
- Continue monitoring scheduled jobs, especially vault-writing jobs, for path and mount mismatches.
- Keep summaries in `/home/hermes/.hermes/daily-summaries/` per current local-container requirement.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
