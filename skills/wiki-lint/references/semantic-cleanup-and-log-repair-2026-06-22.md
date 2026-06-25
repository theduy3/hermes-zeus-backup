# Semantic cleanup and log repair after auto-linking (2026-06-22)

Use this when a wiki-lint run auto-adds `Related:` links to satisfy the 2-outbound rule, especially for sparse captures.

## What happened
- The automated run initially reported `low_outbound: 0` because it inserted heuristic links into four sparse captures.
- Manual inspection showed several links were weak or misleading:
  - `Legal Reserve Note` -> finance/trading pages
  - `Grace Leung YouTube Channel` -> Claude Code course/repo pages
  - `Korean Greeting Phrases` -> Claude Code course page
  - `MYLE GoalAccess Capture` -> generic AI/knowledge pages
- Those links were removed and the same-day log entry was rewritten to report the honest post-cleanup state: 4 low-outbound pages remain.

## Durable workflow
1. After automated related-link insertion, print the full `## Related` block for every page that received links, not only the generated `Related:` line.
2. Remove links that are supported only by generic tags such as `ai`, `personal-development`, `knowledge-management`, or high inbound count.
3. Prefer leaving a page low-outbound when the source capture is too sparse to establish semantic neighbors.
4. Rerun verification after cleanup and recompute low-outbound from the edited files.
5. Rewrite the same-day `wiki-log.md` entry rather than appending a second lint entry.
6. In the final report, say the page is intentionally unresolved for source/human context; do not present honest low-outbound counts as a failed run.

## Verification fields to include
- `low_outbound_titles` after semantic cleanup.
- Related lines after cleanup for each sparse page inspected.
- `same_day_lint_log_entries == 1`.
- All 20 batch pages still have required frontmatter and `updated == run_date`.
