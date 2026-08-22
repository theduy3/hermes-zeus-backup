# Telegram cron Unauthorized — REVOKED token (not stale state)

This is the complement to `telegram-cron-unauthorized.md`. That file covers the
case where the token is VALID (getMe 200) and you only clear stale error state.
This file covers the case where Telegram has REVOKED the bot token itself.

## How to tell revoked vs. stale-valid

A `delivery error: Telegram send failed: Unauthorized` on cron jobs can mean either:

- **Valid token, stale `last_delivery_error`** → `getMe` returns 200, direct send
  works, just clear the stale field (see `telegram-cron-unauthorized.md`).
- **Revoked token** → the bot token was rejected by Telegram's servers. You
  CANNOT fix this without the user; only @BotFather can issue/re-issue a token.

### Diagnosis signal (revoked) — checked this session
1. `gateway_state.json` (default) or `profiles/<p>/gateway_state.json` shows:
   ```json
   "telegram": {"state":"retrying","error_code":"telegram_connect_error",
                "error_message":"Telegram startup failed: The token `8748253752:***` was rejected by the server."}
   ```
2. `logs/gateway.log` retry lines:
   `ERROR ... Failed to connect to Telegram: The token \`...:***\` was rejected by the server.`
3. Other profiles' gateways are `connected` → the problem is isolated to one
   bot token, not a network/auth-pool issue.

### Per-profile token inventory (confirm which profile owns the dead token)
```python
import os, glob, re
BASE=os.path.expanduser('~/.hermes')
envs=[os.path.join(BASE,'.env')]+sorted(glob.glob(os.path.join(BASE,'profiles','*','.env')))
for e in envs:
    scope='default' if (e.endswith('/.env') and 'profiles/' not in e) else e.split('/profiles/')[1].split('/')[0]
    txt=open(e,errors='replace').read()
    m=re.search(r'TELEGRAM_BOT_TOKEN\s*=\s*(\S+)', txt)
    tok=m.group(1).strip("'\"") if m else ''
    print(f"  {scope:8} id={tok.split(':')[0] if tok else '<EMPTY>'}")
```
Each profile has its OWN token in its own `.env`. A revoked token shows up as the
only `connected: false` / `retrying` gateway while the rest are `connected`.

## Interim fix: `deliver=local` stopgap (when user can't regenerate now)

If the user does not have a replacement @BotFather token immediately, stop the
Unauthorized errors WITHOUT rerouting to a personal profile's bot (rerouting is
intrusive — it changes WHERE reports land without the user's say-so).

Set the affected jobs to `deliver=local`:
- Jobs still run, save output to `~/.hermes[/profiles/<p>]/cron/output/<job_id>/`,
  and stop attempting the dead Telegram send → the `Unauthorized` error clears.
- Fully reversible: flip `deliver` back to `origin` (or a working profile's
  `telegram:<chat>`) once the token is repaired.

Edit `jobs.json` directly (the `cronjob` agent tool can't reach non-default
profiles and ignores `deliver`-style fields — see
`cron-missing-provider-repair.md` for the scan pattern):
```python
import json, os
p=os.path.join(os.path.expanduser('~/.hermes'),'cron/jobs.json')   # or profiles/<p>/cron/jobs.json
raw=json.load(open(p)); jobs=raw.get('jobs') if isinstance(raw,dict) else raw
TARGETS={'e83470683a90','c9c38ab77915','8f310c8f4baf','67d44bd30291','12e5ce30563d','067ad023e2d9'}
for j in jobs:
    if (j.get('job_id') or j.get('id')) in TARGETS:
        j['deliver']='local'
        j['last_delivery_error']=None
json.dump(raw,open(p,'w'),indent=1)
```
Leave `no_agent=True` script-only jobs (e.g. gateway watchdog) alone — they never
send an LLM Telegram message and weren't part of the Unauthorized errors.

## Permanent fix (needs the user)
1. User creates/regenerates a bot via @BotFather → new `TELEGRAM_BOT_TOKEN`.
2. Write it to the affected profile's `.env` (`~/.hermes/.env` for default;
   profile `.env` files are NOT protected and can be written with `terminal`/
   `patch`; the DEFAULT `.env` is protected — use `execute_code` terminal bypass
   or `hermes config set` to edit the default).
3. Restart that profile gateway: `hermes [-p <profile>] gateway restart`.
4. Verify a fresh `gateway_state.json` shows `telegram.state: connected` and that
   the newest gateway log line (not an old one) shows a successful connect.
5. Only then revert the affected jobs from `deliver=local` back to `origin`.

## Key lesson
"Unauthorized" is ambiguous. Revoked token = gateway can't even START Telegram
(see `gateway_state.json` + retry logs). Stale-valid = gateway is up, only the
cron error field is old. Diagnose which before choosing fix vs. stopgap.
