# Newsletter substantive issue routing

Use this when an email newsletter issue is more than a welcome/admin message and contains multiple short news items, market tables, policy blurbs, and lifestyle/business snippets.

## Pattern from Morning Brew daily issues

1. Archive the newsletter as one source file in `Sources/` with:
   - `tags: [source, newsletter]`
   - `type: article`
   - original email metadata (`mailbox`, `author`, `received`, `message_id`, `body_format`)
   - `created` and `ingested`
   - a `## Pages Updated` section.
2. Triage item-by-item rather than creating a generic "newsletter issue" note:
   - Durable policy/finance/social topics become atomic Notes pages.
   - Market tables, rates, oil, inflation, jobs, sentiment, and other macro signals update `Notes/Economic Indicators.md`.
   - Routine sports, trivia, calendar, recommendations, ads, and list-cleanup blocks remain source-only unless they connect to an existing durable note.
3. Update the feed/network note when the issue teaches the future routing pattern (for Morning Brew: `Notes/Morning Brew Newsletter Network.md`).
4. Route created pages through the topic MOC, not only Business/Finance. For a flagship Morning Brew item about US policy or household behavior, `MOCs/US Politics & Society MOC.md` can be the best primary MOC.
5. Update `wiki-index.md` rows for new pages and any updated feed/macro notes; update `page_count` for new Notes pages.
6. Append one `wiki-log.md` ingest entry naming the source, created pages, updated pages, MOCs touched, and archive path.
7. Verify exact matches for: new note files, source archive, empty Inbox, `## Pages Updated`, MOC links, index rows, and log entry.

## Example mappings

- Morning Brew item on child savings accounts / Trump Accounts -> create `Trump Accounts Child Retirement Savings`; link to `Social Security Trust Fund Depletion Crisis`, `American Household Saving Rate 2026`, `Economic Indicators`, and `US Politics & Society MOC`.
- Morning Brew item on adult children living with parents -> create `Boomerang Kids Housing Affordability`; link to `American Household Saving Rate 2026`, `Asia Filial Piety Laws Spreading`, `Economic Indicators`, and `US Politics & Society MOC`.
- Morning Brew YTD market table + 10-year yield + OPEC/oil-output notes -> update `Economic Indicators`, not a standalone newsletter-market page.
