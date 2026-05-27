# Daily Morning Briefing Synthesis

Use this when producing an info-only morning briefing from vault notes plus live data.

## Input sources
- Latest family briefing output from `~/.hermes/profiles/catthew/cron/output/<job-id>/` — read the most recent file.
- Latest Daily note from `/vault/Daily/` for **today's Eastern date** during the Quebec/East Coast trip.
- If today's Daily note does not exist, use the most recent Daily note instead.

## Extraction rules
- Keep only calendar/context items: appointments, visits, family events, timing, and travel context.
- Exclude chores, grocery lists, errands, reminders, checkbox tasks, and action lists unless they are time-sensitive appointments.
- Strip Obsidian markup to clean plaintext:
  - `[[Page]]` → `Page`
  - `[[Page|label]]` → `label`
  - remove `#tag`, `==highlight==`, `**bold**`, and extra brackets

## Output rules
- Keep the briefing compact and scannable.
- Do not include task lists, reminders, overdue items, or checkboxes.
- If there is no useful new context, return `[SILENT]`.

## Practical note
- When the vault is available in Docker, probe `/vault/` first and use it if writable.
- If today's Daily note appears in `find`/file listings but `read_file` says not found or content search reports `Permission denied`, treat it as an access problem rather than a missing note. Use a small Python/pathlib stat/read probe to confirm permissions, report the vault permission issue briefly, and fall back to the most recent readable Daily note.
- For delegated headline sections, do not trust subagent links blindly. Verify returned URLs when practical; if links 404 or the subagent reports inability to verify, replace them with fresh current-source/RSS results before finalizing.