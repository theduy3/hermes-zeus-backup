# Zeus task/event/reminder taxonomy corrections

This reference captures durable lessons from a session debugging Duy's Obsidian/Telegram/Google Calendar workflow.

## Corrections from Duy

- “For Earnings they are not tasks so i dont need any buttons, treat them as event.”
- “There are 3 kinds: Task with buttons, Event = Reminder sync with theduyvault and Google theduy calendar, and Reminder without sync.”
- “Earnings are events, Daily Schedule are reminder, and Tasks are Tasks.”
- “I do not need you to give me what to do in the Daily Schedule Reminder. `9:05–9:30 — Pomodoro 1 — Deep Work` is enough.”

## Resulting model

| Class | Vault | Google Calendar | Telegram | Example |
|---|---|---|---|---|
| Task | `type: task` in `/vault/Tasks/tasks` | Sync to `theduy calendar` | Task card with Done/More buttons | OC Accounting Fix for Vui |
| Event | `type: event` in `/vault/Tasks/tasks` | Sync to `theduy calendar` | No Done button | Earnings: TSLA / SPCX |
| Reminder | No durable note by default | No sync | Plain one-line message | Daily Pomodoro |

## Implementation notes from the session

- Converted existing Nasdaq earnings files from `type: task` to `type: event`.
- Patched earnings importer so future earnings reminders use `type: event`.
- Patched due-task drip to skip non-task records and earnings tags/sources.
- Patched daily plan so events appear under `Fixed` and never in Today Tasks / Pomodoro / Top 3 task selection.
- Patched Google sync to accept both `type: task` and `type: event`.
- SpaceX uses ticker `SPCX`; Nasdaq did not return it in the normal earnings API during the session, but yfinance calendar showed earnings date `2026-08-04`. Use narrow yfinance fallback only for exceptional tickers like `SPCX` to avoid long/fragile full-watchlist yfinance scans.

## Pitfalls

1. **Do not infer from storage path alone.** Earnings live under `/vault/Tasks/tasks` for sync compatibility, but they are events, not tasks.
2. **Do not add buttons to events.** A button implies completion; earnings/events are informational.
3. **Do not make Pomodoro reminders actionable.** They should announce the block label only.
4. **Do not let briefing prompts override generated plan structure.** The daily plan's `Today Tasks` section is authoritative for due-today tasks.
5. **Avoid broad yfinance fallback loops.** They can be slow/noisy; prefer Nasdaq for general earnings and targeted fallback for known missing symbols.
