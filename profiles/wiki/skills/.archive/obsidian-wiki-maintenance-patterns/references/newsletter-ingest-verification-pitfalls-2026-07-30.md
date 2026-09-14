# Newsletter ingest verification pitfalls — 2026-07-30

Context: During a Morning Brew newsletter ingest, the workflow created/updated Notes, MOCs, `wiki-index.md`, `wiki-log.md`, and a normalized `Sources/Newsletter/` archive.

Reusable lessons:

1. **File search is glob, not regex alternation.** A verification probe like `DoorDash Drone Delivery Stack.md|Washington Dulles Airport Megaproject.md|Hims Health Data Advertising Privacy.md` under `search_files(target="files")` returned zero even though the files existed. Use separate exact probes, a wildcard that actually matches, or a terminal `test -s` loop for multiple files.
2. **CRLF source archives can defeat exact delimiter regexes.** Newsletter captures may retain `\r\n`. Searching a patched archive for `^---$` returned zero because the stored lines ended with `\r`. Verify with `read_file` on the first lines or search distinctive fields like `ingested: YYYY-MM-DD`, `## Pages Updated`, and the created page titles.
3. **Watchlist candidates require a positive thesis.** Public-company risk items should still become/update company or risk notes, but do not list a ticker under watchlist candidates merely because it moved or appeared. In the session, DASH had a plausible positive scale thesis; HIMS was tracked as an FTC/privacy overhang rather than surfaced as a candidate.

Good verification checklist:

- Exact note-file presence, one file at a time or via shell `test -s`.
- Source archive plus `.inbox-original.md` presence when preserving raw newsletter captures.
- Inbox file count is zero after archival.
- `wiki-index.md` has new rows and bumped page count.
- `wiki-log.md` has the ingest entry and any watchlist-candidate wording is thesis-qualified.
- MOC content searches find each new routed note.
