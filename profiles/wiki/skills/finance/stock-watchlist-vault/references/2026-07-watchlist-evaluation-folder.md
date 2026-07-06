# Stock watchlist evaluation-folder session notes — 2026-07

## What the user wanted

The user wanted a stock-watchlist folder containing one note per company with:

- company evaluation;
- scenario framing;
- Add / Hold / Reduce suggestion;
- links to every vault note that mentions that company.

Because the wiki profile only writes under approved vault roots, the folder was created at:

`/vault/Notes/Stock Watchlist/`

rather than `/vault/Stock Watchlist/`.

## Durable workflow learned

1. Parse tickers from `/vault/System/Stock Watchlist.md`, using only the `Watchlist:` section.
2. Fetch current quantitative snapshot with `/vault/System/scripts/fetch_watchlist.py --json`.
3. Build/update `/vault/Notes/Stock Watchlist/Stock Watchlist Index.md`.
4. Build/update one note per ticker.
5. Search `/vault/Notes` for ticker/company aliases and add the related-note wikilinks to the company page.
6. Exclude `/vault/Notes/Stock Watchlist/` from the backlink scan to avoid generated notes linking to each other recursively.
7. Add a concise `/vault/System/wiki-log.md` entry.

## Suggested note shape

Each ticker note should have:

- Snapshot table
- Suggestion
- Evaluation
- Scenarios: Base, Bull, Bear
- Decision Rules
- Related Notes Mentioning This Company
- Open Questions
- Related links

## Root-owned shared files pitfall

In this session these were root-owned or unreadable/unwritable:

- `/vault/MOCs/Finance MOC.md`
- `/vault/System/wiki-index.md`

Do not block the main note-generation task when this happens. Report the chown command:

```bash
sudo chown hermes:hermes "/vault/MOCs/Finance MOC.md" /vault/System/wiki-index.md
```

## Daily investment rotation learned earlier in same session

For weekly coverage of a growing watchlist, use weekday buckets:

- preserve Watchlist order;
- selected bucket = `index % 7 == weekday`, with Monday=0 ... Sunday=6 in America/Vancouver;
- insert section `## Watchlist Company Updates (Last 30 Days)` after Stock Watchlist and before Morning Brew;
- include a rotation line like `*Rotation: 6/43 tickers for Thursday; source: System/Stock Watchlist.md*`.
