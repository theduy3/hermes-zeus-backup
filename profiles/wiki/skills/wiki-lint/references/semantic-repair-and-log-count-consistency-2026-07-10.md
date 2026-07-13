# Semantic repair and log-count consistency after exact-20 lint (2026-07-10)

## Context
An exact-20 scheduled wiki-lint run structurally succeeded, then the required semantic review found weak auto-added `## Related` links on sparse/low-context pages. The weak links were removed rather than replaced with unrelated links, leaving those pages honestly low-outbound.

## Durable lessons

1. **Verification should distinguish structural pass from low-outbound honesty.**
   - A touched page can be valid when it has `updated: <run-date>`, valid `type`, valid `wiki_status`, tags, MOC membership, an index row, and no conflict markers, even if it has fewer than two outbound note links.
   - Do not make final verification fail solely because semantic repair removed forced links from sparse captures.

2. **Remove weak links introduced by token/tag accidents.**
   - Examples removed as weak in this run:
     - `Grace Leung YouTube Channel` → Claude Code references (generic `youtube/video/ai` overlap, no channel content proving relation)
     - `Legal Reserve Note` → image-capture / MYLE notes (generic sparse-capture overlap)
     - `Korean Greeting Phrases` → Vietnamese/Antigravity notes (language/personal tags too broad)
     - `2026-W28` → AI sprint framework (weekly-review/workflow overlap too broad without direct body evidence)
     - Canadian Conservative article → `Mortgage Market` (cost-of-living/housing too broad for a politics article)
   - Prefer no replacement over a misleading replacement when no close subject neighbor exists.

3. **Correct provenance links when the page itself identifies the source issue.**
   - `Ma Ning China World Cup Referee` initially got an incorrect Economist issue link from heuristic matching; semantic review corrected it to the issue named in the page body/frontmatter.
   - For Economist article pages, use page-local `issue:` or original headline context before selecting a source-issue link.

4. **After semantic cleanup, regenerate infrastructure and rewrite the same-day log entry.**
   - Regenerate `System/wiki-index.md` after page patches.
   - Rewrite the existing same-day `wiki-log.md` lint entry instead of appending a second one.
   - Re-run exact-20 verification after the log/index repair.

5. **Use the same orphan-counting semantics in post-repair logs as in the pre-scan.**
   - A quick naive corpus count can inflate orphan counts because it ignores the skill’s intentional filters and MOC/index cross-checking.
   - If a repair script needs to update the log after semantic cleanup, either reuse the original scanner’s orphan logic or carry forward the pre/post orphan counts from the verified main run. Do not write a naive orphan count into the log.

## Verification checklist addendum
- All 20 touched pages have `updated` equal to the run date.
- Frontmatter has valid `type`, `wiki_status`, and non-empty `tags`.
- No `>> NEW >>` / `<< OLD <<` markers remain in touched pages.
- No MOC links remain in touched pages’ `## Related` sections.
- Low-outbound touched pages are listed honestly rather than backfilled with broad-tag links.
- Index header date/page_count is current and all 20 titles have rows.
- Exactly one same-day lint log entry exists, and its issue counts use the canonical scanner semantics.