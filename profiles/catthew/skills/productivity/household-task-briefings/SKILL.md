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

4. **Separate reminders only for specific times.**
   - If a household task is merely due today or belongs in the Daily Morning Briefing, do not create/send a standalone reminder.
   - Create or keep a separate reminder only when Sir gives a specific time/date-time, e.g. “9 AM,” “tonight at 6,” or “May 25 at 9:00.”

5. **Update existing scheduled briefing prompts when the formatting rule changes.**
   - If Sir corrects the Daily Morning Briefing format, update the `Daily Morning Briefing` cron prompt, then verify the cron job content reflects the correction.
   - Keep the prompt concise and explicit about grocery vs task formatting.

## Daily Morning Briefing formatting

Preferred sections:

- Date & greeting
- Today's events
- Grocery list
- Pending tasks & chores
- Upcoming
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

- Do not interpret “button” literally as an inline Telegram button unless Sir explicitly asks for actual tappable UI; in this session he reversed that request and kept text-based quick numbers.
- Do not put `[Done 1]` or `[Bought 1]` labels in the final briefing unless Sir asks again.
- Do not forget to persist durable formatting corrections in both memory and this skill when Sir corrects task/list display.
- Do not create redundant reminder cron jobs for tasks already covered by the daily briefing unless the task has a specific time.

## Reference

- See `references/telegram-task-formatting.md` for the correction sequence that established these household display rules.
