# Notes whitespace cleanup

Use when the user says notes have too much space, are hard to read, or asks to compact/clean Obsidian note formatting.

## Scope
Operate on direct `/vault/Notes/*.md` pages unless the user explicitly asks to clean MOCs, Sources, Tasks, Daily, or other folders. The wiki product is `Notes/`; avoid touching read-only or non-wiki areas by default.

## Cleanup rules
Apply formatting-only whitespace normalization:
1. Normalize line endings to `\n`.
2. Strip trailing spaces and tabs from every line.
3. Convert whitespace-only blank lines to empty blank lines.
4. Collapse 3+ consecutive newlines to exactly 2 newlines (one visible blank line).
5. Preserve exactly one final newline.

Do not rewrite prose, links, frontmatter semantics, headings, or lists during a whitespace-only pass.

## Root-owned-safe write pattern
Some notes may be root-owned. If the parent directory is writable, write updated content through a temp file and replace with:

```bash
cp --remove-destination /tmp/updated.md /vault/Notes/Page.md
```

This recreates the destination as the current user and avoids in-place write failures.

## Verification
After cleanup, rescan direct Notes and confirm:
- no trailing spaces/tabs remain;
- no whitespace-only blank lines remain;
- no `\n{3,}` runs remain;
- every note ends with one newline;
- `wiki-log.md` records the cleanup count.

Report scanned count, cleaned count, skipped/unreadable count, and remaining issue count.
