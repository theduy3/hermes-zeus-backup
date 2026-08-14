# Newsletter routing session — 2026-07-22 Morning Brew flagship

Use this as a routing example for broad flagship Morning Brew issues with market tables, regional affordability stories, sports/media consolidation, consumer-IP earnings, healthcare litigation, and IPO rotation.

## Source
- Inbox capture: `2026-07-22-0953-newsletter-the-heat-is-on.md`
- Normalized source archive: `Sources/Newsletter/2026-07-22 - The Heat Is On.md`
- Title: `☕ The heat is on`

## Durable routing decisions

### Create atomic pages when a short item has reusable mechanism + concrete data
Created pages:
- `Miami Cost of Living Shock` — route through `06 US Politics & Society MOC` and `15 Finance & Economics MOC`. Durable mechanism: migration + no-income-tax narrative colliding with insurance, property tax, wage, restaurant-cost, and condo-safety cost inflation. Key facts: Miami consumer prices +36% since 2019; home prices +79% since pandemic; property taxes +62%; total housing cost 5% above greater New York; average restaurant check $94 vs $79 in NYC.
- `ESPN NFL Network Talent Consolidation` — route through `14 Business MOC`. Durable mechanism: sports-rights/equity deals becoming operating-model consolidation and talent cuts. Key facts: NFL took 10% ESPN stake in a $3bn deal; ESPN acquired NFL Network and NFL Red Zone; Ryan Clark/Karl Ravech/Cam Newton among cuts; Disney also cut Pixar/NatGeo jobs after earlier marketing cuts.
- `Magic The Gathering IP Growth Engine` — route through `14 Business MOC`; surface HAS as watchlist candidate, do not edit watchlist. Durable mechanism: live-content release cadence + external licensed IP can make a legacy toy/game property a compounding revenue engine but risks player fatigue. Key facts: Magic Q2 revenue $545.3m, +32%; first $500m+ quarter; first $1bn annual-sales Hasbro brand; Marvel set drove records; 50m+ lifetime players; Star Trek set scheduled; Hasbro cutting video-game spend by at least 25% annually.
- `Biotech IPO Outperformance 2026` — route through `14 Business MOC` and `15 Finance & Economics MOC`. Durable mechanism: healthcare listings can counter-rotate against crowded AI issuance. Key facts: 2026 biotech/pharma IPOs +55% average vs all IPOs +4.4% and ten biggest IPOs -6%; Veradermics +500%; Hemab Therapeutics +100% after $350m IPO; helped by looser regulation, breakthroughs, and Big Pharma acquisition demand.

### Update existing pages instead of creating duplicates
Updated pages:
- `Economic Indicators` — add market table and macro/finance signals. July 22 close: Nasdaq 25,837.21 (+1.29%), S&P 7,509.2 (+0.89%), Dow 52,224.64 (+0.74%), 10-year 4.628% (+3 bps), Bitcoin $66,356.47 (+1.57%), GM $79.52 (+4.91%). Add chip-stock rebound, GM earnings, Miami affordability, and biotech IPO rotation.
- `GLP-1 Obesity Drug Rivalry` — add the flagship Morning Brew confirmation of Novo suing Lilly over allegedly outdated/deceptive GLP-1 ad data; LLY/NVO were already watchlist candidates from Brew Markets, no new watchlist edit.
- `Morning Brew Newsletter Network` — add a July 22 issue routing paragraph so future newsletter sessions know this flagship issue produced four durable pages plus two substantive updates.

### Leave source-only
Do not create pages for: sponsor blocks (Re:You, Cytonics, CAKES), reader poll, games, referrals, word of the day, routine recs, Big Boy opening joke unless tied to an existing rail/tourism note, and short one-line headlines unless they connect to an existing durable page.

## Infrastructure pattern
- Newsletter archives belong under `Sources/Newsletter/` using normalized basename `YYYY-MM-DD - Source Title.md`.
- Preserve the random inbox capture in `original_filename:` when moved into the normalized archive.
- Add `## Pages Updated` with Created/Updated subsections.
- Update `wiki-index.md` rows for every created page and touched existing pages; increment `page_count` by number of new Notes pages only.
- Append a `wiki-log.md` entry with watchlist candidates if public-company implications are clear.

## Watchlist candidate rule example
- HAS — Magic: The Gathering's $545.3m quarter (+32%) shows a central public-company IP growth engine, but release fatigue/player saturation should be reviewed before adding. Do not edit `System/Stock Watchlist.md` autonomously.
