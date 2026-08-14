# Repeated harness temp-digest warning — current-turn verifier pattern

Use when the harness repeats `Verification status: unverified` for a deleted same-directory atomic digest temp file such as `/vault/Daily/.YYYY-MM-DD-tonight.md.tmp`, even after a previous verifier passed.

## Pattern

1. Treat the warning as a fresh verification request, not a dispute about earlier evidence.
2. Create a new OS-safe verifier path with `tempfile.NamedTemporaryFile(prefix='hermes-verify-', suffix='.py', dir='/tmp', delete=False)` from a `terminal` heredoc; do not write a durable wrapper helper.
3. The verifier should assert:
   - final digest exists and is non-empty;
   - digest frontmatter date/day match `System/scripts/calculate_dates.py`;
   - `notes_processed` matches the verified current-run filing count;
   - `find_today_notes.py --json --inbox` queue is empty after the run;
   - the exact flagged temp path is absent (`changed_tmp_path_absent: true`);
   - known prior `/tmp/hermes-verify-*` paths are absent when they were named in the conversation.
4. Put `Path(__file__).unlink()` in a `finally` block inside the verifier, then have the outer heredoc report `verifier_removed_after_run`.
5. Final response should explicitly call it **fresh ad-hoc verification**, include the verifier path, cleanup status, queue counts, and `changed_tmp_path_absent: true`.

## Why

The harness may continue to report the same deleted temp file as an unverified changed path. It only accepts fresh current-turn evidence, so citing earlier verifier output is insufficient.