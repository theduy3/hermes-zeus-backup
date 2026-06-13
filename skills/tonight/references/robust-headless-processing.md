# Robust headless evening processing notes

Use this when running the `tonight` cron job against `/vault`.

## Defensive processing pattern

1. Run `python3 /vault/System/scripts/calculate_dates.py` first and parse `Date:` plus the day name from `Today:`. This date is authoritative for the digest filename and frontmatter.
2. Run `python3 /vault/System/scripts/find_today_notes.py --json --inbox` and treat its output as a mutable work queue.
3. For every queued item, verify the source path still exists before writing/moving. If the queued file is gone or empty, search all relevant vault content (`/vault/Notes`, `/vault/Projects`, and other writable filing destinations) for a distinctive title/source URL/content excerpt and summarize the existing page instead of creating another duplicate.
4. Classify the capture before defaulting to `Notes/`. Some processed captures are project/reference material rather than wiki pages; file them under the best existing project folder from `/vault/CLAUDE.md` and the current project structure with ordinary frontmatter tags. Do **not** invent a new domain folder just because the topic is recognizable: if no domain-specific project folder exists and the item is clearly a draft/post/content asset, use `Projects/Writing/` (as with Vietnamese nail-salon tax/W-2 social post drafts). Only run wiki/MOC/index integration for true `Notes/` wiki pages.
5. For low-content captures (image-only notes, empty GitHub clippings, thin URL shells), either:
   - match/remove them as duplicates of an existing filed page, or
   - create a clearly labeled stub preserving the source URL/attachment path and stating that manual summary/transcript/image interpretation is still needed.
6. After writing a promoted or filed page, verify the target exists and is non-empty, then remove the root/Inbox original. Do not leave root originals copied into the destination.
7. If a prior digest already exists but `find_today_notes.py` still returns items, process the queue anyway. A previous digest may have been written before residual Inbox originals were removed. Match residual captures to existing filed pages by title/source URL/content, summarize those existing pages, archive/remove the residual originals, and overwrite the digest with the current verified counts.
8. Update MOCs/wiki-index/wiki-log only when the files are readable/writable. If they are unavailable, continue and report that limitation; digest creation is the non-negotiable output.
9. Rerun `find_today_notes.py --json --inbox` after filing and include the remaining count in the digest verification section.
10. Write `/vault/Daily/<YYYY-MM-DD>-tonight.md` even when zero notes were processed. Include `notes_processed`, the initial queue count, the post-processing queue count, and whether mini wiki-lint was skipped.
11. Verify the digest by reading it back. If direct overwrite fails but `/vault/Daily` is writable, write a same-directory temp file and atomically replace the final path.

## Digest reporting convention

The final cron response should be short and operational: digest path, date source, processed count, queue remaining count, and any notable limitations. Do not return `[SILENT]` just because there were zero notes; the digest is always a reportable artifact.

## Implementation pitfalls

- When automating the digest writer from Python, parse `calculate_dates.py` with a simple line-based key/value parser (`line.split(': ', 1)` for `Today:` and `Date:`) instead of hand-rolled regex inside nested string literals. Escaping mistakes can make an otherwise valid script fail before the digest is written.
- If the linked `references/robust-headless-processing.md` is not present under `/vault/.claude/skills/...`, do not treat that as a vault failure. In Hermes sessions, the canonical support file is available via the `tonight` skill's linked `references/` file; continue with the loaded SKILL.md instructions when running headless.
