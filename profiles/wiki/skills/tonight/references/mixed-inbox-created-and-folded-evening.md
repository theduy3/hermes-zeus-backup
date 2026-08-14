# Mixed Inbox evening run: created pages + folded captures

Use this pattern when the evening queue contains more than one processable Inbox source and the right outcome is mixed: some captures become new `Notes/` pages while others update existing pages.

## Durable pattern

1. Treat `find_today_notes.py --json --inbox` as the queue, then read each source before deciding whether to create, fold, or remove.
2. Search existing `Notes/` for the durable topic before creating pages. If a page already covers the topic, fold the capture into that page rather than creating a duplicate.
3. For a substantial newsletter/source with two distinct durable topics, create separate atomic pages rather than one broad digest page. Preserve the source URL in `sources:` and add at least two useful wikilinks plus relevant MOC links.
4. For a short social/thread capture that refreshes an existing concept, update the existing page frontmatter (`updated`, `sources`) and add a concise section with the new checklist/facts.
5. Update relevant MOCs with one-line summaries, update `System/wiki-index.md` for new pages and touched existing rows, and append one `System/wiki-log.md` entry listing created pages, folded pages, MOCs touched, and archive/removal status.
6. Only remove each Inbox source after readback confirms the target note exists and is non-empty. Archive substantial newsletter originals to `Sources/Newsletter/` when that convention is already in use; low-value folded captures may be removed after verified fold-in.
7. Rerun `find_today_notes.py --json --inbox`; the post-run queue should be `0` unless a source is intentionally left in place.
8. Write/overwrite the nightly digest. `notes_processed` is the number of source captures filed/folded in this run, not the number of new pages and not the final queue count.
9. Run a fresh `/tmp/hermes-verify-*` ad-hoc verifier that checks digest date/day from `calculate_dates.py`, digest non-empty status, `notes_processed`, queue count, created/touched notes, archive existence, source absence, and same-directory temp digest absence.

## Digest wording

For mixed outcomes, list both created pages and folded/updated pages under `## Notes Filed`, e.g.:

- `[[New Page]] - Created from <source>...`
- `[[Existing Page]] - Updated with folded Inbox capture...`

Then include a short verification section naming the archive/removal behavior and the final queue count.