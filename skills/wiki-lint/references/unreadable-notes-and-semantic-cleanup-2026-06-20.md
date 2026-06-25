# Unreadable direct Notes + semantic cleanup repair (2026-06-20)

## What happened
A cron-safe stdlib wiki-lint scanner over direct `/vault/Notes/*.md` aborted when one direct note was unreadable:

```text
PermissionError: [Errno 13] Permission denied: '/vault/Notes/Claude Code Setup Inventory.md'
```

The run later succeeded after the scanner treated unreadable direct notes as skipped instead of fatal.

## Durable pattern
- Wrap direct note reads in `try/except PermissionError` during scan/load.
- Skip unreadable pages unless they are explicitly in the selected batch; do not let one unreadable root-owned note abort the whole cron run.
- Report counts as readable/scanned pages when any unreadable files are skipped.
- Continue to use root-owned-safe replacement for files that are actually edited.

## Semantic cleanup lesson
The first pass also satisfied low-outbound counts by adding weak related links to sparse captures. After reading the affected pages, those links were removed and the same-day log entry was rewritten rather than appending a second entry.

Use this policy:
- Sparse/low-context captures may remain low-outbound if no semantically defensible related page exists.
- Remove generic forced links, then rerun verification across all 20 pages.
- Rewrite the same-day `wiki-log.md` entry to match post-cleanup low-outbound counts.
- Final success can include non-zero low-outbound pages when the unresolved pages need human/source context rather than unrelated cross-links.

## Minimal code pattern
```python
def try_read_text(path):
    try:
        return path.read_text(encoding='utf-8', errors='replace')
    except PermissionError:
        return None

pages = []
for p in Path('/vault/Notes').glob('*.md'):
    text = try_read_text(p)
    if text is None:
        skipped_unreadable.append(str(p))
        continue
    pages.append(parse_page(p, text))
```
