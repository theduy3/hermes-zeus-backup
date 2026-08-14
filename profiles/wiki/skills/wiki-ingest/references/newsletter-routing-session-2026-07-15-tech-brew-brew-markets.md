# Newsletter routing session — 2026-07-15 Tech Brew + Brew Markets

Use this as a compact precedent for scrambled-body newsletter captures where the email body only contains an online issue link.

## Sources processed

- Tech Brew: `# OpenAI's Her era`, email URL was placeholder `/issues/tk?...`; the placeholder fetched a generic `Tech Brew` shell, so derive the canonical slug from the title: `https://www.techbrew.com/issues/openais-her-era?...`.
- Brew Markets: `# 🍻 PayPal hits paydirt`, canonical URL worked directly: `https://www.brewmarkets.com/issues/paypal-lucid-retirement-savings?...`.

## Routing decisions

### Tech Brew — OpenAI's Her era

Create/update:
- Created `OpenAI Companion Hardware Backlash` — screenless/personality-driven OpenAI companion hardware, loneliness-tech demand, companion-AI lawsuits, minor-safety regulation, China emotional-attachment rules, and Apple trade-secret context.
- Updated `Apple OpenAI Trade Secrets Lawsuit` — the device makes the Apple/OpenAI hardware dispute strategically larger than recruiting; contested know-how sits next to a consumer-device monetization plan.
- Updated `AI Employee Accountability Gap` — short item about a lawsuit alleging Meta used AI in layoffs that disproportionately hit medical/parental-leave workers belongs as a workforce-governance pitfall, not a standalone note.
- Updated `Morning Brew Newsletter Network`.

MOCs:
- `16 Science & Technology MOC` for OpenAI companion hardware.
- `14 Business MOC` for consumer-hardware monetization / business-model angle.

Source-only:
- Humanoid pig gallbladder surgery, reusable rocket test, Parkinson's dopamine-cell transplant, bread-slice social account, Boston Dynamics package-delivery dogs, Kalshi odds, OpenAI model deleting files, xAI codebase-upload allegation, and PS6 digital-only availability were too short for new atomic pages in this pass unless future sources deepen them.

### Brew Markets — PayPal hits paydirt

Create/update:
- Created `PayPal Stripe Takeover Bid` — $53bn Advent/Stripe offer, $60.50/share, 28% premium, PayPal/Venmo payment volume/accounts, Stripe consumer-market ambition, Michael Burry valuation comment, payments-consolidation angle.
- Created `Lucid Liquidity Whiplash` — rumor-driven EV volatility, 40% intraday plunge / 16% close decline / 28.79% rebound, subsidy removal, layoffs, cash burn, liquidity runway.
- Created `Retirement Readiness Gap` — Schroders survey: $1.2m perceived retirement need, only 30% expect $1m, 55% cannot save 10%, 27% cut contributions/borrowed, K-shaped wealth-effect framing.
- Updated `Economic Indicators` — market table, softer PPI/Fed commentary, PayPal consolidation, Lucid liquidity, retirement-savings stress.
- Updated `Morning Brew Newsletter Network`.

MOCs:
- `15 Finance & Economics MOC` for PayPal, Lucid, Retirement Readiness Gap, Economic Indicators.
- `14 Business MOC` for public-company/consumer-payments/EV business context.

Watchlist candidate surfacing:
- PYPL was not in `System/Stock Watchlist.md`; final summary should list it as a watchlist candidate, not add it autonomously.

## Operational pitfalls verified

- `search_files(target="files")` uses glob semantics, not alternation; verify multiple exact paths with separate probes or `ls -la` rather than a `fileA|fileB` pattern.
- Preserve raw scrambled Inbox originals as `Sources/<timestamp-slug>.inbox-original.md` after normalized archives are written and verified.
- For source archive frontmatter, keep both `online_url:` (raw email URL) and `canonical_url:` (successful issue URL) when the placeholder had to be normalized.
