# Morning Brew Flagship Newsletter Routing

Use this for plain-body flagship Morning Brew email captures (not scrambled online-only Tech Brew/Brew Markets issues).

## Durable routing pattern
- Treat the issue as one source archive under `Sources/YYYY-MM-DD - <Issue Title>.md` with `original_filename:` preserved.
- Triage item-by-item instead of creating one generic Morning Brew note.
- Create concept/entity pages for durable items, for example:
  - US-China AI/model access disputes -> AI governance/release-control pages and AI/business MOCs.
  - Platform privacy/product-default controversies (for example Meta Muse public Instagram image reuse) -> create/update an AI/privacy concept page and route to `14 Business MOC` plus technology/AI MOCs.
  - Public-company valuation/competition updates (for example Nvidia AI competition, SpaceX post-index-inclusion weakness) -> update the existing company/market thesis note when it already exists; do not create a duplicate daily-company page.
  - Travel or institutional-operations updates that clearly match an existing durable note (for example EU EES biometric airport delays) -> update that note and its semantic MOC rather than creating a generic travel/news recap.
  - Media-consumption patterns with durable business/culture signal -> Culture/Business notes.
  - Commodity, Treasury-yield, oil, crypto, market-table, or market-sentiment signals -> `Economic Indicators` and `15 Finance & Economics MOC`.
  - Crypto treasury/company-financing stress -> existing Bitcoin/crypto/market notes rather than a one-off company blurb when no full company thesis is warranted.
- Update `Morning Brew Newsletter Network` with a short issue-routing paragraph recording which items became pages, which existing pages were refreshed, and which stayed source-only.

## Source-only by default
Leave routine world headline recaps, ads, sponsored sections, games, polls, trivia, referral blocks, generic recommendations, recipes, and entertainment blurbs inside the source archive only unless they connect to an existing durable page. Short consumer-safety/internet-trend PSAs (for example a dangerous toy challenge) can also remain source-only unless they connect to an existing parenting/safety page or establish a durable pattern worth tracking.

## Archive and verification notes
- For a normal writable `Inbox/` markdown capture, it is acceptable to move it into the normalized `Sources/YYYY-MM-DD - <Issue Title>.md` archive, then patch the archive frontmatter and append `## Pages Updated`.
- After patching any note frontmatter, re-read the first lines (or run a small frontmatter sanity check) to catch accidental malformed YAML from patch payload mistakes before finalizing.

## Verification checklist
- Inbox empty.
- Source archive exists with normalized source frontmatter and `## Pages Updated`.
- New/updated Notes link to the normalized source archive.
- Relevant numbered/domain MOCs contain the new pages (not raw source links).
- `wiki-index.md` has rows for created notes and updated dates for touched notes.
- `wiki-log.md` has an ingest entry listing Created/Updated/MOCs touched.
