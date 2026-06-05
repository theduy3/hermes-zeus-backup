---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-06-05
updated: 2026-06-05
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
# Hermes Daily Summary 2026-06-05

## Summary

- Hermes core checks completed successfully across status, doctor, cron, MCP, and gateway commands.
- Daily summary generated locally on 2026-06-05 in the container workspace, not the read-only vault.

## What Ran Today

- `Hermes status` — OK (exit 0).
- `Hermes doctor` — OK (exit 0).
- `Hermes cron list` — OK (exit 0).
- `Hermes MCP list` — OK (exit 0).
- `Hermes gateway status` — OK (exit 0).

## Health Signals

- Hermes status: OK — ┌─────────────────────────────────────────────────────────┐
- Hermes doctor: OK — ┌─────────────────────────────────────────────────────────┐
- Hermes cron list: OK — ┌─────────────────────────────────────────────────────────────────────────┐
- Hermes MCP list: OK — No MCP servers configured.
- Hermes gateway status: OK — ✓ Gateway is running (PID: 37)

## Next Actions

- No urgent remediation needed from today’s live checks.
- Keep monitoring cron delivery and gateway health during the next weekday run.

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]

## Live Check Output

### Hermes status

- Exit code: `0`

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
... (47 more lines)
```

### Hermes doctor

- Exit code: `0`

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
... (86 more lines)
```

### Hermes cron list

- Exit code: `0`

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                         Scheduled Jobs                                  │
└─────────────────────────────────────────────────────────────────────────┘

  e83470683a90 [active]
    Name:      daily-hermes-health-check
    Schedule:  0 9 * * *
    Repeat:    ∞
    Next run:  2026-06-05T09:00:00-07:00
    Deliver:   origin
    Last run:  2026-06-04T09:01:16.292982-07:00  ok

  c9c38ab77915 [active]
    Name:      weekday-hermes-recap
    Schedule:  0 18 * * 1-5
    Repeat:    ∞
    Next run:  2026-06-05T18:00:00-07:00
    Deliver:   origin
    Last run:  2026-06-04T18:02:48.785731-07:00  ok

  8f310c8f4baf [active]
    Name:      weekly-hermes-ops-review
    Schedule:  15 9 * * 1
    Repeat:    ∞
    Next run:  2026-06-08T09:15:00-07:00
    Deliver:   origin
    Last run:  2026-06-01T09:19:43.853932-07:00  ok

  67d44bd30291 [active]
    Name:      weekday-hermes-vault-summary
    Schedule:  10 18 * * 1-5
    Repeat:    ∞
    Next run:  2026-06-05T18:10:00-07:00
    Deliver:   origin
    Skills:    obsidian
    Last run:  2026-06-03T18:11:08.350648-07:00  ok

  12e5ce30563d [active]
    Name:      nightly-hermes-github-backup
    Schedule:  0 5 * * *
... (49 more lines)
```

### Hermes MCP list

- Exit code: `0`

```text
No MCP servers configured.

  Add one with:
    hermes mcp add <name> --url <endpoint>
    hermes mcp add <name> --command <cmd> --args <args...>
```

### Hermes gateway status

- Exit code: `0`

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
