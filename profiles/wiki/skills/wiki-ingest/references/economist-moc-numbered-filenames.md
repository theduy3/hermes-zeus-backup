# Economist MOC numbered filenames

Use when maintaining full *The Economist* issue ingests and section MOCs in theduyvault.

## User preference
The user wants the canonical *Economist* table-of-contents number in the **actual MOC note filename**, not only in the page H1, a display alias, or a section-order marker.

Examples:
- `MOCs/14 Business MOC.md`
- `MOCs/15 Finance & Economics MOC.md`
- `MOCs/17 Culture MOC.md`

Do not leave the filename as `Business MOC.md` with only `# 14 Business MOC` inside; that was explicitly corrected.

## Canonical numbered MOC filenames
- `06 US Politics & Society MOC.md` — United States
- `07 The Americas MOC.md` — The Americas
- `08 International MOC.md` — International
- `09 Asia MOC.md` — Asia
- `10 China MOC.md` — China
- `11 Middle East & Africa MOC.md` — Middle East & Africa
- `12 Europe MOC.md` — Europe
- `13 Britain MOC.md` — Britain
- `14 Business MOC.md` — Business
- `15 Finance & Economics MOC.md` — Finance and economics
- `16 Science & Technology MOC.md` — Science and technology
- `17 Culture MOC.md` — Culture and Obituary

Obituary remains routed through `17 Culture MOC.md`; do not create a separate `18 Obituary MOC.md` unless the user asks.

## Safe migration pattern
1. Rename the MOC files under `/vault/MOCs/`.
2. Rewrite all Obsidian wikilinks across allowed vault areas (`Notes/`, `MOCs/`, `Sources/`, `System/`) from old targets to numbered targets:
   - `[[Business MOC]]` → `[[14 Business MOC]]`
   - `[[Business MOC|14 Business MOC]]` → `[[14 Business MOC]]`
3. Keep H1 titles matching the new filenames.
4. Update `The Economist MOC` canonical section list to link directly to numbered names.
5. Verify:
   - new numbered files exist;
   - old unnumbered files are gone;
   - no exact old MOC wikilinks remain;
   - no raw numbered article-source links like `[[01-...]]` were introduced into MOCs;
   - `wiki-log.md` records the migration.

## Scope caution
Do not rewrite `.claude/`, `Tasks/`, or `Daily/` unless the user explicitly asks. The wiki librarian is allowed to write only under `Inbox/`, `Notes/`, `MOCs/`, `Sources/`, `Attachments/`, and `System/`.
