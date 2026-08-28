#!/usr/bin/env bash
set -uo pipefail
BASE=/home/hermes/.hermes
PROFILES=(butter catthew charles finance thor zeus)
LOG_BASE="$BASE/profile-supervisor.log"
is_profile_gateway_running() {
  # Match live python hermes gateway procs by HERMES_HOME.
  # Do NOT require contiguous "hermes gateway run" in args — supervisor launches
  #   python3 .../hermes -p <name> gateway run
  # so "hermes" and "gateway" are separated by -p <name>.
  local profile_home="$1"
  local pid cmd
  for pid in /proc/[0-9]*; do
    pid="${pid##*/}"
    [[ "$pid" =~ ^[0-9]+$ ]] || continue
    cmd=$(tr '\0' ' ' < "/proc/$pid/cmdline" 2>/dev/null) || continue
    # real gateway adapter only (python ... hermes ... gateway run|restart)
    # not bash entrypoint wrappers or this supervisor script
    case "$cmd" in
      *python*hermes*gateway*run*|*python*hermes*gateway*restart*) ;;
      *) continue ;;
    esac
    tr '\0' '\n' < "/proc/$pid/environ" 2>/dev/null | grep -Fx "HERMES_HOME=$profile_home" >/dev/null && return 0
  done
  return 1
}

echo "[$(date -Iseconds)] profile supervisor starting" >> "$LOG_BASE"
while true; do
  for name in "${PROFILES[@]}"; do
    p="$BASE/profiles/$name"
    [ -d "$p" ] || continue
    if ! is_profile_gateway_running "$p"; then
      log_dir="$p/logs"
      mkdir -p "$log_dir"
      (
        unset TELEGRAM_BOT_TOKEN TELEGRAM_ALLOWED_USERS DISCORD_BOT_TOKEN
        unset API_SERVER_ENABLED API_SERVER_KEY API_SERVER_PORT API_SERVER_HOST API_SERVER_CORS_ORIGINS API_SERVER_MODEL_NAME
        unset HERMES_TIMEZONE
        [ -f "$p/.env" ] && { set -a; . "$p/.env"; set +a; }
        export HERMES_HOME="$p"
        tz_cfg="$(/home/hermes/.hermes/hermes-agent/venv/bin/python3 - "$p/config.yaml" <<'PY'
import sys, yaml
path = sys.argv[1]
try:
    cfg = yaml.safe_load(open(path, encoding='utf-8')) or {}
    tz = cfg.get('timezone', '')
    print(tz.strip() if isinstance(tz, str) else '')
except Exception:
    print('')
PY
)"
        [ -n "$tz_cfg" ] && export HERMES_TIMEZONE="$tz_cfg"
        exec /home/hermes/.local/bin/hermes -p "$name" gateway run
      ) >> "$log_dir/gateway.log" 2>&1 &
      echo "[$(date -Iseconds)] started $name pid=$!" >> "$LOG_BASE"
    fi
  done
  sleep 20
done
