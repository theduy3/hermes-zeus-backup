#!/usr/bin/env bash
# callmebot_c9_humidifier_at.sh — AT-TIME call reminder for Catthew "Weekly clean humidifier reminder" (Wed 8 PM).
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/callmebot_reminder.sh" "Reminder: clean the humidifier (weekly household task). This is the 8 PM reminder."
