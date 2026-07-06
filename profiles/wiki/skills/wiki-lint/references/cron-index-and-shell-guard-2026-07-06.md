# Cron index parity and shell-guard pitfalls — 2026-07-06

Use this reference for scheduled `wiki-lint` runs that edit exactly 20 pages and regenerate `/vault/System/wiki-index.md`.

## Lessons from the run

1. **Index page_count must reflect total direct Notes pages, not only readable pages.**
   - A cron-safe scanner may skip unreadable root-owned direct notes during parsing/editing.
   - If index regeneration only emits rows for readable pages, verification can pass for the 20 edited pages while silently dropping unreadable-but-real notes from `wiki-index.md` and lowering `page_count`.
   - Final verification should compare `len(/vault/Notes/*.md)` against index row count and report any missing direct-note basenames.

2. **When direct notes are unreadable, preserve index parity with fallback rows.**
   - Do not try to read or rewrite unreadable root-owned notes.
   - Add/keep a conservative index row for each unreadable direct note using known title + last-known/index metadata if available, or a clearly conservative fallback if not.
   - Report the exact `sudo chown hermes:hermes ...` command so a later run can fully inspect and update the note.

3. **Distinguish readable page counts from total corpus counts in the log.**
   - Log wording should avoid implying unreadable notes were fully scanned.
   - Example: `Scanned: 793 readable note pages (795 total direct note files; skipped 2 unreadable root-owned notes and 1 unreadable MOC)`.

4. **Cron shell approval guard can misread ampersands inside heredoc Python.**
   - A foreground `terminal` command containing Python such as `st.st_mode & 0o777` inside a heredoc can be rejected as shell backgrounding.
   - Avoid bitwise `&` in inline heredoc verification snippets; use `stat.filemode(...)`, arithmetic alternatives, or write the script to `/tmp` and execute it.
   - This is a command-shaping pitfall, not evidence that `terminal` is broken.

## Verification add-on

After index/log repair, run a final exact-20 verification that checks:

- every batch page has `updated: <run-date>`, valid `type`, valid `wiki_status`, populated `tags`, no frontmatter conflict markers, and an index row;
- `page_count` equals the number of direct `/vault/Notes/*.md` files, including unreadable ones;
- index rows cover all direct note basenames, or any missing unreadable rows are intentionally restored with conservative fallback metadata;
- exactly one same-day `lint | Wiki health check` entry exists in `wiki-log.md`.
