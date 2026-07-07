# Vault markdown whitespace cleanup

Use when the user reports that notes or vault Markdown are hard to read because of excessive blank space.

## Scope rules
- For `/vault/Notes/`: clean direct note pages when requested; these are the wiki product.
- For other writable wiki folders: clean `MOCs/`, `Sources/`, and `System/` Markdown.
- Skip `Inbox/` raw captures unless the user explicitly asks to mutate Inbox; raw captures are normally immutable.
- Skip `Attachments/` binaries.
- Do not edit `Daily/` or `Tasks/` from the Wiki agent; those are read-only by role.

## Normalization rules
For each Markdown file in scope:
1. Normalize CRLF/CR line endings to LF.
2. Strip trailing spaces and tabs from every line.
3. Convert whitespace-only blank lines to empty blank lines, including Unicode whitespace when encountered.
4. Collapse 3+ consecutive newlines to exactly 2 newlines (one visible blank line).
5. Ensure exactly one final newline at EOF.

Do not rewrite prose, headings, wikilinks, frontmatter keys, or source content semantics. This is readability cleanup only.

## Root-owned file pattern
If a file is root-owned but the directory is writable, write the normalized content to a temp file and replace with:

```bash
cp --remove-destination /tmp/normalized.md /vault/path/file.md
```

This recreates the target as `hermes` without requiring sudo.

## Verification
After cleanup, rescan every Markdown file in scope and report:
- files scanned;
- files changed;
- unreadable files;
- remaining files with trailing whitespace, whitespace-only blank lines, 3+ blank-line runs, or missing final newline.

Expected successful result: `remaining_issue_files: 0`.

## Logging
Append a `wiki-log.md` entry with a concise summary. Do not regenerate the whole index for whitespace-only cleanup unless file titles/frontmatter changed.
