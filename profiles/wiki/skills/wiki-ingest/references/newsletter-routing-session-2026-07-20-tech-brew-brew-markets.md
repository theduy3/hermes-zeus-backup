# Newsletter routing session — 2026-07-20 Tech Brew + Brew Markets

Use this as a precedent for scrambled Morning Brew network captures where the email body only contains a read-online URL.

## Sources processed

- Tech Brew: `Typecast by an algorithm` (`/issues/tk1?...` placeholder returned a generic shell; derived and fetched canonical slug `https://www.techbrew.com/issues/typecast-by-an-algorithm`).
- Brew Markets: `AMC's box-office odyssey` (`https://www.brewmarkets.com/issues/amc-finds-the-magic?...` returned the full issue directly; canonicalized to `/issues/amc-finds-the-magic`).
- Vietnamese Telegram reflection: AI project workflow using Antigravity + multiple model review.

## Routing decisions

### Tech Brew — Typecast by an algorithm

Created durable notes:
- `AI Hiring Bias Amplification` — Princeton/University of Chicago hiring simulation; LLMs scored 65% higher than humans on job segregation; connects to workplace AI governance and `AI Employee Accountability Gap`.
- `AI Advice Overconfidence Effect` — World Cup AI prediction vs goldfish baseline and study where AI advice made users three times less accurate but more confident; connects to forecasting/calibration and `Macro Trading Difficulty`.
- `AWS Billing Glitch Risk` — AWS estimated-cost display bug, including $1.5trn/$2.3trn forecast anecdotes; route as cloud/FinOps operational risk, not only AI/news trivia.

Updated:
- `Morning Brew Newsletter Network`
- `AI Development MOC`
- `14 Business MOC`

Source-only:
- AI phones, Altman/author anecdote, AI note-taking etiquette, possible Chinese AI model bans, Kalshi/Polymarket founder conflict, Apple Genius Bar summaries.

### Brew Markets — AMC's box-office odyssey

Created durable notes:
- `AMC Theater Recovery Valuation` — record $1.6bn revenue, $320.6m adjusted EBITDA, attendance up 12% US / 18% international, but debt/dilution and -99.43% five-year stock context keep it high-risk.
- `Weather Driven Inflation Risk` — El Niño macro channel: crop yields -5% to -12%, rice -2% to -8%, ag commodities +7% month, possible double-digit food inflation by 2027, hydropower/cooling/subsidy second-order effects.

Updated:
- `Economic Indicators` — market table, oil/gasoline, tariffs, El Niño inflation, Korea margin calls.
- `Theatrical Event Cinema Revival` — AMC as exhibitor-side P&L evidence for event-cinema recovery.
- `China Korea AI Equity Rotation` — 1.2m Korean margin calls, 320k-360k full liquidations, Qwen 3.8 Max / Kimi K3 pressure.
- `Anchovy Fishmeal Supply Shock` — broadened into weather-driven food-inflation channel.
- `Morning Brew Newsletter Network`, `14 Business MOC`, `15 Finance & Economics MOC`, `17 Culture MOC`, `AI Development MOC`.

Watchlist candidate surfaced, not added:
- `AMC` — improving theater recovery and EBITDA, but debt/dilution make it high-risk.

Source-only:
- JetBlue slots, Archer/Anduril, Hut 8 lease, StoneX downgrade, Tempus acquisition, Paramount-Warner legal pause, China car market, Jersey Mike's IPO, DOJ white-collar crime posture unless later connected to existing notes.

### Vietnamese AI project workflow reflection

Updated existing `AI Vibe Coding Workflow Vietnamese` rather than creating a duplicate. Durable pattern: context-first `.claude/CLAUDE.md`, human doc review, research-before-code, task/module plan, agent execution, module-level QA, progress reports, iterative testing, independent GPT review, second Claude cross-review, synthesis/fix roadmap, final remediation, GitHub/CI/CD, VPS deploy. Route through `AI Development MOC`.

## Operational lessons

- For Tech Brew placeholders, if `/issues/tk...` or `/issues/tk1...` returns a generic shell (`Tech Brew` title plus “We couldn't find that page”), derive the slug from the email H1/title before downgrading to source-only.
- For Brew Markets, specific issue slugs often work directly; still store both raw `online_url` with tracking and normalized `canonical_url`.
- Preserve raw Inbox originals alongside normalized newsletter archives in `Sources/Newsletter/*.inbox-original.md` after the normalized archive is written and verified.
- Short market-mover blocks can justify refreshing existing dashboards (`Economic Indicators`, market/sector notes) without creating one note per stock mover.
