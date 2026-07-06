# Infrastructure log preservation and recovery

Use this when updating `/vault/System/wiki-log.md`, `wiki-index.md`, or MOCs during ingest.

## Lesson

Do not rewrite an infrastructure file from a partial/paginated read. A `read_file(..., offset=...)` or truncated read is only a window, not the full file. Re-emitting that window through `write_file` can silently truncate historical log/index content.

## Safer update pattern

1. Prefer targeted `patch` appends/replacements with an exact old string from the current file.
2. For append-only files, read the tail, then patch the final known line/block by replacing it with itself plus the new entry.
3. After patching, verify with exact `search_files`/`rg` matches for the new artifact.
4. Check basic preservation signals such as line count or a known recent historical entry when practical.

## Recovery pattern if truncation happens

If `/vault` is a git repo and the overwrite is detected immediately:

```bash
git -c safe.directory=/vault -C /vault show HEAD:System/wiki-log.md > /tmp/wiki-log.restore
cp /tmp/wiki-log.restore /vault/System/wiki-log.md
```

Then re-apply the missing recent entries and the new ingest entry using a targeted patch, not a full rewrite. Verify with `git -c safe.directory=/vault -C /vault diff -- System/wiki-log.md` and exact searches for the new entry.

## Notes

- The `safe.directory` flag avoids git's dubious-ownership refusal on `/vault` without changing global config.
- This is a recovery technique, not the normal path. Normal path remains small targeted patches plus exact verification.
