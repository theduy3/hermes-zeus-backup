# Docker multi-profile gateway hardening

Use this when multiple Hermes profile gateways run inside one Docker container and the user wants them to stay healthy without daily manual fixes.

## Durable failure pattern

Symptoms:

- `hermes gateway status` shows profile gateways running, but each profile process has `HERMES_HOME=/home/hermes/.hermes` instead of `/home/hermes/.hermes/profiles/<name>`.
- Profile logs repeatedly show `api_server` port conflicts such as `Port 8642 already in use`.
- Restarting profile gateways may leave token lock files pointing at zombie PIDs, causing `Telegram bot token already in use (PID X)` even after the old process was terminated.

Root causes:

- Docker entrypoint launches `hermes -p <profile> gateway run` while inheriting main `HERMES_HOME`.
- Parent/container environment includes `API_SERVER_*`; every profile tries to enable the API server on the same port.
- Read-only mounted entrypoint may be impossible to patch in-place, so hardening must happen in writable Hermes paths.

## Fix pattern

1. Verify process environment before changing anything.

```bash
for pid in $(pgrep -f 'hermes -p .*gateway run' | sort -n); do
  cmd=$(tr '\0' ' ' < /proc/$pid/cmdline 2>/dev/null || true)
  hh=$(tr '\0' '\n' < /proc/$pid/environ 2>/dev/null | grep '^HERMES_HOME=' || true)
  echo "$pid $hh :: $cmd"
done
```

2. If the read-only entrypoint cannot be edited, patch the writable Hermes console script wrapper (`~/.hermes/hermes-agent/venv/bin/hermes`) so only profile gateway runs are affected:

```python
# Before importing hermes_cli.main:
# if argv contains `-p/--profile <name>` plus `gateway run`, set:
os.environ['HERMES_HOME'] = str(Path.home() / '.hermes' / 'profiles' / profile)
for key in (
    'API_SERVER_ENABLED', 'API_SERVER_KEY', 'API_SERVER_PORT', 'API_SERVER_HOST',
    'API_SERVER_CORS_ORIGINS', 'API_SERVER_MODEL_NAME',
):
    os.environ.pop(key, None)
```

Keep this surgical: do not change normal `hermes chat`, default gateway, or non-gateway profile commands unless needed.

3. If killing old profile children would make the read-only entrypoint exit PID 1, freeze the entrypoint parent first, then stop only the old bad profile gateway children:

```bash
kill -STOP <entrypoint-parent-pid>
for pid in <old-profile-pids>; do kill -TERM "$pid" 2>/dev/null || true; done
sleep 3
for pid in <old-profile-pids>; do kill -KILL "$pid" 2>/dev/null || true; done
```

4. Start a writable profile supervisor script under `~/.hermes/scripts/` that launches each profile with:

```bash
unset TELEGRAM_BOT_TOKEN TELEGRAM_ALLOWED_USERS DISCORD_BOT_TOKEN
unset API_SERVER_ENABLED API_SERVER_KEY API_SERVER_PORT API_SERVER_HOST API_SERVER_CORS_ORIGINS API_SERVER_MODEL_NAME
[ -f "$profile_dir/.env" ] && { set -a; . "$profile_dir/.env"; set +a; }
export HERMES_HOME="$profile_dir"
exec /home/hermes/.local/bin/hermes -p "$name" gateway run
```

Use `terminal(background=true)` for the supervisor; avoid shell-level `nohup ... &` in foreground terminal calls.

5. Clean stale token locks, including zombie-PID locks.

```python
import glob, json, os
for path in glob.glob('/home/hermes/.local/state/hermes/gateway-locks/*.lock'):
    data = json.load(open(path))
    pid = int(data.get('pid', -1))
    stat = open(f'/proc/{pid}/stat').read().split()[2] if os.path.exists(f'/proc/{pid}/stat') else None
    if stat == 'Z' or pid <= 0 or not os.path.exists(f'/proc/{pid}'):
        os.remove(path)
```

6. Verify every profile after restart:

```bash
hermes gateway status
for p in butter catthew charles finance thor zeus; do
  echo "--- $p"
  tail -300 ~/.hermes/profiles/$p/logs/gateway.log | grep -E 'Active profile:|✓ telegram connected|Gateway running with|Port 8642|token already|polling conflict|Could not parse'
done
```

Success criteria:

- Every profile PID is present in `hermes gateway status`.
- Every profile gateway process has `HERMES_HOME=~/.hermes/profiles/<name>`.
- Current startup window shows `✓ telegram connected` and `Gateway running with 1 platform(s)`.
- No current-startup `api_server` port conflict, polling conflict, or auth failure.

## Watchdog pattern

Add a no-agent cron watchdog that stays silent when healthy and alerts only on live issues:

- Missing default/profile gateway process.
- Profile gateway process with wrong `HERMES_HOME`.
- Current startup window contains `polling conflict`, `token already in use`, Codex auth failure, or `Port 8642 already in use`.

Important: scan only the latest startup window, not the whole log, otherwise resolved startup failures keep triggering false positives.

## Pitfalls

- `hermes gateway restart` may refuse from inside a gateway process. Use shell/process-level restart mechanics instead.
- `patch`/atomic rename may fail on mounted read-only or busy entrypoint scripts. Use writable Hermes paths or in-place shell/Python only where safe.
- A lock PID that exists can still be stale if it is a zombie (`STAT Z`). Treat zombie lock owners as stale.
- Do not record “Telegram is broken” or “api_server is broken”; the durable fix is environment isolation plus stale-lock cleanup.
