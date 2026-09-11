#!/usr/bin/env bash
# callmebot_tasks_events.sh — daily generator for "tasks & events with a specific time".
#
# Runs once each morning (cron: e.g. 5:15 AM local). It scans:
#   1) /vault/Tasks/tasks/*.md  for pending/in_progress tasks with BOTH due_date AND due_time
#   2) /vault/Tasks/calendar/*.md for events with a specific date+start time (not allDay)
# For each TODAY item it creates TWO one-off Hermes cron jobs that fire CallMeBot:
#   - 30 minutes BEFORE the item time
#   - AT the item time
#
# CRITICAL (verified):
# - Hermes cron `script` is a path only. Args are NOT forwarded (`_run_job_script` argv =
#   bash + path). Never pass `callmebot_reminder.sh 'msg'` — that becomes Script not found.
# - Bake the spoken text into a tiny wrapper under scripts/callme_once/.
# - Emit ISO-8601 *with offset* so `hermes cron create` cannot reinterpret wall time in
#   another zone (bare `YYYY-MM-DDTHH:MM:00` caused +3h PDT/EDT skew).
#
# Skips items already in the past, completed/cancelled, or not dated today.
# Emits output only if it scheduled something (else the cron delivery stays silent).
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CALL_BASE="$SCRIPT_DIR/callmebot_reminder.sh"
ONCE_DIR="$SCRIPT_DIR/callme_once"
# Prefer CALL_TZ, then HERMES_TIMEZONE (profile gateway), then America/Toronto.
TZ="${CALL_TZ:-${HERMES_TIMEZONE:-America/Toronto}}"
TASKS_DIR="${TASKS_DIR:-/vault/Tasks/tasks}"
CAL_DIR="${CAL_DIR:-/vault/Tasks/calendar}"

mkdir -p "$ONCE_DIR"

NOW_TS=$(TZ="$TZ" date +%s)
TODAY=$(TZ="$TZ" date +%Y-%m-%d)
OFFSET=$(TZ="$TZ" date +%z)  # e.g. -0400
# ISO offset with colon: -04:00
OFFSET_ISO="${OFFSET:0:3}:${OFFSET:3:2}"

log() { echo "[tasks-events-gen $(TZ="$TZ" date '+%H:%M %Z')] $*"; }

# slug for wrapper filename
_slug() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/-+/-/g' | cut -c1-60
}

# write wrapper that calls callmebot_reminder.sh with a fixed message
write_wrapper() {
  local file="$1" msg="$2"
  cat >"$file" <<EOF
#!/usr/bin/env bash
set -uo pipefail
SCRIPT_DIR="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")" && pwd)"
exec "\$SCRIPT_DIR/../callmebot_reminder.sh" $(printf '%q' "$msg")
EOF
  chmod 700 "$file"
}

# item epoch seconds in TZ
item_epoch() {
  local d="$1" t="$2"
  TZ="$TZ" date -d "${d} ${t:-00:00}" +%s 2>/dev/null || echo 0
}

sched_created=0

