# Fresh verification after repeated deleted-helper warnings

Use this when the harness reports an unverified changed path for a one-off evening helper that has already been removed (for example `/vault/System/scripts/hermes-tonight-YYYY-MM-DD-helper.py`).

## Pattern
1. Treat every repeated harness warning as a fresh verification request, even if a previous verifier passed minutes ago.
2. Create a new verifier with `tempfile.NamedTemporaryFile(prefix="hermes-verify-", suffix=".py", dir="/tmp", delete=False)` from a `terminal` heredoc; do not use a durable wrapper path.
3. The verifier should assert, at minimum:
   - flagged helper path is absent;
   - same-directory atomic digest temp path is absent;
   - final digest exists and is non-empty;
   - digest date/day match `System/scripts/calculate_dates.py`;
   - `notes_processed` matches the verified current-run count;
   - `find_today_notes.py --json --inbox` returns an empty queue after filing;
   - promoted note/source archive exist and are non-empty when the run processed a note;
   - original Inbox capture is absent after verified promotion.
4. Put `Path(__file__).unlink()` in a `finally` block, then report both cleanup attempted and whether the verifier exists afterward.
5. In the final reply, call it **fresh ad-hoc verification**, not a canonical suite result, and name the flagged helper absence check explicitly.

## Pitfall
Do not argue that earlier verification is sufficient. The harness expects current-turn evidence and may repeat the same changed path after a deleted helper; run a new verifier each time.