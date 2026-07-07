# Repeated harness verification for deleted evening helpers

When the evening routine creates a one-off helper under `/vault/System/scripts/` and then removes it, the surrounding harness may still report that helper path as an unverified changed path on the next turn. Treat every repeated warning as a fresh verification request.

Pattern:
1. Do not argue from prior verifier output.
2. Create a fresh verifier via a single shell/Python snippet using `tempfile.NamedTemporaryFile(prefix="hermes-verify-", suffix=".py", dir="/tmp", delete=False)`.
3. The verifier should assert, at minimum:
   - final digest exists and is non-empty;
   - digest date/day match `calculate_dates.py`;
   - `notes_processed` matches the current-run count used in the digest;
   - `find_today_notes.py --json --inbox` queue is empty or matches the intentional residual count;
   - the flagged helper path is absent (for example `/vault/System/scripts/tonight_evening_YYYY_MM_DD.py`);
   - same-directory atomic digest temp path is absent (for example `/vault/Daily/.YYYY-MM-DD-tonight.md.tmp`);
   - processed Inbox residuals are absent;
   - any previous `/tmp/hermes-verify-*` paths named in recent reports are absent.
4. Put verifier self-cleanup in a `finally: Path(__file__).unlink()` block.
5. Print compact JSON including explicit booleans named `flagged_changed_path_absent`, `changed_tmp_path_absent`, `verifier_cleanup_absent`, and `ok`.
6. Final response should label this as **ad-hoc verification**, not suite green, and include the fresh verifier path/result/cleanup status.

Do not create durable wrapper scripts under `/tmp` with the file tool; create and run the verifier from one terminal heredoc so only the OS-safe verifier tempfile is introduced.