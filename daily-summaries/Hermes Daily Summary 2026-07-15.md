---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-07-15
updated: 2026-07-15
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-07-15

## Summary

- Generated from live Hermes operational checks in the local container.
- `hermes status`, `hermes doctor`, `hermes cron list`, `hermes mcp list`, and `hermes gateway status` all completed successfully.
- Core gateway is running, with seven named profile gateways also reported running.
- Main follow-ups are configuration hygiene: outdated config version and missing optional/API-key providers.

## What Ran Today

- **Hermes status** — completed successfully; project at `/home/hermes/.hermes/hermes-agent`, Python 3.11.15, model `gpt-5.5`, provider OpenAI Codex.
- **Hermes doctor** — completed successfully; found 3 issues to address.
- **Hermes cron list** — completed successfully; 6 active scheduled jobs were listed.
- **Hermes MCP list** — completed successfully; no MCP servers are currently configured.
- **Hermes gateway status** — completed successfully; gateway is running manually, not as a system service.

## Health Signals

- **Gateway:** running with PIDs `74, 41, 47, 52, 56, 61, 67, 71`.
- **Profiles:** `butter`, `catthew`, `charles`, `finance`, `thor`, `wiki`, and `zeus` gateways are all running.
- **Cron:** active jobs include daily health check, weekday recap, weekly ops review, weekday vault summary, nightly GitHub backup, and profile gateway watchdog.
- **Doctor clean signals:** no active security advisories, no suspicious MCP stdio commands, Python environment OK, SSL certificates OK, required packages OK, memory provider OK.
- **Doctor warnings:** no API key found in `~/.hermes/.env`; config version is outdated (`v32 → v33`); optional/auth providers such as Nous Portal, MiniMax OAuth, and xAI OAuth are not logged in.
- **Tool availability:** core tools are available; browser/computer-use/web/x_search and several integration tools are unavailable due to missing system dependencies or API keys.
- **MCP:** no MCP servers configured.

## Next Actions

- Run `hermes doctor --fix` or `hermes setup` to migrate config from v32 to v33.
- Configure API keys only for providers/tools that are actually needed; OpenAI Codex auth is already logged in.
- Add MCP servers with `hermes mcp add ...` if MCP-backed Obsidian or other integrations are needed.
- Consider installing the gateway as a service if manual foreground gateway management becomes unreliable.
- Continue monitoring the scheduled jobs, especially `weekday-hermes-vault-summary` and `nightly-hermes-github-backup`.

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]

## Source Command Outputs

<details>
<summary>hermes status</summary>

```text
Environment: project /home/hermes/.hermes/hermes-agent; Python 3.11.15; .env exists; model gpt-5.5 via OpenAI Codex.
Auth: OpenAI Codex logged in; other API-key/OAuth providers mostly not configured.
Gateway: running via docker/manual foreground with multiple PIDs.
Scheduled jobs: 6 active, 7 total.
Sessions: 1 active session.
```

</details>

<details>
<summary>hermes doctor</summary>

```text
No active security advisories. Python, SSL, packages, command installation, directories, profiles, and memory provider OK.
Issues: no API key in ~/.hermes/.env; config version outdated v32 -> v33; missing API keys for full tool access.
Tip reported by doctor: run 'hermes doctor --fix' to auto-fix what's possible.
```

</details>

<details>
<summary>hermes cron list</summary>

```text
Active jobs listed: daily-hermes-health-check, weekday-hermes-recap, weekly-hermes-ops-review, weekday-hermes-vault-summary, nightly-hermes-github-backup, Hermes profile gateway watchdog.
Recent last-run statuses shown were OK for the listed jobs.
```

</details>

<details>
<summary>hermes mcp list</summary>

```text
No MCP servers configured.
```

</details>

<details>
<summary>hermes gateway status</summary>

```text
Gateway running manually, not as a system service. Other profile gateways running: butter, catthew, charles, finance, thor, wiki, zeus.
```

</details>
