# Event reminder tasks

Use this pattern when Duy asks to track a public schedule (sports tournaments, concerts, flights, festivals, TV releases) and add reminders as Obsidian tasks.

## Workflow

1. Load `obsidian` and verify `/vault/Tasks/tasks` exists and is writable.
2. Search existing task files for event keywords before creating new reminders to avoid duplicates.
3. Pull the schedule from a current source, then normalize all times to Duy's active local timezone. For Vancouver/Pacific, include `PDT`/`PST` in the task body.
4. Create one task per event under `/vault/Tasks/tasks/<kebab-title>.md` with:
   - `type: task`
   - `due_date: YYYY-MM-DD`
   - `tags: [personal, event-reminder, ...domain...]`
   - `status: pending`
5. Put the actual start/kickoff time in the body, not only in the filename/frontmatter, because the task system only keys on date.
6. Add a short note explaining why the event was selected if the user asked for “anticipated”, “important”, “must-watch”, etc.
7. Verify by reading back at least one created file and listing the matching filenames.
8. If the user asks “give me the list”, return a concise date/time list grouped chronologically; omit file paths unless asked.

## Selection rules

- If the user asks for “all” games involving a team, include every known match for that team plus conditional knockout reminders/checkpoints if qualification depends on results.
- If the user asks for “most anticipated” or “marquee”, include a curated subset and label it as curated; do not imply it is the full schedule.
- For tournaments where knockout participants are TBD, create checkpoint tasks after group-stage completion and conditional “possible match” reminders only when they are useful.

## Pitfalls

- Do not create reminders only in `/home/hermes`; tasks must live in `/vault/Tasks/tasks/` to show in Obsidian.
- Do not store start time only in `due_date` — frontmatter supports date, not time.
- Do not ask the user to pick timezone if active travel/timezone context is already known; use the active timezone and state it in the final reply.
