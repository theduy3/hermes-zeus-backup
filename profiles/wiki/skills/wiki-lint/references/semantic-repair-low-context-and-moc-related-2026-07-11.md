# Semantic repair after exact-20 lint: low-context pages + MOC-related cleanup (2026-07-11)

## Context
An exact-20 cron lint pass selected mostly Economist pages plus one low-context external politics clipping. The first automated pass satisfied many pages numerically, but final semantic review found `## Related` sections containing MOC links and one unrelated generic link.

## Durable workflow lesson
After any automated cross-link fill, do a separate semantic repair pass before final reporting:

1. Print/read every touched page's `## Related` section, not just outbound counts.
2. Remove all MOC links from `## Related` (`[[... MOC]]`), even if they helped a numeric outbound check.
3. Remove broad/generic or token-collision links that do not share a close subject relationship. Example: a Canada politics clipping was incorrectly linked to `[[Coding for Marketers]]` because of generic tags; remove it and leave the page honestly low-outbound if no close neighbor exists.
4. Prefer provenance/source links plus close same-issue neighbors for Economist pages. Issue/source links such as `[[The Economist May 30 2026 Issue]]` are valid provenance, but should not be padded with MOC links.
5. For digest pages, add only close sibling/digest/domain pages when available; otherwise keep the low-outbound count honest.
6. Regenerate `/vault/System/wiki-index.md` after semantic cleanup.
7. Rewrite the same-day lint log entry so there is exactly one `## [YYYY-MM-DD] lint | Wiki health check` entry and its post-run low-outbound count reflects the repaired state.
8. Rerun exact-20 verification: all batch pages have `updated` set to the run date, valid frontmatter, no conflict markers, index rows present, and no MOC links in `## Related`.

## Reporting pattern
Report low-outbound pages that remain after cleanup as intentional/honest unresolved pages rather than failures. Do not force generic replacements just to satisfy the two-link target.

## Scope reminders
- Preserve numbered Economist MOC filenames.
- Treat `Sources/_cold/` as legacy/low-browse only; do not move active/high-value sources there during lint.
- Keep binaries in `/vault/Attachments/`.
