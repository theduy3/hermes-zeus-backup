# Semantic cleanup after automated related-linking

Session learning from 2026-06-30 wiki-lint cron run.

## Problem
A stdlib automation pass correctly updated 20 pages and initially satisfied the numeric outbound-link target, but its heuristic still produced weak `## Related` links on sparse/imported captures. Examples included language, legal, YouTube-channel, and Canadian-politics notes being linked to unrelated AI-course or astrology pages because of generic tags/tokens or because a MOC-like page appeared in the note-link corpus.

## Durable rule
After any automated link fill, run a semantic cleanup pass before final reporting:

1. Inspect every added `## Related` section for the 20 touched pages, not only the pages whose verification failed.
2. Treat MOC/navigation links as useful for discovery but not as a substitute for real Note-to-Note semantic links.
3. Remove links that are justified only by broad tags, generic tokens, or high-inbound popularity.
4. If cleanup leaves pages below two outbound Note links, keep that honest low-outbound count and rewrite the same-day wiki-log entry to match it.
5. Re-run final verification after cleanup: all 20 frontmatter blocks valid, `updated` equals run date, index header/page count correct, all 20 titles indexed, and exactly one same-day lint log entry.

## Implementation pattern
A small `/tmp` cleanup script is sufficient:

- maintain a per-title denylist of weak links found by spot-checking;
- remove those list items and drop empty `## Related` sections;
- regenerate `System/wiki-index.md` after removals;
- rewrite the existing same-day `wiki-log.md` lint entry rather than appending a second entry;
- print JSON with changed pages, whole-vault counts, and same-day lint-entry count.

Prefer semantic integrity over passing the numeric two-link rule. A non-zero low-outbound count is acceptable when links would otherwise be misleading.