# Ad-hoc verification harness handshake

Use this when the evening routine creates or overwrites `Daily/<date>-tonight.md` and the harness reports the changed Markdown file as unverified because no canonical test/lint/build command exists.

## Pattern

1. Run a **fresh** verification script; do not rely on a previous verifier transcript if the harness repeats the warning.
2. Create the script with Python `tempfile.mkstemp(prefix='hermes-verify-', suffix='.py', dir='/tmp')` so the path is OS-safe and visibly matches the harness requirement.
3. The verifier should check, at minimum:
   - digest exists and is non-empty;
   - digest frontmatter `date` and `day` match `System/scripts/calculate_dates.py`;
   - a fresh `System/scripts/find_today_notes.py --json --inbox` queue check returns the expected current-run count;
   - digest frontmatter `notes_processed` equals that fresh queue count.
4. Always remove the verifier in a `finally` block and report `exists_after: false` when cleanup succeeds.
5. In the final response, call the result **ad-hoc verification**, not suite-green/canonical verification, and include the verifier path, exit code, key fields, and cleanup status.

## Pitfall

If the harness repeats the same unverified changed-path warning after a passing ad-hoc check, treat it as a request for new evidence in the current turn. Run a new `/tmp/hermes-verify-*` verifier rather than arguing from, quoting, or reusing the earlier run.
