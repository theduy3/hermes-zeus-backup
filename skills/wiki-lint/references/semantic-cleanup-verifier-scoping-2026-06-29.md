# Semantic cleanup verifier scoping (2026-06-29)

## Trigger
Use this after a wiki-lint run auto-adds related links, then semantic inspection removes weak forced links from sparse/low-context pages.

## Lesson
Final verification should be scoped to the exact cleanup targets, not to every page in the batch. Some links that look generic or weak in one page can be legitimate on another page. A verifier that globally bans a title such as `[[Learn Claude Code Agent Harness Repo]]` or `[[Legal Reserve Note]]` can create false failures when the same link is valid elsewhere.

## Verification pattern
1. Print bounded `## Related` / `Related:` lines for all 20 pages after the first run.
2. Manually/semantically identify weak forced links and remove only those specific line occurrences from the affected pages.
3. Rerun counts from final files. Count only outbound links to direct `/vault/Notes/*.md` pages; MOC links such as `[[Personal MOC]]` are useful navigation but do not satisfy the 2-note cross-reference rule.
4. Rewrite the same-day wiki-log lint entry to match the final post-cleanup counts.
5. Use an ad-hoc verifier that:
   - compiles helper scripts,
   - checks all 20 pages have `updated: <today>` and required frontmatter,
   - checks no conflict markers remain,
   - checks weak-link removals only on the targeted pages/line occurrences,
   - confirms the index header/date/page_count and rows for all 20 pages,
   - confirms exactly one same-day lint log entry and that its low-outbound count matches final counts.

## Reporting
If cleanup leaves pages with only MOC links or no direct note links, report them as honest low-outbound pages. Do not re-add unrelated links just to make the count zero.