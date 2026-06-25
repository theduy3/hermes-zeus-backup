# Direct Notes Scope + Semantic Link Guard

Session learning from 2026-06-19 wiki-lint run.

## Problem
A scanner that used `Notes.rglob('*.md')` treated nested operational subtrees such as `Notes/Claude-Context/sessions/` and `Notes/ADR/` as wiki pages. Those files can look sparse/orphaned under wiki rules, which causes the lint pass to select non-wiki implementation/session logs and apply wiki frontmatter or unrelated links.

## Durable rule
For normal wiki-lint page selection, treat canonical wiki pages as **direct children of `/vault/Notes`**:

```python
note_files = sorted(p for p in Path('/vault/Notes').glob('*.md') if p.is_file())
```

Do not recursively lint nested subdirectories unless a specific future command explicitly says that subtree is part of the wiki corpus.

## If a mistaken recursive pass happens
Clean it before rerunning:

1. Identify the accidental batch paths with `Path('/vault/Notes').rglob(title + '.md')`.
2. Remove synthetic wiki-lint frontmatter only when it clearly matches the generated shape (`title`, `updated: <run-date>`, `wiki_status`).
3. Remove unrelated generated `Related:` lines from those nested files.
4. Remove accidental MOC additions for nested-file titles.
5. Remove the bad log entry before appending the corrected run entry, so the final day has exactly one lint log entry.

## Semantic cross-link guard
When filling exactly 20 pages from the rolling refresh queue, do **not** add generic high-inbound links just because tags overlap. A `Related: [[Claude Code Architecture and Features]]` line is not valid for unrelated pages such as YouTube channel captures or finance notes.

Acceptable auto-added related links should satisfy at least one of:
- the exact page title appears naturally in the body and can be wikilinked in-place;
- the candidate shares at least two meaningful tags with the page;
- the titles share a meaningful domain token (for example `Claude`, `S&P`, `Obsidian`, `trading`).

If no close neighbor exists, leave the page as honestly unresolved and report it instead of forcing weak links.