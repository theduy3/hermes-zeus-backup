# Semantic repair notes — 2026-07-13 cron lint

This run reinforced the post-autolink semantic repair requirements for exact-20 wiki-lint batches.

## What happened
- The automated pass selected exactly 20 direct `/vault/Notes/*.md` pages and updated frontmatter/MOC/index/log successfully.
- Several heuristic `## Related` additions were numerically valid but semantically weak because they came from broad/shared tags or token collisions rather than close subject proximity.
- Examples removed during repair:
  - Political clipping linked to marketer/NVIDIA notes because of broad `ai`/`marketing`/`research` tags.
  - Canada critical-minerals note linked to a Canada retirement note only because of country overlap.
  - Japanese curry linked to Asian renewable power only because of `asia`/Economist overlap.
  - Better-questions management note linked to a salon SOP note only because of `management` overlap.
  - The Economist MOC was removed from a note's `## Related`; MOCs belong in navigation/provenance, not as subject-neighbor Related links.
- Honest low-outbound counts increased after cleanup. This is correct: sparse/low-context captures should remain low-outbound rather than receive misleading links.

## Durable pattern
1. After any automated related-link fill, print/re-read every touched page's actual `## Related` entries.
2. Remove:
   - any `[[... MOC]]` link from `## Related`;
   - country-only, section-only, publication-only, or generic tag-only links;
   - links based only on broad tags such as `ai`, `research`, `marketing`, `management`, `business`, `finance`, `economist`, `source`, `knowledge-management`, or region tags.
3. Add replacements only when there is close subject evidence:
   - same named entity/event/person/tool;
   - same article series/digest/issue page;
   - explicit mention in the body;
   - narrow domain sibling (e.g. social housing ↔ social housing subsidy, facial-recognition policing ↔ robotaxi surveillance).
4. If no close neighbor exists, leave the page honestly low-outbound and reflect that in the log.
5. Regenerate `System/wiki-index.md`, rewrite exactly one same-day `wiki-log.md` entry, and rerun exact-20 verification after the repair pass.

## Verification nuance
When counting broken outbound links, normalize wikilink targets before matching: strip aliases/headings, `.md`, and folder prefixes. Naive regex output from ripgrep/readback can miscount path-qualified or line-wrapped links as broken.