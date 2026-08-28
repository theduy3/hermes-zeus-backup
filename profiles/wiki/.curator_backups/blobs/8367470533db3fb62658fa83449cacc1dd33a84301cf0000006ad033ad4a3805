# Evening digest: existing-file overwrite hygiene

Session pattern: a zero-note `tonight` cron run found an existing `/vault/Daily/YYYY-MM-DD-tonight.md`, only checked that it existed, then overwrote it. Hermes emitted a sibling-write warning because the agent had not read the file before writing.

Reusable checklist:

1. Use `calculate_dates.py` for `YYYY-MM-DD` and day.
2. Run `find_today_notes.py --json --inbox` and process/fold any queued captures before writing the digest.
3. If `/vault/Daily/<date>-tonight.md` already exists, read it before overwrite. Do not rely on a file-existence search alone.
   - This gives an audit trail for the overwritten content.
   - It lets the agent notice concurrent-run information worth preserving or explicitly replacing.
   - It avoids Hermes warnings about writing a sibling-modified file that the current agent never read.
4. Write the final digest (atomic same-directory temp + `os.replace` if direct overwrite is blocked or if the task skill requires it).
5. Freshly verify:
   - final digest exists and is non-empty;
   - frontmatter date/day match `calculate_dates.py`;
   - `notes_processed` equals the current-run filed/folded count, including `0` for a real zero-note digest;
   - post-run root/Inbox queue is empty;
   - any same-directory temp digest path is absent.
6. Use a fresh `/tmp/hermes-verify-*.py` verifier and ensure it self-removes; then separately check/report verifier removal.
