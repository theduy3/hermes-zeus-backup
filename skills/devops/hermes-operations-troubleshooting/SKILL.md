---
name: hermes-operations-troubleshooting
description: "Troubleshoot Hermes operational issues in live deployments: cron scheduler state, gateway delivery failures, Telegram/Discord delivery, stale cron errors, and safe verification patterns."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [hermes, cron, gateway, telegram, operations, troubleshooting]
---

# Hermes Operations Troubleshooting

Use this skill when the user asks to fix or audit live Hermes operations: cron jobs, gateway status, delivery failures, scheduler health, Telegram/Discord messaging, or stale job errors.

This is an operational supplement for live troubleshooting. If the task is general Hermes setup/configuration, load `hermes-agent` first; if that skill is protected or cannot be updated, record recurring live-ops procedures here.

## Principles

1. Verify the live state, not remembered state.
2. Distinguish job execution from delivery: `last_status=ok` can coexist with delivery failure.
3. Test the platform independently before changing cron jobs.
4. Prefer minimal surgical changes: restart/reload only when needed; do not rewrite working jobs.
5. Clear stale error state only after a successful live verification.
6. Keep the final report terse: fixed/verified/remaining.

## Cron + Telegram delivery failure workflow

When cron outputs are running but Telegram delivery says `Unauthorized`:

1. Inspect cron scheduler and job state.
   - Use `hermes cron status` to confirm the scheduler/gateway PID and next run.
   - Use `hermes cron list --all` or the cronjob list tool to identify affected jobs and delivery targets.

2. Validate the configured Telegram bot token directly.
   - Read `TELEGRAM_BOT_TOKEN` from the active profile `.env` without printing the token.
   - Call Telegram Bot API `getMe` with the token.
   - `200 {"ok":true...}` means the token itself is valid.
   - `401 Unauthorized` means the active token is invalid/revoked or the process is using a different token than the file you inspected.

3. Validate the target chat independently.
   - Send a short direct test message to the target, e.g. `telegram:<chat_id>`.
   - If direct send works, token + chat are valid for the current agent/tool path.

4. Validate cron delivery path separately.
   - Create a one-shot temporary cron job with a tiny prompt and `deliver: telegram:<chat_id>`.
   - Trigger it immediately with `cronjob action=run`.
   - Wait at least one cron tick, usually 60-90 seconds, and verify output under `~/.hermes/cron/output/<job_id>/` or via cron list.
   - Remove the temporary job after verification if it remains listed.

5. If direct Telegram and cron delivery both work, treat old `last_delivery_error` entries as stale state.
   - Patch only `last_delivery_error` fields containing the resolved error.
   - Do not change prompts, schedules, models, skills, or delivery targets.
   - Re-run one affected low-risk job if practical and verify it returns `last_status=ok` with no delivery error.

6. If direct Telegram works but cron delivery still fails:
   - Restart/reload the gateway/scheduler so it picks up the current environment.
   - Re-check gateway logs for which profile and token source it loaded.
   - Verify `HERMES_HOME` / profile selection, especially in Docker multi-profile setups.

## Useful commands

```bash
hermes cron status
hermes cron list --all
ps -p <PID> -o pid,ppid,etime,cmd

python3 - <<'PY'
import urllib.request
from pathlib import Path
for line in (Path.home()/'.hermes/.env').read_text().splitlines():
    if line.startswith('TELEGRAM_BOT_TOKEN='):
        token=line.split('=',1)[1].strip().strip('"\'')
        break
with urllib.request.urlopen(f'https://api.telegram.org/bot{token}/getMe', timeout=15) as r:
    print(r.status, r.read().decode()[:300])
PY
```

## Pitfalls

- `last_status=ok` means the cron agent completed; it does not guarantee delivery succeeded.
- `last_delivery_error` may persist after the underlying Telegram issue is fixed. Clear it only after a successful direct send and a successful cron delivery test.
- `origin` delivery depends on stored origin metadata. If `origin` is null or stale, prefer explicit `telegram:<chat_id>` for jobs that must deliver to Telegram.
- Do not print bot tokens. Redact token values and lengths only if needed.
- Do not capture a transient Unauthorized incident as a permanent claim that Telegram is broken.

## References

- `references/telegram-cron-unauthorized.md` — resolved incident pattern: valid token, working direct send, successful cron test, stale Unauthorized state cleared.
