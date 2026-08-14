---
name: duy-task-event-reminder-system
description: Maintain Duy's Obsidian + Google Calendar + Telegram task/event/reminder workflows without mixing task cards, synced events, and ephemeral reminders.
---

# Duy Task / Event / Reminder System

Use this whenever modifying Zeus task drips, Obsidian task/event files, Full Calendar adoption, Google `theduy calendar` sync, earnings reminders, or daily/Pomodoro schedule reminders.

## Core taxonomy

Duy has three distinct classes. Do not merge them.

1. **Task**
   - Actionable work item.
   - Vault source: `/vault/Tasks/tasks/*.md` with `type: task`.
   - Sync: theduyvault + Google `theduy calendar`.
   - Telegram: may get a task card with Done/More buttons.
   - Examples: `OC Accounting Fix for Vui`, `Update 3R Menu and Order Coupon`.

2. **Event = Reminder**
   - Dated/fixed-time item the user wants surfaced on calendar, but not completed like a task.
   - Vault source: currently may live under `/vault/Tasks/tasks/*.md` for compatibility, but frontmatter must be `type: event`.
   - Sync: theduyvault + Google `theduy calendar`.
   - Telegram: no Done buttons; do not send via due-task drip.
   - Examples: major stock earnings reminders, fixed market events.

3. **Reminder without sync**
   - Ephemeral prompt only.
   - Vault source: none required.
   - Sync: no Google Calendar sync.
   - Telegram: plain text only, no buttons.
   - Examples: Daily Pomodoro schedule reminder.

## Travel itinerary reminders

When Duy sends flight or travel-booking screenshots and says “reminder this itinerary” (including typo variants), treat that as a request for **calendar-synced event reminders**, not actionable task cards:

1. Search `/vault/Tasks/tasks/` for matching route/date, booking reference, or flight number before writing, so already-captured legs remain untouched.
2. Create one `type: event` Markdown file per new travel leg in `/vault/Tasks/tasks/`, named `flight-<origin>-to-<destination>-YYYY-MM-DD.md`.
3. Include `due_date`, local departure `due_time` with the correct timezone abbreviation, `[personal, travel, flight, <destination>]` tags, `status: pending`, and both departure and arrival details in the body. Preserve booking reference and flight number when shown.
4. Treat departure and arrival as separately zoned facts; show the origin-local departure time and destination-local arrival time rather than converting both into one timezone.
5. Run `/home/hermes/.hermes/profiles/zeus/scripts/sync_obsidian_tasks_to_theduy_calendar.py` after creating the notes, then run it once with `--dry-run` and confirm the new events are steady-state unchanged.
6. Reply with only the newly added legs and confirmation they synced. Do not repeat itinerary legs that were already in the vault.

## Non-negotiable formatting preferences

- Daily schedule reminders must be one-line time labels only:
  - Good: `🗓 9:05–9:30 — Pomodoro 1 — Deep Work`
  - Bad: `🗓 9:00–9:05 — Daily setup\n\n☐ Confirm Top 3 and fixed appointments`
- No checklist items, task lists, instructions, Done buttons, or Log buttons in schedule reminders.
- Task cards and schedule reminders are separate channels.
- Specific-time tasks/events stay fixed; never feed them into Pomodoro reminders.
- Due-task drip is due-today only; do not drip overdue tasks.

## Earnings reminders

Major US stock-market earnings reminders are **events**, not tasks.

When creating/updating earnings reminders:
- Use `type: event`.
- Include `due_date: YYYY-MM-DD`.
- Include `due_time:` such as `Before market open`, `After market close`, or `Time not confirmed`.
- Include `time_block: fixed`.
- Include `source: nasdaq-earnings-calendar`.
- Include symbol/session metadata when available:
  - `earnings_symbol:`
  - `earnings_session:`
  - `earnings_fiscal_quarter:`
- Include tags like `[finance, stocks, earnings]`.
- Sync them to Google `theduy calendar` as calendar events.
- Exclude them from any Telegram task-card/Done-button workflow.

The quarterly importer should include both:
- major US-listed earnings, and
- every ticker from `/vault/System/Stock Watchlist.md`.

## Implementation checklist

When changing this system, check these scripts together:

- `/home/hermes/.hermes/profiles/zeus/scripts/due_task_drip.py`
  - Must only send `type: task`.
  - Must skip `type: event`, `source: nasdaq-earnings-calendar`, and `earnings` tags.

- `/home/hermes/.hermes/profiles/zeus/scripts/send_daily_schedule_reminder.py`
  - Must output one-line schedule labels only.
  - Must not read plan section tasks into the message body.

- `/home/hermes/.hermes/profiles/zeus/scripts/generate_daily_plan.py`
  - `type: event` belongs under `Fixed`.
  - `type: task` due today belongs under `Today Tasks`.
  - Pomodoro picks only actionable `type: task` items without specific times.

- `/home/hermes/.hermes/profiles/zeus/scripts/sync_obsidian_tasks_to_theduy_calendar.py`
  - Must sync both `type: task` and `type: event` to `theduy calendar`.
  - Calendar extended properties should preserve source path and source type.

- `/home/hermes/.hermes/profiles/zeus/scripts/fetch_major_earnings_reminders.py`
  - Must write new earnings reminders as `type: event`.
  - Must read `/vault/System/Stock Watchlist.md` in addition to major-cap/core ticker filters.

## Verification

After any change:

```bash
python3 -m py_compile \
  /home/hermes/.hermes/profiles/zeus/scripts/due_task_drip.py \
  /home/hermes/.hermes/profiles/zeus/scripts/send_daily_schedule_reminder.py \
  /home/hermes/.hermes/profiles/zeus/scripts/generate_daily_plan.py \
  /home/hermes/.hermes/profiles/zeus/scripts/sync_obsidian_tasks_to_theduy_calendar.py \
  /home/hermes/.hermes/profiles/zeus/scripts/fetch_major_earnings_reminders.py
```

Then verify behavior:

```bash
python3 /home/hermes/.hermes/profiles/zeus/scripts/send_daily_schedule_reminder.py --dry-run --force p1
python3 /home/hermes/.hermes/profiles/zeus/scripts/due_task_drip.py --dry-run
python3 /home/hermes/.hermes/profiles/zeus/scripts/generate_daily_plan.py --date YYYY-MM-DD --print
python /home/hermes/.hermes/profiles/zeus/scripts/sync_obsidian_tasks_to_theduy_calendar.py --dry-run
```

Expected:
- Schedule dry-run: one line only.
- Task drip: no earnings/event cards.
- Daily plan: earnings/events under Fixed; due-today tasks under Today Tasks.
- Calendar sync: steady state after live sync is `0 created, 0 updated, 0 stale deleted, N unchanged`.

## Pitfalls from past corrections

- Full Calendar/Obsidian Today view can show items not present as canonical task files; orphan stubs may need adoption before Telegram/GCal can see them.
- Morning briefing must include the authoritative `Today Tasks` section; do not let an LLM substitute future high-priority items.
- Do not add `#catthew` to non-family tasks just to make them visible.
- Catthew/Kitty family calendar is separate from Zeus/theduy calendar.
- Host `/vault` may differ from container `/vault`; fix file ownership inside the correct Docker container if Hermes cannot read a vault file.
