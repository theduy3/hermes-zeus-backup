---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-21
updated: 2026-07-21
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
# Hermes Daily Summary 2026-07-21

## Summary

- Daily Hermes operations checks ran against live local container state.
- Gateway is running for the default profile, with additional named profile gateways active.
- `hermes doctor` completed and reported 4 issues, mostly missing optional/API configuration and npm workspace vulnerabilities.
- MCP has no configured servers in this profile.

## What Ran Today

- `date +%F` → `2026-07-21`.
- Writable target check for `/home/hermes/.hermes/daily-summaries/` → passed.
- `hermes status` → exit `0`.
- `hermes doctor` → exit `0`.
- `hermes cron list` → exit `0`.
- `hermes mcp list` → exit `0`.
- `hermes gateway status` → exit `0`.

## Health Signals

- Environment: Hermes Agent project at `/home/hermes/.hermes/hermes-agent`; Python `3.11.15`; model `gpt-5.5`; provider `OpenAI Codex`.
- Authentication: OpenAI Codex is logged in; most API-key providers are not configured; Nous Portal, MiniMax OAuth, and xAI OAuth are not logged in.
- Gateway: default gateway is running manually, not as a system service.
- Profile gateways: `butter`, `charles`, `finance`, `wiki`, and `zeus` reported running from `hermes gateway status`; `hermes doctor` also listed `catthew` and `thor` as running.
- Cron: 6 active jobs shown, including health check, weekday recap, vault summary, weekly ops review, nightly GitHub backup, and profile gateway watchdog.
- Cron recent status: listed active jobs show last runs as `ok` where available.
- MCP: no MCP servers are configured for this profile.
- Tool availability: core tools are available; browser/computer-use/web/x_search and several integrations are unavailable due to missing dependencies or API keys.
- Doctor issues: missing API keys/full tool access, 2 web workspace npm vulnerabilities, and 2 ui-tui workspace npm vulnerabilities.
- Security: no active security advisories and no suspicious MCP stdio commands.

## Next Actions

- Decide whether missing API/API-key providers are intentional for this container; run `hermes setup` only if broader web/provider access is needed.
- Review the web and ui-tui npm vulnerability findings; doctor notes they are build-tool advisories that clear via lockfile bump.
- If MCP tools are expected in this profile, configure them with `hermes mcp add ...`; otherwise keep current no-MCP state.
- Consider installing the gateway as a service if manual foreground gateway management is no longer desired.
- Continue monitoring scheduled jobs, especially `weekday-hermes-vault-summary` and profile gateway watchdog.

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
