---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-05-14
updated: 2026-05-14
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary — 2026-05-14

## 1. Summary

Hermes Agent v0.13.0 running on macOS (theduy), model `deepseek-v4-pro` via DeepSeek. Gateway PID 96225 (launchd-managed). 6 active cron jobs, 5 gateway profiles running (default, 3r, charlesbourg, maily, ss). **CRITICAL**: disk at 99% (3.6 GiB free / 228 GiB) — immediate cleanup needed. One cron delivery failure (Telegram Unauthorized on `weekday-hermes-vault-summary`).

## 2. What Ran Today

- **daily-hermes-health-check** — `0 9 * * *` → ✓ 2026-05-14 09:01 UTC
- **weekday-hermes-recap** — `0 18 * * 1-5` → ✓ 2026-05-14 18:04 UTC
- **nightly-hermes-github-backup** — `0 5 * * *` → ✓ 2026-05-14 05:10 UTC
- **ensure-telegram-profile-gateways** — every 2m → ✓ continuous
- **weekly-hermes-ops-review** — `15 9 * * 1` → last ✓ 2026-05-11 (next Mon)
- **weekday-hermes-vault-summary** — `10 18 * * 1-5` → ✗ deliver failed 2026-05-13 `Telegram send failed: Unauthorized`

## 3. Health Signals

### Good (✓)
- Gateway running (PID 96225, launchd)
- DeepSeek API connectivity ✓
- Config v23, Python 3.11.14, virtualenv active
- MCP servers: `cua-driver` ✓, `obsidian-fs` ✓
- Telegram ✓ (profile: 8446251233), Discord ✓
- Messaging: Telegram + Discord configured
- Auth: DeepSeek ✓, FAL ✓, Firecrawl ✓, Tavily ✓, Gemini OAuth ✓
- 5 gateway profiles: default, 3r, charlesbourg, maily, ss
- Sessions: 17,044 logged in state.db
- Security: no active advisories

### Warning (⚠)
- **Disk critically low** — 3.6 GiB free / 228 GiB (99% full)
- **`weekday-hermes-vault-summary` delivery failed** — Telegram Unauthorized (last run 2026-05-13)
- DeepSeek config has unknown keys: `api_base`, `env_key` (harmless but noisy; fills errors.log)
- Nous Portal auth not logged in
- OpenAI Codex auth not logged in
- No `GITHUB_TOKEN` set (60 req/hr rate limit on Skills Hub)
- Playwright Chromium not installed (browser tools unavailable)
- Missing API keys: OpenRouter, OpenAI, xAI/Grok, ElevenLabs, Anthropic, WandB

## 4. Next Actions

### Immediate
- **Free disk space** — 3.6 GiB remaining. Clear `~/.hermes/logs/` (gateway.log 4.4M, agent.log 2.3M, gateway.error.log 3.2M, errors.log 1.4M), old sessions, or Docker images
- **Fix Telegram Unauthorized** on `weekday-hermes-vault-summary` cron — re-auth or rotate bot token

### Today
- Clean up `api_base` / `env_key` from DeepSeek provider config in `config.yaml`
- Set `GITHUB_TOKEN` in `~/.hermes/.env` for Skills Hub rate limits

### This Week
- Install Playwright Chromium: `npx playwright install --with-deps chromium`
- Log into Nous Portal: `hermes auth add nous --type oauth`
- Review and prune old session files (~17K sessions, ~3 GB in `~/.hermes/sessions/`)

## 5. Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[AI Agent Tooling MOC]]
