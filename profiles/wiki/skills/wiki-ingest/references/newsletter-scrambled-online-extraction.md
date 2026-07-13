# Newsletter scrambled-body online extraction

Use this when a captured newsletter email body says the provider scrambled the email and only includes a "read it online" URL (common with Morning Brew / Tech Brew / Brew Markets plain-text captures).

## Pattern

1. Keep the original email body and metadata as provenance in the eventual `Sources/` archive.
2. Fetch the online issue URL from the body rather than treating the capture as low-content/admin mail.
3. If the supplied online URL returns 404 or is an opaque placeholder path, recover before giving up:
   - derive a slug from the email H1/title: remove emoji, lowercase, remove most punctuation, turn possessive apostrophe-s into `s`, collapse whitespace to hyphens;
   - retry the likely canonical host from the sender, e.g. `https://www.techbrew.com/issues/<slug>` or `https://www.brewmarkets.com/issues/<slug>`;
   - keep the failed/raw URL in the archived original-body block, and store the successful URL as `online_url:` (plus `canonical_url:` when different).
4. Extract the readable issue content from the HTML page:
   - Prefer the page's `<main>` content when available.
   - Strip `script`, `style`, `noscript`, `svg`, navigation, and footer boilerplate.
   - Preserve issue title, date/deck, authors, market tables, section headings, and durable article items.
5. Ingest item-by-item using the existing substantive-newsletter routing rules:
   - durable AI/technology labor or strategy items -> existing AI/technology notes or new atomic concepts;
   - public-company operating/valuation items -> company/strategy notes and Business/Finance MOCs;
   - market tables/rates/oil/gold/bitcoin/index levels -> `Notes/Economic Indicators.md`;
   - routine ads, recs, referral blocks, and sponsor copy -> source-only.
6. Archive one normalized source under `Sources/YYYY-MM-DD - Source Title.md` containing:
   - original email metadata/body;
   - `original_filename:` for the Inbox basename;
   - `online_url:`/`canonical_url:` copied exactly from the successful extraction;
   - a concise extracted online issue section;
   - `## Pages Updated`.
7. Move/preserve the Inbox original out of `Inbox/` only after the normalized source archive exists. Prefer `Sources/<stem>.inbox-original.md` when preserving raw originals so raw captures do not pollute `Notes/`.
8. Verify Inbox emptiness, source archive presence, preserved-original presence (if used), note/MOC/index/log matches, and YAML validity.

## Example recovery

A Tech Brew capture titled `Reddit's AI Ouroboros problem` contained `https://www.techbrew.com/issues/tk?...`, which returned 404. Deriving the slug `reddits-ai-ouroboros-problem` and retrying `https://www.techbrew.com/issues/reddits-ai-ouroboros-problem` recovered the full issue.

## Pitfalls

- Do not create one generic page per newsletter issue when only a few items are durable. The issue archive is the source; durable items become/upsert atomic wiki pages.
- Do not ignore these as low-content admin captures just because the email body itself is sparse; the online URL often contains the substantive issue.
- Do not copy unsubscribe URLs into wiki note bodies except inside the source archive's original-body provenance block.
- Do not stop after the first failed online URL when the email title gives enough information to reconstruct the canonical issue URL.
