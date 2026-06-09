#!/usr/bin/env bash
set -uo pipefail
BASE=/home/hermes/.hermes
PROFILES=(butter catthew charles finance thor zeus)
LOG_BASE="$BASE/profile-supervisor.log"
echo "[$(date -Iseconds)] profile supervisor starting" >> "$LOG_BASE"
while true; do
  for name in "${PROFILES[@]}"; do
    p="$BASE/profiles/$name"
    [ -d "$p" ] || continue
    if ! ps -eo args= | grep -F "hermes -p $name gateway run" | grep -v grep >/dev/null; then
      log_dir="$p/logs"
      mkdir -p "$log_dir"
      (
        unset TELEGRAM_BOT_TOKEN TELEGRAM_ALLOWED_USERS DISCORD_BOT_TOKEN
        unset API_SERVER_ENABLED API_SERVER_KEY API_SERVER_PORT API_SERVER_HOST API_SERVER_CORS_ORIGINS API_SERVER_MODEL_NAME
        [ -f "$p/.env" ] && { set -a; . "$p/.env"; set +a; }
        export HERMES_HOME="$p"
        exec /home/hermes/.local/bin/hermes -p "$name" gateway run
      ) >> "$log_dir/gateway.log" 2>&1 &
      echo "[$(date -Iseconds)] started $name pid=$!" >> "$LOG_BASE"
    fi
  done
  sleep 20
done
