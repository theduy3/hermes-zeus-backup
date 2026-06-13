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
4. For very sparse/personal/fleeting stubs, a relevant MOC plus a true workflow/context note is better than forcing a random same-tag page. Avoid letting a generic `ai` tag connect language notes, legal stubs, or mobile captures to Claude/AI pages unless the body actually discusses AI.
5. For repo/source notes, prefer a same-domain entity/product page or same operational category (e.g. email/self-hosted/customer-support) over an arbitrary high-inbound or recently ingested GitHub source.
6. Treat generic shared tags (`ai`, `reference`, `legal`, `personal`, `fleeting`, `to-process`) as insufficient evidence by themselves. During review, remove links that were added only because of these generic tags (e.g. a Korean phrase stub linked to an AI workflow page, or a vague reference capture linked to unrelated reference pages).
7. Check for contradictions between the generated summary and the generated `## Related` section. If the summary says “no second wiki page is forced” but the Related section contains forced links, remove the Related links and update verification/log counts accordingly.
8. If no genuinely relevant second link exists, prefer a relevant MOC or leave the page counted as low-outbound for future human/ingest work rather than forcing an unrelated note.

## Final verification shape

After any semantic link patch, rerun verification checks for all 20 pages:
- frontmatter has required fields and `updated` equals the run date
- no `>> NEW >>` / `<< OLD <<` artifacts in frontmatter
- page owner is not unexpectedly root for rewritten pages
- index header date/page_count are current
- all 20 batch titles appear in index rows
- exactly one log entry was appended for the run date
