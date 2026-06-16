---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-06-15
updated: 2026-06-15
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
# Hermes Daily Summary 2026-06-15

## Summary
- Daily local Hermes operations snapshot generated from live CLI checks in the container.
- Gateway, cron, MCP, doctor, and disk state were checked; warnings were detected.
- This note is written to the local container path, not the read-only vault.

## What Ran Today
- Cron list checked; no parseable job rows found. Command exit code: 0.

## Health Signals
- **Good (✓):**
  - Hermes version/status checked: `Hermes Agent v0.16.0 (2026.6.5) · upstream 975b9f0a`.
  - Gateway status command completed without explicit errors; PID 52
  - Cron list command completed.
  - MCP list command completed without explicit errors.
  - Local Hermes disk check: `/dev/sda1       194G  121G   74G  63% /home/hermes/.hermes`.
  - ✓ No active security advisories
  - ✓ Python 3.11.15
  - ✓ Virtual environment active
  - ✓ Version files consistent (0.16.0)
- **Warning (⚠):**
  - → Running inside a container — using local terminal backend (docker-in-docker is not configured by default)
  - ⚠ OpenRouter API (not configured)
  - ⚠ discord (missing DISCORD_BOT_TOKEN)
  - ⚠ discord_admin (missing DISCORD_BOT_TOKEN)
  - ⚠ moa (missing OPENROUTER_API_KEY)
  - ⚠ x_search (missing XAI_API_KEY)
  - Recent errors/warnings found in `~/.hermes/logs/errors.log`; inspect the tail for details.

## Next Actions
- **Immediate:** Review warning lines above, especially any failed Hermes CLI health command or recent `errors.log` entries.
- **Today:** Improve cron parsing/reporting if the CLI output format changed.
- **This week:** Keep gateway, MCP, and cron checks in this daily local summary workflow; prune stale logs if disk usage rises.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[AI Agent Tooling MOC]]

<details><summary>Raw command excerpts</summary>