# schedule two calls. Args: title date time
schedule_item() {
  local title="$1" d="$2" t="$3"
  [ "$d" = "$TODAY" ] || { log "skip (not today): $title @ $d $t"; return 0; }
  local ep at_ep before_ep at_iso before_iso slug w_before w_at
  ep=$(item_epoch "$d" "$t")
  [ "$ep" -eq 0 ] && return 0
  [ "$ep" -lt "$NOW_TS" ] && { log "skip past: $title @ $d $t"; return 0; }
  at_ep=$ep
  before_ep=$(( ep - 30*60 ))
  # ISO with explicit offset — do not omit zone
  at_iso=$(TZ="$TZ" date -d "@$at_ep" "+%Y-%m-%dT%H:%M:00${OFFSET_ISO}")
  before_iso=$(TZ="$TZ" date -d "@$before_ep" "+%Y-%m-%dT%H:%M:00${OFFSET_ISO}")
  local msg_at="Reminder: $title at $t."
  local msg_before="Heads up in 30 minutes: $title at $t."
  slug="$(_slug "$title-$d-$t")"
  [ -z "$slug" ] && slug="item-$at_ep"

  if [ "$before_ep" -gt "$NOW_TS" ]; then
    w_before="callme_once/${slug}-30m.sh"
    write_wrapper "$ONCE_DIR/${slug}-30m.sh" "$msg_before"
    if hermes cron create "$before_iso" "CALL 30m before: $title ($d $t)" --no-agent --script "$w_before" >/dev/null 2>&1; then
      sched_created=$((sched_created+1))
    else
      log "FAILED create 30m job for $title ($before_iso)"
    fi
  fi
  w_at="callme_once/${slug}-at.sh"
  write_wrapper "$ONCE_DIR/${slug}-at.sh" "$msg_at"
  if hermes cron create "$at_iso" "CALL at time: $title ($d $t)" --no-agent --script "$w_at" >/dev/null 2>&1; then
    sched_created=$((sched_created+1))
  else
    log "FAILED create at-time job for $title ($at_iso)"
  fi
  log "scheduled calls for: $title @ $d $t ($TZ) at=$at_iso before=$before_iso"
}

# ---- 1) Tasks with specific due_time ----
if [ -d "$TASKS_DIR" ]; then
  for f in "$TASKS_DIR"/*.md; do
    [ -e "$f" ] || continue
    d=""; t=""; status=""; tags=""
    in_fm=0
    while IFS= read -r line; do
      case "$line" in
        '---') [ "$in_fm" -eq 0 ] && { in_fm=1; continue; } || break ;;
      esac
      [ "$in_fm" -eq 1 ] || continue
      case "$line" in
        due_date:*) d="${line#due_date:}"; d="$(echo "$d" | tr -d '[:space:]')" ;;
        due_time:*) t="${line#due_time:}"; t="$(echo "$t" | tr -d '[:space:]')" ;;
        status:*)   status="${line#status:}"; status="$(echo "$status" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')" ;;
        tags:*)     tags="${line#tags:}"; tags="$(echo "$tags" | tr -d '[:space:]')" ;;
      esac
    done < "$f"
    case "$status" in completed|done|cancelled|canceled|blocked) continue ;; esac
    case "$tags" in *catthew*) continue ;; esac   # household tasks -> family group, not user phone
    [ -z "$d" ] && continue
    [ -z "$t" ] && continue
    title="$(basename "$f" .md)"
    schedule_item "$title" "$d" "$t"
  done
fi

# ---- 2) Calendar events with specific start time (not allDay) ----
if [ -d "$CAL_DIR" ]; then
  for f in "$CAL_DIR"/*.md; do
    [ -e "$f" ] || continue
    c_title=""; c_date=""; c_start=""; c_allday=""; c_done=""
    in_fm=0
    while IFS= read -r line; do
      case "$line" in
        '---') [ "$in_fm" -eq 0 ] && { in_fm=1; continue; } || break ;;
      esac
      [ "$in_fm" -eq 1 ] || continue
      case "$line" in
        title:*)    c_title="${line#title:}"; c_title="$(echo "$c_title" | sed 's/^ *//')" ;;
        date:*)     c_date="${line#date:}"; c_date="$(echo "$c_date" | tr -d '[:space:]')" ;;
        start:*)    c_start="${line#start:}"; c_start="$(echo "$c_start" | tr -d '[:space:]')" ;;
        allDay:*)   c_allday="${line#allDay:}"; c_allday="$(echo "$c_allday" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')" ;;
        completed:*) c_done="${line#completed:}"; c_done="$(echo "$c_done" | tr -d '[:space:]')" ;;
      esac
    done < "$f"
    [ -n "$c_done" ] && continue
    [ "$c_allday" = "true" ] && continue
    [ -z "$c_start" ] && continue
    [ -z "$c_date" ] && continue
    c_time="${c_start:0:5}"
    schedule_item "$c_title" "$c_date" "$c_time"
  done
fi

log "done. created $sched_created call job(s) for today."
if [ "$sched_created" -gt 0 ]; then
  echo "Scheduled $sched_created phone-call reminder(s) for timed tasks/events today."
fi
