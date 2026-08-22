#!/usr/bin/env bash
# callmebot_reminder.sh — place a spoken reminder via CallMeBot.
#
# Primary: Telegram in-app voice call (bot rings you inside Telegram, speaks TTS).
#   No API key required — only a one-time authorization of @CallMeBot to your @username.
# Also supports real PSTN phone call if CALLMEBOT_KEY + a +phone USER are set.
#
# Usage:
#   callmebot_reminder.sh "Pick up Victoria at 3:45pm" [lang]
#   callmebot_reminder.sh "Reminder text"            # defaults lang=en-US-Standard-B
#
# Designed to be fired by a one-off Hermes cron job (no_agent=true, script=this file).
# Exit 0 on dispatch (or if CallMeBot reports already-queued); non-zero on hard error.

set -uo pipefail

CONF="${CALLMEBOT_CONF:-/home/hermes/.hermes/scripts/callmebot.conf}"
if [ -f "$CONF" ]; then
  # shellcheck disable=SC1090
  u="$(grep -E '^[[:space:]]*USER=' "$CONF" | head -1 | cut -d= -f2- | tr -d '[:space:]')"
  k="$(grep -E '^[[:space:]]*CALLMEBOT_KEY=' "$CONF" | head -1 | cut -d= -f2- | tr -d '[:space:]')"
fi
USER="${u:-}"
CALLMEBOT_KEY="${CALLMEBOT_KEY:-${k:-}}"

: "${USER:?CallMeBot USER (@username or +phone) not set in $CONF}"

MSG="${1:-Reminder}"
LANG="${2:-en-US-Standard-B}"

if [[ "$USER" == @* ]]; then
  ENDPOINT="https://api.callmebot.com/start.php"
  resp="$(curl -sL --max-time 30 -G \
    --data-urlencode "source=hermes" \
    --data-urlencode "user=$USER" \
    --data-urlencode "text=$MSG" \
    --data-urlencode "lang=$LANG" \
    "$ENDPOINT")"
else
  : "${CALLMEBOT_KEY:?CALLMEBOT_KEY required for PSTN phone calls (set in $CONF)}"
  ENDPOINT="https://api.callmebot.com/call.php"
  resp="$(curl -sL --max-time 30 -G \
    --data-urlencode "phone=$USER" \
    --data-urlencode "text=$MSG" \
    --data-urlencode "lang=$LANG" \
    --data-urlencode "key=$CALLMEBOT_KEY" \
    "$ENDPOINT")"
fi

# Reduce HTML noise to a single readable line for the cron output log.
clean="$(printf '%s' "$resp" | sed -e 's/<[^>]*>//g' -e 's/&nbsp;/ /g' -e 's/  */ /g')"
printf '%s\n' "$clean"

# CallMeBot signals failure with a warning glyph / explicit error words.
case "$resp" in
  *⚠️*|*WARNING*|*Wrong\ APIkey*|*not\ authorized*|*not\ allowed*|*disabled*)
    # Surface the one-time authorization link so the user can finish setup.
    auth="$(printf '%s' "$resp" | grep -oiE 'href="[^"]*auth[^"]*"' | head -1 | sed 's/href=\"//;s/\"//')"
    [ -n "$auth" ] && echo "Authorize CallMeBot once: $auth" >&2
    echo "CALLMEBOT_ERROR: dispatch rejected" >&2
    exit 1 ;;
  *)
    echo "CallMeBot voice call dispatched to $USER" ;;
esac
