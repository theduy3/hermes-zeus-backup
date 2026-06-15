#!/usr/bin/env bash
set -uo pipefail
BASE=/home/hermes/.hermes
PROFILES=(butter catthew charles finance thor zeus)
LOG_BASE="$BASE/profile-supervisor.log"
is_profile_gateway_running() {
  local profile_home="$1"
  local pid
  for pid in $(ps -eo pid=,args= | awk '/hermes gateway run/ && !/awk/ {print $1}'); do
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
