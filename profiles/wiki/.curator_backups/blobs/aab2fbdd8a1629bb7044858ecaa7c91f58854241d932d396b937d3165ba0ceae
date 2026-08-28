# MOC placement final verification — 2026-08-01

Use this after a headless exact-batch wiki maintenance run when automated MOC placement or semantic repair touched MOCs.

## Durable lesson
Final verification should inspect each touched page's actual MOC memberships, not only whether it appears in at least one MOC. A page can pass the numeric MOC-gap check while still being filed in a misleading broad or stale MOC.

## Repair pattern
1. Freeze the exact touched title list after the first mutation.
2. For each touched page, collect all readable MOC files containing `[[Title]]`.
3. Review whether each membership is a close domain fit from the page title/body, not merely broad tag overlap.
4. Remove stale/misleading placements and add the narrowest correct placement.
5. Update any edited MOC frontmatter `updated:` date to the run date.
6. Regenerate `System/wiki-index.md` and rewrite exactly one same-day maintenance log entry.
7. Rerun final verification over the frozen batch and assert:
   - the requested batch size was verified,
   - every touched title has valid frontmatter and `updated:` equal to the run date,
   - every touched title appears in the index,
   - exactly one same-day log entry exists,
   - weak Related links have been removed,
   - actual MOC memberships are semantically acceptable.

## Examples from the 2026-08-01 run
- `SafetyCulture ArgoCD GitOps Migration Case Study` was initially filed under `AI Agent Tooling MOC` because of tooling/devops overlap. It is a DevOps/GitOps infrastructure case study, not an AI-agent tooling note, so the better placement was `16 Science & Technology MOC`.
- `Legal Reserve Note` was sparse and ambiguous; it had been placed in both `Finance MOC` and `Personal MOC`. Because the note is a low-context personal/legal stub, `Personal MOC` was the honest placement and the Finance MOC link was removed.

## Guardrail
Do not let a verifier pass only because `mocs_for_title` is non-empty. Print and inspect the MOC filenames for all touched pages after semantic repair.