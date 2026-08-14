# Economist full-issue quality corrections — July 11 repair lessons

Use this reference when a full The Economist issue ingest is judged too thin or MOCs are hard to browse.

## What went wrong

- Article Notes can look complete structurally while failing the user's reading need if `## Briefing` is only 1 sentence or generic.
- MOC date sections can be technically present but backwards: newest issues must be at the top, not appended at the bottom.
- Multiple article extracts sharing the same PDF page can contaminate each other if slicing grabs the whole page instead of the article boundary.
- Section MOCs can accumulate duplicate issue-date blocks after repeated repair passes unless the repair script deduplicates by heading.

## Durable repair pattern

1. Treat `Sources/<Issue> Articles/00-index.md` as the authoritative issue article list; exclude it from article counts.
2. For every article extract, ensure a mapped `/vault/Notes/<Durable Title>.md` exists.
3. Each article Note needs a substantive `## Briefing`:
   - 3–5 sentences minimum for the core argument.
   - Include concrete facts, figures, named actors, geography, mechanism, or stakes from the article.
   - Avoid placeholder language like “this is a durable signal” unless it is followed by specific evidence.
4. For articles that share PDF pages, slice by actual article boundary:
   - Use the article title/headline when present.
   - Prefer text after the preceding `■` end marker and before the next `■` marker.
   - Watch for drop-cap starts and source-extraction blank title fields.
5. Rebuild MOC issue sections newest-first:
   - Main `The Economist MOC`: newest issue/date block above older issue/date blocks.
   - Numbered section MOCs: newest date block above older date blocks, preserving article order within the issue.
6. Deduplicate section MOC date blocks after any bulk rewrite.
7. Verify before final reply:
   - Source article count maps to Notes count.
   - Every mapped Note has `## Briefing`.
   - No raw `Sources/... Articles/NN-...` links remain in readable MOCs.
   - No duplicate `### <issue date>` blocks in numbered MOCs.
   - Main and section MOCs put newest issue/date first.

## User-facing summary expectation

When repairing a disappointing issue ingest, report concrete verification numbers: notes regenerated, MOCs touched, remaining duplicates, and ordering checks. Keep the chat concise; the improved reading experience should live in the vault.
