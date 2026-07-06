# Fresh ad-hoc verification when the harness flags temp/helper paths

Use this when the evening routine wrote the digest successfully, but the coding harness returns a repeated "changed paths lack verification" warning for transient paths such as:

- `/vault/Daily/.YYYY-MM-DD-tonight.md.tmp`
- `/tmp/hermes-create-tonight-verifier.py`
- `/tmp/hermes-create-tonight-verifier-2.py`
- a previous `/tmp/hermes-verify-*.py`

## Pattern

1. Treat every repeated harness warning as a new verification request. Do not cite an earlier verifier as sufficient.
2. Do not create another durable wrapper script with the file tool. Run one terminal heredoc that itself creates a fresh OS-safe verifier via `tempfile.NamedTemporaryFile(prefix='hermes-verify-', suffix='.py', dir='/tmp', delete=False)`.
3. Inside the verifier:
   - Verify the final digest exists and is non-empty.
   - Parse `calculate_dates.py` with simple `splitlines()`/`startswith()` logic:
     - `Today:` supplies the day name.
     - `Date:` supplies the canonical `YYYY-MM-DD`.
   - Rerun `find_today_notes.py --json --inbox`.
   - Parse `notes_processed` from digest frontmatter.
   - Assert `notes_processed == queue.count` for the current run.
   - Explicitly assert absence of every path named in the harness warning, especially the same-directory atomic temp digest path.
   - Unlink `Path(__file__)` in a `finally` block.
4. Print compact JSON containing at least:
   - `ad_hoc_verification: true`
   - `digest_exists`, `digest_nonempty`
   - `date_from_calculate_dates`, `day_from_calculate_dates`
   - `queue_count`, `notes_processed`
   - `notes_processed_matches_verified_current_run_count`
   - `changed_tmp_path_absent`
   - `changed_paths_absent` for every flagged path
   - `ok`
5. In the final report, call it **ad-hoc verification**, not suite-green/canonical tests.

## Pitfall captured from a cron session

Writing wrapper files like `/tmp/hermes-create-tonight-verifier.py` with the file tool can itself create more changed paths that the harness asks to verify. Prefer inline terminal generation of the fresh verifier, and if wrapper paths already exist, remove them or assert they are absent in the next fresh verifier output.
