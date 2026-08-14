# Economist batch semantic Related repair (2026-07-30)

Context: an exact-20 theduyvault wiki-lint run selected a rolling batch of Economist article notes. The first automated pass normalized frontmatter but produced or preserved weak Related entries.

Durable lessons:

- Freeze the selected 20 titles after the first mutation; all semantic repair, index regeneration, log rewrite, and verification should use that same frozen list.
- For Economist article notes, `sources:` frontmatter and `## Source` section entries may contain issue/extract provenance links. Treat those as provenance, not as evidence that the page has good semantic outbound links.
- Do not put MOC links in `## Related`. If an automated pass leaves `[[... MOC]]` or plaintext `... MOC` bullets under Related, remove them rather than replacing them with broad topic links.
- Generic token overlap can create bad links even when the link count passes. Examples:
  - `Modi Diplomatic Travel Strategy` was incorrectly linked to `Credit Card Churning Strategy for Travel`; the close neighbor was `Aung San Suu Kyi Death Rumour Myanmar Secrecy` because the clipped body was actually about Myanmar/ASEAN.
  - `South African Television Politics` was incorrectly linked to `African Heritage Restitution Politics`; no close second neighbor existed, so it was left honestly low-outbound.
  - `Federal Reserve After QE Balance Sheet` was better linked to `Federal Reserve Kevin Warsh Chair Risks` and `AI and Neutral Interest Rate`, not an off-balance-sheet AI debt page.
- Search by distinctive title/body entities before adding replacements: `Kevin Warsh`, `QE`, `LNG`, `heatwave`, `Starmer`, `sovereign AI`, `Red Bull`, etc. Avoid broad tags like `economist`, `finance`, `politics`, `culture`, `travel`, `africa`, or `ai` as sufficient evidence.
- If no close same-domain sibling exists, leave the page low-outbound and report the honest count. This is preferable to forcing country-only, section-only, publication-only, or generic-tag links.

Verification pattern:

1. Re-read every touched page and inspect actual `## Related` bullets.
2. Remove MOC-substitute and weak broad links.
3. Add only close semantic siblings discovered through distinctive term searches.
4. Regenerate `System/wiki-index.md` with the same direct Notes count.
5. Rewrite exactly one same-day `wiki-log.md` lint entry for the frozen batch.
6. Verify all 20 pages for required frontmatter, run-date `updated`, no conflict artifacts, no MOC entries in Related, index row present, and exactly one same-day lint log entry.
