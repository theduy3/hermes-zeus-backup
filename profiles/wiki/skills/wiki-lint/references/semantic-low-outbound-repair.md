# Semantic low-outbound repair for wiki-lint

Use this when the automation satisfies the numeric “2 outbound links” rule by adding weak `## Related` links to sparse or ambiguous notes.

## Trigger
- Newly added Related links are based only on generic tags (`ai`, `reference`, `personal`, `fleeting`, `legal`) or high-inbound fallbacks.
- The note summary says no clear domain neighbor exists, but the page still has forced Related links.
- Final verification passes structurally but semantic spot-check shows irrelevant links.

## Repair pattern
1. Re-read every sparse/low-context page in the 20-page batch, not only the pages with script errors.
2. Remove weak forced `## Related` bullets rather than preserving a misleading numeric pass.
3. Keep honest MOC/context links that are already in prose (for example, `[[Personal MOC]]`) if they accurately describe where the capture belongs.
4. Recompute post-run counts after removal. The correct result may be a non-zero `low_outbound` count.
5. Rewrite the same-day `wiki-log.md` entry (do not append a second entry) to say the low-outbound pages are semantically unresolved rather than failed.
6. Rerun final verification across all 20 pages, index, and log.

## Reporting
- Treat unresolved low-outbound sparse captures as pending human/context work, not a failed run, if frontmatter, index, and log checks pass.
- Name the unresolved pages in the final report and suggest what context is needed.

## Pitfall
Do not let an `all_titles_present`/frontmatter verification hide semantic damage. A page can pass all structural checks while still containing harmful unrelated cross-links.