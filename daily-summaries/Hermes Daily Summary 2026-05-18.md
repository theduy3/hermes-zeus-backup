---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-05-18
updated: 2026-05-18
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-05-18

## 1. Summary

Hermes Agent v0.13.0 running on macOS (theduy) with deepseek-v4-pro via DeepSeek. Gateway is healthy (PID 96225) with 4 profile gateways active. 6 cron jobs configured, 4 running today (2 completed OK, 2 timed out). **Critical issue:** Telegram bot token is `Unauthorized` — all 4 origin-delivery cron jobs are failing to deliver results.

## 2. What Ran Today

- **daily-hermes-health-check** — `0 9 * * *`
  - ✗ Error: TimeoutError (idle 2430s, limit 600s). Delivery: Telegram Unauthorized.
  - Last run: 2026-05-18 11:43 PDT

- **weekday-hermes-recap** — `0 18 * * 1-5`
  - ✓ OK. Delivery: Telegram Unauthorized.
  - Last run: 2026-05-18 18:11 PDT

- **weekly-hermes-ops-review** — `15 9 * * 1`
  - ✗ Error: TimeoutError (idle 2430s). Delivery: Telegram Unauthorized.
  - Last run: 2026-05-18 11:43 PDT

- **weekday-hermes-vault-summary** — `10 18 * * 1-5`
  - ✓ OK (skill: obsidian). Delivery: Telegram Unauthorized.
  - Last run: 2026-05-18 11:48 PDT

- **ensure-telegram-profile-gateways** — `every 2m`
  - ✓ OK. Local delivery.
  - Last run: 2026-05-18 18:01 PDT

- **nightly-hermes-github-backup** — `0 5 * * *`
  - ✓ OK at 05:01 PDT

## 3. Health Signals

### Good (✓)
- Gateway running (PID 96225, 4 profile gateways: 3r, charlesbourg, maily, ss)
- Python 3.11.14, config v23 up-to-date
- DeepSeek API key active
- 2 MCP servers enabled (cua-driver, obsidian-fs)
- FAL, Tavily, Firecrawl API keys configured
- 18,448 sessions in state.db
- Directory structure intact (cron/, sessions/, logs/, skills/, memories/)
- 12 profiles configured, 4 gateways running
- Messaging: Telegram + Discord configured

### Warning (⚠)
- **Telegram Unauthorized** — bot token invalid for user 8446251233; 4 cron jobs failing delivery
- **304 commits behind** — `hermes update` available (current: 2026.5.7)
- **No OpenRouter API key** — moa tool unavailable
- **No Anthropic API key** — Claude models unavailable
- **No GITHUB_TOKEN** — Skills Hub limited to 60 req/hr
- **Playwright Chromium not installed** — browser tools unavailable
- **1 moderate vulnerability** in browser deps (agent-browser)
- **1 moderate vulnerability** in WhatsApp bridge deps
- **3 auth providers not logged in** (Nous Portal, OpenAI Codex, MiniMax OAuth)
- **config.yaml noise** — `providers.deepseek` has unknown keys `api_base, env_key`

## 4. Next Actions

### Immediate
- Fix Telegram bot token (`Unauthorized`) — re-generate in @BotFather and update `TELEGRAM_BOT_TOKEN` in `~/.hermes/.env`

### Today
- Investigate TimeoutError on `daily-hermes-health-check` and `weekly-hermes-ops-review` (both idle >40 min)
- Review `config.yaml` for unknown deepseek keys (`api_base`, `env_key`)

### This Week
- Run `hermes update` (304 commits behind)
- Install Playwright Chromium: `npx playwright install --with-deps chromium`
- Set `GITHUB_TOKEN` for Skills Hub rate limits
- Re-authenticate Nous Portal, Codex, and MiniMax OAuth

## 5. Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[AI Agent Tooling MOC]]
