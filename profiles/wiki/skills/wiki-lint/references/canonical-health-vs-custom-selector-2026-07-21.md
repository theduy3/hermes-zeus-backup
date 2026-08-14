# Canonical health vs custom selector — 2026-07-21

## Trigger
Use during exact-20 scheduled `wiki-lint` runs when a custom Python selector/editor is used instead of relying entirely on `System/scripts/wiki-health.py`.

## Lesson
A custom batch selector can produce misleading pre-run issue counts if it does not match the canonical scanner semantics. In the 2026-07-21 run, a custom helper initially counted many pages as `orphan` because its inbound-link calculation only considered direct Notes links and did not include MOC membership/index cross-check semantics the canonical health script uses. Canonical `System/scripts/wiki-health.py` correctly reported `0` orphans.

## Required pattern
1. Run `python3 /vault/System/scripts/wiki-health.py` before mutation and treat its headline counts as canonical for final reporting.
2. If using a custom selector, label its counts narrowly (for example, `selected-batch low-outbound candidates`) and do **not** report them as vault-wide orphan/sparse/MOC counts unless the scanner intentionally reproduces canonical semantics.
3. After the first mutation, freeze the exact 20 selected titles and reuse that list for semantic repair, index regeneration, verification, and log rewrite.
4. Run a semantic repair pass even if numeric link counts look good:
   - remove self-links from `sources:` or `## Related`;
   - remove token-collision links (for example legal/reserve text linked to an unrelated Federal Reserve policy page);
   - remove source-stub-to-source-stub links when the only evidence is broad `source`, `ai`, or `developer-tools` overlap;
   - leave sparse captures honestly low-outbound when no close sibling exists.
5. Regenerate `System/wiki-index.md`, then rewrite exactly one same-day `wiki-log.md` lint entry using canonical health plus frozen-batch verification.
6. Verify all 20 selected pages: frontmatter present, `updated` equals run date, no conflict markers, no broken outbound references in the frozen batch, no MOC gaps, all titles present in `wiki-index.md`, and exactly one same-day lint log entry.

## Reporting wording
Prefer wording like:

> canonical health scan found 0 orphans, 0 sparse frontmatter, 0 MOC gaps; selected-batch semantic scan left N low-outbound pages honest after semantic guard.

Avoid wording that implies custom-selector orphan counts are canonical vault health.
