# GitHub repo URL capture + existing-page refresh

Use when the user sends a full GitHub repository URL, including tracking query strings such as `fbclid=...`.

## Pattern
1. Capture the raw URL verbatim to `Inbox/YYYY-MM-DD-HHMM-<repo-slug>-github-url.md`.
2. Normalize a canonical repo URL by stripping query params: `https://github.com/<owner>/<repo>`.
3. Fetch GitHub API metadata and README from the canonical owner/repo.
4. Dedup by exact repo URL, owner/repo, and likely existing note title across `Notes/` and `System/wiki-index.md`.
5. If an existing substantive page exists, update that page instead of creating a duplicate.
6. Create a source archive in `Sources/<capture-basename>.md` with:
   - `source:` = exact raw captured URL, preserving tracking params for provenance
   - `canonical_url:` = normalized GitHub URL
   - repo metadata: stars, forks, open issues, language, license, created/updated/pushed
   - README body
   - `## Pages Updated`
7. Preserve the raw Inbox capture under `Notes/Archived Inbox Originals/` and keep Inbox empty.
8. Update MOC/index/log and verify exact matches.

## What to update in an existing repo note
- Frontmatter `updated` date and source wikilink.
- A dated refresh section with *new or changed* durable facts: app availability, new install methods, supported tools, limits/workarounds noted by upstream, expanded divisions/categories.
- Avoid rewriting the whole older page unless the upstream README structure changed enough to make the note misleading.

## Pitfalls
- Preserve the raw tracked URL exactly in the source archive; do not silently replace it with the canonical URL.
- Do not create a separate repo source page in `Notes/` when `Sources/` is writable.
- If GitHub fetch fails and only URL metadata is available, archive metadata-only and do not fabricate capabilities from the repo name.