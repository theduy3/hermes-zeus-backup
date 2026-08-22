---
name: task-calendar-reminder-automation
description: Maintain Duy's Obsidian/Telegram/Google Calendar task-event-reminder pipeline without mixing item classes.
---

# Task / Event / Reminder Automation

Use when Duy asks to create, fix, review, or debug tasks, calendar events, earnings reminders, Telegram task cards, Pomodoro schedule reminders, or Obsidian Full Calendar sync.

## Core taxonomy — do not mix classes

Duy uses three distinct item types:

1. **Task**
   - Frontmatter: `type: task`
   - Source: `/vault/Tasks/tasks/*.md`
   - Sync: Obsidian/theduyvault + Google `theduy calendar`
   - Telegram: may get a task card with **Done/More buttons**
   - Example: `OC Accounting Fix for Vui`

2. **Event**
   - Frontmatter: `type: event`
   - Source: `/vault/Tasks/tasks/*.md` for sync compatibility
   - Sync: Obsidian/theduyvault + Google `theduy calendar`
   - Telegram: **no Done button**; not an actionable task
   - Examples: earnings dates, specific-time public/company events

3. **Reminder**
   - No durable vault note unless explicitly requested
   - No Google Calendar sync
   - Telegram only, plain message
   - Example: Daily Schedule / Pomodoro reminder

If Duy says “this is not a task,” patch the sender/filter first so it cannot recur, then convert existing records.

## Duy-specific rules

- Daily schedule reminders are one-line time labels only:
  - Good: `🗓 9:05–9:30 — Pomodoro 1 — Deep Work`
  - Bad: `☐ Confirm Top 3 and fixed appointments`
  - Bad: task/checklist text, instructions, Done/Log buttons, or “what to do” content.
- Work reminders use 25-minute Pomodoro sessions.
- Specific-time events/tasks stay fixed; do not feed them into Pomodoro reminders.
- Due-task drip sends only `due_date == today`, not overdue. Duy moves overdue tasks manually during planning.
- Catthew/family tasks remain separate; do not route business/finance/personal tasks to Kitty/Family calendar or add `#catthew` just for visibility.
- Zeus sync target is Duy's Google `theduy calendar`; Catthew uses family calendar separately.

## Operational files

- Daily plan generator: `/home/hermes/.hermes/profiles/zeus/scripts/generate_daily_plan.py`
- Due task Telegram cards: `/home/hermes/.hermes/profiles/zeus/scripts/due_task_drip.py`
- Daily Pomodoro reminders: `/home/hermes/.hermes/profiles/zeus/scripts/send_daily_schedule_reminder.py`
- Obsidian → Google Calendar sync: `/home/hermes/.hermes/profiles/zeus/scripts/sync_obsidian_tasks_to_theduy_calendar.py`
- Google Calendar → Obsidian task import: `/home/hermes/.hermes/profiles/zeus/scripts/import_theduy_calendar_tasks.py`
- Full Calendar adoption/render sync: `/vault/System/scripts/sync-calendar-events.py`
- Major/watchlist earnings importer: `/home/hermes/.hermes/profiles/zeus/scripts/fetch_major_earnings_reminders.py`
- Watchlist source: `/vault/System/Stock Watchlist.md`

## Fix patterns

### Telegram task cards showing events

1. Patch `due_task_drip.py` to require `type: task`.
2. Add explicit skip for earnings/event sources/tags if needed.
3. Convert existing event-like files from `type: task` to `type: event`.
4. Verify `due_task_drip.py --dry-run` does not select events.

### Earnings reminders

- Earnings are **events**, not tasks.
- Existing and new earnings files should use:
  - `type: event`
  - `due_date: YYYY-MM-DD`
  - `due_time: "Before market open" | "After market close" | "Time not confirmed"`
  - `time_block: fixed`
  - `tags: [finance, stocks, earnings]`
- Sync to `theduy calendar` via the Zeus Obsidian sync.
- Do not send Done buttons for earnings.
- Quarterly importer runs Jan/Apr/Jul/Oct and should include both major names and Duy's watchlist.
- Watchlist is `/vault/System/Stock Watchlist.md`; add listed tickers there first.
- For unusual/new tickers that Nasdaq misses, use a narrow fallback in `fetch_major_earnings_reminders.py` rather than scanning yfinance for every ticker if that causes timeouts.

