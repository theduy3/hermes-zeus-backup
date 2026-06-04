# Robust headless evening processing notes

Use this when running the `tonight` cron job against `/vault`.

## Defensive processing pattern

1. Run `python3 /vault/System/scripts/calculate_dates.py` first and parse `Date:` plus the day name from `Today:`. This date is authoritative for the digest filename and frontmatter.
2. Run `python3 /vault/System/scripts/find_today_notes.py --json --inbox` and treat its output as a mutable work queue.
3. For every queued item, verify the source path still exists before writing/moving. If the queued file is gone or empty, search for a distinctive title/source URL in `/vault/Notes` and summarize the existing page instead of creating another duplicate.
4. For low-content captures (image-only notes, empty GitHub clippings, thin URL shells), either:
   - match/remove them as duplicates of an existing Notes page, or
   - create a clearly labeled stub preserving the source URL/attachment path and stating that manual summary/transcript/image interpretation is still needed.
5. After writing a promoted Notes page, verify the target exists and is non-empty, then remove the root/Inbox original. Do not leave root originals copied into `Notes/`.
6. If a prior digest already exists but `find_today_notes.py` still returns items, process the queue anyway. A previous digest may have been written before residual Inbox originals were removed. Match residual captures to existing Notes pages by title/source URL/content, summarize those existing pages, archive/remove the residual originals, and overwrite the digest with the current verified counts.
7. Update MOCs/wiki-index/wiki-log only when the files are readable/writable. If they are unavailable, continue and report that limitation; digest creation is the non-negotiable output.
8. Rerun `find_today_notes.py --json --inbox` after filing and include the remaining count in the digest verification section.
9. Write `/vault/Daily/<YYYY-MM-DD>-tonight.md` even when zero notes were processed. Include `notes_processed`, the initial queue count, the post-processing queue count, and whether mini wiki-lint was skipped.
10. Verify the digest by reading it back. If direct overwrite fails but `/vault/Daily` is writable, write a same-directory temp file and atomically replace the final path.

## Digest reporting convention

The final cron response should be short and operational: digest path, date source, processed count, queue remaining count, and any notable limitations. Do not return `[SILENT]` just because there were zero notes; the digest is always a reportable artifact.
