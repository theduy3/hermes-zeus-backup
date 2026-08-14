# GitHub Repo Web Clip with Overlong/Extensionless Inbox Filename

Session pattern: an Inbox item may be a GitHub README web clip whose filename is an overlong title fragment and has no `.md` extension. It can still be normal Markdown and should be ingested as a repo source, not sent through OCR/binary handling.

## Recognition

- Inbox basename looks like `owner_repo_ Practical patterns...` and may be truncated without `.md`.
- The file begins with YAML frontmatter such as `title:` and `source:` and then README markdown.
- `source:` may include tracking parameters like `?fbclid=...`; preserve this exact raw URL for provenance.

## Reliable workflow

1. Sniff/read the Inbox file as text before classifying it as non-Markdown.
2. Parse the raw `source:` exactly and derive `canonical_url: https://github.com/<owner>/<repo>`.
3. Fetch GitHub API metadata when possible, and use the captured README body for substance.
4. Dedup by exact repo/page title in `Notes/` and `System/wiki-index.md`.
5. Create or update a substantive repo/entity page in `Notes/` with canonical URL/repo fields and links to existing harness/tooling concepts.
6. Write a normalized source archive such as `Sources/YYYY-MM-DD - <Repo Title> GitHub.md` with:
   - `source:` = exact captured URL including tracking parameters
   - `canonical_url:` = clean repo URL
   - `original_filename:` = the long/opaque Inbox basename
   - `## Pages Updated`
7. Move/preserve the raw Inbox original as `Sources/YYYY-MM-DD - <Repo Title> GitHub.inbox-original.md` after the normalized archive exists.
8. Update MOCs, `wiki-index.md`, and `wiki-log.md`; verify exact note/source/original/MOC/index/log matches and that Inbox is empty.

## Example outcome

For `cobusgreyling/loop-engineering`, the normalized source was `Sources/2026-07-21 - Loop Engineering GitHub.md`, the raw original was preserved as `Sources/2026-07-21 - Loop Engineering GitHub.inbox-original.md`, and the wiki note was `Notes/Loop Engineering GitHub.md`, cross-linked to harness/agent-tooling pages.