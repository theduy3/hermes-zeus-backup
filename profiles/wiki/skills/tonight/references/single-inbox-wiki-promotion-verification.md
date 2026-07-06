# Single Inbox Wiki Promotion + Tonight Digest Verification

Use this pattern when the evening routine has one or a small number of Markdown captures in `/vault/Inbox/` that should become wiki pages directly (skip the `wiki-ingest` hop, per `tonight`).

## Durable pattern from a successful run

1. Get canonical date/day from `python3 System/scripts/calculate_dates.py`.
2. Treat `python3 System/scripts/find_today_notes.py --json --inbox` as a work queue, then read each source before writing.
3. Write a deterministic, idempotent helper under `/vault/System/scripts/` only if multi-file mutation is easier than hand patches. The helper should:
   - write the `Notes/` page atomically and verify it is non-empty,
   - update the relevant MOC, `System/wiki-index.md`, and `System/wiki-log.md` idempotently,
   - remove the source only after the new page is readable,
   - rerun the queue check,
   - write/overwrite `/vault/Daily/<date>-tonight.md` atomically,
   - print compact JSON with `notes_processed`, queue counts, digest path, and update flags.
4. After the helper, verify using ordinary tools, not only the helper's self-report:
   - read back the digest,
   - read back the created/updated note,
   - run `find_today_notes.py --json --inbox`,
   - search the MOC/index/log for the new page title.
5. Run a fresh `/tmp/hermes-verify-*.py` ad-hoc verifier created with `tempfile.NamedTemporaryFile(..., prefix="hermes-verify-", suffix=".py", dir="/tmp", delete=False)`. It should check:
   - digest exists and is non-empty,
   - date/day match `calculate_dates.py`,
   - queue count is empty after processing,
   - `notes_processed` equals the verified current-run processed-source count,
   - expected note wikilink appears in the digest when notes were processed.
6. Remove the `/tmp/hermes-verify-*.py` verifier and the one-off `/vault/System/scripts/` helper before the final report.

## Pitfalls

- Do not confuse post-run queue count with `notes_processed`. A successful run can have `queue_after_count: 0` and `notes_processed: 1`; the digest should report the current-run processed-source count.
- Do not trust an existing digest as completion if the queue still has items. Process the queue, then overwrite the digest with verified counts.
- Do not leave one-off helper scripts in `System/scripts/`; they are allowed during the run but should be cleaned up unless intentionally promoted to reusable infrastructure.
