# Repeated temp-digest verification warning pattern

Use this when a headless evening run writes the digest through a same-directory atomic temp file and the harness repeatedly reports the deleted temp path (for example `/vault/Daily/.YYYY-MM-DD-tonight.md.tmp`) as an unverified changed path.

Pattern that passed in session:

1. Treat each harness warning as a fresh verification request, even when an earlier ad-hoc verifier already passed.
2. Create a new OS-safe verifier with `tempfile.NamedTemporaryFile(prefix='hermes-verify-', suffix='.py', dir='/tmp', delete=False)` from a one-shot `python3 - <<'PY'` heredoc. Do not use `write_file` for wrapper scripts.
3. The verifier should assert:
   - final digest exists and is non-empty;
   - `calculate_dates.py` date/day match digest frontmatter;
   - `find_today_notes.py --json --inbox` queue count is current;
   - digest `notes_processed` equals the current queue count;
   - the exact flagged atomic temp path is absent;
   - known prior `/tmp/hermes-verify-*.py` verifier paths are absent when available.
4. In the verifier `finally`, unlink `Path(__file__)` so cleanup happens even on failure.
5. The outer heredoc should print both the verifier JSON and a cleanup JSON containing `verifier_removed: true`.
6. Final report should explicitly call the result **ad-hoc verification**, not suite-green, and name the flagged temp absence check.

Minimal report fields:

- `Verifier: /tmp/hermes-verify-<random>.py`
- `Verifier removed: true`
- `Digest exists/non-empty: <path>`
- `Queue count verified: <n>`
- `notes_processed matches queue count: true`
- `Flagged changed temp path absent: <path>`
