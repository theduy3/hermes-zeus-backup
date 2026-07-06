# Bare GitHub repo shorthand capture

Use when a Telegram message is only an `owner/repo` identifier, e.g. `langchain-ai/deepagents`.

## Pattern

1. Capture the raw text verbatim to `Inbox/YYYY-MM-DD-HHMM-<owner-repo>.md`.
2. Normalize the repository URL: `https://github.com/<owner>/<repo>`.
3. Fetch current GitHub metadata and README text before ingesting:
   - API metadata: `https://api.github.com/repos/<owner>/<repo>`
   - README raw: `https://raw.githubusercontent.com/<owner>/<repo>/main/README.md` (fallback to default branch from API if needed).
4. Dedup-check likely note names and related concepts in `Notes/` and `System/wiki-index.md`.
5. Create/update a substantive entity/repo note from metadata + README, not from the short Telegram text alone.
6. Archive a normalized source in `Sources/<timestamp>-<owner-repo>.md` with:
   - `tags: [source]`
   - `type: repo`
   - `source: https://github.com/<owner>/<repo>`
   - `created` and `ingested`
   - key metadata and README extract
   - `## Pages Updated`
7. Preserve the raw Inbox capture in `Notes/Archived Inbox Originals/` and remove it from `Inbox/`.
8. Update MOCs, `System/wiki-index.md`, and `System/wiki-log.md`; verify exact matches for the created page, source archive, MOC link, index row, log entry, and Inbox emptiness.

## Pitfalls

- Do not create a page from the title/repo name alone if README/API fetch fails; archive as metadata-only with `Pages Updated: None` and report the blocker.
- Before adding inferred wikilinks such as `[[LangGraph]]`, exact-search for the page. If no page exists and the source does not warrant creating it, mention the term in plain text to avoid dangling links.
- Multi-file patches that include a no-op hunk can fail the whole patch. Keep infrastructure patches small and non-no-op; append `wiki-log.md` separately if needed, then verify with exact search.
