# Source archive naming convention

Use when processing Inbox captures into `/vault/Sources/`, especially when the user dumps material quickly with random filenames.

## Canonical filename format

`YYYY-MM-DD - Source Title.md`

Examples:
- `2026-07-06 - The Economist USA May 30th-June 5th 2026.md`
- `2026-07-06 - Welcome to Tech Brew.md`
- `2026-07-06 - Vietnamese W-2 vs 1099 Nail Worker Comparison.md`

Use the ingest date for the prefix. Preserve publication date in frontmatter/body when known.

## Title derivation priority
1. YAML `title:` field from the captured source.
2. First Markdown H1 (`# Title`).
3. Remote/page metadata title after fetch/extraction.
4. GitHub repo name + concise description.
5. Video metadata title from `yt-dlp` sidecar JSON.
6. PDF/issue title from document metadata or visible cover/title page.
7. If no title exists, infer a concise descriptive title from the content.

Do not preserve random dump names such as `gdjd.md`, `rfff.md`, `th.md`, etc. as final source archive names unless the source is intentionally opaque and no title can be inferred.

## Filename sanitation
- Remove unsafe filename characters: `/ \ : * ? " < > |`.
- Collapse repeated spaces.
- Prefer human-readable Title Case for source titles.
- Drop meaningless emoji from filenames; keep the title text in frontmatter/body.
- Enforce the existing 200-byte UTF-8 basename cap with collision reserve.
- On collision, append a numeric suffix, e.g. `2026-07-06 - Welcome to Tech Brew 2.md`.

## Preserve provenance
When renaming from a random/original capture name, add or preserve:

```yaml
original_filename: "gdjd.md"
title: "Vietnamese W-2 vs 1099 Nail Worker Comparison"
created: YYYY-MM-DD
ingested: YYYY-MM-DD
```

For URL captures, preserve both raw and normalized URLs when available:

```yaml
source: "https://raw-url.example/..."
canonical_url: "https://canonical-url.example/..."
original_filename: "rfff.md"
```

## Wikilink migration
If a source archive is renamed, update all source wikilinks in `/vault/Notes`, `/vault/MOCs`, `/vault/Sources`, and `/vault/System` from the old basename to the new basename.

Example:

```yaml
sources:
  - "[[gdjd]]"
```

becomes:

```yaml
sources:
  - "[[2026-07-06 - Vietnamese W-2 vs 1099 Nail Worker Comparison]]"
```

## Exceptions
- Do not rename numbered article extracts inside issue folders, e.g. `Sources/The Economist May 30 2026 Articles/01-world-politics-digest-may-2026.md`; those names preserve reading order.
- Do normalize the issue-level source archive name.
- Do not mutate raw Inbox captures in place; create normalized source archives and move/preserve originals according to the root-owned Inbox patterns in `wiki-ingest`.

## Operational pattern
1. During ingest, derive source title before archiving.
2. Create the archive under `Sources/YYYY-MM-DD - Source Title.md`.
3. Add `original_filename:` if the capture basename differed.
4. Use the normalized source basename in new Notes `sources:` links, `## Pages Updated`, `wiki-log.md`, and index rows.
5. Verify no links remain to the old random basename before final summary.

## Bulk normalization script

For existing source libraries, use the vault helper script:

```bash
python3 /vault/System/scripts/normalize-source-filenames.py --dry-run --include-cold --all-missing-date
python3 /vault/System/scripts/normalize-source-filenames.py --apply --include-cold --all-missing-date
```

The script should:
- scan direct `Sources/` and `_cold/` Markdown files;
- skip numbered issue article extracts under `Sources/<Issue> Articles/`;
- skip `.inbox-original.md` raw preservation files;
- preserve `original_filename:`;
- rewrite old source wikilinks across `Notes/`, `MOCs/`, `Sources/`, and `System/`;
- support fallback title extraction from `title:`, `Full Title:`, first H1, URL last path segment, and first substantial body line.

Verification target after applying: a follow-up dry run reports `0 source files would be renamed; ambiguous skipped: 0` and an independent scan finds all eligible source Markdown files matching `YYYY-MM-DD - Source Title.md`.
