# Newsletter routing session — 2026-07-13

Use this as a concrete example for scrambled Morning Brew network captures that require online extraction and item-by-item routing.

## Inputs

- Tech Brew email capture: `Apple bites back at OpenAI` with placeholder online URL `/issues/tk?...`.
- Brew Markets email capture: `Apple's winning its AI bet` with usable online URL `/issues/apples-winning-its-ai-bet?...`.

## Extraction pattern

1. Preserve the original plain-text email body in the normalized `Sources/YYYY-MM-DD - Source Title.md` archive.
2. If the online URL is a placeholder like `/issues/tk`, derive the likely slug from the email H1/title (`apple-bites-back-at-openai`) and retry the canonical host URL.
3. Store both provenance fields in source frontmatter when applicable:
   - `failed_url:` for the placeholder/failed URL from the email body.
   - `online_url:` for the successfully extracted canonical issue URL.
4. Write the normalized archive first, then move the raw Inbox capture to `Sources/<original-stem>.inbox-original.md` when preserving the original capture separately.

## Routing example

### Tech Brew — Apple bites back at OpenAI

Do not create a duplicate if the flagship Morning Brew issue already created the core note. Refresh the existing note instead:

- Updated: `Apple OpenAI Trade Secrets Lawsuit`
  - Add extra allegations from the Tech Brew issue: hardware-part interviews, offboarding-control evasion, Apple supplier metal-finishing access.
- Updated: `Morning Brew Newsletter Network`
  - Record that Tech Brew required online extraction from a placeholder `/issues/tk` link.
- MOCs: `14 Business MOC`, `AI Development MOC`.

### Brew Markets — Apple's winning its AI bet

Create a small cluster rather than one monolithic note:

- Created: `Apple Restrained AI Capital Strategy` — Apple rewarded for muted AI capex, strong free cash flow, foldable-iPhone cycle.
- Created: `Meta AI Capex Valuation Risk` — Meta Louisiana AI campus budget rising to $50bn and high annual AI spend.
- Created: `Agriculture Stocks Anti AI Rotation` — AGCO/Deere as depressed-cycle non-AI rotation ideas.
- Created: `Citigroup Turnaround Earnings Catalyst` — Citi as low-expectation bank turnaround into earnings.
- Updated: `Apple OpenAI Trade Secrets Lawsuit`, `AI Infrastructure Bond Binge`, `Memory Chip Trade Reversal`, `Texas Rise as Corporate Business Hub`, `AI as Investment Megatrend Framing`, `Economic Indicators`, `Morning Brew Newsletter Network`.
- MOCs: `15 Finance & Economics MOC`, `14 Business MOC`, `AI Development MOC`.

## Watchlist surfacing

For Brew Markets public-company/investable mentions, read `System/Stock Watchlist.md` but do not edit it. If tickers are not present and the source gives a clear thesis, list them in the final summary only:

- `AGCO` — agriculture-equipment cyclical rebound thesis.
- `DE` — Deere agriculture-equipment rebound thesis.
- `C` — Citigroup turnaround/earnings catalyst.

## Verification checklist

- Inbox empty.
- Normalized source archives exist under `Sources/`.
- Raw originals preserved under `Sources/*.inbox-original.md` when moved separately.
- New/updated Notes have valid YAML and `sources:` links to the normalized source archives.
- `wiki-index.md` has new rows and updated dates for touched existing rows.
- `wiki-log.md` has one entry per processed source.
- Relevant MOC exact searches find the new page links.
