---
name: vault-wiki-maintenance
description: Maintain and verify Obsidian/theduyvault wiki pages in exact batches, with semantic link repair and index/log consistency.
version: 1.0.0
---

# Vault Wiki Maintenance

Use this skill when maintaining an Obsidian-style wiki vault: linting pages, refreshing frontmatter, repairing links, updating MOCs, regenerating an index, or writing a maintenance log.

## Core workflow

1. Freeze the batch first.
   - Select the required pages once.
   - Use the same frozen list for mutation, semantic repair, verification, index regeneration, and log rewrite.
   - Do not rerun a selector after repairs; lower issue counts can accidentally advance to another batch.

2. Repair structure conservatively.
   - Normalize frontmatter fields (`tags`, `type`, `created`, `updated`, `sources`, `wiki_status`).
   - Remove merge/conflict artifacts in frontmatter.
   - Preserve page content unless the task explicitly authorizes cleanup.

3. Add links semantically, not numerically.
   - Do not force two outbound links by broad tag overlap, same publication issue, same date, or generic words.
   - Treat MOC links as navigation, not `## Related` evidence.
   - Use distinctive title/body terms to find close subject neighbors.
   - If no close neighbor exists, leave the page honestly low-outbound and report it.

4. Review MOCs separately from Related links.
   - MOC membership should be the narrowest correct domain/section.
   - Preserve numbered Economist MOC filenames and keep high-value/active sources under `Sources/`, not `_cold`.
   - Keep binary artifacts in `Attachments/`.

5. Regenerate infrastructure and verify.
   - Regenerate the wiki index after page edits.
   - Append or rewrite exactly one same-day maintenance log entry.
   - Re-read every touched page, not a sample.
   - Verify frontmatter, updated dates, index rows, log count, and semantic Related sections.

## Pitfalls

- Token-overlap autolinks can create absurd neighbors (same issue/date or incidental vocabulary). Always print and inspect actual `## Related` sections before final reporting.
- A numeric verifier can pass while Related semantics are wrong. Human-readable final verification must include each touched page’s Related lines.
- Semantic cleanup may increase low-outbound counts. This is acceptable when removed links were weak.
- If a returned patch diff shows accidental chat/tool-call residue in YAML or body text, stop and repair that exact contamination before any further edits; then exact-search for the leaked fragments and re-read the touched frontmatter.
- When inserting rows into `wiki-index.md`, avoid broad multi-row replacements unless you preserve every neighbor row verbatim. Immediately re-read the local window and exact-search both the new rows and any neighboring rows you touched; a successful patch can still silently delete or mutate an adjacent existing row if the replacement context was incomplete.
- For verification, remember `search_files(target="files")` is glob-based, not regex alternation; verify multiple exact files with separate probes or a narrow read-only `test -f ...` command. Do not rely on `git diff --stat` alone because untracked new files may be invisible.

## References

- `references/semantic-repair-after-token-overlap-2026-07-26.md` — session-specific repair pattern for weak token-overlap autolinks in exact-20 wiki lint batches.
- `references/patch-contamination-and-verification-2026-07-28.md` — recovery pattern for accidental patch-argument residue and stronger file/infrastructure verification.
- `references/economist-batch-semantic-related-repair-2026-07-30.md` — Economist exact-20 repair pattern: freeze the batch, treat source links as provenance, remove MOC/broad Related links, search by distinctive entities, and leave sparse pages honestly low-outbound when no close sibling exists.
- `references/exact-20-semantic-curation-2026-07-31.md` — repair pattern for exact-20 lint runs where token-overlap scripts pass numeric outbound checks but create weak links; print Related sections, search distinctive terms, clean tag pollution, and accept honest low-outbound pages.
