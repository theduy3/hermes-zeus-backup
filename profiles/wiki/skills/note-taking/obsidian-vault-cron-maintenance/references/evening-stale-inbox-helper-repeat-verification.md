# Evening Digest: Stale Inbox Item + Deleted Helper Repeat Verification

Use this when a headless evening/digest job promotes some queued Markdown captures, another queued source disappears before readback, and the harness later repeats a warning about a removed helper under the vault.

## Durable pattern

1. Treat `find_today_notes.py --json --inbox` as a work queue, not proof that every source still exists.
2. Before creating or updating a note, read the source path. If it is gone or empty:
   - Do not recreate it.
   - Search for distinctive title/source URL/content when available to avoid duplicates.
   - If no already-filed page is verified, report it as a skipped stale queue item.
   - Do not increment `notes_processed` for the disappeared source unless it was folded into a verified page during the current run.
3. For each successfully promoted Markdown capture:
   - Write/read back the atomic `Notes/` page.
   - Update MOCs, wiki-index, and wiki-log idempotently.
   - Delete the Inbox/root source only after the new/updated page is non-empty and readable.
4. Always write or overwrite the digest with the verified current-run count, then rerun the queue finder and require post-run queue count `0`.
5. If a deterministic helper is needed under `/vault/System/scripts/`, make it idempotent, emit compact JSON, then remove it after digest and queue verification succeed.

## Repeated harness warning for a removed helper

When the harness repeats an unverified-changed-path warning for an already-deleted one-off helper, treat it as a new verification request. Do not cite prior verifier output as sufficient. Run a fresh `/tmp/hermes-verify-*` verifier and explicitly assert:

- `flagged_changed_path_absent: true` for the exact helper path.
- `changed_tmp_path_absent: true` for the same-directory atomic digest temp path.
- Prior verifier paths are absent when known.
- Digest exists and is non-empty.
- Digest date/day match `calculate_dates.py`.
- `notes_processed` matches the verified current-run filing/folding count.
- Post-run Inbox queue count is `0`.
- Newly filed notes exist and are linked from the digest when applicable.
- The current verifier removed itself after execution.

## Final report wording

Keep the report compact and label the check accurately:

- Say "fresh/current-turn ad-hoc verification", not "canonical suite green".
- Include the digest path, `notes_processed`, skipped stale sources, exact verifier path, and cleanup status.
- Include the two explicit absence booleans when they were the warning trigger: `flagged_changed_path_absent: true` and `changed_tmp_path_absent: true`.
