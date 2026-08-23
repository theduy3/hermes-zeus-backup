# Gateway restart stdout triage

Use when the user pastes `hermes gateway restart` / gateway.log and asks what to fix.

## Live checks first

Do not restart from the paste alone. Verify:

- `hermes gateway status` + per-profile PIDs
- `/proc/<pid>/environ` `HERMES_HOME` (default `~/.hermes`; profiles `~/.hermes/profiles/<name>`)
- Redacted `getMe` for every `TELEGRAM_BOT_TOKEN` (unique bot ids)
- `gateway_state.json` `platforms.telegram.state`

## Noise (do not “fix”)

- `check_fn` False for browser / CDP / vision / image-gen / kanban / computer-use on a headless VPS
- `skill_manage` 60-char description rejects
- memory char-limit / unmatched `replace`
- `execute_code` blocked in unattended cron
- `cronjob` rejecting absolute `script` paths (confirm jobs already use names relative to `~/.hermes/scripts/`)
- Auto-repaired tool names (`web_fetch` → `web_search`)
- Relay skip / mid-stream drop on concurrent turns

## Recovered Telegram flap (not a token failure)

Pattern: `Bad Gateway` / `Timed out` → reconnect 1/10…N/10 → `Telegram polling restarted after network error; health pending getUpdates progress` → later `Session expiry` or inbound messages, no new network errors.

- `getMe` 200 + unique tokens = auth is fine
- `gateway_state` `connected` with a pre-flap `updated_at` is stale-connected, not proof of death
- Idle polling does not update log mtime
- Do **not** restart unless a bot is silent *now*

Matches weekly-ops-audit recovered-flap reporting: monitor/proxy, not Unauthorized.

## Action-worthy from the same dump

- `Firecrawl client initialization failed` / “Web tools are not configured” + Nous “no usable paid credits”: capability gap. Needs `FIRECRAWL_API_KEY` or `FIRECRAWL_API_URL`, or portal credits + `hermes model` refresh. Do not invent a key.
- Default status PID is `hermes gateway restart` while profiles are `gateway run`: expected in `--all` / supervisor topology. Confirm a real adapter via latest “Connected to Telegram” / inbound / session-expiry, not the parent PID alone.
