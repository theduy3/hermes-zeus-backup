# Zero-note evening digest with repeated temp-path verification

Session pattern captured 2026-07-15 for the `tonight` cron routine.

## Situation
- `find_today_notes.py --json --inbox` returned an empty queue (`count/root_count/inbox_count = 0`).
- The routine still had to overwrite `/vault/Daily/<date>-tonight.md` because zero-note nights are reportable.
- The digest was written via same-directory atomic temp path, then moved into place:
  `/vault/Daily/.<date>-tonight.md.tmp` -> `/vault/Daily/<date>-tonight.md`.
- The harness repeatedly flagged the deleted temp path as an unverified changed path even after successful ad-hoc verification.

## Durable response pattern
On every repeated harness warning, run a fresh verifier created with `tempfile.NamedTemporaryFile(prefix='hermes-verify-', suffix='.py', dir='/tmp', delete=False)` from a `terminal` heredoc. The verifier should:

1. Re-run `System/scripts/calculate_dates.py` from `/vault` and parse with `splitlines()`/`startswith()`.
2. Re-run `System/scripts/find_today_notes.py --json --inbox` from `/vault`.
3. Read the final digest and parse frontmatter fields: `date`, `day`, `notes_processed`.
4. Assert:
   - final digest exists and is non-empty;
   - digest `date`/`day` match `calculate_dates.py`;
   - queue count is the expected verified current-run count;
   - `notes_processed` equals queue count;
   - the exact flagged atomic temp path is absent (`changed_tmp_path_absent: true`).
5. If prior `/tmp/hermes-verify-*` paths are known from earlier verifier output, assert they are absent too.
6. Unlink the verifier script in a `finally` block and print a separate cleanup boolean from the parent heredoc.

## Final report shape
Keep the response compact and explicitly label it as ad-hoc verification, not suite green. Include:

- fresh verifier path;
- verifier cleanup/absence status;
- final digest path;
- digest non-empty status;
- date/day match;
- queue count;
- `notes_processed`;
- exact flagged temp path absence;
- prior verifier path absence if checked.

This pattern satisfies the harness without rewriting the digest or creating new durable helper files.