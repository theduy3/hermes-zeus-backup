# Patch contamination and verification pattern — 2026-07-28

This session surfaced an avoidable but recoverable wiki-edit hazard: malformed patch arguments accidentally wrote chat/tool-call residue into YAML source lists (`}}, {` and `...oops`). The important reusable lesson is the recovery sequence, not the specific source.

## Recovery sequence

1. Stop normal edits as soon as the returned diff shows accidental prose/tool residue.
2. Patch the exact contaminated scalar/sub-string immediately with a narrow replacement.
3. Run an exact vault search for the distinctive residue fragments before continuing.
4. Re-read the touched frontmatter/body window and confirm YAML structure is clean.
5. Only then resume MOC/index/log edits.

## Verification notes

- Do not trust `search_files(target="files")` with alternation-style patterns for multi-file verification; it is glob-based. Use separate file probes or a narrow read-only `test -f ... && test ! -e ...` command.
- Do not rely on `git diff --stat` alone for final verification, because untracked newly-created files may not appear in the stat. Pair git sanity checks with explicit note/source file-existence probes.
- Email/newsletter archives often preserve CRLF line endings. After frontmatter replacement, re-read the first lines and verify both delimiters are exactly `---`, not `----`.

## Example final checks

- Exact-search leaked fragments: `}}, {`, `...oops`, or any other distinctive accidental token.
- Probe touched files explicitly: new `Notes/*.md`, source archive, and absence of the moved Inbox source.
- Exact-search infrastructure rows for every created/updated page and final `wiki-log.md` entry.
