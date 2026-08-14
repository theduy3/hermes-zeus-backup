# Newsletter Routing Session — 2026-07-18 Morning Brew Flagship

Use this as a concrete routing example for a broad flagship Morning Brew issue where the durable signal is concentrated in AI model economics, market rotation, food safety, geopolitics/oil, and public-company capacity monetization.

## Source
- Inbox capture: `2026-07-18-0941-newsletter-catching-up.md`
- Normalized archive: `Sources/2026-07-18 - Catching Up.md`
- Issue title: `☕️ Catching up`
- Source type: Morning Brew flagship newsletter, plain email body.

## Routing decisions
- Created `Notes/Kimi K3 AI Price Shock.md` as a durable AI/model-economics concept page.
  - Why it warranted its own page: Moonshot's Kimi K3 combined claimed near-frontier benchmark performance, 2.8T parameters, lower token pricing ($15/million output tokens vs $30 GPT-5.6 Sol and $50 Claude Fable 5), coding/agentic-task implications, and market/geopolitical impact.
- Updated existing AI/model pages instead of duplicating them:
  - `AI Model Distillation Geopolitics` — Kimi/DeepSeek/Alibaba allegations and Xi messaging.
  - `Open Weight AI Price Compression` — concrete Kimi enterprise pricing numbers.
  - `Nvidia Valuation Reset 2026` — Kimi-driven semiconductor weakness and Apple-vs-Nvidia market-cap rotation.
  - `Apple Restrained AI Capital Strategy` — Apple briefly overtaking Nvidia as low-capex AI posture got market confirmation.
  - `Meta AI Capex Valuation Risk` — possible $10B Anthropic excess-compute sale as AI-capacity monetization signal.
- Updated non-AI existing pages rather than creating headline-only notes:
  - `Midwest Cyclospora Produce Outbreak` — Taylor Farms recall of central-Mexico iceberg lettuce after CDC/FDA links to Taco Bell supplied shredded lettuce.
  - `SpaceX Nasdaq 100 Index Inclusion` — reported $1T market-value drawdown and ~$4B short-seller profit.
  - `Strait of Hormuz Protection Fee` — physical US-Iran/oil/Strait-crossing risk after earlier toll reversal.
  - `Andy Burnham Economic Challenges Prime Minister` — pro-business/decentralization/public-ownership posture as incoming PM.
  - `Economic Indicators` — market table and oil/geopolitical/chip-rotation signals.
  - `Morning Brew Newsletter Network` — issue-level routing summary and source triage record.

## MOCs touched
- `AI Development MOC`
- `14 Business MOC`
- `15 Finance & Economics MOC`
- `13 Britain MOC`
- `16 Science & Technology MOC`

## Watchlist handling
- Read `System/Stock Watchlist.md` before finalizing public-company implications.
- Existing watchlist tickers included `AAPL`, `META`, and `NVDA`; added `tickers: [AAPL]` to Apple note and `tickers: [META]` to Meta note.
- Did not edit `System/Stock Watchlist.md`.
- No new watchlist candidates surfaced from this issue.

## Pitfall reinforced: CRLF frontmatter delimiter repair
Email captures can have CRLF line endings. When patching normalized source frontmatter, a replacement that appears to set `---` can leave `----` because CRLF delimiters and patch context interact badly. After patching any newsletter/email source archive:
1. Re-read the first 20 lines of the source archive.
2. Verify line 1 and the closing YAML delimiter are exactly `---`.
3. If they are `----`, repair both delimiters immediately with a narrow replacement.
4. Search for `^----$` in the touched source before finalizing.

## Verification checklist used
- Inbox empty.
- Source archive exists at normalized `Sources/YYYY-MM-DD - Source Title.md` path.
- Source frontmatter begins/ends with exact `---` and includes `original_filename`.
- `## Pages Updated` exists in the source archive.
- New/updated notes include `[[2026-07-18 - Catching Up]]` in sources.
- `wiki-index.md` has exact rows for created and updated pages with date `2026-07-18`.
- `wiki-log.md` has exact `## [2026-07-18] ingest | Catching Up` entry.
- MOC exact searches find the created page and updated routing links.
