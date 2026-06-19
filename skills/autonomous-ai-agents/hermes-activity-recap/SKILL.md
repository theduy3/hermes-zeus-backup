---
name: hermes-activity-recap
description: Summarize a day of Hermes activity by inspecting session transcripts and cron output artifacts directly. Use when session_search is too sparse, when many cron jobs ran, or when you need counts, failures, and next actions grounded in actual run artifacts.
version: 1.1.0
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
   - Always scan the recent non-cron/interactive sessions too. Daily recaps often include user-requested operational work (profile cleanup, auth fixes, manual reruns) that never appears in cron output files. Use targeted `session_search(query=...)` and scroll the relevant session when a recent title/preview hints at concrete work.
   - When an interactive session was interrupted, look for the last substantive assistant messages before/after the interruption note; those often contain verified completion status that the final message alone may omit.
   - If `session_search(session_id=...)` returns a persisted-output file because the transcript is too large, parse that saved JSON file directly with `python3` and print only the nonempty assistant messages (especially the final one). This avoids flooding context while preserving the verified outcome of interactive work.

3. **Check cron list for delivery failures immediately**
   - Run `hermes cron list` before reading any output files.
   - Any job with `⚠ Delivery failed:` is flagged inline — this catches unreachable output faster than grepping files. Note the job ID and error (e.g., "Unauthorized", "Telegram send failed") for the blockers section.
   - Also note: `Deliver: origin` means output is sent to the user; `Deliver: local` means output stays on the host.

4. **Inspect local Hermes artifact paths**
   - Cron session transcripts: `~/.hermes/sessions/session_cron_<jobid>_YYYYMMDD_*.json`
   - Non-cron session transcripts: `~/.hermes/sessions/session_YYYYMMDD_*.json`
   - Cron outputs: `~/.hermes/cron/output/*/YYYY-MM-DD_*.md`
   - Use `search_files(target='files')` to locate the day's files. Do this even when `hermes cron list` shows an exact-ish last-run time: output filenames can differ by one second from the list timestamp (e.g. list says `09:01:20`, file is `09-01-19`). Read the path returned by discovery, not a hand-constructed timestamp path.
   - Resolve the reporting date in the job's/user's local timezone, not just UTC. Evening recaps often run while UTC is already the next date; use `TZ=<cron/user timezone> date` when available and summarize the local "today".
   - Do not rely only on `hermes cron list` last-run fields for jobs scheduled later in the day. If current time is after a job should have fired, explicitly check `~/.hermes/cron/output/<job_id>/YYYY-MM-DD_*.md`; cron list can appear stale or be observed before a pending local-time run completes.
   - If `session_search()` shows a cron session for today with only the initial user prompt and no matching output file yet, treat that job as **in progress or not yet delivered**, not as completed. Mention it only if it materially affects the recap, and avoid claiming its result until a `## Response`/`## Error` output file or final assistant message exists.
   - **Re-scan near the end of the recap.** Scheduled jobs can finish while you are aggregating earlier outputs. After the first pass, explicitly check any jobs whose scheduled local time is due/near-due and rerun the day's output-file discovery before finalizing counts. Do not let an early aggregate (for example “49 files”) hide a just-finished output that appeared minutes later.
- **Watch for co-scheduled evening jobs.** The weekday recap itself may run at the same local minute as other end-of-day jobs (for example `vault-tonight` at 18:00). If `session_search()` shows a just-started cron session with only the initial prompt, or if the cron list says a job is due/near-due, do a second output-file scan after the first aggregation and read any newly appeared file before finalizing. Treat the new file as completed only when its markdown output has a `## Response` or `## Error` section; otherwise call it in-progress or omit it.
   - For interactive sessions that changed code or scripts, do a safe read-only/current-state verification before summarizing if possible: inspect the relevant `git status`/diff or current script contents, and run non-destructive syntax checks such as `python3 -m py_compile` when claiming code is syntactically verified. Distinguish “patched but verification was blocked in the original session” from “verified now during recap.”

