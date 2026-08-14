# July 16 2026 scrambled newsletter ingest pattern

Session pattern for two plain-text Morning Brew network captures whose bodies only said the email was scrambled and linked to an online issue.

## What worked

1. Preserve the raw email capture as the source of provenance, but fetch/extract the online issue before deciding routing.
2. For Tech Brew placeholder links like `https://www.techbrew.com/issues/tk?...`, a direct fetch can return a generic “We couldn't find that page” shell. Derive the canonical slug from the email H1 (`xAI sues one of its users` → `https://www.techbrew.com/issues/xai-sues-one-of-its-users`) and retry.
3. For Brew Markets, a specific issue URL (`/issues/merck-eli-lilly-consumer-international-ai?...`) fetched cleanly; preserve both raw tracking URL as `online_url:` and clean URL as `canonical_url:`.
4. Extract `<main>` text after removing script/style/nav/footer/header/svg boilerplate. Keep market tables and article sections; leave sponsor/recs/fashion/footer material source-only unless it updates an existing durable page.
5. Create normalized source archives named `YYYY-MM-DD - Source Title.md` containing:
   - source/newsletter frontmatter
   - `online_url:` raw email URL
   - `canonical_url:` fetched URL
   - original email capture fenced under `## Original Email Capture`
   - cleaned online text under `## Online Issue Extract`
   - `## Pages Updated`
6. After the normalized archive exists, move the raw Inbox capture to `Sources/<original-stem>.inbox-original.md` and verify Inbox emptiness plus both archive files.

## Routing examples from this session

- Tech Brew “xAI sues one of its users”: create `xAI Grok Abuse Liability Lawsuit` and `Siri AI Phone Agent Review`; update `Morning Brew Newsletter Network`; route to `AI Development MOC` and `14 Business MOC`.
- Brew Markets “The checkout crunch”: create `Pharma Patent Cliff Pipeline Race`, `Consumer Grocery Affordability Stress`, and `Global AI Localization Race`; update `Economic Indicators`, `Stablecoins Narrow Bank Economics`, and `Morning Brew Newsletter Network`; route to `15 Finance & Economics MOC`, `14 Business MOC`, and `AI Development MOC`.

## Watchlist reminder

For Brew Markets items involving clear investable public-company theses, read `System/Stock Watchlist.md` but do not edit it. Surface candidates in the final summary when absent from the watchlist. This session surfaced MRK, LLY, and V for review.