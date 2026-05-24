---
name: hermes-activity-recap
description: Summarize a day of Hermes activity by inspecting session transcripts and cron output artifacts directly. Use when session_search is too sparse, when many cron jobs ran, or when you need counts, failures, and next actions grounded in actual run artifacts.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, cron, sessions, recap, reporting, monitoring]
---

# Hermes Activity Recap

Use this skill when asked to summarize “what happened today” in Hermes, especially for cron-heavy days. The reliable source of truth is usually the local artifact store, not just `session_search()`.

## Why this exists

Learned in practice:
- `session_search()` recent mode is useful for discovering session IDs, but it can miss detail or surface sparse sessions.
- Cron transcript JSON files under `~/.hermes/sessions/` often contain the raw prompt and message history.
- Human-readable cron outputs under `~/.hermes/cron/output/<job_id>/` are often the fastest way to see final results, repeated failures, and exact error messages.
- On monitoring-heavy days, counting successes/failures across output files is more accurate than inferring from a few recent sessions.

## Recommended workflow

1. **Get today’s date from the live system**
   - Use `terminal("date '+%Y-%m-%d %A %I:%M %p %Z'")`
   - Do not infer the date from memory.

2. **Discover recent Hermes sessions**
   - Start with `session_search()` with no query to see the latest session IDs.
   - Treat this as a pointer, not the full data source.

3. **Inspect local Hermes artifact paths**
   - Session transcripts: `~/.hermes/sessions/session_*_YYYYMMDD_*.json`
   - Cron outputs: `~/.hermes/cron/output/*/YYYY-MM-DD_*.md`
   - Use `search_files(target='files')` to locate the day’s files.

4. **Read representative outputs first**
   - Open a few cron output markdown files to understand each job’s purpose and final response.
   - Identify job IDs and recurring job names before trying to summarize the whole day.

5. **Use code for aggregation when volume is high**
   - If there are many session/output files, use `execute_code` to:
     - count runs per job
     - classify successes vs failures
     - detect repeated errors (for example `HTTP 429`)
     - extract recurring facts from assistant final responses
   - Prefer summarizing counts from files rather than eyeballing dozens of transcripts.

6. **Look specifically for blockers**
   - Search cron outputs for phrases like:
     - `HTTP 429`
     - `usage limit`
     - `Failed to`
     - `Permission denied`
     - `not writable`
     - `not found`
   - Report exact operational blockers, not vague guesses.

7. **Cross-check with health-check jobs**
   - If a daily health-check cron exists, read its output directly; it often contains the cleanest summary of gateway health, missing credentials, and broken dependencies.

8. **Write the final recap in 3 sections**
   - What got done today
   - Failures / blockers
   - Top next actions

## Patterns that worked well

- For repeated cron monitoring jobs, summarize the **aggregate behavior** (“431 gateway checks ran; 331 succeeded; 100 hit HTTP 429”) instead of listing many nearly identical runs.
- Distinguish **actual implementation work** from **automated monitoring/reporting**.
- If a write job failed due to permissions, report the exact target path and exact permission error.
- When a health check exists, use it to ground claims about invalid keys, missing auth, missing dependencies, or broken services.

## Pitfalls

- Don’t rely only on `session_search()` for daily recaps.
- Don’t assume the latest session is the most informative one.
- Don’t treat a cron job’s existence as proof it succeeded; inspect its output.
- Don’t overstate work done when the day mostly consisted of automated checks.
- Don’t generalize from one transcript if there are hundreds of runs available to count.

## Useful file patterns

```text
~/.hermes/sessions/session_*_YYYYMMDD_*.json
~/.hermes/cron/output/<job_id>/YYYY-MM-DD_*.md
```

## Good recap style

- Concise bullets
- Quantified when possible
- Separate “healthy but repetitive monitoring” from “new work completed”
- Include exact blocker names when they materially affect tomorrow’s next steps
