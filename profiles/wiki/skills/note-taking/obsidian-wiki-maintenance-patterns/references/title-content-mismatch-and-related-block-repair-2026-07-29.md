# Title/content mismatch + Related-block repair after exact-20 lint (2026-07-29)

Context: an exact-20 wiki-lint cron run selected several Economist-derived pages. The automated pass updated frontmatter and added Related links, but semantic inspection showed some pages' title/topic did not match the article excerpt body. Examples included:

- `South Korean Buddhism Revival` containing an Indian mango/food-safety article excerpt.
- `Canada Critical Minerals Development` containing a Mexico passenger-rail article excerpt.
- `Demis Hassabis AI Safety Regulation Plan` containing Eli Lilly/GLP-1 content.
- `Europe Carbon Price Competitiveness Risk` containing Ukraine defence-ministry/manpower content.
- `Emo Culture Revival` containing Christopher Nolan/film content.
- `Congo Ebola Outbreak Vaccine Race` containing Iraq/Shia militia content.

## Durable workflow

1. **After auto-linking, inspect each touched page's body snippet, not only its Related section.** Search for distinctive body phrases across the notes corpus to find whether the content belongs to another existing note. If a note title/body mismatch is detected during lint, do not rewrite the whole article from memory; avoid compounding the error with weak links and report/leave it for a future ingest/content repair pass.
2. **Prefer body-matched neighbors over title/tag neighbors when content appears displaced.** If the body clearly matches an existing page, a Related link to that body-matched page is better than a broad tag match. If no close body-matched neighbor exists, leave the page honestly low-outbound.
3. **Do not use lifestyle/personal adjacency as a second link.** For health/personal sparse notes, remove broad MOC or lifestyle-neighbor links unless the body has a real subject relationship. Example: a lymphatic-drainage routine can link to a close exercise/health page if available, but not to unrelated food/lifestyle notes just to reach two links.
4. **Strip all existing `## Related` blocks before rewriting them.** Simple regexes can leave duplicate Related sections when blank lines or prose/bullets follow the heading. Use a line-based remover: when a line equals `## Related`, skip until the next `## ` heading, then append one clean Related block if semantically warranted.
5. **Re-run exact frozen-batch verification after Related cleanup.** Confirm: all selected pages have today's `updated`, required frontmatter, index rows, MOC membership, exactly one same-day log entry, no conflict markers, no MOC links in Related, and an honest low-outbound list.

## Reporting

A higher low-outbound count after removing weak links is acceptable. Report it explicitly as semantic cleanup rather than failure, and keep canonical health counts separate from selected-batch low-outbound counts.
