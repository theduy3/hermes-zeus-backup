#!/usr/bin/env bash
# callmebot_tasks_events.sh — daily generator for "tasks & events with a specific time".
#
# Runs once each morning (cron: e.g. 5:15 AM Toronto). It scans:
#   1) /vault/Tasks/tasks/*.md  for pending/in_progress tasks with BOTH due_date AND due_time
#   2) /vault/Tasks/calendar/*.md for events with a specific date+start time (not allDay)
# For each TODAY item it creates TWO one-off Hermes cron jobs that fire callmebot_reminder.sh:
#   - 30 minutes BEFORE the item time
#   - AT the item time
# The spoken message is the item title + time.
#
# Skips items already in the past, completed/cancelled, or not dated today.
# Emits output only if it scheduled something (else the cron delivery stays silent).
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CALL_BASENAME="callmebot_reminder.sh"   # CLI resolves under ~/.hermes/scripts/
TZ="${CALL_TZ:-America/Toronto}"
TASKS_DIR="${TASKS_DIR:-/vault/Tasks/tasks}"
CAL_DIR="${CAL_DIR:-/vault/Tasks/calendar}"

NOW_TS=$(TZ="$TZ" date +%s)
TODAY=$(TZ="$TZ" date +%Y-%m-%d)

log() { echo "[tasks-events-gen $(TZ="$TZ" date '+%H:%M')] $*"; }

# single-quote a message so it is a safe single arg for the script string
_q() { printf '%s' "$1" | sed "s/'/'\\\\''/g; 1s/^/'/; \$s/\$/'/"; }

# item epoch seconds
item_epoch() {
  local d="$1" t="$2"
  TZ="$TZ" date -d "${d} ${t:-00:00}" +%s 2>/dev/null || echo 0
}

sched_created=0

# schedule two calls. Args: title date time
schedule_item() {
  local title="$1" d="$2" t="$3"
  [ "$d" = "$TODAY" ] || { log "skip (not today): $title @ $d $t"; return 0; }
  local ep at_ep before_ep at_iso before_iso
  ep=$(item_epoch "$d" "$t")
  [ "$ep" -eq 0 ] && return 0
  [ "$ep" -lt "$NOW_TS" ] && { log "skip past: $title @ $d $t"; return 0; }
  at_ep=$ep
  before_ep=$(( ep - 30*60 ))
  at_iso=$(TZ="$TZ" date -d "@$at_ep" '+%Y-%m-%dT%H:%M:00')
  before_iso=$(TZ="$TZ" date -d "@$before_ep" '+%Y-%m-%dT%H:%M:00')
  local msg_at="Reminder: $title at $t."
  local msg_before="Heads up in 30 minutes: $title at $t."
  if [ "$before_ep" -gt "$NOW_TS" ]; then
    hermes cron create "$before_iso" "CALL 30m before: $title ($d $t)" --no-agent --script "$CALL_BASENAME $( _q "$msg_before" )" >/dev/null 2>&1 \
      && sched_created=$((sched_created+1))
  fi
  hermes cron create "$at_iso" "CALL at time: $title ($d $t)" --no-agent --script "$CALL_BASENAME $( _q "$msg_at" )" >/dev/null 2>&1 \
    && sched_created=$((sched_created+1))
  log "scheduled calls for: $title @ $d $t"
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
