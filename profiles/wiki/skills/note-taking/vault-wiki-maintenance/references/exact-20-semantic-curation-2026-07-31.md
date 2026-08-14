# Exact-20 Semantic Curation After Heuristic Autolinking (2026-07-31)

Use this for `wiki-lint` / vault maintenance runs where a heuristic or script numerically fixes low-outbound pages but the resulting `## Related` links need semantic review.

## Session lesson

A first-pass lint script selected 20 low-outbound pages and filled `## Related` by token overlap. The numeric verifier passed, but inspection showed weak links caused by:

- country/region-only overlap (`Myanmar`, `Africa`, `Europe`)
- broad/generic tags (`ai`, `economist`, `finance`, `business`, `culture`, `research`)
- same-publication or same-date digest proximity rather than subject proximity
- body-fragment collisions from imperfect imported article excerpts
- source/provenance pages used as unrelated fillers

A repair pass removed weak links and accepted a higher honest low-outbound count.

## Workflow to reuse

1. **Freeze the exact 20 titles** after the first mutation. Do not rerun selection after semantic cleanup.
2. **Print each touched page's actual links and full `## Related` section**; do not trust outbound counts alone.
3. **Search by distinctive subject terms**, not broad tags:
   - names: `Kevin Warsh`, `Aung San Suu Kyi`, `QXO`, `George Sand`
   - domain phrases: `Strait of Hormuz`, `Ebola`, `Pix`, `Gibraltar`, `Base64`
   - specific policy/market terms: `antitrust`, `rollup`, `medical schools`, `restitution`
4. **Replace only with close subject neighbors** that exist under `/vault/Notes`.
5. **Remove weak links instead of replacing them blindly.** If no close neighbor exists, leave the page low-outbound and say so in the log/report.
6. **Clean tag pollution from automated inference.** Remove generic accidental tags unless the page specifically supports them.
7. **Regenerate and verify**: `System/wiki-index.md`, exactly one same-day `System/wiki-log.md` entry, all frozen batch rows present, all 20 pages re-read.

## Good semantic replacements

- `World Business Digest July 18 2026` → `[[Kevin Warsh Fed Force Five]]`, `[[Economic Indicators]]`
- `World Politics Digest July 18 2026` → `[[Hormuz Shipping Security Crisis]]`, `[[Iraq Zaidi Iran America Balancing Act]]`
- `Congo Ebola Outbreak Vaccine Race` → `[[Uganda Ebola Response Capacity Gap]]`, `[[Africa Health Sovereignty After USAID Cuts]]`
- `Global Payments Infrastructure Power` → `[[Stablecoins Narrow Bank Economics]]`, `[[Economic Indicators July 18 2026]]`

## Honest low-outbound cases

Do not force links for:

- tiny personal/legal captures (`Legal Reserve Note`)
- standalone country-specific article stubs with no sibling page
- one-off recipe/wellness/social-media captures with only one close adjacent note
- source fallback pages whose meaningful provenance is already in `## Pages Updated`

## Reporting language

If semantic cleanup raises the low-outbound count, report it as intentional: “left sparse/low-context pages honestly low-outbound rather than forcing unrelated links.”