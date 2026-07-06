# Semantic cleanup + honest low-outbound verification (2026-06-26)

Context: a headless `wiki-lint` run enhanced exactly 20 direct `/vault/Notes/*.md` pages, regenerated `System/wiki-index.md`, and wrote a same-day `System/wiki-log.md` entry. Several referenced helper files were absent, so the run used a self-contained stdlib Python scanner/editor.

## Durable lessons

1. **Do not trust heuristic related-link insertion without inspection.**
   - Tag/title overlap produced weak links such as parenting notes linking to astrology/persuasion pages, and a Canadian politics clipping linking to marketing/game-app pages.
   - After automated insertion, print each touched page's bounded `## Related` section and inspect it semantically before final reporting.

2. **Prefer honest low-outbound counts over forced links.**
   - For low-context captures, empty/minimal notes, or broad clipped articles with no clear wiki neighbor, remove weak links and report the resulting low-outbound page as remaining work.
   - Accept that semantic cleanup can increase the verified low-outbound count; that is a quality improvement, not a failure.

3. **After semantic cleanup, rerun infrastructure updates from edited files.**
   - Recompute post-run issue counts after cleanup, regenerate `System/wiki-index.md`, and rewrite the same-day `wiki-log.md` entry so the log reflects final verified state rather than pre-cleanup success counts.

4. **Patch only clearly relevant replacements.**
   - Example of acceptable replacement: a Qatar Qsuite/travel-points note can link to `[[Credit Card Churning Strategy for Travel]]` and `[[AI Travel Flight Optimization Engine]]`.
   - Example of unacceptable replacement: generic high-inbound or same-tag pages when the page body does not establish the relationship.

## Verification pattern used

- Re-read all 20 touched pages.
- Confirm required frontmatter fields exist: `tags`, `type`, `updated`, `wiki_status`.
- Confirm `updated` equals the run date on all 20.
- Confirm no frontmatter conflict markers remain.
- Confirm all 20 titles appear in `System/wiki-index.md`.
- Confirm exactly one same-day lint entry exists in `System/wiki-log.md`.
- Report skipped unreadable direct notes separately instead of aborting the batch.
