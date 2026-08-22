#!/usr/bin/env bash
# callmebot_c7_vehicle.sh — call-reminder wrapper for Catthew "Vehicle maintenance odometer check".
# The base job fires 9:00 AM on Jun 30 and Dec 30. This wrapper adds the +30min-before call.
# Scheduled by Hermes: 8:30 AM on the same dates (cron expr: 30 8 30 6,12 *).
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/callmebot_reminder.sh" "Heads up: in 30 minutes, Catthew's vehicle maintenance odometer check reminder at 9 AM. Reply with current odometer, brake status, and any oil change done."
