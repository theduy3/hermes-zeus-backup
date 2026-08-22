# Wrapped call-reminders — live wiring (as of 2026-08-21)

Captures the concrete cron jobs + scripts that wrap existing reminders with
phone calls, so a future session knows the current state without re-deriving it.

## Scope
Profiles in scope (user chose "for now"): **zeus, catthew**.
Out of scope this build: charles, finance, butter, thor, wiki, default.

## Fixed recurring reminders (known cron time → pair of call jobs)
Each reminder gets TWO `no_agent` cron jobs pointing at wrapper scripts:
one at the exact time, one 30 min before.

| Source reminder | 30-min-before job | at-time job | Wrapper scripts |
|---|---|---|---|
| Catthew "Vehicle maintenance odometer check" (9 AM Jun 30 & Dec 30) | cron `30 8 30 6,12 *` | cron `0 9 30 6,12 *` | `callmebot_c7_vehicle.sh` / `callmebot_c7_vehicle_at.sh` |
| Catthew "Weekly clean humidifier reminder" (8 PM Wed) | cron `30 20 * * 3` | cron `0 20 * * 3` | `callmebot_c9_humidifier.sh` / `callmebot_c9_humidifier_at.sh` |

## Dynamic "tasks & events with a specific time" digest
- Generator: `callmebot_tasks_events.sh`, cron `15 5 * * *` (5:15 AM, Toronto).
- Scans each morning for items DATED TODAY:
  - `/vault/Tasks/tasks/*.md` — tasks with BOTH `due_date` + `due_time`,
    `status` not in {completed,done,cancelled,canceled,blocked}, and NOT tagged
    `catthew` (household tasks go to the family group, not the user's phone).
  - `/vault/Tasks/calendar/*.md` — events with a real `start` time,
    `allDay: false`, and not `completed`.
- For each match it creates TWO one-off call jobs via
  `hermes cron create "<ISO>" "name" --no-agent --script "callmebot_reminder.sh '<msg>'"`:
  one 30 min before, one at the time. Emits output only if it scheduled something.

## Notes for future sessions
- Generator-created jobs land in the **default** profile's `jobs.json`
  regardless of which profile the source task/event "belongs" to — calls fire to
  the user's phone either way. That's intended.
- Server is UTC; the gateway runs cron in the user's local tz (America/Toronto).
  `date` calls in the generator use `TZ=America/Toronto`.
- Free CallMeBot = a few calls/day. C7 fires 2 days/yr, C9 once/wk, and the
  generator only creates calls for items dated *today* — stays within fair-use.
- Calendar times are messy (`earnings-*` = `"Aftermarketclose"`,
  flights = `"8:35PMEDT"`); none parse as `HH:MM` so they're safely skipped.
  Only clean `HH:MM`/`HH:MM:SS` times schedule a call.
- Verified 2026-08-21: real spoken call dispatched to `@theduynguyen` through
  the cron script path; generator dry-run + live test created/cleaned 4 call
  jobs correctly.

## How to extend
- Add a fixed reminder: write a `callmebot_<tag>.sh` + `callmebot_<tag>_at.sh`
  wrapper pair, then `cronjob create` two jobs (basename-only script path).
- Add a profile to the dynamic set: nothing to change — the generator already
  reads all of `/vault/Tasks/tasks` + `/vault/Tasks/calendar`. Just stop
  excluding that profile's tasks (e.g. allow `catthew`-tagged) if desired.
