# Batch selection and orphan filtering notes

This skill operates best when the run is bounded and false positives are filtered before reporting.

## Batch selection
- Use the wiki index as the source of truth for batch ordering.
- Advance by `updated` date so each run refreshes the next oldest slice.
- Keep the run capped at 20 pages; log remaining backlog instead of expanding scope.

## Orphan filtering
- Treat raw link-graph orphan hits cautiously.
- Exclude system/date pages and other intentional infrastructure pages before counting orphans.
- Validate apparent orphans against `/vault/System/wiki-index.md` and MOC membership before reporting them.
- If a page is still missing from the graph after filtering, then it is a real orphan candidate.

## Verification
- Spot-check representative pages from the batch after editing.
- Confirm the index row shows the expected `updated` date and that the page is still linked from the relevant MOC or related pages.
