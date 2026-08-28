# Newsletter Source Ingest Verification — 2026-07-23

This reference captures a cron-safe pattern from a Morning Brew flagship ingest where a newsletter issue became several atomic wiki notes plus updates to existing notes, MOCs, wiki-index, and wiki-log.

## When to use
Use when a headless vault job processes an email/newsletter capture and must archive the source, update semantic notes, route through MOCs, and verify infrastructure without user interaction.

## Routing pattern
1. Keep the newsletter issue as **one source archive**, not one archive per item.
2. Triage each item:
   - Create atomic pages for durable concepts/entities with reusable evidence.
   - Update existing pages for new datapoints in an existing theme.
   - Leave ads, games, referrals, recs, and low-durable viral color source-only.
3. Archive under `Sources/Newsletter/YYYY-MM-DD - Source Title.md`; preserve random Inbox/capture basename in `original_filename`.
4. Add `## Pages Updated` to the archive with created, updated, and source-only/skipped bullets.
5. Route notes to semantic MOCs. For date/issue-shaped MOC sections, add newest items above older items.
6. Update index/log only after content and MOC edits are done.

## CRLF/frontmatter pitfall
Newsletter captures may have CRLF line endings. After patching source frontmatter or moving the source archive, re-read the first lines and verify:
- opening delimiter is exactly `---`
- closing delimiter is exactly `---`
- no accidental `----`, leaked patch text, or malformed YAML scalar

## Duplicate MOC entry pitfall
When adding a fresh same-note MOC entry above an older entry in the same section, remove/avoid a neighboring duplicate. Keep the freshest hook rather than stacking multiple adjacent bullets for the same note.

## Verification checklist
- Inbox/capture original absent or marked ingested according to policy.
- Normalized source archive exists and has `## Pages Updated`.
- Created note files exist.
- Every touched note has the normalized source wikilink in `sources:`.
- Exact MOC links exist for newly created pages.
- Index page count increased by the number of newly created note pages.
- Index rows exist for new pages and updated rows show the run date.
- Log entry names the source, created pages, updated pages, MOCs touched, and archive path.
- Exact search over touched Notes/MOCs/source for diff markers or patch residue returns zero matches.

## Example routing: Morning Brew `Breaking Out`, 2026-07-23
Created:
- `Saudi Nuclear 123 Agreement Risk`
- `AI Circular Compute Deals`
- `Foldable Smartphone Platform Shift`

Updated:
- `Autonomous AI Cyber Escape Risk`
- `Magnificent Seven AI Capex Test`
- `Economic Indicators`
- `Morning Brew Newsletter Network`
- `Strait of Hormuz Protection Fee`
- `IBM AI Infrastructure Spending Squeeze`
- `Paramount Warner Bros Merger Antitrust Pause`
- `Apple Restrained AI Capital Strategy`

Source-only/skipped:
- sponsor blocks
- Jimothy/raccoon virality
- games/recs/referrals
- one-line generic-drug tariff item except as a macro/risk signal
