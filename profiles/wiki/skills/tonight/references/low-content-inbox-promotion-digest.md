# Low-content Inbox promotion during tonight runs

Session lesson from a one-source evening run where the queue contained only `Inbox/weight-loss-recipe-facebook-link.md`.

## Durable pattern
- Low-content captures can still be promoted if they are clearly labeled as placeholders and preserve the original source URL in quoted YAML or body text.
- Do not invent missing content. Add explicit follow-up bullets for manual review/transcription.
- Add at least two related wikilinks plus a relevant MOC link before deleting the source.
- Verify the new `Notes/` page is non-empty, then remove the Inbox/root source and rerun `find_today_notes.py --json --inbox`.
- Update `wiki-index.md`, `wiki-log.md`, and the MOC, then immediately search/read back those targets. A patch can appear successful while not inserting a new wiki-index row if the attempted hunk lacks enough context; verify the exact new `[[Page Name]]` row and insert beside an alphabetical neighbor if missing.
- In the digest, `notes_processed` is the current-run processed-source count (for example `1`), not the final queue count (`0` after cleanup). The ad-hoc verifier should assert both values separately.

## Verification fields to include
- `note_exists_nonempty: true`
- `source_removed: true`
- `index_has_note: true`
- `moc_has_note: true`
- `log_has_ingest: true`
- `queue_empty: true`
- `notes_processed_matches_current_run: true`
- `changed_tmp_path_absent: true` when relevant
