# MOC date-section ordering

Use when editing or linting `/vault/MOCs/*.md`, especially sections like `## Articles by Issue` that contain date headings.

## User expectation

Date-grouped MOC sections should be newest-first. If headings include issue dates such as:

```markdown
### July 4th 2026
### June 6th 2026
### June 27th 2026
```

reorder them to:

```markdown
### July 4th 2026
### June 27th 2026
### June 6th 2026
```

This applies across all MOCs, not just Finance & Economics.

## Safe workflow

1. Scan every readable `/vault/MOCs/*.md` for consecutive date headings at the same heading level.
2. Parse both `Month Dth YYYY` style and `YYYY-MM-DD` style headings.
3. Sort only contiguous runs of date sections at the same heading level; preserve all non-date sections and all content inside each date block verbatim.
4. Root-owned MOCs may be unreadable (`600`) or readable but not directly writable. If the MOC directory is writable, replace a root-owned readable file by writing a same-directory temporary file and `os.replace(tmp, path)`; do not use `/tmp` for `os.replace` across filesystems.
5. If a MOC is unreadable, skip it and report the exact `chown` command instead of aborting the whole run.
6. Verify by rereading all readable MOCs and asserting every date run is descending.
7. Append a concise `wiki-log.md` lint/maintenance entry.

## Pitfalls

- Do not sort all headings globally; only date-heading runs. Many MOCs have semantic sections that must remain in authored order.
- Do not rewrite MOCs from partial reads.
- `os.replace('/tmp/file', '/vault/...')` can fail with `Invalid cross-device link`; use a temporary file in the destination directory.
