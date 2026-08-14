# Multi-Artifact Vault/Cron Verification — 2026-07-29

Use when a headless job mutates several files and must prove success without relying on a single broad search.

## Pattern

1. Verify the queue/source-of-truth is empty or at the expected count after the run.
2. Verify every expected output path explicitly.
   - Prefer a narrow shell check such as `test -f 'file1' && test -f 'file2' ...` for exact files.
   - Do not use one `search_files(target="files")` pattern with regex alternation (`a.md|b.md`); file search is glob-style and will return zero.
3. Verify representative content with exact text searches in each infrastructure surface:
   - content notes/pages;
   - source archives;
   - MOCs/navigation files;
   - index/catalog;
   - log/changelog.
4. For Markdown/YAML artifacts, parse or at least delimiter-check all touched frontmatters after final patches, not before final type/source corrections.
5. If a verification tool returns zero due to a bad verifier pattern, fix the verifier and rerun before reporting. Do not treat a verifier bug as an artifact failure.

## Example from the session

A wiki ingest created four source archives, three notes, five note updates, four MOC updates, index rows, and log entries. A first `search_files(target="files")` check using `file1.md|file2.md` returned zero because the tool uses globs, not regex. The robust replacement was an exact `test -f` chain plus file-size prints, exact content searches for notes/MOCs/index/log, and a final YAML parse over every touched note/source frontmatter.
