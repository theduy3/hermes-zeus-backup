# Newsletter routing learnings — 2026-07-10

Use this as an example pattern for scrambled Tech Brew / Brew Markets issues where the email body only contains a read-online URL.

## Tech Brew placeholder recovery + life-ops routing

- If a Tech Brew email contains a placeholder `/issues/tk?...` URL that returns a generic "We couldn't find that page" page, derive the slug from the email H1/title and retry `https://www.techbrew.com/issues/<slug>`.
- Archive both provenance URLs:
  - `raw_online_url:` = exact placeholder URL from the email body.
  - `online_url:` / `canonical_url:` = successful recovered issue URL.
- When a Tech Brew issue contains a practical AI prompt/workflow for household or personal operations, do not leave it source-only just because it is not market/technology news. Create or update a durable productivity/personal-operations concept page, link it from `Personal MOC`, and cross-file in `AI Development MOC` when the durable value is an AI prompt/workflow pattern.
- Example: Tech Brew "Netflix channels its inner cable" contained a "run my life without me" / "just in case file" prompt. It created `Notes/Household Emergency File.md`, updated `Netflix Second Season Viewership Drop`, refreshed the newsletter network note, and touched `Personal MOC`, `AI Development MOC`, and `14 Business MOC`.

## Brew Markets crypto/bank/stablecoin routing

- For Brew Markets issues about stablecoins entering the banking system, prefer updating an existing stablecoin/bank-economics note instead of creating a generic newsletter or company note.
- Circle/OCC/USDC trust-bank material routes well to `Stablecoins Narrow Bank Economics`; add `Economic Indicators` when the source includes bank-liquidity, lending-displacement, rates, oil, Bitcoin, or market-table signals.
- Capture concrete regulatory numbers in the finance note and macro dashboard. In the July 10 example, the durable facts were Circle's OCC trust-bank approval, CLARITY Act yield-loophole concerns, a potential >20% lending reduction, and an $850bn community-bank lending risk.
- When the issue also has AI-semiconductor market items, refresh existing notes such as `SK Hynix AI Memory Listing` and `Memory Chip Trade Reversal` rather than creating duplicate day-specific pages.

## Verification checklist from this run

- Source archives used normalized names: `YYYY-MM-DD - Source Title.md`.
- Raw scrambled email captures were moved out of Inbox to `Sources/<stem>.inbox-original.md` after normalized archives existed.
- `## Pages Updated` in each archive listed created/updated pages and touched MOCs.
- Verified: Inbox empty; source archives and preserved originals present; exact MOC links; exact `wiki-index.md` rows; exact `wiki-log.md` entries; frontmatter delimiters not accidentally changed to `----`.