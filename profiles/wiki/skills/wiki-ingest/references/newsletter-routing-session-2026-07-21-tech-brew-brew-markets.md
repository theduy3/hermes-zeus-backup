# Newsletter routing session — 2026-07-21 Tech Brew + Brew Markets

Use this as a compact worked example for scrambled Morning Brew-family newsletter captures.

## Sources

- Tech Brew: `# Ice, ice, Gemini`; scrambled plain-text email only exposed `https://www.techbrew.com/issues/tk?...`.
- Brew Markets: `# 🍻 Everyone is selling`; scrambled email exposed `https://www.brewmarkets.com/issues/novo-lilly-spacex-wall-street-selling?...`.

## Extraction pattern

1. Preserve the raw email capture in `Sources/Newsletter/<normalized>.inbox-original.md` after the normalized source archive exists.
2. Try the raw online URL first.
3. If a Tech Brew placeholder `/issues/tk?...` returns 404 or a generic shell, derive a canonical slug from the email H1:
   - `Ice, ice, Gemini` → `ice-ice-gemini`
   - canonical URL: `https://www.techbrew.com/issues/ice-ice-gemini`
4. Fetch HTML to a temporary file, parse locally, and extract `<main>` text after removing script/style/nav/footer/header/noise. Do not pipe remote HTML directly into Python in headless cron.
5. Keep unsubscribe/referral/sponsor boilerplate source-only unless it establishes a durable routing or operational lesson.

## Routing decisions from this run

### Tech Brew — Ice, ice, Gemini

Created:
- `Model Specific AI Silicon` — Google/Frozen v2, Gemini-specific silicon, 6x-10x claimed inference-efficiency angle, custom-chip race with OpenAI/Broadcom and Anthropic/Samsung.
- `Gmail Advanced Protection Program` — practical account-hardening note; route through Personal MOC rather than finance/business.
- `Prediction Markets as Social Entertainment` — wedding prop-bets as prediction-market mechanics leaking into social rituals; route through Finance & Economics because it extends the World Cup/Kalshi participation pattern.

Updated:
- `Economic Indicators` — Alphabet/custom-chip stock-support signal.
- `Morning Brew Newsletter Network` — record scrambled-link handling and issue routing.

MOCs touched:
- `16 Science & Technology MOC`
- `AI Development MOC`
- `15 Finance & Economics MOC`
- `Personal MOC`

### Brew Markets — Everyone Is Selling

Created:
- `GLP-1 Obesity Drug Rivalry` — Novo/Lilly ad lawsuit, oral GLP-1 data, $100bn-by-2030 market, tickers `[LLY, NVO]`.
- `AI Equity Supply Overhang` — hedge-fund tech selling, insider selling, equity/equity-linked issuance as an AI-trade supply warning.

Updated:
- `SpaceX Nasdaq 100 Index Inclusion` — earnings/lock-up/insider-share release and short-interest overhang.
- `Pharma Patent Cliff Pipeline Race` — connect GLP-1 rivalry to Lilly capital allocation and pharma competitive moat.
- `Economic Indicators` — market table, rates, oil, Canada tariffs, pharma/public-equity signals.
- `Morning Brew Newsletter Network`.

MOCs touched:
- `14 Business MOC`
- `15 Finance & Economics MOC`

Watchlist candidates surfaced, not added:
- LLY — investor-favored side of GLP-1 rivalry despite Novo's oral-pill efficacy claim.
- NVO — oral Wegovy efficacy lead, but fighting Lilly through ad litigation and corrective-ad demands.

## Verification checklist used

- Inbox empty.
- Normalized archives and `.inbox-original.md` files present under `Sources/Newsletter/`.
- New Notes exist and parse as YAML.
- `wiki-index.md` has rows for all new notes and updated rows for touched notes.
- Relevant MOCs have exact wikilinks to new notes.
- `wiki-log.md` has one ingest entry per newsletter source.
- If an index insertion accidentally removes or mutates a neighboring row, repair the neighbor immediately and verify both new and preserved rows by exact search.