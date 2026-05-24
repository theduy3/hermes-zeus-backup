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

3. **Check cron list for delivery failures immediately**
   - Run `hermes cron list` before reading any output files.
   - Any job with `⚠ Delivery failed:` is flagged inline — this catches unreachable output faster than grepping files. Note the job ID and error (e.g., "Unauthorized", "Telegram send failed") for the blockers section.
   - Also note: `Deliver: origin` means output is sent to the user; `Deliver: local` means output stays on the host.

4. **Inspect local Hermes artifact paths**
   - Session transcripts: `~/.hermes/sessions/session_*_YYYYMMDD_*.json`
   - Cron outputs: `~/.hermes/cron/output/*/YYYY-MM-DD_*.md`
   - Use `search_files(target='files')` to locate the day's files.

5. **Read representative outputs first**
   - Open a few cron output markdown files to understand each job's purpose and final response.
   - Identify job IDs and recurring job names before trying to summarize the whole day.

6. **Count and classify with terminal tools first, then sample**
   - For high-volume jobs, use terminal `grep -c` or `grep -l` for fast aggregate counts before using `execute_code`.
   - Pitfall: `execute_code` loops calling `read_file` on 400+ files are slow (~45 sec for 436 files). Use terminal `grep` to count SILENT vs non-SILENT responses, error patterns, etc. first, then `read_file` only the representative samples.
   - Example fast-count: `grep -l "\[SILENT\]" ~/.hermes/cron/output/<job_id>/YYYY-MM-DD_*.md | wc -l`

7. **Use code for aggregation when volume is high**
   - If there are many session/output files, use `execute_code` to:
     - count runs per job
     - classify successes vs failures
     - detect repeated errors (for example `HTTP 429`)
     - extract recurring facts from assistant final responses
   - Prefer summarizing counts from files rather than eyeballing dozens of transcripts.
   - Pre-filter with terminal `grep` first (see step 6) — only use `execute_code` for classification logic that needs Python.

8. **Look specifically for blockers**
   - Search cron outputs for phrases like:
     - `HTTP 429`
     - `HTTP 401`
     - `usage limit`
     - `Failed to`
     - `Permission denied`
     - `not writable`
     - `not found`
     - `Unauthorized`
   - Report exact operational blockers, not vague guesses.

9. **Cross-check with health-check jobs**
   - If a daily health-check cron exists, read its output directly; it often contains the cleanest summary of gateway health, missing credentials, and broken dependencies.

10. **Write the final recap in 3 sections**
   - What got done today
   - Failures / blockers
   - Top next actions

## Patterns that worked well

- For repeated cron monitoring jobs, summarize the **aggregate behavior** (“431 gateway checks ran; 331 succeeded; 100 hit HTTP 429”) instead of listing many nearly identical runs.
- **Gateway health-check monitor pattern**: When the dominant job is a health-check that runs every 2 min (like `ensure-telegram-profile-gateways`), the key question is “were any gateways actually restarted?” Most runs will say “no restarts needed” — grep for actual actions: `grep "gateway run\|Starting\|Started" | grep -v "No restarts\|no restarts"`. If zero hits, report zero restarts and move on.
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
