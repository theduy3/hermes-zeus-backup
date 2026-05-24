---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-05-15
updated: 2026-05-15
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Operations Daily Summary — 2026-05-15

## 1. Summary

Hermes v0.13.0 running on macOS (theduy) with DeepSeek v4-pro. Gateway PID 96225 stable, 4 profile gateways (3r, charlesbourg, maily, ss) all up. 6 cron jobs active. ⚠️ **Critical: disk at 99% (2.1 GB free).** ⚠️ `daily-hermes-health-check` delivery failing (Telegram Unauthorized). Several DeepSeek stream timeout events observed. 55 commits behind — update pending.

## 2. What Ran Today

- **daily-hermes-health-check** — `0 9 * * *` — Last run: 09:41 PDT ✓ (⚠️ delivery failed: Telegram Unauthorized)
- **ensure-telegram-profile-gateways** — `every 2m` — Last run: 11:12 PDT ✓ (⚠️ stream stale event at 11:10, recovered)
- **nightly-hermes-github-backup** — `0 5 * * *` — Last run: 05:03 UTC ✓
- **weekday-hermes-vault-summary** — `10 18 * * 1-5` — Last run: 01:13 UTC ✓ (⚠️ `/home/hermes` path unavailable on macOS; note written to `/Users/theduy/.hermes/daily-summaries/`)
- **weekday-hermes-recap** — `0 18 * * 1-5` — Next run: 18:00 PDT today
- **weekly-hermes-ops-review** — `15 9 * * 1` — Next run: Mon 2026-05-18

## 3. Health Signals

### Good (✓)
- ✓ Gateway PID 96225 running (launchd-managed)
- ✓ DeepSeek API connectivity OK
- ✓ Config v23 up to date
- ✓ Python 3.11.14, all required packages present
- ✓ MCP servers: cua-driver, obsidian-fs both enabled
- ✓ Telegram & Discord messaging configured
- ✓ 12 profiles defined, 4 gateways running
- ✓ State DB: 3,593 sessions tracked
- ✓ Firebase, Tavily, FAL API keys set
- ✓ All cron jobs active, no disabled jobs

### Warning (⚠)
- ⚠ **Disk at 99%** — only 2.1 GB free on `/System/Volumes/Data`. Risk of session failures, log truncation, or DB corruption
- ⚠ `daily-hermes-health-check` delivery failing — Telegram token appears invalid/revoked
- ⚠ DeepSeek stream timeouts: ReadTimeout at 41 min (stream drop, retry succeeded) and 39 min stale-stream kill on ensure-telegram job
- ⚠ Config warning spam: `providers.deepseek: unknown config keys ignored: api_base, env_key` — every session startup
- ⚠ BSD `ps` incompatibility in cron workers — GNU `ps --no-headers` flag fails on macOS
- ⚠ Hermes 55 commits behind (v0.13.0, update available)
- ⚠ No GITHUB_TOKEN — Skills Hub rate-limited to 60 req/hr
- ⚠ Playwright Chromium not installed — browser tools unavailable
- ⚠ Missing API keys: OpenRouter, OpenAI, Google Gemini, xAI, Anthropic

## 4. Next Actions

### Immediate
- **Free disk space** — 99% full is critical. Clear old sessions/logs or prune Docker images
- **Fix Telegram token** — `daily-hermes-health-check` delivery has been failing; re-auth Telegram bot

### Today
- Run `hermes update` to pull 55 commits
- Fix `ps` BSD/GNU incompatibility in `ensure-telegram-profile-gateways` cron job
- Clean up `providers.deepseek` unknown config keys (`api_base`, `env_key`) from config.yaml

### This Week
- Install Playwright Chromium: `npx playwright install --with-deps chromium`
- Set GITHUB_TOKEN for Skills Hub
- Configure missing API providers if needed (Anthropic, Google, xAI)
- Update vault-summary cron to use macOS-native path instead of `/home/hermes`

## 5. Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[AI Agent Tooling MOC]]
