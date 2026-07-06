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

### Pitfall: helper-script dependency recovery
If `fetch_watchlist.py`, `fetch_earnings_reports.py`, or `fetch_lunar_date.py` fail because optional Python packages are missing, try installing the missing packages into the active Hermes venv before falling back to a skipped section:

```bash
python3 -m pip install yfinance lunardate
```

Do **not** use `--user` from inside the Hermes venv; user site-packages may be hidden and the install can fail. After installing, rerun only the failed helper scripts and continue assembly with the recovered outputs. If install or rerun still fails, include the skipped/unavailable note and complete the briefing.

### Pitfall: post-processing helper-script output
When assembling the daily Markdown manually from helper outputs, sanitize embedded helper sections before writing:
- `compile_tasks.py` appends a `---` separator and `**Summary**` block after `Later / No Date`; do **not** include that summary inside the daily file body. Use it only for the final confirmation/report. Strip this robustly: the separator may appear as either `\n---\n\n**Summary**` or `\n---\n**Summary**`, so use a regex such as `\n---\n\s*\*\*Summary\*\*:[\s\S]*?(?=\n---\n\n## Morning Brew|\Z)` after assembly if needed, then re-verify `**Summary**` is absent.
- `fetch_weather.py` returns both `## Weather Forecast (7-Day)` and `## Moon Phase`; after splitting out the moon phase, trim any trailing `---` so the final daily file does not contain duplicate horizontal rules before `*Generated:*`.
- Most helper outputs that already start with their own `## ...` heading (finance news, earnings, Morning Brew, weather) should have that first heading stripped before insertion under the canonical daily heading, but do not strip the stock watchlist because it starts directly with tables. Strip by prefix/heading level, not only exact title: e.g. `fetch_finance_news.py` may output `## Finance News (Top Headlines)`, which must not remain as a nested duplicate under the canonical `## Finance News`.
- In scheduled/headless runs, do output processing and file assembly with a terminal-launched Python script in `/tmp/`, then inspect the result with `read_file`; this keeps the workflow inside the cron-safe tool path and preserves the `/vault` write workaround.
- Keep helper stdout and stderr separate when assembling the daily body. Some helpers/libraries (notably Yahoo/yfinance in `fetch_watchlist.py`) can print recoverable warnings such as ticker 404s to stderr while still producing valid markdown on stdout. Insert stdout into the daily file; reserve stderr for the final run report or a skipped-section note only when the helper truly failed. As a final guard, verify helper warning strings like `HTTP Error` did not leak into the generated note.
- After writing, verify the actual file by reading/counting sections: expected task counts should match the compiler summary, `**Summary**` should be absent from the file body, helper stderr/warning text such as `HTTP Error` should be absent, `\n---\n\n---\n` should not appear, and `## Moon Phase` should appear exactly once.
- `fetch_weather.py` includes both weather and moon output. When removing the moon block from the weather section, allow optional blank lines around the separator, e.g. `\n---\n\s*## Moon Phase\n[\s\S]*?(?=\n---\n\s*\*Generated:|\Z)` or split on the final `## Moon Phase` block. A too-strict regex can leave a duplicate Moon Phase section at the bottom of the generated note even though the top canonical Moon Phase section is correct.
- When parsing `calculate_dates.py` output in a helper script, use multiline regex (`re.M`) for fields like `^Week`, `^Date`, and `^Victoria`; otherwise the daily header can end up with blank week/Victoria values even though the script output was correct.
- When verifying task counts by Markdown section, account for headings with suffixes such as `## This Week (YYYY-MM-DD to YYYY-MM-DD)`. Match `^## This Week(?: .*?)?$` rather than only the bare heading, or verification may falsely count zero tasks.
