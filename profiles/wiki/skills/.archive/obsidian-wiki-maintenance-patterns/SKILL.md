---
name: obsidian-wiki-maintenance-patterns
description: Use when maintaining Obsidian wiki pages safely.
version: 1.0.0
---

# Obsidian Wiki Maintenance Patterns

Use this for recurring maintenance of an Obsidian/theduyvault-style wiki: linting direct note pages, repairing frontmatter, preserving MOC/index/log consistency, and doing semantic cross-link cleanup after automated edits.

## Core principles

1. **Freeze the batch.** Once a maintenance/lint batch is selected, use the same titles for all repairs, verification, index regeneration, and log rewrite. Do not rerun a mutating selector after cleanup.
2. **Prefer semantic truth over numeric link targets.** Remove MOC links, broad tag-overlap links, provenance-only/source links, and token-collision links from `## Related`. Leave sparse or mismatched pages honestly low-outbound when no close neighbor exists.
3. **Inspect the body, not just metadata.** Tags and titles can be stale or polluted. Read a body snippet and search distinctive phrases before adding Related links or deciding MOC placement.
4. **Keep infrastructure coherent.** After page edits, regenerate the index, append or rewrite exactly one maintenance log entry for the run, then verify page count/index/log parity.
5. **Separate canonical health from selected-batch checks.** Use the vault's canonical health scanner for global issue counts when available; use a frozen-batch verifier for the pages actually touched.

## Standard workflow

1. Load vault conventions and the relevant task-specific skill/command if available.
2. Scan direct top-level Notes pages, readable MOCs, and the index/log.
3. Select the required batch size from issue-bearing pages, filling from the oldest updated queue if necessary.
4. Normalize selected pages:
   - required frontmatter fields;
   - `updated` date;
   - conflict-marker artifacts;
   - broken path-qualified wikilinks where a real basename exists.
5. Add only close, defensible Related links.
6. Run a separate semantic repair pass:
   - print/read each touched page's Related block and body snippet;
   - remove weak links;
   - inspect newly added MOC placements;
   - allow honest low-outbound results.
7. Regenerate index/log.
8. Verify every touched page and report concise counts plus unresolved backlog.

## Implementation notes

- For root-owned vault files, replace via the vault's documented root-owned-safe strategy rather than repeatedly retrying failed in-place writes.
- For file-presence verification, remember `search_files(target="files")` uses glob semantics, not regex alternation. Verify several exact filenames with separate probes or a simple wildcard that actually matches; a pattern like `A.md|B.md` can return zero even when both files exist.
- For CRLF newsletter/source archives, exact content regexes such as `^---$` may miss valid frontmatter delimiters because the line ends include `\r`. Re-read the first lines or search for the distinctive fields (`ingested:`, `Pages Updated`, source title) before concluding the archive/frontmatter patch failed.
- For `## Related` cleanup, prefer line-based section rewriting over fragile regexes that can leave duplicate headings.
- When article/title mismatches appear, do not invent a new article summary from memory. Link to body-matched neighbors if present and report the mismatch for future content repair.

## References

- `references/title-content-mismatch-and-related-block-repair-2026-07-29.md` — exact-20 lint run lessons: title/body mismatches, body-phrase search, honest low-outbound pages, and robust Related section cleanup.
- `references/newsletter-ingest-verification-pitfalls-2026-07-30.md` — newsletter/source verification pitfalls: glob-vs-regex file probes, CRLF delimiter searches, and watchlist-candidate thesis filtering.
