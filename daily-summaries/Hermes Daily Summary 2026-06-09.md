---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-06-09
updated: 2026-06-09
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-06-09

## Summary
- Generated from live Hermes operational checks on 2026-06-09.
- Local target directory `/home/hermes/.hermes/daily-summaries/` was created/verified writable before writing.
- Hermes is running on model `gpt-5.5` via OpenAI Codex auth; gateway is active.
- Main attention items: outdated config version, missing API keys for some providers/tools, browser dependencies unavailable, and no MCP servers configured.

## What Ran Today
- `hermes status` completed successfully.
- `hermes doctor` completed successfully and reported 3 issues to address.
- `hermes cron list` completed successfully and showed 11 active scheduled jobs.
- `hermes mcp list` completed successfully and reported no MCP servers configured.
- `hermes gateway status` completed successfully and confirmed the default gateway plus profile gateways are running.

## Health Signals
- Gateway: running manually with PID `37`; profile gateways also running for butter, catthew, charles, finance, thor, and zeus.
- Scheduled jobs: 11 active, 12 total; recent listed jobs mostly report last run `ok`.
- Cron warning: `weekday-hermes-vault-summary` last run was `ok`, but delivery previously failed due to Telegram timeout.
- Doctor: no active security advisories; Python 3.11.15; Hermes version files consistent at `0.16.0`.
- Doctor warnings: no API key found in `~/.hermes/.env`; config version outdated `v24 → v27`; Nous Portal, MiniMax OAuth, and xAI OAuth not logged in.
- Tool warnings: browser/computer-use unavailable due to missing Playwright Chromium/system dependencies; web/x_search/MOA and several integrations gated by missing API keys.
- MCP: no MCP servers configured.

## Next Actions
- Run `hermes doctor --fix` or `hermes setup` when ready to migrate config from v24 to v27.
- Configure only the missing API keys/providers that are actually needed; OpenAI Codex auth is already logged in.
- Install Playwright Chromium if browser automation is needed: `cd /home/hermes/.hermes/hermes-agent && npx playwright install --with-deps chromium`.
- Investigate the Telegram timeout on `weekday-hermes-vault-summary` if delivery failures recur.
- Add MCP servers with `hermes mcp add` only if workflows require MCP-backed tools.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
