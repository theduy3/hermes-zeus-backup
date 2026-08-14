# Exact-20 batch freeze + tag-pollution repair (2026-07-20)

A cron lint run exposed two durable pitfalls for automated exact-20 workflows.

## Freeze the selected batch after first mutation

If a helper script both selects a batch and mutates pages, do **not** rerun that same helper after a repair pass. Once the first mutation lowers issue counts, a fresh selection pass may choose the next rolling-refresh pages, causing the run to touch more than the intended 20 pages and rewrite the same-day log with the wrong batch.

Safer pattern:
1. Run the selector/mutator once and persist the `selected_titles` list to `/tmp/wiki-lint-selected-YYYY-MM-DD.json` or embed it in subsequent repair/verifier helpers.
2. For tag cleanup, semantic repair, index regeneration, and log rewriting, operate only on the frozen selected list.
3. Verification scripts may scan the whole vault for counts, but must report and log the original frozen batch.
4. Never use a post-repair issue score to choose another 20 pages in the same cron run.

## Clean polluted frontmatter tags

Some pages have URL strings, `[[wikilinks]]`, or `none` values in `tags:` from earlier ingestion/frontmatter normalization. When touching such pages:
- remove tag values that start with `http`, contain `[[...]]`, contain `/` or `:`, are very long, or equal `none`;
- preserve useful provenance by moving URLs/wikilinks into `sources:` with quoted list entries;
- de-duplicate both `tags:` and `sources:` before regenerating the index;
- verify the regenerated index does not leak YAML list dashes or polluted tag values into the tags column.

## Final verification checklist addition

For the frozen 20 pages, verify:
- `updated` equals the run date;
- frontmatter fields are valid and tag values are clean semantic tags only;
- no conflict artifacts remain in frontmatter;
- all selected titles appear in `wiki-index.md` and a MOC;
- exactly one same-day lint log entry names the frozen batch;
- any low-outbound pages are intentionally low-context, not victims of a broken repair pass.
