# Frontmatter source-link and empty Related cleanup — 2026-07-16

## Context
A cron `wiki-lint` run repaired exactly 20 direct `/vault/Notes/*.md` pages and reduced canonical `System/scripts/wiki-health.py` broken outbound targets from 54 to 37. The first automated pass fixed body links but left some broken wikilinks inside YAML frontmatter (`sources:` list entries such as `[[missing source page]]`) and left empty `## Related` headings after semantic cleanup.

## Durable lesson
Canonical broken-link scans count wikilinks anywhere in `Notes/` and `MOCs/`, including YAML frontmatter. Post-edit semantic repair must inspect both:

1. Body text and `## Related` sections.
2. Frontmatter fields such as `sources:` / `source:` that may contain `[[...]]` links to absent source pages.

If the linked source page does not exist and there is no correct target to repoint to, do **not** create a dummy source page. Convert the unresolved wikilink to a plain text provenance label or URL, preserving the information but removing the broken graph edge.

## Cleanup pattern
After automated related-link or broken-link repair:

1. Re-run canonical `python3 System/scripts/wiki-health.py --list`.
2. For each touched page, re-read the full file, not only the body.
3. Remove unresolved wikilink brackets in frontmatter when no real page exists:
   - `- "[[0xNyk awesome-hermes-agent GitHub]]"` -> `- "0xNyk awesome-hermes-agent GitHub"`
   - keep real source links when a matching `/vault/Sources` or `/vault/Notes` page exists.
4. Remove empty `## Related` or `## Related Pages` sections created by link cleanup.
5. Regenerate `System/wiki-index.md`.
6. Rewrite exactly one same-day lint log entry with canonical pre/post counts.
7. Verify all 20 touched pages still have valid frontmatter, `updated` set to the run date, no conflict markers, and index rows.

## Guardrails
- Do not force replacements for sparse pages solely to satisfy a numeric outbound-link target.
- Do not add broad MOC links or generic high-inbound pages as replacements.
- Count a higher honest low-outbound number as acceptable if the removed links were weak or broken.
- Preserve active/high-value Sources directly under `/vault/Sources`; this cleanup is about links, not archive relocation.
