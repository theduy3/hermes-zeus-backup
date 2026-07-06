---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-06-30
updated: 2026-06-30
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-06-30

## Summary

- Hermes is running in the local container with model `gpt-5.5` via OpenAI Codex auth.
- Gateway is healthy and running manually in Docker/foreground mode.
- Doctor found 3 actionable configuration issues: missing API keys, outdated config version, and incomplete tool-provider setup.
- Scheduled automation is active: 15 active jobs out of 16 total.
- MCP is currently not configured; `hermes mcp list` reports no MCP servers.

## What Ran Today

- `hermes status` completed successfully.
- `hermes doctor` completed and reported no active security advisories.
- `hermes cron list` completed and showed 15 active scheduled jobs.
- `hermes mcp list` completed and showed no configured MCP servers.
- `hermes gateway status` completed and confirmed the gateway plus profile gateways are running.
- Local write target `/home/hermes/.hermes/daily-summaries/` was created/checked and verified writable before this note was written.

## Health Signals

- Security advisories: none active.
- Python environment: OK on Python 3.11.15; virtual environment active; version files consistent at 0.17.0.
- Gateway: running with PIDs `65, 32, 38, 43, 48, 53, 58, 62`.
- Profiles: `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, and `zeus` gateways are running.
- Disk: `/home/hermes/.hermes` is 56% used with 45G available.
- Auth: OpenAI Codex is logged in; Nous Portal, MiniMax OAuth, xAI OAuth, and Qwen OAuth are not logged in.
- Config: `~/.hermes/config.yaml` is outdated from v30 to v32.
- Tools: core tools are available; several optional/system-gated tools are unavailable or missing credentials, including browser, computer_use, web, x_search, Discord, Home Assistant, Spotify, video_gen, and Yuanbao.
- MCP: no MCP servers configured.

## Next Actions

- Run `hermes doctor --fix` or `hermes setup` to migrate config from v30 to v32.
- Configure provider API keys if non-Codex providers or web/search tools are needed.
- Add MCP servers only if current workflows require them.
- Consider installing/configuring browser dependencies if browser or computer-use workflows are expected.
- Keep monitoring cron jobs; current recurring jobs mostly show successful last runs.

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
