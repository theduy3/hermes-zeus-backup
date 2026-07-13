# Semantic review of Economist related links (2026-07-09)

## Context
An exact-20 cron lint pass over direct `/vault/Notes/*.md` pages selected mostly Economist article-derived notes. The first automated pass structurally succeeded but produced weak `## Related` links from token/tag accidents and left MOC links inside `## Related` sections.

## Durable lessons

1. **Do not use MOCs as Related links.** `[[The Economist MOC]]` and numbered domain MOCs such as `[[15 Finance & Economics MOC]]` belong in `/vault/MOCs/` membership, not in a note's subject-neighbor `## Related` section.
2. **Keep provenance/source issue links when meaningful.** For Economist article-derived notes, the source issue link such as `[[The Economist May 30 2026 Issue]]` is valid provenance and can remain in `## Related` when no closer source-specific page exists.
3. **Remove token-collision links.** Examples from this run that were removed as weak:
   - `Gatorade Sports Hydration Origin` → `Blue Origin Explosion and Lunar Plans` (shared “Origin” only)
   - `Japanese Curry Cultural Soft Power` → `Riesling and Soft Havarti` (food/culture too broad)
   - `Offshore Reinsurance Private Credit Risk` → `Sporting Prodigies Early Peak Risk` (shared “Risk” only)
   - `Europe East West Inequality Convergence` → `Middle East Power Struggles After Gaza War` (geography/world-politics too broad)
4. **Prefer close domain neighbors from title/body evidence.** Replacements used in this run included:
   - `Edible Medical Electronics Capsules` → `3D Printing on Living Tissue`
   - `Modern War Sensor Kill Zone` ↔ `Modern War Technology Transformation`
   - `Southeast Asia Autocracy Renewal` → `Malaysia Anwar Ibrahim Coalition Pressure`
   - `Federal Reserve Kevin Warsh Chair Risks` → `Monetary Policy`
5. **Leave low-outbound honest if no close neighbor exists.** Do not force a second link for sparse or narrowly scoped article pages. This run intentionally left `Ferrari Electric Supercar Strategy`, `Japanese Curry Cultural Soft Power`, and `Offshore Reinsurance Private Credit Risk` below two outbound note links after semantic cleanup.
6. **After semantic repair, regenerate infrastructure and rewrite—not append—the same-day lint log entry.** Re-verify that all 20 touched pages have `updated: <run-date>`, no conflict markers, no MOC links in `## Related`, index rows, and exactly one same-day lint log entry.

## Source/archive hygiene reminders reinforced by this run
- Preserve numbered Economist MOC filenames (`06 ...`, `15 ...`, etc.); do not rename or collapse them during lint.
- Treat `Sources/_cold/` as legacy/low-browse bulk only. Active/high-value source archives remain directly under `/vault/Sources/`.
- Keep binaries in `/vault/Attachments/`; lint should not move or duplicate binary artifacts.
