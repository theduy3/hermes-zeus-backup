---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-05-28
updated: 2026-05-28
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-05-28

## Summary
- Generated from live container state on 2026-05-28; target is local container storage, not the read-only Obsidian vault.
- Hermes version/status signal: `Hermes Agent v0.14.0 (2026.5.16)`.
- Gateway PID/status: `37`; cron listing returned about 4 visible job rows.

## What Ran Today
- • `Schedule:  0 9 * * *`
- • `Next run:  2026-05-28T09:00:00-07:00`
- • `Last run:  2026-05-27T09:00:41.941038-07:00  ok`
- • `Schedule:  0 18 * * 1-5`
- • `Next run:  2026-05-28T18:00:00-07:00`
- • `Last run:  2026-05-27T18:01:56.776048-07:00  ok`
- • `Schedule:  15 9 * * 1`
- • `Next run:  2026-06-01T09:15:00-07:00`
- • `Last run:  2026-05-25T09:20:36.912567-07:00  ok`
- • `Schedule:  10 18 * * 1-5`
- • `Next run:  2026-05-28T18:10:00-07:00`
- ✗ `Last run:  2026-05-26T18:10:35.804819-07:00  error: RuntimeError: 'NoneType' object is not iterable`

## Health Signals
- **Good (✓):** Daily summary path is writable: `/home/hermes/.hermes/daily-summaries`.
- **Good (✓):** Status command completed with exit code 0.
- **Good (✓):** Doctor command completed with exit code 0.
- **Good (✓):** Gateway status command completed with exit code 0.
- **Good (✓):** MCP snapshot: No MCP servers configured.; Add one with:; hermes mcp add <name> --url <endpoint>.
- **Good (✓):** Session file count snapshot: `sessions=24077`.
- **Warning (⚠):** → Running inside a container — using local terminal backend (docker-in-docker is not configured by default) ⚠ OpenRouter API (not configured) Recent log warnings/errors detected; inspect `~/.hermes/logs/` if persistent.
- **Disk:** `Filesystem      Size  Used Avail Use% Mounted on`
- **Recent logs:** `2026-05-28 01:12 /home/hermes/.hermes/logs/agent.log; 2026-05-28 01:09 /home/hermes/.hermes/logs/gateway.log; 2026-05-28 01:01 /home/hermes/.hermes/logs/gateway-default.log; 2026-05-28 01:01 /home/hermes/.hermes/logs/errors.log; 2026-05-27 17:54 /home/hermes/.hermes/logs/gateway-exit-diag.log`

## Next Actions
- **Immediate:** Review any warning/error lines in `~/.hermes/logs/` if they repeat across summaries.
- **Today:** Confirm cron jobs with delivery targets are completing as expected from `hermes cron list` raw output.
- **This week:** Periodically run `hermes doctor` and update credentials/tool configuration for any reported gaps.

## Related Notes
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[AI Agent Tooling MOC]]

<!-- Raw command snapshots (trimmed) -->

### Raw Status
```text
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
  Nous Portal   ✗ not logged in (run: hermes auth add nous --type oauth)
  OpenAI Codex  ✓ logged in
    Auth file:  /home/hermes/.hermes/auth.json
    Refreshed:  2026-05-27 03:31:57 UTC
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
  Discord       ✗ not configured
  WhatsApp      ✗ not configured
  Signal        ✗ not configured
  Slack         ✗ not configured
  Email         ✗ not configured
  SMS           ✗ not configured
  DingTalk      ✗ not configured
  Feishu        ✗ not configured
  WeCom         ✗ not configured
  WeCom Callback  ✗ not configured
  Weixin        ✗ not configured
  BlueBubbles   ✗ not configured
  QQBot         ✗ not configured
  Yuanbao       ✗ not configured

◆ Gateway Service
…
```

### Raw Doctor
```text
┌─────────────────────────────────────────────────────────┐
│                 🩺 Hermes Doctor                        │
└─────────────────────────────────────────────────────────┘

◆ Security Advisories
  ✓ No active security advisories

◆ Python Environment
  ✓ Python 3.11.15
  ✓ Virtual environment active

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
  ✓ Config version up to date (v24)

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
  ✓ MEMORY.md exists (2092 chars)
  ✓ USER.md exists (1005 chars)
  ✓ ~/.hermes/state.db exists (12495 sessions)

◆ Command Installation
  ✓ Venv entry point exists (venv/bin/hermes)
  ✓ ~/.local/bin/hermes → correct target

◆ External Tools
  ✓ git
  ✓ ripgrep (rg) (faster file search)
    → Running inside a container — using local terminal backend (docker-in-docker is not configured by default)
  ✓ Node.js
  ✓ agent-browser (Node.js) (browser automation)
  ⚠ Playwright Chromium not installed (browser_* tools will be hidden from the agent)
    → Install with: cd /home/hermes/.hermes/hermes-agent && npx playwright install --with-deps chromium
  ✓ Browser tools (agent-browser) deps (no known vulnerabilities)

◆ API Connectivity
  Running 27 connectivity checks in parallel…                                                                        ⚠ OpenRouter API (not configured)

◆ Tool Availability
  ✓ clarify
  ✓ code_execution
  ✓ cronjob
  ✓ terminal
  ✓ delegation
  ✓ feishu_doc
  ✓ feishu_drive
  ✓ file
  ✓ image_gen
  ✓ memory
  ✓ messaging
  ✓ session_search
  ✓ skills
  ✓ todo
  ✓ tts
  ✓ visi
…
```

