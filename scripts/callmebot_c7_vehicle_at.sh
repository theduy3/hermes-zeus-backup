#!/usr/bin/env bash
# callmebot_c7_vehicle_at.sh — AT-TIME call reminder for Catthew "Vehicle maintenance odometer check" (9 AM Jun 30 / Dec 30).
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/callmebot_reminder.sh" "Catthew's vehicle maintenance odometer check is due now. Reply with current odometer, brake status, and any oil change done since the last check."
