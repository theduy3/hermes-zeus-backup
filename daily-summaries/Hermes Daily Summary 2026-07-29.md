---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-29
updated: 2026-07-29
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-07-29

## Summary
- Hermes default profile is running on Python 3.11.15 with model `gpt-5.5` via OpenAI Codex.
- Gateway is running manually in Docker with default plus seven named profile gateways active.
- Doctor reports no active security advisories and core environment checks pass.
- Main follow-up: Graphify daily refresh failed with SIGKILL during Hermes code extraction.

## What Ran Today
- `hermes status`: gateway running; 7 active scheduled jobs, 8 total; 1 active session.
- `hermes doctor`: completed diagnostics; found 3 issues.
- `hermes cron list`: active cron jobs include health check, weekday recap, weekday vault summary, weekly ops review, nightly GitHub backup, profile gateway watchdog, and graphify daily refresh.
- `hermes mcp list`: Graphify MCP servers enabled for Hermes and vault graphs.
- `hermes gateway status`: default gateway plus butter, catthew, charles, finance, thor, wiki, and zeus profiles are running.

## Health Signals
- Positive:
  - OpenAI Codex auth is logged in and refreshed recently.
  - Version files are consistent at 0.19.0.
  - Required Python packages are installed.
  - Config version is current at v33.
  - Tool availability includes terminal, file, memory, skills, session search, delegation, todo, TTS, video, and vision.
  - Disk usage for `/home/hermes/.hermes` is 72%: 71G used, 29G available.
- Warnings:
  - No API key found in `~/.hermes/.env`; OpenAI Codex auth is still available.
  - Nous Portal, MiniMax OAuth, and xAI OAuth are not logged in.
  - Browser/computer-use dependent tools are unavailable due to missing system dependencies.
  - Web search toolset lacks configured API keys.
  - UI TUI workspace has 7 high npm vulnerabilities in build-time tooling.
  - Skills Hub has no GitHub token, so GitHub API rate limit is lower.
- Failures:
  - `graphify-daily-refresh` last run failed: `graphify extract /home/hermes/.hermes/hermes-agent ...` died with `SIGKILL` after AST extraction reached 100%.
  - `weekday-hermes-vault-summary` shows a running execution from 2026-07-27, which may need review if still stale.

## Next Actions
- Investigate `graphify-daily-refresh` memory/runtime pressure; retry with fewer workers or split Hermes extraction.
- Check whether stale execution `ef2dc8c77f894568aa41e5fb0db413ed` for `weekday-hermes-vault-summary` is actually still running or stuck.
- Decide whether to configure API keys in `~/.hermes/.env` or keep OpenAI Codex-only auth intentionally.
- Clear or document UI TUI npm vulnerability status if it remains build-time only.
- Add a GitHub token if Skills Hub rate limits become operationally relevant.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
