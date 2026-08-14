# Zeus task/calendar/Pomodoro/earnings workflow notes

Use this when maintaining Duy's task pipeline, daily schedule reminders, or market/earnings reminders.

## Source-of-truth layers

- Durable tasks live in `/vault/Tasks/tasks/*.md`.
- Full Calendar stubs live in `/vault/Tasks/calendar/*.md` and are a display/capture layer.
- Zeus Google Calendar sync targets `theduy calendar` (`duynt1989@gmail.com`) for non-`#catthew` tasks.
- Catthew/Kitty Family calendar is separate; do not route finance/business/personal work tasks through Catthew just to make them visible.

## Full Calendar orphan adoption

If Duy creates an item directly in Obsidian Full Calendar, it may produce an orphan stub with `title:`, `date:`, and `completed: false`, but no source task note. `/vault/System/scripts/sync-calendar-events.py` should:

1. Detect current/future unfinished orphan stubs with no `generated_by: sync-calendar-events` and no `source_note:`.
2. Create a real task under `/vault/Tasks/tasks/<slug>.md` with `source: full-calendar` and `fc_source_path:`.
3. Delete the orphan stub.
4. Regenerate the canonical Full Calendar mirror stub.

This lets Zeus task cards, daily plans, and theduy Google Calendar see the item.

## Separate task cards from schedule reminders

Duy explicitly wants these separated:

- **Task card:** source task from `/vault/Tasks/tasks/*.md`; may include Done button; no `Block:` line.
- **Schedule/Pomodoro reminder:** one-line plain Telegram time label only, no Done/Log button, no task registry write, no checkbox/task list, and no “what to do” instructions. Example: `🗓 9:05–9:30 — Pomodoro 1 — Deep Work`.

Do not combine a task Done button and a Pomodoro/block reminder into one message. Do not include task names inside daily schedule reminders; task names belong in separate task cards and in the morning briefing/daily plan.

## Due-today only task drip

`/home/hermes/.hermes/profiles/zeus/scripts/due_task_drip.py` sends at most one non-catthew Obsidian task card per run. It should:

- Include only `due_date == today`.
- Exclude overdue tasks. Duy moves overdue items himself while planning.
- Show `Time:` when the task has `due_time`, `time`, `start_time`, `Kickoff:`, `Start:`, `Due:`, `Time:`, or `Date/time:` metadata.

Cron: `Due-Today Obsidian Task Card Drip` (`056878e263a5`), every 10 minutes 8AM–11PM.

## Pomodoro schedule reminders

`/home/hermes/.hermes/profiles/zeus/scripts/send_daily_schedule_reminder.py` owns plain schedule reminders. It should use 25-minute Pomodoro work windows:

- 09:00–09:05 setup
- 09:05–09:30 Pomodoro 1
- 09:30–09:35 break
- 09:35–10:00 Pomodoro 2
- 10:00–10:30 brunch
- 10:30–10:55 Pomodoro 3
- 10:55–11:00 break
- 11:00–11:25 Pomodoro 4
- 11:25–11:45 buffer/messages
- 11:45–12:15 company review
- 12:15–12:40 Pomodoro 5 admin/finance
- 12:40–13:00 buffer/reset
- 13:00–13:25 Pomodoro 6
- 13:25–13:30 break
- 13:30–13:55 Pomodoro 7
- 14:00 protein
- 14:15–14:35 exercise/shutdown
- 14:35–14:45 pickup transition

Cron: `Daily Pomodoro Schedule Reminders` (`7909be6c0881`), every 5 minutes 9AM–8PM; script stays silent outside windows.

Legacy `planned_task_drip.py` / `Time-Blocked Obsidian Task Card Drip` (`ab4de922b388`) should stay paused unless Duy explicitly wants old block-based reminders again.

## Specific-time tasks

Specific-time tasks/events are fixed-time items, not Pomodoro work. Detect metadata such as `due_time`, `time`, `start_time`, `kickoff`, or body lines `Time:`/`Kickoff:`/`Date/time:`.

- Put them in the daily plan `Fixed` section.
- Show their time on task cards.
- Do not feed them into Pomodoro reminders.

## Major earnings reminders

`/home/hermes/.hermes/profiles/zeus/scripts/fetch_major_earnings_reminders.py` fetches major US-listed earnings from Nasdaq and creates task reminders under `/vault/Tasks/tasks/earnings-*.md`.

Rules:

- Use Nasdaq earnings API (`api.nasdaq.com/api/calendar/earnings`).
- Include mega-caps and a curated core ticker list.
- Create idempotent tasks with `tags: [finance, stocks, earnings]`, `company: finance`, `source: nasdaq-earnings-calendar`, `earnings_symbol:`, and `due_time:` set to session (`Before market open`, `After market close`, or `Time not confirmed`).
- Because earnings tasks have `due_time`, they are fixed items and must not be fed into Pomodoro reminders.
- After creating tasks, run Zeus Obsidian→theduy Calendar sync so they appear on Google Calendar.

Cron: `Quarterly Major Earnings Reminder Import` (`ccdc2300f9fe`) runs `0 8 1 1,4,7,10 *` and imports roughly the next 70 days.