# Repeated harness warning: deleted same-directory digest temp path

Use this when the evening routine already wrote `/vault/Daily/<date>-tonight.md` atomically via a same-directory temp file, the temp file was moved/removed, but the harness repeats an unverified changed-path warning for `/vault/Daily/.<date>-tonight.md.tmp`.

## Required current-turn response

1. Treat the warning as a fresh verification request; do not cite an earlier verifier as sufficient.
2. Create a new OS-safe `/tmp/hermes-verify-*.py` using `tempfile.NamedTemporaryFile(prefix='hermes-verify-', suffix='.py', dir='/tmp', delete=False)` from a `terminal` heredoc.
3. The verifier must assert:
   - final digest exists and is non-empty;
   - frontmatter date/day match `/vault/System/scripts/calculate_dates.py`;
   - `notes_processed` equals the current-run filed/folded count;
   - `find_today_notes.py --json --inbox` reports `count/root_count/inbox_count == 0` when the run processed everything;
   - the exact flagged same-directory temp path is absent, reported as `changed_tmp_path_absent: true`;
   - known prior `/tmp/hermes-verify-*` paths are absent when the harness keeps mentioning them.
4. Put `Path(__file__).unlink()` in a `finally` block inside the verifier so self-cleanup happens even on assertion/parsing failure.
5. Print compact JSON from both the verifier and the wrapper showing verifier path, return code, and `cleanup_absent`.
6. Final reply should explicitly label the result **fresh ad-hoc verification**, include the verifier path, cleanup status, digest path, queue count, `notes_processed`, and `changed_tmp_path_absent: true`.

## Pitfalls

- Do not answer from previous evidence; repeated harness warnings require new current-turn evidence.
- Do not use a deterministic verifier filename or durable wrapper under `/tmp`; those can themselves become changed-path warnings.
- Do not claim suite/canonical green. This is an ad-hoc verifier for a Markdown digest and deleted temp path.
