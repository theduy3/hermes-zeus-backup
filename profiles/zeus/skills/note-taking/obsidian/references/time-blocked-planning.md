# Duy time-blocked planning system

Use this when working on Duy's theduyvault Tasks, daily planning notes, task-card drips, or morning/evening task briefings.

## Approved weekday structure

- Before 9:00 AM: baby/family; no normal work task cards.
- 9:00–9:10: daily setup / top priorities.
- 9:10–10:00: Deep Work 1.
- 10:00–10:30: brunch; protected.
- 10:30–11:45: Deep Work 2.
- 11:45–12:15: rotating company review.
- 12:15–12:45: admin / finance batch.
- 12:45–1:00: buffer.
- 1:00–2:15: Deep Work 3.
- 2:15–2:35: shutdown / mark Done / reschedule.
- 2:35–2:45: pickup transition; stop work.
- Around 2:45: pick up Victoria / family transition.
- After 2:45: family-first; only urgent fixed reminders or evening planning.

## Company review rotation

- Monday: SalonX
- Tuesday: Sans Souci / SS
- Wednesday: Ongles Rivieres
- Thursday: Ongles Maily
- Friday: Ongles Charlesbourg

Review checklist:
- Cash / revenue abnormal?
- Staff / schedule issue?
- Customer reviews / complaints?
- Supplies / equipment / vendor / software?
- Pick one follow-up action if needed.

## Vault artifacts

- Active tasks: `/vault/Tasks/tasks/*.md`
- Daily plans: `/vault/Tasks/planning/YYYY-MM-DD.md`
- Planning generator: `/home/hermes/.hermes/profiles/zeus/scripts/generate_daily_plan.py`
- Time-block task-card sender: `/home/hermes/.hermes/profiles/zeus/scripts/planned_task_drip.py`

Task metadata fields used by the planner:

```yaml
time_block: deep_work      # deep_work | admin_batch | calls | finance | company_review | family | errand | review | waiting | backlog
estimated_minutes: 60
energy: high              # high | medium | low
priority: normal          # urgent | high | normal | low
company: salonx           # salonx | ss | rivieres | maily | charlesbourg | personal | family | finance
```

## Cron jobs

- `901801e68cb5` — Generate Daily Time-Blocked Plan, `55 8 * * 1-5`, script `generate_daily_plan.py`, local delivery.
- `ab4de922b388` — Time-Blocked Obsidian Task Card Drip, `*/5 9-14 * * 1-5`, script `planned_task_drip.py`, local delivery.
- Morning briefing `e6711b998b07` should refresh/read today's planning note and output plan-first.
- Evening briefing `b83af24484d0` should generate/read tomorrow's planning note and output tomorrow prep.

## Google Calendar integration note

For Zeus, Google Calendar access should default to Duy's primary calendar only:

```text
GOOGLE_CALENDAR_ID=duynt1989@gmail.com
GOOGLE_CALENDAR_NAME="theduy calendar"
```

The token should have only Calendar scope when the user asks for calendar-only access. Catthew may already have a compatible Calendar token; if OAuth is stuck and the same OAuth client/account is already authorized in Catthew, copying the calendar-only token into Zeus and verifying with a live Calendar API call is an acceptable setup shortcut. Do not broaden scopes to Gmail/Drive/Docs/Sheets unless the user explicitly asks.

## Verification checklist

After changes, verify:

- Generated plan contains brunch, pickup transition, Top 3, No-Date Triage, and correct weekday company.
- Drip window logic sends only at: 9:00, 9:10, 10:30, 11:45, 12:15, 13:00, 14:15.
- No normal work cards before 9:00, during brunch, after 2:45, or on weekends.
- `python3 -m py_compile` passes for modified scripts.
- Google Calendar default list/create/delete commands target `GOOGLE_CALENDAR_ID` unless the user explicitly gives another calendar ID.
