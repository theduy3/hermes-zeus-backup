# Duy Schedule Restructure — Cascade Checklist

When Duy asks to change the recurring daily schedule (move pickup time, delete
Pomodoro/deep-work blocks, add/remove a recurring block), the time anchor is
WIRED INTO MANY FILES. Editing only the cron prompt leaves the generated plans
and reminder scripts stale. Touch ALL of these:

## Source of truth (edit these)
1. `/home/hermes/.hermes/profiles/zeus/scripts/generate_daily_plan.py`
   - Module docstring schedule notes.
   - `BLOCKS` constant (if still present) and the generated plan sections.
   - Weekday constraint lines + `Fixed` pickup line + weekday body sections.
2. `/home/hermes/.hermes/profiles/zeus/scripts/send_daily_schedule_reminder.py`
   - `WEEKDAY_WINDOWS` list (currently: exercise/brunch/company/protein/pickup).
3. `/home/hermes/.hermes/profiles/zeus/scripts/planned_task_drip.py` (legacy, paused)
   - summary "Protected:" line + shutdown window text.
4. Cron job prompts in `/home/hermes/.hermes/profiles/zeus/cron/jobs.json`:
   - `b83af24484d0` Daily Evening Briefing (schedule constraints).
   - `e6711b998b07` Daily Morning Briefing (remove/add sections here too).

## Skill / doc references (keep in sync)
5. `skills/note-taking/obsidian/SKILL.md` — "Duy's time-blocked planning system".
6. `skills/note-taking/obsidian/references/time-blocked-planning.md`.
7. `skills/note-taking/obsidian/references/zeus-task-calendar-earnings-pomodoro.md`.
8. `skills/devops/cron-job-patterns/SKILL.md` — "Approved Duy schedule constraints".

## Already-generated plans (fix forward)
9. `/vault/Tasks/planning/YYYY-MM-DD.md` for any date >= today that still shows
   the old times / Pomodoro sections. Bulk-rewrite with a script:
   replace pickup strings, drop Pomodoro/deep-work `##` sections.

## Verify
- `python3 scripts/generate_daily_plan.py --date <weekday> --print` → no
  Pomodoro/Deep Work headings, correct pickup/pickup-transition times.
- `python3 -c "import ast; ast.parse(open('scripts/send_daily_schedule_reminder.py').read())"` → OK.
- Import the reminder module and assert `WEEKDAY_WINDOWS` keys are the expected set.
- grep the scripts/skills/cron dirs for stale `2:45` / `Pomodoro` / `Deep Work`.
