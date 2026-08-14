# Google Calendar task sync — Catthew / Kittyggup Family

Session learning: Catthew task creation should write to both the Obsidian task vault and the Google Calendar chosen by Sir.

## Target calendar

- Name: Kittyggup Family
- Calendar ID: `05a625d510ad884bcedf222735efe0ab5926b8b43f20e4b80493d84309466802@group.calendar.google.com`
- Timezone: `America/Vancouver`
- Required OAuth scope for writing: `https://www.googleapis.com/auth/calendar`

## Creation workflow

When Sir says `new task:` or otherwise asks Catthew to create a dated/timed household task:

1. Check `/vault/Tasks/tasks/` for a duplicate filename/content.
2. Create the Markdown file under `/vault/Tasks/tasks/<kebab-title>.md`.
3. Include frontmatter:
   ```yaml
   ---
   type: task
   due_date: YYYY-MM-DD
   due_time: "HH:MM"   # if timed
   tags: [catthew, ...]
   status: pending
   google_calendar_id: <event id>  # after calendar creation
   ---
   ```
4. Body should include an Obsidian checkbox (`- [ ] ...`) and `#catthew`.
5. If dated/timed, create a Google Calendar event on Kittyggup Family using Pacific time.
6. Store the returned event ID in `google_calendar_id` in the task note.
7. Verify by reading the task file and fetching/listing the calendar event before confirming to Sir.

## Calendar event conventions

- Timed task: use `dateTime` start/end with `timeZone: America/Vancouver`.
- Untimed full-day task: use all-day `date` start and exclusive next-day `date` end.
- Description should mention the vault path and `#catthew` tag.
- For events with an explicit range in the user text, preserve the range exactly.
- For tasks with only a start time, default to 30 minutes unless the task class implies otherwise.

## Existing task backfill pattern

If Sir says tasks are missing from Kittyggup Family:

1. Scan `/vault/Tasks/tasks` and `/vault/Tasks/bugs`.
2. Include only files with `catthew` frontmatter tag or literal `#catthew` in the body.
3. Skip completed tasks and tasks already containing `google_calendar_id`.
4. Create events on Kittyggup Family for pending tasks with `due_date`.
5. Patch each task note with the returned `google_calendar_id`.
6. Report created vs skipped counts.

## OAuth troubleshooting learned

- If broad Google Workspace consent hangs or produces errors, reduce OAuth to Calendar only.
- For read-only briefings: `https://www.googleapis.com/auth/calendar.readonly`.
- For task sync/write: `https://www.googleapis.com/auth/calendar`.
- Use the OAuth JSON’s exact redirect URI if `localhost:1` causes trouble; in this session `http://localhost` worked.
- Have Sir open auth links in Safari/Chrome rather than Telegram’s in-app browser.
- If the app is in Testing, add `duynt1989@gmail.com` as a Google Cloud OAuth test user.
