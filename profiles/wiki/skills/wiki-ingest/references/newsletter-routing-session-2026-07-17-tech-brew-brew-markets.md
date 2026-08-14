# Newsletter routing session — 2026-07-17 Tech Brew + Brew Markets

Use this as a concrete example for scrambled Morning Brew network captures where the email body only contains an online issue URL.

## Inputs

- Tech Brew: `AI's "Great Value" era`, email body contained placeholder-style `https://www.techbrew.com/issues/tk?...`.
- Brew Markets: `SpaceX's failure to launch`, email body contained a concrete online slug `https://www.brewmarkets.com/issues/spacexs-failure-to-launch?...`.

## Extraction pattern

1. Preserve the original email body in the normalized source archive.
2. Fetch the online issue HTML to a temp file first; do not pipe downloaded HTML directly into Python.
3. Parse saved HTML locally, remove `script/style/nav/footer/header/svg/noscript`, then extract `<main>` or `<article>` text.
4. For placeholder `/issues/tk` links, inspect the returned page title and body before deriving a slug. In this session the Tech Brew placeholder URL plus query params returned the full correct issue (`AI's "Great Value" era`), so no slug retry was needed.
5. If the returned body is a generic shell or too-short failure, then derive/retry the canonical slug as documented in the main skill.

## Routing decisions

### Tech Brew — AI's "Great Value" era

Created:
- `Notes/Open Weight AI Price Compression.md`

Updated:
- `AI Model Distillation Geopolitics` — added Kimi K3 / low-cost Chinese open-weight model pricing and distillation-pressure angle.
- `Morning Brew Newsletter Network` — recorded July 17 Tech Brew routing.

MOCs:
- `AI Development MOC`
- `14 Business MOC`
- `16 Science & Technology MOC`

Source archive:
- `Sources/2026-07-17 - AI's Great Value era.md`
- Raw original preserved as `Sources/2026-07-17-1813-newsletter-ai-s-great-value-era.inbox-original.md`.

### Brew Markets — SpaceX's failure to launch

Updated existing pages rather than creating a generic issue note:
- `Economic Indicators` — daily market table, oil/rates, tech rotation, semiconductor bear-market signal.
- `Apple Restrained AI Capital Strategy` — Apple briefly overtook Nvidia; HSBC cited AI spend around 2.5% of sales versus 39% for hyperscalers.
- `Nvidia Valuation Reset 2026` — Kimi K3 / memory-supplier rotation pressure.
- `SpaceX Nasdaq 100 Index Inclusion` — Starship scrub, below-IPO trading, six losing days, short interest.
- `Midwest Cyclospora Produce Outbreak` — restaurant-stock rebound after CDC attribution narrowed to Taco Bell lettuce supplier.
- `Morning Brew Newsletter Network` — recorded July 17 Brew Markets routing.

MOCs:
- `14 Business MOC`
- `15 Finance & Economics MOC`
- `16 Science & Technology MOC`

Source archive:
- `Sources/2026-07-17 - SpaceX's failure to launch.md`
- Raw original preserved as `Sources/2026-07-17-2037-newsletter-spacex-s-failure-to-launch.inbox-original.md`.

## Verification checklist used

- Inbox empty.
- Both normalized source archives present.
- Both raw `.inbox-original.md` files present under `Sources/`.
- `wiki-index.md` rows for created/updated pages reflect current dates.
- `wiki-log.md` has one entry per source.
- Exact MOC searches find new links/hooks.
- YAML frontmatter parses for touched notes, source archives, and index.