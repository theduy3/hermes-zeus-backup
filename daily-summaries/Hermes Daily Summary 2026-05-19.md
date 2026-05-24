---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-05-19
updated: 2026-05-19
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-05-19

## 1. Summary

Hermes Agent running on macOS host (user: theduy), v0.13.0 (602 commits behind), DeepSeek v4-pro provider. Gateway active (PID 96225) with 5 profile gateways running. 6 active cron jobs. **CRITICAL ALERT: disk at 100% (830MB free on /System/Volumes/Data).** All cron delivery to Telegram failing with "Unauthorized" — gateway Telegram bridge may need re-auth. DeepSeek API experiencing stream drops and timeouts across multiple cron runs.

## 2. What Ran Today

- **daily-hermes-health-check** — `0 9 * * *` — ✓ Last run 2026-05-19 09:04 PDT (ok) — ⚠ Delivery: Telegram Unauthorized
- **weekday-hermes-recap** — `0 18 * * 1-5` — ✓ Last run 2026-05-18 18:11 PDT (ok) — ⚠ Delivery: Telegram Unauthorized — *Today's run in progress*
- **weekly-hermes-ops-review** — `15 9 * * 1` — ✗ Last run 2026-05-18 11:43 PDT (**error: Timeout 2430s**) — ⚠ Delivery: Telegram Unauthorized
- **weekday-hermes-vault-summary** — `10 18 * * 1-5` — ✓ Last run 2026-05-18 18:15 PDT (ok) — ⚠ Delivery: Telegram Unauthorized — *Today's run in progress*
- **ensure-telegram-profile-gateways** — `every 2m` — ✓ Last run 2026-05-19 17:16 PDT (ok). Earlier run at 11:21 PDT **timed out** after 3660s stale stream
- **nightly-hermes-github-backup** — `0 5 * * *` — ✓ Last run 2026-05-19 05:36 PDT (ok)

## 3. Health Signals

### Good (✓)
- DeepSeek API connected
- Config v23 (up to date)
- Gateway running (PID 96225, launchd)
- 5 profile gateways live: default, 3r (94947), charlesbourg (94939), maily (94931), ss (94957)
- 2 MCP servers active: cua-driver, obsidian-fs
- 12 profiles configured (3r, alan, catthew, charles, charlesbourg, finance, maily, mira, ss, thor, turing, zeus)
- Python 3.11.14, OpenAI SDK 2.24.0
- 23 toolsets enabled
- 18,639 sessions in state.db
- Nightly GitHub backup succeeding

### Warning (⚠)
- **🔴 CRITICAL: Disk at 100%** — `/System/Volumes/Data` has only 830MB free. This will cause session DB write failures, log rotation stalls, and cron failures. Needs immediate cleanup.
- **Telegram delivery failing on all cron jobs** — "Telegram send failed: Unauthorized". Gateway log should show whether this is a token expiry or rate-limit issue.
- **DeepSeek stream drops** — multiple occurrences today: `ensure-telegram-profile-gateways` stream stale for 1963s (11:21 AM), 3660s (2:23 PM); `weekday-hermes-recap`/`weekday-hermes-vault-summary` stream stale for 898s (6:44 PM). ReadTimeout errors from CloudFront upstream.
- **weekly-hermes-ops-review failed** — job idle for 2430s (limit 600s), timeout error
- **602 commits behind** — `hermes update` available (current: 2026.5.7)
- **No GITHUB_TOKEN** — Skills hub limited to 60 req/hr
- **Playwright Chromium not installed** — browser tools unavailable
- **3 profiles incomplete**: catthew, charles, finance — missing config/.env/alias
- **Unknown config keys**: `providers.deepseek: api_base, env_key` — logged as warnings

## 4. Next Actions

### Immediate (today)
- **Free disk space** — /System/Volumes/Data at 100% is an emergency. Clean logs, sessions, caches, or old backups. Check `~/.hermes/logs/` (51MB in errors.log + gateway.error.log), `~/.hermes/sessions/` (18,639 sessions)
- **Fix Telegram delivery** — investigate "Unauthorized" error. Check gateway.error.log for Telegram token expiry. May need to rotate `TELEGRAM_BOT_TOKEN` in `.env` and restart gateway

### Today
- Run `hermes update` to catch up on 602 commits
- Investigate DeepSeek stream stability — recurring ReadTimeout via CloudFront. Consider switching to alternate provider for cron jobs if pattern continues
- Fill in 3 incomplete profiles (catthew, charles, finance) or remove them

### This week
- Install Playwright Chromium: `cd ~/.hermes/hermes-agent && npx playwright install --with-deps chromium`
- Set `GITHUB_TOKEN` in `.env` for skills hub rate limits
- Review and clean up session store (18,639 sessions)
- Fix `providers.deepseek` config warnings (unknown keys: api_base, env_key)

## 5. Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[AI Agent Tooling MOC]]
