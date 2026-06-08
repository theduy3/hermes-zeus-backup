# Cron wiki-lint permission and semantic verification notes

Use this as a compact reference when a scheduled wiki-lint run is implementing its own scanner/editor.

## Read-permission pitfall

Some root-owned vault notes may be mode `600`, which means the `hermes` user cannot even read them. This is different from the common root-owned write failure where deleting/recreating the file works after content is already known.

Recommended scanner behavior:
1. Wrap every Notes/MOCs read in `try/except PermissionError`.
2. Skip unreadable files for the bounded run rather than aborting the cron job.
3. Record skipped paths in the JSON/report and wiki-log notes if relevant.
4. Do **not** delete an unreadable note just to satisfy the batch; without read access, the content cannot be preserved.
5. Continue selecting exactly 20 readable issue-bearing pages.

## Semantic cross-reference verification

Heuristic related-link selection can produce technically valid but semantically poor links, especially for short/stub pages with generic tags. After the first pass:
1. Print or inspect the `## Related` links for all 20 batch pages.
2. Replace unrelated generic links with closer domain neighbors before final verification.
3. Use title/file searches to find better neighbors, e.g. browser pages for browser notes, travel pages for travel notes, source/repo pages for GitHub source notes.
4. If no genuinely relevant second link exists, prefer a relevant MOC or leave the page counted as low-outbound for future human/ingest work rather than forcing an unrelated note.

## Final verification shape

After any semantic link patch, rerun verification checks for all 20 pages:
- frontmatter has required fields and `updated` equals the run date
- no `>> NEW >>` / `<< OLD <<` artifacts in frontmatter
- page owner is not unexpectedly root for rewritten pages
- index header date/page_count are current
- all 20 batch titles appear in index rows
- exactly one log entry was appended for the run date