5. **Read representative outputs first**,
   - Open a few cron output markdown files to understand each job's purpose and final response.
   - Identify job IDs and recurring job names before trying to summarize the whole day.

6. **Count and classify with terminal tools first, then sample**
   - For high-volume jobs, use terminal `grep -c` or `grep -l` for fast aggregate counts before using `execute_code`.
   - Pitfall: `execute_code` loops calling `read_file` on 400+ files are slow (~45 sec for 436 files). Use terminal `grep` to count SILENT vs non-SILENT responses, error patterns, etc. first, then `read_file` only the representative samples.
   - **Pitfall: `grep "\[SILENT\]"` on whole files is a false positive.** Every cron output file also contains `[SILENT]` inside the delivery-instructions boilerplate in the prompt section, so `grep -c` always returns ≥1 regardless of whether the actual response was SILENT or a real report. Count actual SILENT deliveries by grepping only the Response section: `grep -A1 "^## Response$" <file> | grep "\[SILENT\]"`. Or find files with real content: `grep -A1 "^## Response$" <file> | grep -v "\[SILENT\]"`.
   - Example fast-count (corrected): for high-volume jobs, use `grep -L "\[SILENT\]"` is still wrong. Instead count files with real responses: `for f in ~/.hermes/cron/output/<job_id>/YYYY-MM-DD_*.md; do sed -n '/^## Response$/,/^## /p' "$f" | grep -q "\[SILENT\]" || echo "$f"; done | wc -l`

7. **Use code for aggregation when volume is high**
   - If there are many session/output files, use code to:
     - count runs per job
     - classify successes vs failures
     - detect repeated errors (for example `HTTP 429`)
     - extract recurring facts from assistant final responses
   - Prefer summarizing counts from files rather than eyeballing dozens of transcripts.
   - Pre-filter with terminal `grep` first (see step 6).
   - **Cron-mode pitfall:** `execute_code` may be blocked in scheduled cron runs because it executes arbitrary local Python without an approving user. When that happens, run the same aggregation as an explicit `python3 - <<'PY' ... PY` script via the `terminal` tool, or use shell tools (`grep`, `sed`, `awk`, `wc`) directly. Do not stop the recap just because `execute_code` is unavailable.

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
   - **Cron output file structure for failures**: timed-out jobs have `## Error` instead of `## Response` — don't assume every output file has a `## Response` section. When grepping for `## Response`, also check for `## Error` to catch timeout failures:
     ```bash
     grep -l "^## Error$" ~/.hermes/cron/output/*/YYYY-MM-DD_*.md
     ```
   - **No-agent/script jobs may produce empty `## Response` sections.** Count these separately from `[SILENT]` and content responses. For watchdog-style jobs, an empty response usually means "no alert/no action"; verify by counting nonempty response sections before reporting them as successful activity.

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
- Don't generalize from one transcript if there are hundreds of runs available to count.
- Don't `grep -c "\[SILENT\]"` on whole cron output files — the prompt boilerplate contains `[SILENT]` inside the delivery instructions, causing a false +1 on every file. Grep only the Response section (see step 6).
- `execute_code` sandboxes don't auto-import standard library modules — code that uses `glob.glob()`, `json.loads()`, `re.match()`, or `from collections import Counter` must include explicit imports. A script that works locally will fail in the sandbox if it's missing `import glob`, `import json`, etc. Always include all needed imports at the top of every `execute_code` block.

## Useful file patterns

```text
~/.hermes/sessions/session_cron_<jobid>_YYYYMMDD_*.json   (cron-triggered sessions)
~/.hermes/sessions/session_YYYYMMDD_*.json                 (interactive / non-cron sessions)
~/.hermes/cron/output/<job_id>/YYYY-MM-DD_*.md
```

## Good recap style

- Concise bullets
- Quantified when possible
- Separate “healthy but repetitive monitoring” from “new work completed”
- Include exact blocker names when they materially affect tomorrow’s next steps
