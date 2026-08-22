# Schedule Anchor Cascade — Duy/Zeus

When Duy changes a recurring time anchor, it is a **multi-file cascade**, not a one-line fix. The same constant is hardcoded in many places; edit them all consistently or briefings, plans, and reminders will disagree.

## Why

Duy's schedule was built incrementally: the daily-plan generator, the schedule-reminder script, the legacy drip, the two briefing cron prompts, and the note-taking skill docs each embed the anchors independently. There is no single source of truth for times.

## Files that hardcode anchors

| File | What it holds |
|------|---------------|
| `profiles/zeus/scripts/generate_daily_plan.py` | `BLOCKS` list, constraints text, "Pick up Victoria" fixed line, exercise/shutdown label |
| `profiles/zeus/scripts/send_daily_schedule_reminder.py` | `WINDOWS` list (exercise start/end/heading, fallback text "before Victoria pickup"), shutdown window text |
| `profiles/zeus/scripts/planned_task_drip.py` | "Protected: ... pickup transition 2:35–2:45" summary text; shutdown window text |
| `profiles/zeus/cron/jobs.json` | Morning Briefing prompt (family rule re pickup) + Evening Briefing prompt ("2:35–2:45 PM: pickup transition", "Around 2:45 PM: pick up Victoria", "Deep work only between 9:00 AM and 2:45 PM") |
| `profiles/zeus/skills/note-taking/obsidian/SKILL.md` | schedule rules block (same 2:45 anchors) |
| `profiles/zeus/skills/note-taking/obsidian/references/time-blocked-planning.md` | time-block table |
| `profs/zeus/skills/note-taking/obsidian/references/zeus-task-calendar-earnings-pomodoro.md` | time-block table |
| `profiles/zeus/skills/devops/cron-job-patterns/SKILL.md` | "Approved Duy schedule constraints" block |
| `/vault/Tasks/planning/YYYY-MM-DD.md` | generated plans (past + future-dated, e.g. 2026-09-17) with old anchors in `Fixed`/`## Constraints`/Pomodoro sections |

## Grep tokens to sweep

```
2:45   2:35   Pick up Victoria   pickup transition
before Victoria pickup   Deep work only between   2:15–2:35
```

Search both `~/.hermes` and `/vault/Tasks/planning`.

## Procedure

1. Sweep with the tokens above; record every hit and its file.
2. **Clarify scope before editing** (live session only): when shifting one anchor, confirm whether adjacent blocks move too. Example from this session: pickup shifted 2:45→3:45; user chose to keep the transition block adjacent (3:35–3:45) and keep exercise at 2:15–2:35. Later, an out-of-band message moved exercise to a **morning 9:00–10:00** window after daycare drop-off — which collided with the pre-brunch Pomodoro `BLOCKS`, so the generator's `BLOCKS` needed restructuring, not just a relabel.
3. Edit each source consistently. Cron prompts: patch `jobs.json` in place (see cron-job-patterns: "Editing a Job Prompt In-Place").
4. Regenerate or hand-edit future-dated `/vault/Tasks/planning/*.md`.
5. `python3 -m py_compile` the scripts; re-run the skill's verification dry-runs.

## Gotchas

- `cronjob update` resupplies the **entire** prompt; prefer surgical `patch` of `jobs.json` for add/remove clauses.
- The "Approved Duy schedule constraints" block in cron-job-patterns is the canonical mirror — keep it in sync with `generate_daily_plan.py`.
- Duy revises anchors live and sometimes mid-session (out-of-band messages). Re-read the live request before committing a cascade; a mid-turn redirect can change the whole plan.
