# Patch Contamination Recovery

Use this when a malformed `patch` call or interrupted tool-call draft writes assistant prose/tool-call fragments into a vault file.

## Immediate recovery sequence

1. **Stop normal edits.** Do not continue ingest, index, or MOC work until the contaminated file is clean.
2. **Inspect the diff and re-read the affected window.** Focus on YAML frontmatter, `sources:` lists, and `wiki-index.md` rows, where one polluted scalar can invalidate Obsidian/frontmatter parsing.
3. **Repair with the smallest unique replacement.** Patch only the contaminated line or unique leaked phrase; do not rewrite a whole infrastructure file from a partial read.
4. **Re-read after repair.** Confirm the repaired line is exactly the intended Markdown/YAML, especially closing quotes and frontmatter delimiters.
5. **Search for leak signatures.** Run exact searches over touched `Notes/`, `Sources/`, `MOCs/`, and `System/` files for unique leaked snippets such as fragments of the accidental assistant prose. Avoid broad generic terms that create noise.
6. **Validate frontmatter and artifacts.** Check touched note/source frontmatter begins and ends with exact `---`; then exact-search for the intended note/source/index/log/MOC artifacts before final summary.

## Durable lesson

The original failure mode is less important than the recovery pattern: narrow repair, exact leak-signature search, frontmatter validation, and artifact verification before finalizing.