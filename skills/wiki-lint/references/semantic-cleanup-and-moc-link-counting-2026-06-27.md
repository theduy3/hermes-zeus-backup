# Semantic cleanup + MOC link counting (2026-06-27)

Session learning from a scheduled wiki-lint run that processed exactly 20 direct `/vault/Notes/*.md` pages.

## What happened
- The automated pass added some heuristic `## Related` links to sparse captures.
- Post-generation inspection found several weak links that were only tag-adjacent, not semantically grounded:
  - `Legal Reserve Note` → `QuantAgent Multi-Agent Trading System`
  - `Grace Leung YouTube Channel` → `Learn Claude Code Agent Harness Repo`
  - `Korean Greeting Phrases` → `Vietnamese Early Childhood Learning Materials`
  - `10 Non-Boring Real World AI Use Cases` → `World Monitor Global Intelligence Dashboard`
  - `Mind Games Pro E-Ink App Review` → `Obsidian Mind Vault Template`
- Those links were removed, the index was regenerated, and the same-day wiki-log entry was rewritten from the final edited files.
- The verified low-outbound count increased honestly after cleanup. That is correct; do not preserve a lower pre-cleanup count by keeping weak links.

## Durable rule
When verifying low-outbound wiki pages, count only outbound links to direct Notes pages. Links to MOCs such as `[[Personal MOC]]` are navigation/context links, not page-to-page wiki cross-references, and must not satisfy the “2 outbound links” health rule.

## Recommended sequence
1. Run the normal 20-page batch enhancement.
2. Print all batch `## Related` / `Related:` lines bounded by the next heading or horizontal rule.
3. Inspect sparse captures especially carefully.
4. Remove weak heuristic links even if this raises the low-outbound count.
5. Recompute outbound counts from the edited files, counting direct Notes pages only.
6. Regenerate `/vault/System/wiki-index.md`.
7. Rewrite the same-day `/vault/System/wiki-log.md` lint entry so there is exactly one entry and its counts match the final files.

## Reporting guidance
Report unresolved sparse captures explicitly rather than forcing generic cross-links. Good final phrasing: “8 low-outbound pages remain intentionally unresolved because there was not enough source context to add honest links.”
