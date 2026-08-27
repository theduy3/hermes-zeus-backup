---
tags: [hermes, daily, operations, automation]
type: synthesis
created: 2026-08-26
updated: 2026-08-26
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---

# Hermes Daily Summary - 2026-08-26

## Summary

Hermes Agent is operational with the gateway running and all 7 profiles active. 13 scheduled cron jobs are configured. Notable issues: graphify-daily-refresh failed with SIGKILL, OpenRouter API key not configured, config version outdated (v37 to v39).

## What Ran Today

- daily-hermes-health-check: ok (09:03 EDT)
- weekday-hermes-recap: ok (18:04 EDT)
- weekly-hermes-ops-review: last ran 2026-08-24, ok
- weekday-hermes-vault-summary: running (started 18:12 EDT)
- nightly-hermes-github-backup: ok (00:01 EDT)
- profile gateway watchdog: ok (18:01 EDT)
- graphify-daily-refresh: FAILED (SIGKILL at 03:31 EDT, 66 source files produced zero nodes, 3711 code files extracted before kill)
- Daily Tasks/Events Call Generator: ok (05:15 EDT)
- Catthew vehicle/humidifier calls: no run today (scheduled for future dates)

One-shot: ox-alpha-free-expiry-model-switch fires 2026-08-28 13:00 PDT.

## Health Signals

- Gateway: RUNNING (PIDs: 2799855, 2167383, 2388278, 2388288, 2388291, 2388293, 2388294, 2895923). Manual mode, not system service.
- Profiles: 7/7 running - butter, catthew, charles, finance, thor, wiki, zeus
- MCP Servers: 5 enabled (graphify-vault, graphify-vault-core, graphify-vault-sources, graphify-vault-daily, remarkable), 1 disabled (graphify-hermes)
- Cron Jobs: 13 active, 14 total. 1 failed today (graphify-daily-refresh)
- Auth: Nous Portal logged in (expires 2026-08-26 22:50 UTC). OpenAI Codex, MiniMax OAuth, xAI OAuth not logged in.
- API Keys: None configured in .env. OpenRouter set as model.provider but no key.
- Config: v37 -> v39 migration available. No deprecated keys.
- SQLite: WAL mode, 693.8 MB state.db, healthy.
- npm advisories: web workspace (4 high), ui-tui workspace (3 high) - build-time only, no runtime impact
- Python: 3.11.15, venv active, all required packages present
- Skills Hub: 8 hub-installed skills, lock file OK
- OpenAI Codex: not installed (optional)
- OpenRouter API: connectivity check failed (not configured)

## Next Actions

- [ ] Run 'hermes setup' or set OpenRouter API key in .env - missing key blocks tool access
- [ ] Run 'hermes doctor --fix' to migrate config v37 -> v39
- [ ] Investigate graphify-daily-refresh failure: SIGKILL during graphify extract on 3711 files. Check dmesg/journalctl for OOM. May need to reduce --max-workers or split extraction
- [ ] Log in OpenAI Codex, MiniMax OAuth, xAI OAuth if those providers are needed
- [ ] Add Nous Portal credits if browser/web/TTS/STT/Modal tools are needed (currently unavailable)
- [ ] Set GITHUB_TOKEN in .env for better GitHub rate limits (currently 60 req/hr)
- [ ] Before 2026-08-28 13:00 PDT: verify ox-alpha-free replacement model/provider is configured

## Related Notes

- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