### Raw Cron List
```text
┌─────────────────────────────────────────────────────────────────────────┐
│                         Scheduled Jobs                                  │
└─────────────────────────────────────────────────────────────────────────┘

  e83470683a90 [active]
    Name:      daily-hermes-health-check
    Schedule:  0 9 * * *
    Repeat:    ∞
    Next run:  2026-05-28T09:00:00-07:00
    Deliver:   origin
    Last run:  2026-05-27T09:00:41.941038-07:00  ok

  c9c38ab77915 [active]
    Name:      weekday-hermes-recap
    Schedule:  0 18 * * 1-5
    Repeat:    ∞
    Next run:  2026-05-28T18:00:00-07:00
    Deliver:   origin
    Last run:  2026-05-27T18:01:56.776048-07:00  ok

  8f310c8f4baf [active]
    Name:      weekly-hermes-ops-review
    Schedule:  15 9 * * 1
    Repeat:    ∞
    Next run:  2026-06-01T09:15:00-07:00
    Deliver:   origin
    Last run:  2026-05-25T09:20:36.912567-07:00  ok

  67d44bd30291 [active]
    Name:      weekday-hermes-vault-summary
    Schedule:  10 18 * * 1-5
    Repeat:    ∞
    Next run:  2026-05-28T18:10:00-07:00
    Deliver:   origin
    Skills:    obsidian
    Last run:  2026-05-26T18:10:35.804819-07:00  error: RuntimeError: 'NoneType' object is not iterable

  12e5ce30563d [active]
    Name:      nightly-hermes-github-backup
    Schedule:  0 5 * * *
    Repeat:    ∞
    Next run:  2026-05-28T05:00:00-07:00
    Deliver:   origin
    Last run:  2026-05-27T05:00:51.719084-07:00  ok

  b92449d7f332 [active]
    Name:      vault-today
    Schedule:  0 4 * * *
    Repeat:    ∞
    Next run:  2026-05-28T04:00:00-07:00
    Deliver:   origin
    Skills:    today
    Last run:  2026-05-27T04:02:31.831981-07:00  ok

  ce61f73456fe [active]
    Name:      vault-process
    Schedule:  0 10 * * *
    Repeat:    ∞
    Next run:  2026-05-28T10:00:00-07:00
    Deliver:   origin
    Skills:    process
    Last run:  2026-05-27T10:00:52.681181-07:00  ok

  e358e0a4cb18 [active]
    Name:      vault-wiki-ingest
    Schedule:  0 8,14,20 * * *
    Repeat:    ∞
    Next run:  2026-05-27T20:00:00-07:00
    Deliver:   origin
    Skills:    wiki-ingest
    Last run:  2026-05-27T14:01:23.756139-07:00  ok

  1b7bcc26dda2 [active]
    Name:      vault-wiki-lint
    Schedule:  0 2 * * *
    Repeat:    ∞
    Next run:  2026-05-28T02:00:00-07:00
    Deliver:   origin
    Skills:    wiki-lint
    Last run:  2026-05-27T02:09:19.119953-07:00  error: RuntimeError: [Errno 32] Broken pipe

  2f8f46180850 [active]
    Name:      vault-tonight
    Schedule:  0 18,23 * * *
    Repeat:    ∞
    Next run:  2026-05-27T23:00:00-07:00
    Deliver:   origin
    Skills:    tonight
    Last run:  2026-05-27T18:01:18.583275-07:00  ok
```

### Raw MCP List
```text
No MCP servers configured.

  Add one with:
    hermes mcp add <name> --url <endpoint>
    hermes mcp add <name> --command <cmd> --args <args...>
```

### Raw Gateway Status
```text
✓ Gateway is running (PID: 37)
  (Running manually, not as a system service)

To install as a service:
  hermes gateway install
  sudo hermes gateway install --system

Other profiles:
  ✓ butter           — PID 20
  ✓ catthew          — PID 23
  ✓ charles          — PID 26
  ✓ finance          — PID 29
  ✓ thor             — PID 32
  ✓ zeus             — PID 35
```
