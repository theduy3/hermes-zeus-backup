# Semantic cleanup for low-context captures (2026-06-23)

## Trigger
During a 20-page wiki-lint run, the automation correctly selected exactly 20 pages and verified frontmatter/index/log, but its first-pass related-link filler added weak links to sparse captures whose bodies did not justify them.

Examples removed as weak forced links:
- `Legal Reserve Note` → finance/legal pages picked from tags only.
- `Grace Leung YouTube Channel` → Claude-course pages picked from broad `ai`/`claude-code` tags only.
- `Korean Greeting Phrases` → generic personal-development page.
- `MYLE GoalAccess Capture` → generic AI/knowledge-management pages.
- `10 Non-Boring Real World AI Use Cases` → Obsidian/QMD pages despite an empty source body.

## Durable workflow
1. After any automated related-link insertion, print every batch `## Related`, `Related:`, and bullet wikilink line.
2. Inspect sparse/low-context captures first. If the page says source context is missing, do not let broad tags (`ai`, `reference`, `personal-development`, `finance`, `fleeting`) justify extra links.
3. Remove weak forced links even when that makes the post-run `low_outbound` count non-zero.
4. If a page is essentially empty, add only a small honest stub summary/title if needed; do not invent source content.
5. Rewrite the same-day wiki-log entry rather than appending a second entry. The log should explicitly say low-outbound pages remain semantically unresolved after removing weak forced links.
6. Rerun final verification after cleanup: all 20 pages, index header/page_count/all batch rows, and exactly one same-day lint log entry.

## Reporting pattern
Treat these as successful structural lint runs with honest semantic backlog:
- `Remaining: 0 structural/stale pages; N low-outbound pages remain semantically unresolved after removing weak forced links`
- list the unresolved page titles in both the wiki-log and final report.

## Pitfall
A structural verification with `out_note_links >= 2` can be worse than a non-zero low-outbound count if those links are irrelevant. Semantic integrity wins over the numeric 2-link target for low-context captures.