```text
--- hermes status ---
┌─────────────────────────────────────────────────────────┐
│                 ⚕ Hermes Agent Status                  │
└─────────────────────────────────────────────────────────┘

◆ Environment
  Project:      /home/hermes/.hermes/hermes-agent
  Python:       3.11.15
  .env file:    ✓ exists
  Model:        gpt-5.5
  Provider:     OpenAI Codex

◆ API Keys
  OpenRouter    ✗ (not set)
  OpenAI        ✗ (not set)
  Google / Gemini  ✗ (not set)
  DeepSeek      ✗ (not set)
  xAI / Grok    ✗ (not set)
  NVIDIA NIM    ✗ (not set)
  Z.AI / GLM    ✗ (not set)
  Kimi          ✗ (not set)
  StepFun Step Plan  ✗ (not set)
  MiniMax       ✗ (not set)
  MiniMax-CN    ✗ (not set)
  Firecrawl     ✗ (not set)
  Tavily        ✗ (not set)
  Browser Use   ✗ (not set)
  Browserbase   ✗ (not set)
  FAL           ✗ (not set)
  ElevenLabs    ✗ (not set)
  GitHub        ✗ (not set)
  Anthropic     ✗ (not set)

◆ Auth Providers
  Nous Portal   ✗ not logged in (run: hermes portal)
  OpenAI Codex  ✓ logged in
    Auth file:  /home/hermes/.hermes/auth.json
    Refreshed:  2026-06-06 06:00:47 UTC
  Qwen OAuth    ✗ not logged in (run: qwen auth qwen-oauth)
    Auth file:  /home/hermes/.qwen/oauth_creds.json
    Error:      Qwen CLI credentials not found. Run 'qwen auth qwen-oauth' first.
  MiniMax OAuth  ✗ not logged in (run: hermes auth add minimax-oauth)
  xAI OAuth     ✗ not logged in (run: hermes auth add xai-oauth)
    Auth file:  /home/hermes/.hermes/auth.json
    Error:      No xAI OAuth credentials stored. Select xAI Grok OAuth (SuperGrok / Premium+) in `hermes model`.

◆ API-Key Providers
  Z.AI / GLM       ✗ not configured (run: hermes model)
  Kimi / Moonshot  ✗ not configured (run: hermes model)
  StepFun Step Plan ✗ not configured (run: hermes model)
  MiniMax          ✗ not configured (run: hermes model)
  MiniMax (China)  ✗ not configured (run: hermes model)

◆ Terminal Backend
  Backend:      local
  Sudo:         ✗ disabled

◆ Messaging Platforms
  Telegram      ✓ configured
  Di

--- hermes doctor ---
┌─────────────────────────────────────────────────────────┐
│                 🩺 Hermes Doctor                        │
└─────────────────────────────────────────────────────────┘

◆ Security Advisories
  ✓ No active security advisories

◆ Python Environment
  ✓ Python 3.11.15
  ✓ Virtual environment active
  ✓ Version files consistent (0.16.0)

◆ Required Packages
  ✓ OpenAI SDK
  ✓ Rich (terminal UI)
  ✓ python-dotenv
  ✓ PyYAML
  ✓ HTTPX
  ✓ Croniter (cron expressions) (optional)
  ✓ python-telegram-bot (optional)
  ✓ discord.py (optional)

◆ Configuration Files
  ✓ ~/.hermes/.env file exists
  ⚠ No API key found in ~/.hermes/.env
  ✓ ~/.hermes/config.yaml exists
  ⚠ Config version outdated (v27 → v29) (new settings available)

◆ xAI Model Retirement (May 15, 2026)
  ✓ No retired xAI models in config

◆ Auth Providers
  ⚠ Nous Portal auth (not logged in)
  ✓ OpenAI Codex auth (logged in)
  ✓ Google Gemini OAuth (logged in (duynt1989@gmail.com, project=kempt-simplicity-j55t8))
  ⚠ MiniMax OAuth (not logged in)
  ⚠ xAI OAuth (not logged in)
    → No xAI OAuth credentials stored. Select xAI Grok OAuth (SuperGrok / Premium+) in `hermes model`.

◆ Directory Structure
  ✓ ~/.hermes directory exists
  ✓ ~/.hermes/cron/ exists
  ✓ ~/.hermes/sessions/ exists
  ✓ ~/.hermes/logs/ exists
  ✓ ~/.hermes/skills/ exists
  ✓ ~/.hermes/memories/ exists
  ✓ ~/.hermes/SOUL.md exists (persona configured)
  ✓ ~/.hermes/memories/ directory exists
  ✓ MEMORY.md exists (2461 chars)
  ✓ USER.md exists (1198 chars)
  ✓ ~/.hermes/state.db exists (12699 sessions)

◆ Command Installation
  ✓ Venv entry point exists (venv/bin/hermes)
  ✓ ~/.local/bin/hermes → correct target

◆ External Tools
  ✓ git
  ✓ ripgrep (rg) (faster file search)
    → Running inside a container — using local terminal backend (docker-in-docker is not configured by default)
  ✓ Node.js
  ⚠ agent-browser not installed (run: npm install)
  ✓ Browser tools (agent-browser) deps (no known vulnerabilities)
  ⚠ web workspace deps (0 critical, 2 high, 1 moderate — run: cd /home/hermes/.hermes/hermes-agent && npm audit fix --workspace web)
  ⚠ ui-tui workspace deps (0 critical, 2 high, 1 moderate — run: cd /home/hermes/.hermes/hermes-agent && npm audit fix --workspace ui-tui)

◆ API Connectivity
  Running 26 connectivity checks in parallel…
                                                                      
  ⚠ OpenRouter API (not configured)

◆ Tool Availability
  ✓ clarify
  ✓ code_execution
  ✓ cronjob
  ✓ terminal

--- hermes cron list ---
┌─────────────────────────────────────────────────────────────────────────┐
│                         Scheduled Jobs                                  │
└─────────────────────────────────────────────────────────────────────────┘

  e83470683a90 [active]
    Name:      daily-hermes-health-check
    Schedule:  0 9 * * *
    Repeat:    ∞
    Next run:  2026-06-16T09:00:00-04:00
    Deliver:   origin
    Last run:  2026-06-15T09:00:53.681550-04:00  ok

  c9c38ab77915 [active]
    Name:      weekday-hermes-recap
    Schedule:  0 18 * * 1-5
    Repeat:    ∞
    Next run:  2026-06-16T18:00:00-04:00
    Deliver:   origin
    Last run:  2026-06-15T18:02:08.223638-04:00  ok

  8f310c8f4baf [active]
    Name:      weekly-hermes-ops-review
    Schedule:  15 9 * * 1
    Repeat:    ∞
    Next run:  2026-06-22T09:15:00-04:00
    Deliver:   origin
    Last run:  2026-06-15T09:17:45.329705-04:00  ok

  67d44bd30291 [active]
    Name:      weekday-hermes-vault-summary
    Schedule:  10 18 * * 1-5
    Repeat:    ∞
    Next run:  2026-06-16T18:10:00-04:00
    Deliver:   origin
    Skills:    obsidian
    Last run:  2026-06-12T18:11:32.237348-04:00  ok

  12e5ce30563d [active]
    Name:      nightly-hermes-github-backup
    Schedule:  0 5 * * *
    Repeat:    ∞
    Next run:  2026-06-16T05:00:00-04:00
    Deliver:   origin
    Last run:  2026-06-15T05:00:40.180782-04:00  ok

  b92449d7f332 [active]
    Name:      vault-today
    Schedule:  0 4 * * *
    Repeat:    ∞
    Next run:  2026-06-16T04:00:00-04:00
    Deliver:   origin
    Skills:    today
    Last run:  2026-06-15T04:01:47.155220-04:00  ok

  ce61f73456fe [active]
    Name:      vault-process
    Schedule:  0 10 * * *
    Repeat:    ∞
    Next run:  2026-06-16T10:00:00-04:00
    Deliver:   origin
    Skills:    process
    Last run:  2026-06-15T10:00:26.270842-04:00  ok

  e358e0a4cb18 [active]
    Name:      vault-wiki-ingest
    Schedule:  0 8,14,20 * * *
    Repeat:    ∞
    Next run:  2026-06-15T20:00:00-04:00
    Deliver:   origin
    Skills:    wiki-ingest
    Last run:  2026-06-15T14:00:35.219713-04:00  ok

  1b7bcc26dda2 [active]
    Name:      vault-wiki-lint
    Schedule:  0 2 * * *
    Repeat:    ∞
    Next run:  2026-06-16T02:00:00-04:00
    Deliver:   origin
    Skills:    wiki-lint
    Last run:  2026-06-15T02:05:02.339993-04:00  ok

  2f8f46180850 [active]
    Name:      vault-tonight
    Schedule:  0 18,23 * * *
    Repeat:    ∞
    Next run:  2026-06-15T23:00:00-04:00
    Deliver:   origin
    Skills:

--- hermes mcp list ---
No MCP servers configured.

  Add one with:
    hermes mcp add <name> --url <endpoint>
    hermes mcp add <name> --command <cmd> --args <args...>

--- hermes gateway status ---
✓ Gateway is running (PID: 52, 24, 29, 34, 38, 44, 49)
  (Running manually, not as a system service)

To install as a service:
  hermes gateway install
  sudo hermes gateway install --system

Other profiles:
  ✓ butter           — PID 24
  ✓ catthew          — PID 29
  ✓ charles          — PID 34
  ✓ finance          — PID 38
  ✓ thor             — PID 44
  ✓ zeus             — PID 49

--- recent errors ---
2026-06-14 03:00:25,231 WARNING [cron_2f8f46180850_20260613_230004] agent.tool_executor: Tool read_file returned error (0.33s): {"content": "", "total_lines": 0, "file_size": 0, "truncated": false, "is_binary": false, "is_image": false, "error": "File not found: /vault/.claude/skills/tonight/references/robust-headless-processi
2026-06-14 03:00:50,411 WARNING [cron_2f8f46180850_20260613_230004] agent.tool_executor: Tool execute_code returned error (0.00s): {"status": "error", "error": "BLOCKED: execute_code runs arbitrary local Python (including subprocess calls that bypass shell-string approval checks). Cron jobs run without a user present to approve i
2026-06-14 03:01:02,934 WARNING [cron_2f8f46180850_20260613_230004] agent.tool_executor: Tool terminal returned error (0.12s): {"output": "", "exit_code": -1, "error": "", "status": "pending_approval", "approval_pending": true, "command": "python3 -c \"import os; os.replace('/vault/Daily/.2026-06-13-tonight.md.tmp','/vault/Da
2026-06-14 06:00:14,796 WARNING [cron_1b7bcc26dda2_20260614_020004] agent.tool_executor: Tool read_file returned error (0.18s): {"content": "", "total_lines": 0, "file_size": 0, "truncated": false, "is_binary": false, "is_image": false, "error": "File not found: /vault/.hermes/skills/wiki-lint/references/batch-and-orphan-filte
2026-06-14 06:02:20,284 WARNING [cron_1b7bcc26dda2_20260614_020004] agent.tool_executor: Tool terminal returned error (0.24s): {"output": "{\"error\": \"PyYAML unavailable\", \"detail\": \"No module named 'yaml'\"}", "exit_code": 1, "error": null}
2026-06-14 18:00:46,898 WARNING [cron_e358e0a4cb18_20260614_140006] agent.tool_executor: Tool search_files returned error (0.29s): {"total_count": 0, "error": "Search failed: rg: /vault/Notes/Claude Code Setup Inventory.md: Permission
```

</details>
