---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-09-10
updated: 2026-09-10
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary 2026-09-10

## Summary

VPS/container Hermes **v0.21.1** (upstream `6c3d4a4a`, **143 commits behind**) is up on **xAI OAuth / grok-4.5**, with gateway running under Docker (primary PIDs include **123, 71, 79, 90, 92, 99, 107, 115**). Default profile shows **12 active / 14 total** cron jobs; multi-profile gateways are up. Critical ops signals today: stale post-update gateway modules, **graphify-mcp** binary missing (MCP parked), **nightly GitHub backup failed**, **weekday-hermes-recap** interrupted by shutdown, and vault-summary Telegram delivery still Unauthorized for target `8446251233`.

## What Ran Today

- **daily-hermes-health-check** — `0 9 * * *` — ✓ last 2026-09-10 09:02 PDT
- **weekday-hermes-recap** — `0 18 * * 1-5` — ✗ last 2026-09-10 18:08 PDT — `Interrupted by shutdown before terminal completion`
- **weekday-hermes-vault-summary** — `10 18 * * 1-5` — running now; prior delivery ✗ Telegram Unauthorized (`telegram:8446251233`); last completed note 2026-09-09
- **nightly-hermes-github-backup** — `0 0 * * *` — ✗ last 2026-09-10 00:01 PDT — execution failed / pending None
- **Hermes profile gateway watchdog** — every 30m — ✓ last 2026-09-10 17:57 PDT
- **graphify-daily-refresh** — `30 3 * * *` — ✓ last 2026-09-10 03:31 PDT
- **Daily Tasks/Events Call Generator (Zeus+Catthew)** — `15 5 * * *` — ✓ last 2026-09-10 05:15 PDT
- **CALL Catthew Weekly humidifier (Wed at/30m-before)** — last ✓ 2026-09-09 (next Wed 2026-09-16)
- **CALL Catthew Vehicle odometer** — seasonal; next 2026-12-30
- **weekly-hermes-ops-review** — Mondays 09:15 — last ✓ 2026-09-07; next 2026-09-14
- Profiles with cron inventories: default 14, thor 13, catthew 11, charles 11, wiki 8, zeus 7, finance 3, butter 1

## Health Signals

**Good (✓)**
- Gateway running (docker/foreground multi-process)
- Model path: xAI OAuth logged in (refreshed 2026-09-11 01:00 UTC); primary grok-4.5 across default + 7 named profiles
- Nous Portal logged in (refresh enabled)
- Doctor: no security advisories; config v42 current; Python 3.11.15; SSL OK; core packages OK
- Telegram + several messaging plugins configured; terminal backend local
- Disk: root + `/vault` ~60% used, **~40G free**
- state.db integrity OK historically; WAL mode; ~13,221 sessions / ~78,815 messages (~715 MB)
- Firecrawl web search/extract tools available; Skills Hub lock OK (8 hub skills)

**Warning (⚠)**
- `hermes update` pulled code but gateways **not restarted** → mixed `sys.modules` risk until `hermes gateway restart` / full update cycle
- Agent **143 commits behind** — pending update
- MCP list marks graphify-vault* **enabled**, but runtime parks all with `FileNotFoundError: graphify-mcp` (repeated in errors.log / gateway-default.log)
- graphify-hermes MCP disabled (expected unless debug)
- Nous Tool Gateway: no usable paid credits (managed web/image/TTS/STT/browser/Modal unavailable)
- Nous access/key expiry ~**2026-09-11 02:08 UTC** (refresh yes — monitor)
- OpenAI Codex / MiniMax OAuth not logged in; no API keys in `.env` (OAuth-primary setup — doctor still flags setup)
- No `GITHUB_TOKEN` → Skills Hub 60 req/hr
- Tool gaps expected on this host: a2a, browser-cdp, browser-use, computer_use, discord token, homeassistant, image_gen, spotify, etc.
- Recent unclean gateway exits earlier today (swap pressure noted in exit-diag; state.db integrity ok)
- Telegram network path flapping earlier (sticky IPv4 fallbacks in gateway.log ~20:28–20:29 PDT)
- web/ui-tui workspace: moderate npm vulns reported by doctor

## Next Actions

**Immediate**
- Restart gateways after update (`hermes gateway restart` or controlled `hermes update`) to clear mixed-module warning
- Fix `graphify-mcp` binary PATH/install so vault Graphify MCP servers can connect
- Investigate **nightly-hermes-github-backup** failure and re-run/verify backup artifact
- Resolve Telegram Unauthorized for vault-summary delivery target `8446251233` (bot token vs chat id / auth)

**Today**
- Re-run or accept miss for **weekday-hermes-recap** after shutdown interrupt
- Confirm this vault-summary job completes and delivery path works (local note path is healthy)
- Watch Nous OAuth refresh past 02:08 UTC expiry window

**This week**
- Catch up Hermes upstream (143 commits) on a maintenance window
- Optional: set `GITHUB_TOKEN` for Skills Hub rate limits
- Review gateway memory/swap headroom (prior unclean exits under low available RAM / high swap)
- Weekly ops review Mon 2026-09-14 09:15

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[AI Agent Tooling MOC]]
