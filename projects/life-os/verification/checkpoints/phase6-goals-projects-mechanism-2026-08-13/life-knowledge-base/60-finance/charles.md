# Charles — investment operating layer

Charles manages investment context: theses, risk rules, positions, decisions, and watch items. It operates **under Finance** — it references the liquidity/cash-flow facts in `finance_summary.md` and never overwrites them.

## Dependency
- Finance is the authority for cash/liquidity. Charles decisions must respect the $10k liquid buffer goal and current cash flow (`finance_summary.md`).
- Charles cannot assert liquidity facts; it links them.

## Source evidence (theduyvault, read-only references)
These are raw watchlist/briefing snapshots, NOT migrated claims. They inform theses but are not positions.
- `Daily/2026-08-12-investment.md` — watchlist: MSFT/AAPL/GOOG/META/AMZN (mega-cap), DELL/ORCL/CRM/PLTR/CRWB (AI infra), indices VIX/GSPC/RUT, BTC, gold.
- `Daily/2026-08-11-investment.md`, `2026-08-10-investment.md`, `2026-08-09-investment.md` — preceding briefings.
- Vault `Notes/` investment research (e.g. Aschenbrunner AI Power thesis, Carson Block crash thesis) — reference only.

## Current investment state
- No positions, theses, risk rules, or decisions recorded in Life OS yet.
- Awaiting user-supplied real investment data (forward-only capture via `tracker/charles_log.py`).

## Capture
`python3 tracker/charles_log.py --date YYYY-MM-DD --kind <thesis|position|risk_rule|decision|watch> ...`
