# Semantic repair after auto-linking (2026-06-21)

## Context
A cron wiki-lint run processed exactly 20 pages and used an automated related-link filler. Verification passed structurally, but a manual semantic spot-check showed four weak forced links on sparse captures:

- `Legal Reserve Note` got `[[MYLE GoalAccess Capture]]` and `[[2026-W21]]`
- `Korean Greeting Phrases` got `[[Dan Koe Personal Development Framework]]`
- `MYLE GoalAccess Capture` got `[[2026-W21]]` and `[[Awesome Generative AI Guide]]`
- `Grace Leung YouTube Channel` got broad AI/video links without evidence from the page body

These links satisfied the numeric two-outbound rule but violated the semantic-link guard.

## Durable workflow
After any automated cross-link insertion, run a focused semantic spot-check over the exact batch before final reporting:

1. Print each selected page's `## Related` / `Related:` lines.
2. Inspect sparse or low-context pages first; they are most likely to receive weak generic links.
3. Remove links that are not supported by at least one of:
   - explicit title mention in the body;
   - strong shared domain tokens in the title/body;
   - at least two meaningful shared tags plus compatible topic context.
4. Regenerate `System/wiki-index.md` after cleanup.
5. Rewrite the same-day `wiki-log.md` entry rather than appending another entry.
6. Re-run final verification and allow a non-zero low-outbound count when the unresolved pages are honestly sparse.

## Reporting pattern
If semantic cleanup leaves low-outbound pages, report that explicitly:

> Four sparse captures were left with honest low-outbound status after removing weak forced links.

Do not claim `Remaining: 0` in a way that hides the post-run low-outbound count. Separate structural backlog from semantic low-outbound debt.
