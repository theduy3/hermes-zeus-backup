# Refreshed capture fold-in example — 13F scheduled refreshes

Session pattern: two Inbox captures (`Pershing Square Update.md`, `Situational Awareness Update.md`) were refreshed snapshots of existing wiki pages rather than new durable topics.

Reusable handling:
1. Detect existing coverage by searching `Notes/` for the capture subject/title.
2. Compare capture content to the existing note; if it is the same topic and same filing/report period, fold in rather than create a duplicate.
3. Update the existing note's frontmatter `updated:` date and any visible "Updated:" or source/caveat timestamp lines.
4. Ensure at least two useful wikilinks remain in the note and the relevant MOC link is present.
5. Touch the relevant MOC bullet to reflect the refresh date or current summary.
6. Update only the existing `System/wiki-index.md` row dates; do not increment page count when no new `Notes/` pages are created.
7. Append one `System/wiki-log.md` entry listing all source captures, created pages (`None` if none), updated pages, MOCs touched, and removal/archive status.
8. Remove the processed Inbox capture(s).
9. Run ad-hoc verification plus `find_today_notes.py --json --inbox` and delete the temporary verifier in a separate command.

Pitfall: if multiple rows in the same index/log/MOC need edits, serialize those patches rather than parallelizing writes to the same file.
