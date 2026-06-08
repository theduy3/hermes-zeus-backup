---
name: today
description: Generate the theduyvault daily briefing (tasks, finance, weather, lunar, quote) into Daily/. Scheduled headless job.
version: 1.0.0
metadata:
  hermes:
    requires_toolsets: [terminal, file]
    tags: [vault, daily, theduyvault]
---

# today — theduyvault daily briefing (headless)

You are running as a scheduled cron job. No human is watching: never ask for
confirmation, never stop to ask a question. Run the full "all tasks" briefing
(no project filter).

## Canonical instructions
Read and follow **`/vault/.claude/skills/today/SKILL.md`** exactly — it lists every
step (date context, sync task status, compile tasks, watchlist, finance news,
earnings, horoscope, weather, lunar date, Morning Brew, quote) and the exact output
format for the daily file.

## Runtime adaptations (this environment)
- The vault is mounted at **`/vault`** (not `/root/theduyvault`). Run every helper as
  an absolute path, e.g. `python3 /vault/System/scripts/calculate_dates.py`. The
  scripts self-locate the vault from their own path, so any working directory is fine.
- Write the briefing to **`/vault/Daily/<YYYY-MM-DD>.md`**.
- Vault conventions live in `/vault/CLAUDE.md`; the daily-file frontmatter/format is in
  the canonical skill above — match it precisely.
- Use the **terminal** tool for the `python3` scripts. If a fetch script fails
  (e.g. missing `NEWS_API_KEY`), include whatever sections succeeded and note the
  skipped one — do not abort the whole briefing.

### Pitfall: writing the daily file to the vault
The `write_file` tool and `execute_code` sandbox **cannot write to `/vault/`** —
they run as a different user and get PermissionError. Shell redirection (`cat >
/vault/...`) also fails with PermissionError. The only reliable method is
**terminal-launched Python** (runs as `hermes`, who owns the vault directories):

1. Write a helper Python script to `/tmp/` using `cat > /tmp/daily_out.py << 'PYEOF'`
2. Use Python raw strings (`r"""..."""`) for the file content — this avoids shell
   interpreting `&` in URLs and HTML entities as background operators
3. Run it: `python3 /tmp/daily_out.py`
4. If a root-owned stale file exists at the target path (from a prior `write_file`
   attempt), the script can `os.remove()` it first (hermes owns the directory, so
   delete-by-name works even on root-owned files), then write the new one

See `references/vault-write-workaround.md` for the exact code template.

### Pitfall: post-processing helper-script output
When assembling the daily Markdown manually from helper outputs, sanitize embedded helper sections before writing:
- `compile_tasks.py` appends a `---` separator and `**Summary**` block after `Later / No Date`; do **not** include that summary inside the daily file body. Use it only for the final confirmation/report.
- `fetch_weather.py` returns both `## Weather Forecast (7-Day)` and `## Moon Phase`; after splitting out the moon phase, trim any trailing `---` so the final daily file does not contain duplicate horizontal rules before `*Generated:*`.
- After writing, verify the actual file by reading/counting sections: expected task counts should match the compiler summary, `**Summary**` should be absent from the file body, and `\n---\n\n---\n` should not appear.
- When parsing `calculate_dates.py` output in a helper script, use multiline regex (`re.M`) for fields like `^Week`, `^Date`, and `^Victoria`; otherwise the daily header can end up with blank week/Victoria values even though the script output was correct.
- When verifying task counts by Markdown section, account for headings with suffixes such as `## This Week (YYYY-MM-DD to YYYY-MM-DD)`. Match `^## This Week(?: .*?)?$` rather than only the bare heading, or verification may falsely count zero tasks.
