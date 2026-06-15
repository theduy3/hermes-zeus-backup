# Dependency-free cron scanner pattern for wiki-lint

Use this when a scheduled wiki-lint run needs a self-contained `/tmp/wiki_lint_run.py` but the cron Python environment may not include optional packages like PyYAML.

## Durable lesson

Do not make the fallback scanner depend on non-stdlib packages unless the skill explicitly installs or verifies them first. For cron-safe wiki maintenance, prefer a conservative stdlib-only frontmatter parser/dumper that handles the common Obsidian subset:

- `---` delimited frontmatter
- scalar `key: value`
- null/empty `key:`
- indented list items under the current key
- quoted strings via JSON-style quoting on dump
- artifact detection/removal for `>> NEW >>` and `<< OLD <<` inside frontmatter

This avoids aborting the run when `import yaml` fails and still lets the job repair canonical wiki fields (`tags`, `type`, `created`, `updated`, `sources`, `wiki_status`, plus useful metadata such as `title`/`source`).

## Recommended workflow

1. Generate the fallback scanner under `/tmp/` and execute it with `terminal`.
2. Use only Python stdlib for parsing, writing, verification, and JSON reporting.
3. Treat the parser as conservative:
   - preserve fields it understands;
   - normalize canonical fields;
   - flag but do not overfit exotic YAML constructs;
   - re-read all 20 pages after writing.
4. If semantic review removes weak auto-added links, run a second stdlib-only repair script that:
   - patches the affected pages;
   - regenerates `System/wiki-index.md`;
   - rewrites the same-day lint log entry rather than appending another;
   - reruns all-20 verification.

## Pitfalls

- A page can pass structural checks while still carrying misleading `## Related` links. Dependency-free verification still needs semantic review of sparse pages.
- Do not record “PyYAML is unavailable” as a durable constraint. The durable pattern is: cron fallback scripts should either verify dependencies up front or avoid them.
- When removing forced links from sparse pages, update the log’s low-outbound count and explicitly mark those pages as intentionally unresolved rather than failed.
