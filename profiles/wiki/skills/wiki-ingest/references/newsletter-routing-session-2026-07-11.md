# Newsletter Routing Session — 2026-07-11 Morning Brew Flagship

Use this as a concrete routing example for a normal writable Morning Brew flagship newsletter capture.

## Source
- Inbox capture: `Inbox/2026-07-11-0943-newsletter-still-reeling.md`
- Normalized source archive: `Sources/2026-07-11 - Still Reeling.md`
- Raw original preserved: `Sources/2026-07-11-0943-newsletter-still-reeling.inbox-original.md`
- Source title came from the newsletter H1 (`☕ Still reeling`), normalized to `Still Reeling`.

## Routing decisions
- Netflix live-channel/bundling/Letterboxd story: update existing `Notes/Netflix Second Season Viewership Drop.md` rather than create a new Netflix note. The durable point is engagement decline → live channels, bundles, ads, and possible niche taste-graph acquisition.
- EU Meta addictive-app DSA findings: create a new concept note `Notes/Meta Addictive App Regulation.md` because it is durable platform-regulation knowledge distinct from earlier Meta Muse image-reuse/privacy notes.
- Meta Muse rollback sentence: update `Notes/Meta Muse Public Image Reuse.md`; do not create a separate rollback note.
- 21st Century ROAD to Housing Act one-line item: update `Notes/Boomerang Kids Housing Affordability.md` as a policy-process datapoint; do not create a standalone atomic page without implementation substance.
- Market table: update `Notes/Economic Indicators.md` with Nasdaq/S&P/Dow/10-year/Bitcoin/SK Hynix/oil framing. Flagship Morning Brew market tables still count as macro dashboard inputs.
- Newsletter-network routing: update `Notes/Morning Brew Newsletter Network.md` with a dated section describing created/updated pages and explicitly noting ads, polls, entertainment ICYMI, games, referrals, and recs as source-only.

## MOCs touched
- `MOCs/14 Business MOC.md`: add `[[Meta Addictive App Regulation]]` under Business Media and Newsletters.
- `MOCs/06 US Politics & Society MOC.md`: add/refresh `[[Boomerang Kids Housing Affordability]]` with the housing-act datapoint.
- `MOCs/15 Finance & Economics MOC.md`: add `[[Economic Indicators]]` with the July 11 market snapshot.

## Infrastructure / verification pattern
1. Copy Inbox capture to the normalized `Sources/YYYY-MM-DD - Source Title.md` archive.
2. Patch only the archive frontmatter (include `tags: [source, newsletter, morning-brew]`, `type: article`, `created`, `ingested`, and `original_filename`).
3. Append `## Pages Updated` to the archive.
4. Move the raw Inbox original to `Sources/<original-stem>.inbox-original.md` after the archive exists.
5. Update `wiki-index.md` page count and rows for created/updated notes.
6. Append `wiki-log.md` entry.
7. Verify: Inbox empty, source archive + raw original present, exact index/log/MOC/note matches.

## CRLF caution
Newsletter captures may have CRLF line endings. After frontmatter patches, read back the first lines of the archive and confirm delimiters are exactly `---`. Patch tools may show large diffs because line endings normalize; that is acceptable only if the final archive frontmatter and body are intact.