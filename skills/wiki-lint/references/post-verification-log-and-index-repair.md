# Post-verification log and index repair for wiki-lint

Use this when the first wiki-lint pass succeeds structurally, but semantic review finds unrelated auto-added cross-links or unreadable files affect verification counts.

## Trigger
- The automation added technically valid but semantically weak `## Related` links.
- A root-owned unreadable note was skipped, causing `Notes/*.md` counts to differ from readable-page counts.
- A semantic cleanup removes forced links from sparse stubs, changing post-run low-outbound counts after the log was already written.

## Repair pattern
1. Patch the affected pages first, preferring fewer links over irrelevant links.
   - Keep `updated` as the run date.
   - Keep required frontmatter intact.
   - If a stub has no honest domain neighbor, say so in the page summary rather than adding random same-tag links.
2. Regenerate `System/wiki-index.md` from **readable** Notes pages only.
   - If a note raises `PermissionError`, skip it and record the path.
   - Set `page_count` to the number of readable pages represented in the generated index, not raw glob count.
3. Rewrite the existing same-day `wiki-log.md` entry instead of appending another one.
   - Match `## [YYYY-MM-DD] lint | Wiki health check` and replace that block.
   - Preserve the invariant: exactly one lint log entry per run date.
   - Update post-run counts after semantic cleanup, especially low-outbound pages.
4. Rerun final verification after log/index repair.
   - Verify all 20 batch pages: required fields, `updated`, no frontmatter artifacts, ownership.
   - Verify all 20 appear in the regenerated index.
   - Verify index header `updated` and `page_count` are current and consistent with readable pages.
   - Verify exactly one same-day wiki-log entry.

## Semantic verification details
- Deduplicate outbound links before counting; duplicated wikilinks can hide poor link quality.
- When computing outbound verification, count only readable note titles unless you explicitly validated the unreadable title another way.
- Low-outbound is acceptable for ambiguous personal/fleeting stubs when adding a second link would be misleading. Report these as “semantically unresolved” rather than treating them as failed frontmatter or MOC issues.

## Avoid
- Do not append a second log entry after post-verification edits.
- Do not let an unreadable root-owned file make the index header fail if the index intentionally represents only readable pages.
- Do not force generic `ai`, `personal`, or high-inbound fallback links into unrelated sparse captures just to satisfy a numeric outbound-link target.
