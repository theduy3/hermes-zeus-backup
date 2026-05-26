# Telegram task and grocery formatting corrections

Session summary for future Catthew household briefings.

## Corrections established

1. Sir rejected Markdown bracket checkboxes in Telegram chat.
   - Wrong in chat: `- [ ] Task name`
   - Right in chat: `☐ Task name`

2. Sir wanted quick reference numbers at the end of chat tasks.
   - Right: `☐ Collapse the baby crib (1)`
   - Purpose: Sir can reply quickly with which task is done.

3. Sir clarified standalone reminders should be reserved for tasks with a specific time.
   - Ordinary due-today tasks belong in the Daily Morning Briefing only.
   - Do not create an extra reminder for tasks that are simply part of the daily plan.

4. Sir experimented with text labels that looked like buttons:
   - Tasks: `[Done 1]`
   - Groceries: `[Bought 1]`
   He then asked to reverse that change. Current preferred state is:
   - Tasks/chores in chat: `☐ Task name (1)`
   - Groceries in daily briefing: simple bullets, e.g. `- Ghee`

## Implementation note

When applying these rules to the Daily Morning Briefing cron job, update the job prompt rather than relying only on memory. The prompt should explicitly distinguish:

- Grocery list: simple bullets.
- Pending tasks & chores: no hyphen bullets; use square checkbox at start and number in parentheses at end.

## Good example

```text
Grocery list
- Korean pear
- Ghee

Pending tasks & chores
☐ Collapse the baby crib (1)
☐ Build the cabinet (2)
☐ Move current cabinet from dining room to master bedroom (3)
```
