#!/usr/bin/env bash
# callmebot_c9_humidifier.sh — call-reminder wrapper for Catthew "Weekly clean humidifier reminder".
# Base job: Wed 8:00 PM. This wrapper adds the +30min-before call (Wed 7:30 PM).
# Scheduled by Hermes: 30 20 * * 3 (the at-time call reuses the original reminder text spoken aloud).
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/callmebot_reminder.sh" "Reminder: clean the humidifier (weekly household task). This is your 30-minute heads up before the 8 PM reminder."
