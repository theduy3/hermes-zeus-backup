---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-06-02
updated: 2026-06-02
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-06-02

## Summary

- Hermes Agent is running in the local container on Python 3.11.15 with model `gpt-5.5` via OpenAI Codex auth.
- Gateway is healthy and running manually under Docker foreground management; default profile PID is `37`.
- Doctor found no security advisories and reports core Python packages, configuration, memory, session DB, and CLI installation as present.
- Main operational gaps are missing API-key configuration for several optional providers/tools and missing browser system dependencies.

## What Ran Today

- `hermes status` completed successfully and reported 10 active scheduled jobs out of 11 total.
- `hermes doctor` completed successfully with 2 configuration issues: API keys are missing or incomplete for full tool access.
- `hermes cron list` completed successfully; most recent tracked cron runs were mostly `ok`.
- `hermes mcp list` completed successfully and reported no MCP servers configured.
- `hermes gateway status` completed successfully and confirmed the default gateway plus six profile gateways are running.

## Health Signals

- Gateway: running, PID `37`, manually launched rather than installed as a system service.
- Other profile gateways: `butter`, `catthew`, `charles`, `finance`, `thor`, and `zeus` are all running.
- Auth: OpenAI Codex is logged in; Google Gemini OAuth is logged in; Nous Portal, MiniMax OAuth, xAI OAuth, and Qwen OAuth are not logged in.
- Tooling: terminal, file, cronjob, delegation, memory, session_search, skills, todo, TTS, image, vision, video, Feishu, and kanban runtime-gated tools are available.
- Tool gaps: browser/browser-cdp/computer_use unavailable due to missing Playwright Chromium/system dependency; web and x_search lack required API keys.
- Cron: `vault-wiki-lint` last run errored with `RuntimeError: [Errno 32] Broken pipe`; other listed jobs show latest run status `ok`.
- MCP: no MCP servers are configured.
- Disk: `/` has 66G available, 67% used.
- Local summary path: `/home/hermes/.hermes/daily-summaries/` was created/confirmed writable.

## Next Actions

- Investigate the `vault-wiki-lint` broken pipe failure and rerun or adjust the job if needed.
- Run `hermes setup` or update `~/.hermes/.env` to configure API keys required for web, x_search, OpenRouter, GitHub, and other optional tools.
- Install Playwright Chromium dependencies if browser automation is needed: `cd /home/hermes/.hermes/hermes-agent && npx playwright install --with-deps chromium`.
- Consider installing the gateway as a service if persistent service management is preferred over manual Docker foreground execution.
- Add MCP servers only if current workflows require them; none are configured today.

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
