# Partial-run crash recovery + unreadable MOC handling (2026-07-04)

## What happened
A scheduled `wiki-lint` run updated the 20 selected `Notes/*.md` pages, then crashed during post-edit verification because a root-owned MOC (`/vault/MOCs/Finance MOC.md`, mode `600`) raised `PermissionError`. The first script had already modified Notes and regenerated the index, but had not appended the final log entry. A follow-up recovery script inspected recently touched pages, semantically cleaned weak links, repaired MOC placement, regenerated `System/wiki-index.md`, appended one log entry, and verified the exact 20-page batch.

## Durable workflow lesson
Cron lint scripts must treat unreadable MOCs like unreadable Notes: skip and report them rather than letting one permission error abort the run after page mutations.

## Recovery pattern if a lint script crashes after editing pages
1. Identify the actual touched batch from the previous script output or recent mtimes under `/vault/Notes/*.md`.
2. Re-read all touched pages and inspect any added `## Related` sections for weak/generic links.
3. Remove weak links that are justified only by broad tags or MOC/popularity overlap; accept honest low-outbound pages rather than forcing unrelated links.
4. Review newly added MOC memberships semantically. In the 2026-07-04 recovery, finance/trading pages were moved from `AI Development MOC` to `Finance & Economics MOC`, and a Canada politics article was moved from `Home` to `The Americas MOC`.
5. Reload MOCs with `try/except PermissionError`; unreadable root-owned MOCs should be added to `unreadable_skipped` and reported with a `chown` command.
6. Regenerate `/vault/System/wiki-index.md` with `cp --remove-destination` replacement.
7. Append exactly one `/vault/System/wiki-log.md` entry for the completed run. If a prior partial script already appended one, rewrite the same-day entry instead of appending another.
8. Final verification must check: exactly 20 touched pages reread, `updated` is today, frontmatter has no conflict markers, every batch title is present in the index, index header has today's date/page count, and the log delta is exactly one.

## Implementation cautions
- Do not rely on a script's in-memory pre-crash state after a crash. Recompute outbound counts, MOC membership, index rows, and log-entry counts from disk.
- Treat MOC links as navigation, not sufficient semantic related links for the two-outbound rule.
- If a direct selected Note is root-owned, use the delete-then-rewrite workflow; if an unreadable file is not selected for editing, skip and report it.
- Permission blockers worth reporting from this run were root-owned mode-600 files. The actionable fix is:
  `sudo chown hermes:hermes <paths>`
