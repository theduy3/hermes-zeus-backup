---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-03
updated: 2026-07-03
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-07-03

## Summary
- Core Hermes checks completed against live container state at 2026-07-03 01:11:00 UTC.
- Local summary directory `/home/hermes/.hermes/daily-summaries/` was created/verified writable before writing.
- Hermes is running on Python 3.11.15 with model `gpt-5.5` via OpenAI Codex.
- Gateway is running manually in Docker foreground, not as a system service.
- Doctor reports 2 configuration issues: missing API keys in `.env` and missing API keys for full tool access.

## What Ran Today
- `hermes status --all` → ok; reports `.env` and `config.yaml` exist, OpenAI Codex auth is logged in, Telegram configured, gateway running, and 10 active scheduled jobs.
- `hermes doctor` → ok; validates Python, packages, directory structure, command installation, memory, and profiles; flags missing API keys/tool credentials.
- `hermes cron list` → ok; lists 10 active jobs, including health checks, recaps, vault summary, GitHub backup, gateway watchdog, and travel-context resets.
- `hermes mcp list` → ok; no MCP servers configured.
- `hermes gateway status` → ok; default gateway and 7 profile gateways are running.

## Health Signals
- Environment: project path `/home/hermes/.hermes/hermes-agent`; Python `3.11.15`; provider `OpenAI Codex`; model `gpt-5.5`.
- Auth: OpenAI Codex logged in; Nous Portal, Qwen OAuth, MiniMax OAuth, and xAI OAuth are not logged in.
- Messaging: Telegram configured; Discord, Slack, WhatsApp, Signal, Email, SMS, and other platforms are not configured.
- Gateway: running with PIDs `65, 32, 37, 42, 47, 52, 57, 62`; profiles `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, and `zeus` are running.
- Cron: 10 active jobs / 11 total; recent listed last runs are ok where present.
- MCP: no MCP servers configured.
- Tools: core toolsets available; browser/computer_use/web/x_search/discord/homeassistant/spotify/video_gen and several integrations are unavailable due to missing system dependencies or credentials.
- Skills hub: present; no `GITHUB_TOKEN`, so GitHub API rate limit is 60 req/hr.
- Memory: built-in memory active; `MEMORY.md` and `USER.md` present.

### Command Output Snapshots

#### `hermes status --all`
- Result: ok.
- Key lines:
  - Project: `/home/hermes/.hermes/hermes-agent`
  - Python: `3.11.15`
  - Model: `gpt-5.5`
  - Provider: `OpenAI Codex`
  - Gateway Service: running, docker foreground
  - Scheduled Jobs: `10 active, 11 total`

#### `hermes doctor`
- Result: ok, with configuration warnings.
- Key lines:
  - No active security advisories.
  - Python environment and version files consistent.
  - Config version up to date: `v32`.
  - Found 2 issue(s): configure API keys; configure missing API keys for full tool access.

#### `hermes cron list`
- Result: ok.
- Active jobs listed:
  - `daily-hermes-health-check`
  - `weekday-hermes-recap`
  - `weekly-hermes-ops-review`
  - `weekday-hermes-vault-summary`
  - `nightly-hermes-github-backup`
  - `Hermes profile gateway watchdog`
  - `switch-back-to-vancouver-after-quebec-trip`
  - `Post-trip PDT context sync after Montreal/Laval/Quebec return`
  - `Silent Vancouver return travel-context reset`
  - `Reassert Vancouver PDT after Quebec/Montreal trip`

#### `hermes mcp list`
- Result: ok.
- Output: no MCP servers configured.

#### `hermes gateway status`
- Result: ok.
- Default gateway running manually, not as a system service.
- Profile gateways running: `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, `zeus`.

## Next Actions
- Configure optional API keys if web search, browser automation, x_search, Discord, or other integrations are expected to be available in cron jobs.
- Consider adding a `GITHUB_TOKEN` to raise the skills hub GitHub API rate limit.
- Leave the daily summary cron target on `/home/hermes/.hermes/daily-summaries/` when the vault is intentionally read-only.
- Review whether MCP servers are intentionally absent; add only if a workflow needs them.
- Periodically archive or rotate old local daily summary files if disk usage grows.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[Hermes Daily Summaries]]
