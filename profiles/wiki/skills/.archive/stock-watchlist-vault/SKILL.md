---
name: stock-watchlist-vault
description: "Maintain theduyvault's stock watchlist knowledge layer: ticker config, daily investment rotation, company evaluation pages, scenario notes, and links to related vault notes."
version: 1.0.0
metadata:
  hermes:
    tags: [vault, obsidian, finance, stocks, watchlist, investment]
    requires_toolsets: [terminal, file, web]
---

# Stock Watchlist Vault Workflow

Use this skill when the user asks to manage, generate, audit, or enrich the stock watchlist, daily investment briefing, ticker pages, company evaluations, Add/Hold/Reduce labels, or links from watchlist companies to existing vault notes.

## Core vault paths

- Watchlist config: `/vault/System/Stock Watchlist.md`
- Daily investment files: `/vault/Daily/YYYY-MM-DD-investment.md`
- Company evaluation folder: `/vault/Notes/Stock Watchlist/`
- Index page: `/vault/Notes/Stock Watchlist/Stock Watchlist Index.md`
- Finance MOC, if writable: `/vault/MOCs/Finance MOC.md`
- Wiki log: `/vault/System/wiki-log.md`

Respect the wiki profile rule: write only under allowed vault roots. If the user says "from the root" but asks for durable wiki notes, prefer `/vault/Notes/Stock Watchlist/` unless they explicitly override the vault rules.

## Watchlist config parsing

`/vault/System/Stock Watchlist.md` has two sections:

- `Indicators:` — market indicators; do not create company evaluation pages for these.
- `Watchlist:` — tickers/instruments to evaluate; preserve this order.

Parse only bullet lines under `Watchlist:`.

## Daily investment company-update rotation

For recurring daily investment enrichment:

1. Parse all Watchlist tickers, preserving order.
2. Divide across 7 balanced weekday buckets using zero-based `index % 7`.
3. Select the bucket using America/Vancouver local weekday: Monday=0 ... Sunday=6.
4. Insert or replace exactly one section in the daily investment file:
   `## Watchlist Company Updates (Last 30 Days)`
5. Place it after `## Stock Watchlist` and before `## Morning Brew`.
6. Include rotation metadata: `*Rotation: N/TOTAL tickers for WEEKDAY; source: System/Stock Watchlist.md*`.
7. Use last-30-days research with source links; never invent facts if search fails.

## Company evaluation folder workflow

When generating `/vault/Notes/Stock Watchlist/`:

1. Fetch current watchlist snapshot via `/vault/System/scripts/fetch_watchlist.py --json` when available.
2. Create/update one page per Watchlist ticker plus `Stock Watchlist Index.md`.
3. Each company page should include:
   - frontmatter: `type: entity`, `tags: finance/watchlist/stocks`, `ticker`, `suggestion`, `sources`, `wiki_status: draft`;
   - current snapshot table: price, change, 52W range, forward P/E, market cap, analyst target, implied upside;
   - Add/Hold/Reduce-style suggestion;
   - evaluation bullets;
   - Base/Bull/Bear scenarios;
   - decision rules;
   - all detected existing `/vault/Notes` wikilinks that mention the company, ticker, or known aliases;
   - related links: `[[Stock Watchlist Index]]`, `[[Finance MOC]]`, `[[Stock Trading Masterplan]]`, `[[Stock Market Trading Rules]]`.
4. The index should summarize ticker, company/instrument, suggestion, count of linked notes, and page wikilink.
5. Add a concise `/vault/System/wiki-log.md` entry.

Use `scripts/generate_watchlist_notes.py` as a reusable generator/starter when available.

## Suggestion labels

Automated suggestions are triage labels, not final investment advice. Use conservative wording:

- `Add on weakness`
- `Hold / Opportunistic add`
- `Hold`
- `Hold / Research further`
- `Reduce / Avoid adding`
- `Reduce / Wait for pullback`
- `Hold / Watch` for missing data

Always include a caveat in the page body that this is a working note and should be manually reviewed.

## Linking existing notes

Search `/vault/Notes` for each ticker and aliases. For ambiguous short tickers, rely more on company aliases than ticker alone. Record note wikilinks with mention counts. Exclude the generated `/vault/Notes/Stock Watchlist/` folder from the scan to avoid self-reinforcing links.

## Ownership pitfalls

Some shared files may be root-owned in this runtime. If a MOC or wiki-index is unreadable/unwritable, do not block the whole task. Create/update the company pages and report the exact ownership fix, e.g.:

```bash
sudo chown hermes:hermes "/vault/MOCs/Finance MOC.md" /vault/System/wiki-index.md
```

## Support files

- `scripts/generate_watchlist_notes.py` — reusable starter script for generating the company evaluation folder.
- `references/2026-07-watchlist-evaluation-folder.md` — notes from the session that established this workflow.
