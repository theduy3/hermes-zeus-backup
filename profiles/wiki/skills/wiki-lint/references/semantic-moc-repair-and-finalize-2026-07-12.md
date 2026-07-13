# Semantic MOC repair + final verification after exact-20 lint (2026-07-12)

## Context
An exact-20 wiki-lint cron pass successfully updated 20 direct `/vault/Notes/*.md` pages, regenerated `wiki-index.md`, and rewrote the same-day `wiki-log.md`. The first automated pass still produced two classes of semantic issues that numeric verification did not catch:

- Low-context pages were appended to broad MOCs because of generic tags (`ai`, `finance`, `youtube`, `personal-development`, etc.).
- A few `## Related` entries were technically valid wikilinks but weak subject matches, e.g. local-LLM tooling linked to unrelated local apps or a Canada politics clipping linked to a broad US foreign-policy page.

## Durable workflow
After the first exact-20 automation pass, run a small semantic repair/finalize pass before reporting:

1. Re-read every touched page's `## Related` section and remove weak links whose only evidence is broad tag overlap or generic "related wiki context" filler.
2. Do not replace removed links unless there is a close subject neighbor. Leave low-context pages honestly low-outbound.
3. Inspect MOC destinations for every newly added MOC link. Broad tag-to-MOC mapping is not sufficient:
   - personal/contact/language stubs belong in `Personal MOC`, not AI/Finance MOCs just because they contain generic tags;
   - politics clippings should be placed in a narrow politics/international section with an explanatory bullet, not in `Related MOCs` or unrelated regional/finance sections;
   - tool/source captures should be placed only where the page body shows the domain, not because of `source`, `github`, `ai`, or `youtube` tags.
4. Remove MOC-substitute prose from page bodies such as "linked to [[Personal MOC]] for now"; MOC membership should live in MOCs, not as a forced outbound wiki link inside the page.
5. Regenerate `/vault/System/wiki-index.md` after semantic cleanup.
6. Rewrite the same-day `wiki-log.md` entry (remove earlier same-day lint entries first) so there is exactly one lint entry and its post-run counts reflect the repaired state.
7. Rerun exact-20 verification after the log rewrite:
   - all 20 touched pages have `updated: <run-date>`;
   - required frontmatter is present and valid;
   - no conflict markers in frontmatter;
   - every touched page has an index row;
   - index header `page_count` equals direct `Notes/*.md` count;
   - no `[[... MOC]]` links in touched pages' `## Related` sections;
   - exactly one same-day wiki-log entry exists.

## Reporting
Report remaining low-outbound pages as intentional/honest unresolved pages when they are sparse captures or source fallback notes. Do not treat them as failed lint if weak links were deliberately removed.
