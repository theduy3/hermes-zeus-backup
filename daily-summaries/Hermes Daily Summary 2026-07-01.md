---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-01
updated: 2026-07-01
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
# Hermes Daily Summary 2026-07-01

## Summary
- Hermes is running on `gpt-5.5` via OpenAI Codex auth in the local container.
- Gateway is up and cron scheduling is active.
- Doctor found 3 configuration issues: missing API keys, outdated config version, and incomplete provider/tool setup.
- MCP has no servers configured.

## What Ran Today
- `hermes status` → exit 0.
- `hermes doctor` → exit 0.
- `hermes cron list` → exit 0.
- `hermes mcp list` → exit 0.
- `hermes gateway status` → exit 0.

## Health Signals
- **Environment:** project at `/home/hermes/.hermes/hermes-agent`; Python `3.11.15`; `.env` exists.
- **Auth:** OpenAI Codex logged in; Nous Portal, Qwen OAuth, MiniMax OAuth, and xAI OAuth are not logged in.
- **Gateway:** running manually, not as a system service; active PIDs include `65, 32, 43, 48, 53, 58, 234384, 234655`.
- **Profiles:** 7 profiles detected and reporting gateway running: butter, catthew, charles, finance, thor, wiki, zeus.
- **Cron:** 10 active jobs, 11 total; recent health/recap/backup jobs report `ok` last runs.
- **Doctor:** no active security advisories; Python environment, required packages, directory structure, command installation, and memory provider passed.
- **Warnings:** no API key found in `~/.hermes/.env`; config version is outdated (`v30 → v32`); some optional tools are gated by missing dependencies or keys.
- **MCP:** no MCP servers configured.

## Next Actions
- Run `hermes doctor --fix` or `hermes setup` to migrate config from `v30` to `v32`.
- Configure any required API keys/providers if full tool access is needed beyond OpenAI Codex auth.
- Add MCP servers only if current workflows need them.
- Consider installing the gateway as a service if manual gateway supervision is not intentional.
- Keep this cron summary writing to `/home/hermes/.hermes/daily-summaries/` as requested.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
