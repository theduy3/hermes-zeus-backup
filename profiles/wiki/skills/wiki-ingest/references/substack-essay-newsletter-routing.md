# Substack / Essay Newsletter Routing

Use this when a newsletter capture is a substantive essay issue (for example a Vietnamese Substack like Đọc Chậm), not a short admin/welcome email and not a Morning Brew-style itemized news digest.

## Trigger
- Inbox markdown has `type: newsletter` or email metadata and a long essay body.
- The issue has one or more durable essays plus a short reading-list / links section.
- Online URL may be present, but the email body already contains enough source text to ingest.

## Routing pattern
1. Archive as one normalized source under `Sources/YYYY-MM-DD - Source Title.md` with:
   - `tags: [source, newsletter, <topic tags>]`
   - `type: article`
   - `source: email`
   - `online_url:` copied exactly when present
   - `original_filename:` when the Inbox filename was random/truncated.
2. Create a small cluster of durable atomic notes from the essay's main arguments rather than one monolithic newsletter page.
   - For urban/economic-development essays, create/update concept pages for the main mechanisms (e.g. knowledge flows, talent policy, institutional bottlenecks).
   - For short reading-list items, create a note only if the item adds a durable thesis; otherwise update an existing finance/AI/macro note or leave source-only.
3. Route the notes to semantic MOCs, not a generic newsletter MOC only:
   - regional policy/economic development -> numbered regional MOC (e.g. `09 Asia MOC`) and `14 Business MOC` when it concerns business hubs or growth models;
   - financing / market-risk snippets -> `15 Finance & Economics MOC`;
   - AI financing / labor snippets -> existing AI/finance pages before creating a new page.
4. Update existing pages when a short item is clearly an addendum. Example: an AI borrowing / bond-market caution should update `AI as Investment Megatrend Framing` and may create a small focused note like `AI Debt Market Discipline` only when it provides a reusable concept.
5. Add `## Pages Updated` to the source archive and verify exact note/MOC/index/log matches.
6. Preserve the raw Inbox capture as `Sources/<stem>.inbox-original.md` when moving it out of Inbox is the safer/current hygiene pattern; do not place raw originals under `Notes/`.

## Pitfalls
- Do not treat non-Morning-Brew newsletter issues as admin/welcome emails just because they come from a newsletter inbox.
- Do not over-create pages for every recommended link in a reading list when the body only gives a one-line teaser.
- Preserve Vietnamese titles and author metadata in the source archive, but use durable English concept titles for wiki pages when that keeps the graph navigable.
