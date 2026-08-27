# Timezone drift: config is correct but jobs fire in the wrong tz

Class-level knowledge for `hermes-cron-ops`. Symptom: a job meant for 3pm local
fires 3h early/late; `next_run_at` in `jobs.json` shows the wrong UTC offset
(e.g. `-04:00` Toronto while config says `America/Vancouver`/`-07:00`).

## Root cause (verified)
- `hermes_time.py` resolves the timezone **once per process and caches it**
  (`get_timezone()` -> `_cache_resolved=True`; only an explicit `reset_cache()`
  clears it). A `config.yaml` `timezone` edit, or `sync_travel_context.py`,
  writes the disk correctly but does **NOT** reload running gateway processes.
- Gateways launched before the change keep the tz they loaded at startup.
  A stale `HERMES_TIMEZONE=America/Toronto` env var (set at process start by the
  supervisor) forces Toronto even when config says Vancouver.
- A previous "sync fixed all profiles" claim was false for this reason: disk was
  right, RAM was stale. Mixed `-04:00`/`-07:00` offsets across jobs = an
  in-flight migration that never completed because the long-lived gateways were
  never recycled.

## Diagnose (all read-only)
1. On-disk truth:
   - `grep timezone ~/.hermes/config.yaml ~/.hermes/profiles/*/config.yaml`
   - `~/.hermes/travel_context.json` (`timezone` + `label` fields)
2. Live truth per gateway (the decisive check):
   - `for pid in $(pgrep -f "hermes gateway run"); do
        tr '\0' '\n' < /proc/$pid/environ | grep -E '^HERMES_TIMEZONE=|HERMES_HOME=';
      done`
   - Stale `HERMES_TIMEZONE=America/Toronto` = the smoking gun.
3. `next_run_at` offsets in `jobs.json` (`~/.hermes/cron/jobs.json` +
   `~/.hermes/profiles/*/cron/jobs.json`). `-04:00` = stale Toronto,
   `-07:00` = Vancouver.
4. Fleet scan helper (already registered): `scripts/check_tz_offsets.py` -
   run first to scope the drift per profile.

## Fix - restart the gateway processes
This container is **NOT s6**: PID 1 is `tini`; supervision is bash `while true`
loops inside `entrypoint.sh`. Each loop respawns its gateway fresh (re-reading
`config.yaml`) within ~10s. That self-heal is the intended restart mechanism.

**DO NOT run `hermes gateway restart --all` from inside a gateway session.**
Its code path calls a **foreground `run_gateway()`** in the same process after
`kill_gateway_processes(all_profiles=True)`; the supervisor loops immediately
respawn the default gateway on the same Telegram bot token -> "token already in
use" crash (the entrypoint explicitly warns about this collision).

**Correct procedure:**
- `SIGTERM` the stale `hermes gateway run` PIDs directly. The entrypoint
  `while true` loops respawn each fresh, re-reading `config.yaml` (Vancouver)
  with no stale `HERMES_TIMEZONE` override.
- Exclude the PID serving the current chat so you don't drop the live session
  mid-turn. Find it: `ps -o ppid= -p $$` walks up to your session's gateway
  parent. All other gateways can be killed safely - their loops self-heal.
- This is a fleet-wide kill: it trips the terminal approval gate. Do not retry
  it unprompted; ask the user to approve.
- Expected: 10-30s delivery blip per profile during respawn; nothing lost.

**Post-restart verification:**
- Re-run `scripts/check_tz_offsets.py`: every `next_run_at` should now show the
  configured offset (`-07:00` for Vancouver).
- Fire a test: `hermes cron run --profile <p> <job_id>` (returns "Ran now:
  succeeded"). Confirm `next_run_at` flipped to the new offset.
- Your 3pm job (e.g. catthew "Victoria 3 PM developmental game reminder")
  should now read `...T15:00:00-07:00` = 3:00pm Vancouver, not `-04:00`.
