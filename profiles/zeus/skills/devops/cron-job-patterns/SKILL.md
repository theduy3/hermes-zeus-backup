---
name: cron-job-patterns
title: Cron Job Patterns
description: Patterns for setting up cron jobs in Hermes — timezone handling, multi-profile coordination, context chaining via filesystem, and watchdog scripts.
category: devops
---

# Cron Job Patterns

## Timezone Handling (US/CA Pacific)

When a Vancouver/Pacific-time user says a time in "PST" during DST (mid-Mar to early Nov), **clarify**:

> Vancouver is on PDT (UTC-7) right now. "5AM PST" would be 6AM your clock.
> 1. **Match your clock** — runs at 5AM local year-round (UTC-7 in summer, UTC-8 in winter)
> 2. **True PST** — UTC-8 always (runs at 6AM local in summer, 5AM in winter)

Offer both options with explicit local-clock impact so the user can choose.

**Conversion reference:**
- True PST = UTC-8 (winter standard)
- Local clock during DST = UTC-7 (PDT)
- DST in Canada: 2nd Sun Mar → 1st Sun Nov

**Key insight:** Many users say "PST" as a generic label for Pacific time even during DST. Always disambiguate.

## Cross-Profile Cron Coordination

Zeus can chain off another profile's cron output by reading its output files directly (same filesystem):

```
catthew output: ~/.hermes/profiles/<profile>/cron/output/<job_id>/<YYYY-MM-DD_HH-MM-SS>.md
```

In the downstream cron prompt, include a step like:
```
FIRST, read Catthew's latest family briefing output from the most recent file in /home/hermes/.hermes/profiles/catthew/cron/output/<job_id>/
```

For profiles that store task/reminder cron jobs, aggregate due-today/overdue items by reading their `jobs.json` directly:
```
finance tasks: ~/.hermes/profiles/finance/cron/jobs.json
investment strategist tasks: ~/.hermes/profiles/charles/cron/jobs.json
```
Include enabled jobs whose `next_run_at`/`run_at` is today in the user's Pacific timezone, plus overdue enabled one-shot jobs whose repeat has not completed. Omit that subsection when none are due. If a profile's `jobs.json` does not exist yet, treat it as no due items rather than failing the briefing.

**Important:** `context_from` only works within the **same profile's** scheduler. Cross-profile context requires filesystem reads.

## Editing Another Profile's Cron Jobs

The `cronjob` tool only manages the **current profile's** scheduler. To modify another profile:

1. Determine the target profile's cron path: `~/.hermes/profiles/<profile>/cron/jobs.json`
2. Read → edit → write the JSON directly (must match schema exactly)
3. Include `updated_at` timestamp
4. Verify the job is in the right state afterwards

## Pipeline Schedule Pattern

When chaining Job A → Job B:

1. Job A runs first (e.g. Catthew family briefing)
2. Job B runs 15 min later and reads A's output
3. Gap is intentional — ensures A's output file exists before B tries to read it

For morning-briefing prompts that include Obsidian tasks, explicitly require clean, user-readable output:
- Strip wiki-link brackets: `[[Page]]` → `Page`, `[[Page|label]]` → `label`
- Strip markdown/Obsidian markup such as `#tags`, `==highlight==`, and bold/italic markers
- Do not preserve raw brackets or internal note syntax in Telegram briefings; legibility beats note fidelity
- If the user wants task/reminder items as checkboxes, use Telegram-readable checkbox lines like `☐ Task text`; do **not** emit raw Obsidian `- [ ]` syntax in Telegram unless the destination is an actual vault note

### Split Morning Briefings

When a user says the morning briefing is too dense or wants tasks separated, split into two jobs instead of one mixed briefing:
1. **Info-only job** (e.g. 6:15AM): family/schedule context, stocks, headlines, weather, horoscope. Explicitly forbid task lists, checkboxes, overdue items, and reminders.
2. **Tasks-only job** (e.g. 2 minutes later): Obsidian tasks, Catthew tasks, finance advisor reminders, investment strategist reminders, timezone triggers. Every actionable line should be `☐ item`; omit empty sections.

Keep the gap short but nonzero so Telegram receives two readable messages. See `references/zeus-morning-briefing-split.md` for a concrete prompt pattern.

Use `enabled_toolsets` to restrict tools per job:
- `["web", "memory", "skills", "terminal", "file"]` - typical for briefing-type jobs
- Fewer tools = fewer input tokens per run

## Pitfalls

- **Cron prompts must be self-contained** — no conversation context, no memory of previous turns
- **Cross-profile context requires filesystem** — context_from is single-profile only
- **Always `cronjob action=list` before remove/update** — never guess job IDs
- **State file is the source of truth** — for non-current profiles, edit their jobs.json directly
- **Can't use `clarify` in cron** — make reasonable default choices; the job runs autonomously
