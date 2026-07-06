# Semantic cleanup + honest low-outbound reporting (2026-06-25)

## Context
A scheduled `wiki-lint` run processed exactly 20 direct `/vault/Notes/*.md` pages. The automated pass initially satisfied the numeric outbound-link rule by adding several weak `Related:` links to sparse captures and broad articles.

Examples of links that were removed during semantic review:
- `Legal Reserve Note` → `Zi Wei Dou Shu Chinese Astrology Resources`
- `Grace Leung YouTube Channel` → `Learn Claude Code Agent Harness Repo`
- `MYLE GoalAccess Capture` → `17 Agentic AI Design Patterns`
- `Qatar Qsuite Business Class Booking Strategy` → AI agent pages
- Canadian politics clipping → generic coding/research-tool pages

## Durable lesson
After automated related-link insertion, semantic cleanup can legitimately increase the post-run low-outbound count. This is correct. Do not keep misleading cross-links just to preserve a zero low-outbound report.

## Recommended repair pattern
1. Print and inspect each selected page's bounded `## Related` section and standalone `Related:` lines.
2. Remove links that are only justified by generic tags such as `ai`, `research`, `knowledge-management`, `clippings`, or broad MOC membership.
3. Keep links only when they are supported by the page body, title/domain overlap, or a clearly close neighbor.
4. Re-run verification from the edited files, not from the pre-cleanup report.
5. Regenerate `/vault/System/wiki-index.md` after cleanup.
6. Rewrite the same-day lint entry in `/vault/System/wiki-log.md` so there is exactly one entry for the run and its post-run low-outbound count matches the verified filesystem state.

## Reporting language
Prefer explicit wording such as:

> `12 selected pages left semantically unresolved rather than forcing unrelated links`

This makes the non-zero low-outbound count a quality-control result rather than a failure.

## Pages often needing this treatment
Sparse captures, imported article clippings, travel-points posts, parenting notes, and empty/minimal app/tool captures often lack enough local context for two honest outbound wiki links. Add stub context or source-follow-up notes if useful, but do not invent content or force broad-topic links.
