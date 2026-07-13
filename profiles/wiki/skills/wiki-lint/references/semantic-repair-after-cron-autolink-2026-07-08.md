# Semantic repair after cron autolink (2026-07-08)

## Durable lesson

A structurally successful exact-20 wiki-lint run can still add misleading links or MOC placements when the candidate page has broad tags or low-context source text. Do a post-run semantic pass over every touched page before reporting success.

## What to check

1. Re-read the `## Related` section of all 20 touched pages.
2. Remove Related entries that are only justified by broad tags such as `china`, `britain`, `culture`, `finance`, `security`, `ai`, `business`, or `economist`.
3. Remove MOC links from `## Related`; MOC membership belongs in `/vault/MOCs/`, not as a substitute for subject-neighbor links.
4. Keep provenance/source links such as `[[The Economist May 30 2026 Issue]]` when they point to the issue/source that informed the note.
5. If removing weak links increases the post-run low-outbound count, report the honest count rather than forcing replacements.
6. Semantically review MOC placement, especially for rolling-refresh notes whose tags are wrong or stale. Example: a weekly review framework note tagged with finance/investing was wrongly added to `15 Finance & Economics MOC.md`; fix tags and move it to `Personal MOC.md` instead.
7. Regenerate `System/wiki-index.md` and rewrite the same-day `wiki-log.md` entry after semantic repair; do not append a second same-day lint entry.

## Verification pattern

After repair, verify:

- exactly 20 selected pages still have `updated: <run-date>`;
- all 20 appear in `System/wiki-index.md`;
- same-day lint log entry count is exactly 1;
- no touched page has MOC links in `## Related`;
- any deliberate low-outbound increase is reflected in the log's Remaining line.

## Pitfall

Do not treat a verifier's “2 outbound links” as success when the links are generic, navigational, or MOC-only. The purpose is semantic cross-reference quality, not satisfying a numeric rule at any cost.
