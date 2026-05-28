---
name: household-task-briefings
description: Manage Catthew household task lists, grocery lists, daily briefings, and reminder formatting for the family Telegram chat.
version: 1.0.0
---

# Household Task Briefings

Use this skill whenever Sir asks Catthew to add, display, revise, schedule, or summarize household tasks, chores, grocery items, or daily morning briefings.

## Core workflow

1. **Separate storage format from chat format.**
   - Obsidian/task files use real Markdown task syntax: `- [ ] Task`.
   - Telegram chat confirmations use the household-friendly display format below.

2. **For Telegram chat task/chores lists, use square checkbox + quick number.**
   - Format: `☐ Task name (1)`
   - Continue numbering sequentially within the task/chores section.
   - Do not use `- [ ]` or hyphen bullets in chat task/chores confirmations unless Sir explicitly asks.

3. **For Telegram grocery lists, use simple bullets unless Sir requests otherwise.**
   - Example:
     - `- Korean pear`
     - `- Ghee`
   - Do not add `[Bought 1]` buttons/labels unless Sir re-requests that format.

4. **Task delivery preference.**
   - Send household task reminders and task-containing briefings to the family Telegram group (`telegram:-5249331607`, “Catthew - the Butler”), not Sir’s private DM.
   - List today and overdue household tasks inside the Daily Morning Briefing under **Pending tasks & chores**.
   - If individual Telegram Done-button cards are also enabled, treat them as supplemental; do not remove today/overdue tasks from the briefing.
   - Create or keep a separate reminder only when Sir gives a specific time/date-time, e.g. “9 AM,” “tonight at 6,” or “May 25 at 9:00.”

5. **Update existing scheduled briefing prompts when the formatting rule changes.**
   - If Sir corrects the Daily Morning Briefing format, update the `Daily Morning Briefing` cron prompt, then verify the cron job content reflects the correction.
   - Keep the prompt concise and explicit about grocery vs task formatting.

## Daily Morning Briefing formatting

Preferred sections:

- Date & greeting
- Today's events
- Grocery list
- Pending tasks & chores (list today and overdue tasks)
- Upcoming (next 7 days)
- Closing

In the **Pending tasks & chores** section, format items like:

```text
☐ Collapse the baby crib (1)
☐ Build the cabinet (2)
☐ Move current cabinet from dining room to master bedroom (3)
```

In the **Grocery list** section, use ordinary simple bullets:

```text
- Korean pear
- Ghee
```

## Pitfalls

- When Sir asks for task Done buttons, use the established Catthew task-card drip: `scripts/send_household_task_buttons.py`, callback prefix `ct:`, and registry `~/.hermes/profiles/catthew/task_buttons/registry.json`. Ensure `/home/hermes/.hermes/profiles/catthew/.env` has `TASK_BUTTON_CHAT_ID=-5249331607` so cards go to the Catthew group, not Sir's private `TELEGRAM_HOME_CHANNEL`.
- Victoria's same-day household events count as tasks for the individual Done-button drip, so recurring events in `events.md` (e.g. music class or Playgym) should be sent as Done-button task cards on their day. Date-limited recurring events may use `from YYYY-MM-DD through YYYY-MM-DD`; the drip ignores them outside that range.
- Do not put `[Done 1]` or `[Bought 1]` labels in the final briefing unless Sir asks again.
- Do not forget to persist durable formatting corrections in both memory and this skill when Sir corrects task/list display.
- Prefer the individual Done-button task card style for household tasks and same-day household events, even when they have a time. Do not create standalone cron-style reminder messages for these unless Sir explicitly asks for a separate reminder.

## Reference

- See `references/telegram-task-formatting.md` for the correction sequence that established these household display rules.
