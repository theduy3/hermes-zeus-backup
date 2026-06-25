---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-06-24
updated: 2026-06-24
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-06-24

## Summary

- Hermes default profile is running on Python 3.11.15 with model `gpt-5.5` via OpenAI Codex.
- Gateway is up in Docker/manual foreground mode; default plus seven named profile gateways are running.
- Doctor reports no active security advisories and a healthy core install, with two configuration issues around missing API keys.
- Scheduler has 14 active jobs out of 15 total; most recent listed recurring jobs report `ok`, with one prior Telegram delivery timeout on the vault summary job.

## What Ran Today

- Checked live Hermes status with `hermes status`.
- Ran diagnostics with `hermes doctor`.
- Reviewed scheduled automation with `hermes cron list`.
- Checked MCP configuration with `hermes mcp list`.
- Confirmed gateway state with `hermes gateway status`.
- Verified local daily summary directory is writable: `/home/hermes/.hermes/daily-summaries/`.

## Health Signals

- ✅ Gateway running with PIDs reported for default and profile gateways.
- ✅ Doctor: Python, virtualenv, version files, SSL certificates, required packages, directory structure, command installation, memory provider, and profile gateways are healthy.
- ✅ Security: no active security advisories; no suspicious MCP stdio commands.
- ✅ Auth: OpenAI Codex logged in; Google Gemini OAuth logged in.
- ⚠️ Configuration: no API key found in `~/.hermes/.env`; several API-key providers are not configured.
- ⚠️ Tool availability: browser/computer-use/web/x_search and some integrations are unavailable due to missing system dependencies or API keys.
- ⚠️ MCP: no MCP servers configured.
- ⚠️ Delivery: `weekday-hermes-vault-summary` last run was `ok`, but delivery previously failed with a Telegram timeout.

## Next Actions

- Decide whether missing API-key providers are intentional; if not, run `hermes setup` to configure them.
- Investigate the Telegram timeout for `weekday-hermes-vault-summary` if delivery failures recur.
- Add MCP servers only if current workflows require them; current state reports none configured.
- Consider installing or enabling browser/web dependencies if workflows need browsing, computer use, or web search tools.

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
