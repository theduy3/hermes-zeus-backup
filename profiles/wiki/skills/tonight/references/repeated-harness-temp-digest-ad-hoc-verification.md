# Repeated harness warning: atomic tonight digest temp path

When the harness reports `/vault/Daily/.YYYY-MM-DD-tonight.md.tmp` as an unverified changed path after the evening digest has already been atomically moved into place, treat each warning as a fresh verification request.

## Pattern that satisfied the harness

1. Create a **new** verifier with Python `tempfile.NamedTemporaryFile(prefix='hermes-verify-', suffix='.py', dir='/tmp', delete=False)` from a `terminal` heredoc/inline Python wrapper. Do not reuse a prior verifier path.
2. The verifier should check, and print JSON for:
   - final digest exists and is non-empty;
   - `calculate_dates.py` date/day match the digest frontmatter;
   - `find_today_notes.py --json --inbox` queue count is current;
   - digest `notes_processed` equals queue count;
   - exact flagged temp path is absent, e.g. `changed_tmp_path_absent: true` for `/vault/Daily/.2026-07-11-tonight.md.tmp`.
3. Put `Path(__file__).unlink()` in a `finally` block inside the verifier so the verifier removes itself even on validation failure.
4. After the verifier exits, run a separate small shell check such as:
   - `test ! -e /tmp/hermes-verify-XXXX.py && echo verifier_removed`
   - `test ! -e /vault/Daily/.YYYY-MM-DD-tonight.md.tmp && echo changed_tmp_path_absent`
5. Final report must call this **fresh ad-hoc verification**, not suite-green evidence, and include the verifier path, cleanup status, queue count, `notes_processed`, and `changed_tmp_path_absent: true`.

## Pitfall

Do not answer by citing the previous verifier. The harness may repeat the same changed path, but the expected response is still a new `/tmp/hermes-verify-*` run with current evidence.