### Full Calendar orphan stubs

Duy may drag/create items in Obsidian Full Calendar. Those can become orphan stubs under `/vault/Tasks/calendar/*.md` that are visible in Obsidian but invisible to Telegram/GCal. Fix by adopting current/future unfinished orphan stubs into canonical `/vault/Tasks/tasks/*.md`, then regenerating calendar mirrors. Do not treat `/vault/Tasks/calendar` as source of truth.

### Morning briefing wrong today tasks

The briefing must not substitute future/high-priority backlog for due-today items. Ensure generated daily plan has:
- `## Today Tasks` = authoritative due-today non-fixed tasks
- `## Fixed` = specific-time tasks/events
- `## Top 3` derived from today tasks when available

The morning briefing prompt should read Today Tasks and include every item there.

### Changing a recurring schedule anchor (multi-file cascade)

Duy's time anchors (pickup, exercise window, brunch, company-review rotation, deep-work window) are **hardcoded in many files**, not configured in one place. Changing any anchor is a coordinated cascade — editing only one file leaves briefings, plans, and reminders disagreeing.

Anchor-bearing files (full map + grep tokens in `references/schedule-anchor-cascade.md`):

- `scripts/generate_daily_plan.py` (BLOCKS, constraints text, pickup line, exercise label)
- `scripts/send_daily_schedule_reminder.py` (WINDOWS, fallback/transition text)
- `scripts/planned_task_drip.py` (Protected summary, shutdown text)
- `cron/jobs.json` (Morning + Evening briefing prompts)
- `skills/note-taking/obsidian/SKILL.md` and its `references/time-blocked-planning.md`, `references/zeus-task-calendar-earnings-pomodoro.md`
- `skills/devops/cron-job-patterns/SKILL.md` ("Approved Duy schedule constraints")
- already-generated `/vault/Tasks/planning/YYYY-MM-DD.md` (including future-dated plans)

Procedure:

1. `grep -r` the old time tokens across `~/.hermes` and `/vault/Tasks/planning` (`2:45`, `2:35`, `Pick up Victoria`, `pickup transition`, `before Victoria pickup`, `Deep work only between`).
2. **Clarify scope before editing** — when shifting one anchor, ask whether adjacent blocks shift too (e.g. pickup transition, or moving exercise to a different part of the day). Use `clarify` in a live session; cron runs cannot ask.
3. Edit each source consistently. For cron prompts, patch `jobs.json` in place (see cron-job-patterns: "Editing a Job Prompt In-Place").
4. Regenerate or hand-edit future-dated `/vault/Tasks/planning/*.md`.
5. `python3 -m py_compile` the edited scripts and re-run the verification dry-runs.

When an anchor moves, the pre-brunch deep-work/Pomodoro `BLOCKS` may need restructuring, not just relabeling — Duy has moved exercise to a morning window after daycare drop-off while keeping pickup in the afternoon. Treat `BLOCKS` as negotiable.

## Verification checklist

After changes, run the relevant dry-runs/compiles:

```bash
python3 -m py_compile \
  /home/hermes/.hermes/profiles/zeus/scripts/generate_daily_plan.py \
  /home/hermes/.hermes/profiles/zeus/scripts/due_task_drip.py \
  /home/hermes/.hermes/profiles/zeus/scripts/send_daily_schedule_reminder.py \
  /home/hermes/.hermes/profiles/zeus/scripts/sync_obsidian_tasks_to_theduy_calendar.py

python3 /home/hermes/.hermes/profiles/zeus/scripts/due_task_drip.py --dry-run
python3 /home/hermes/.hermes/profiles/zeus/scripts/send_daily_schedule_reminder.py --dry-run --force p1
python /home/hermes/.hermes/profiles/zeus/scripts/sync_obsidian_tasks_to_theduy_calendar.py --dry-run
```

Expected:
- Task drip selects only actionable due-today tasks.
- Schedule reminder prints one line only.
- Calendar sync steady state: `0 created, 0 updated, 0 stale deleted, N unchanged`.

## Session-specific detail

See `references/zeus-task-event-reminder-taxonomy.md` for the concrete corrections that led to this skill.
See `references/schedule-anchor-cascade.md` for the full file map + grep tokens when Duy changes a recurring time anchor (pickup, exercise, brunch, etc.).