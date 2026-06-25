# Frontmatter parser and semantic cleanup verification

Use this after an automated wiki-lint pass that edits exactly 20 pages and then performs semantic review of added cross-links.

## Lessons from cron-safe automation

1. **Do not use a line-only frontmatter parser for final whole-vault counts.**
   - YAML list fields such as `tags:` and `sources:` span multiple lines.
   - A verifier that only records `key: value` lines can falsely classify nearly every page as sparse because `tags:` appears with an empty value on the header line.
   - Reuse the same list-aware parser from the main scanner/editor for final counts, or explicitly treat `key:` followed by `- item` lines as a populated list.

2. **Separate batch verification from whole-vault issue counts.**
   - Batch verification should require `updated == run_date` for the 20 touched pages.
   - Whole-vault sparse-frontmatter counts should not require every page to have today’s date; they only need valid required fields and valid status/type.

3. **Semantic cleanup can intentionally leave low-outbound pages.**
   - If heuristic links were added to sparse captures only because of generic tags or high-inbound fallbacks, remove them.
   - Recompute outbound counts and update the same-day log entry rather than appending a second log entry.
   - Report unresolved low-outbound pages as needing source/human context, not as a failed run, when frontmatter/index/log checks pass.

4. **After log repair, verify again.**
   - Confirm the same-day log entry count increased by exactly one relative to the start of the run, or that there is exactly one entry when replacing an already-created same-day entry during repair.
   - Confirm index header date/page_count and all 20 batch titles after any cleanup patch.
