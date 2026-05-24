---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-05-21
updated: 2026-05-21
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary — 2026-05-21

## 1. Summary

Hermes Agent v0.14.0 is operational in a Docker container (Linux) using deepseek-v4-pro via DeepSeek. Gateway is running (PID 53) with all 12 profiles active. 11 cron jobs are configured, 9 of 11 had successful last runs. Two delivery failures (Telegram Unauthorized) and one timeout on the weekly ops review need attention. A Docker image update is available (44 commits behind).

## 2. What Ran Today

Events from the past 24h (2026-05-20 through 2026-05-21 01:12 UTC):

- **daily-hermes-health-check** — `0 9 * * *` — ✓ ok (2026-05-20 09:01 PDT)
- **weekday-hermes-recap** — `0 18 * * 1-5` — ✓ ok (2026-05-20 18:05 PDT)
- **weekday-hermes-vault-summary** — `10 18 * * 1-5` — ✓ ok (2026-05-19 18:50 PDT) — ⚠ delivery failed: Telegram Unauthorized
- **weekly-hermes-ops-review** — `15 9 * * 1` — ✗ error (2026-05-18 11:43 PDT) — TimeoutError: idle 2430s (limit 600s), delivery failed: Telegram Unauthorized
- **ensure-telegram-profile-gateways** — `every 2m` — ✓ ok (continuous)
- **nightly-hermes-github-backup** — `0 5 * * *` — ✓ ok (2026-05-20 05:01 PDT)
- **vault-today** — `0 4 * * *` — ✓ ok (2026-05-20 04:18 PDT)
- **vault-process** — `0 10 * * *` — ✓ ok (2026-05-20 10:01 PDT)
- **vault-wiki-ingest** — `0 8,14,20 * * *` — ✓ ok (2026-05-20 14:01 PDT, next 20:00 PDT)
- **vault-wiki-lint** — `0 2 * * *` — ✓ ok (2026-05-20 02:21 PDT)
- **vault-tonight** — `0 18,23 * * *` — ✓ ok (2026-05-20 18:02 PDT)

## 3. Health Signals

### Good (✓)
- ✓ Gateway running (PID 53, manual mode), all 12 profiles up
- ✓ Model: deepseek-v4-pro (DeepSeek API key valid)
- ✓ Config up to date (v23), Python 3.11.15
- ✓ 23,921 sessions in state DB
- ✓ Nightly GitHub backup active
- ✓ Disk: 67% used (65G free on 194G `/dev/sda1`)
- ✓ No active security advisories
- ✓ Core packages: OpenAI SDK, Rich, PyYAML, HTTPX, Croniter all installed

### Warning (⚠)
- ⚠ **Telegram Unauthorized**: 2 cron jobs fail delivery (`weekly-hermes-ops-review`, `weekday-hermes-vault-summary`) — bot token may need refresh
- ⚠ **Telegram Bad Gateway**: transient network error at 01:11 PDT, auto-reconnect scheduled
- ⚠ **weekly-hermes-ops-review timeout**: idle 2430s (vs 600s limit) on 2026-05-18
- ⚠ **Docker image stale**: 44 commits behind `nousresearch/hermes-agent:latest` — run `docker pull`
- ⚠ **Multi-agent-context DB failures**: repeated "unable to open database file" warnings
- ⚠ **DeepSeek vision_analyze**: `image_url` variant unsupported by deepseek-v4-pro — vision requests will fail
- ⚠ **No MCP servers configured**
- ⚠ **Missing API keys**: OpenRouter, OpenAI, Google, xAI, Anthropic, GitHub, Firecrawl, Tavily, FAL, ElevenLabs — limiting tool access
- ⚠ **No GitHub token**: 60 req/hr rate limit on Skills Hub

## 4. Next Actions

### Immediate
- Refresh Telegram bot token — 2 cron jobs failing delivery with "Unauthorized"
- Investigate weekly-hermes-ops-review timeout (2430s) — may need task scoping or timeout increase

### Today
- `docker pull nousresearch/hermes-agent:latest` — apply 44 pending commits
- Investigate multi-agent-context DB failures ("unable to open database file") in error logs

### This Week
- Configure GitHub token in `.env` to lift Skills Hub rate limit
- Consider adding MCP servers for extended tooling
- Evaluate adding missing API keys for expanded tool access (web search, browser, x_search, etc.)
- Address deepseek-v4-pro vision incompatibility — either switch model for vision tasks or disable vision tools

## 5. Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[AI Agent Tooling MOC]]
