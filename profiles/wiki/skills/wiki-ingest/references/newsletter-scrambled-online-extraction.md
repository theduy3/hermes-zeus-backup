# Newsletter scrambled-body online extraction

Use this when a captured newsletter email body says the provider scrambled the email and only includes a "read it online" URL (common with Morning Brew / Tech Brew / Brew Markets plain-text captures).

## Pattern

1. Keep the original email body and metadata as provenance in the eventual `Sources/` archive.
2. Fetch the online issue URL from the body rather than treating the capture as low-content/admin mail.
3. Extract the readable issue content from the HTML page:
   - Prefer the page's `<main>` content when available.
   - Strip `script`, `style`, `noscript`, `svg`, navigation, and footer boilerplate.
   - Preserve issue title, date/deck, authors, market tables, section headings, and durable article items.
4. Ingest item-by-item using the existing substantive-newsletter routing rules:
   - durable AI/technology labor or strategy items -> existing AI/technology notes or new atomic concepts;
   - public-company operating/valuation items -> company/strategy notes and Business/Finance MOCs;
   - market tables/rates/oil/gold/bitcoin/index levels -> `Notes/Economic Indicators.md`;
   - routine ads, recs, referral blocks, and sponsor copy -> source-only.
5. Archive one normalized source under `Sources/<original-inbox-basename>.md` containing:
   - original email metadata/body;
   - `online_url:` copied exactly from the capture;
   - a concise extracted online issue section;
   - `## Pages Updated`.
6. Move the Inbox original out after the archive exists and verify Inbox emptiness, source archive presence, note/MOC/index/log matches, and YAML validity.

## Pitfalls

- Do not create one generic page per newsletter issue when only a few items are durable. The issue archive is the source; durable items become/upsert atomic wiki pages.
- Do not ignore these as low-content admin captures just because the email body itself is sparse; the online URL often contains the substantive issue.
- Do not copy unsubscribe URLs into wiki note bodies except inside the source archive's original-body provenance block.
