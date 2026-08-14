# Newsletter routing session — 2026-07-14 Morning Brew / Tech Brew / Brew Markets

Use this as a concrete routing example for newsletter issues that mix markets, geopolitical risk, consumer-brand items, media/culture, workplace/social trends, AI infrastructure, and public-company earnings. It also records two scrambled-online extraction edge cases from Tech Brew and Brew Markets.

## Sources
- Morning Brew flagship Inbox capture: `2026-07-14-0942-newsletter-infinite-pasta-glitch.md`
  - Normalized source archive: `Sources/2026-07-14 - Infinite pasta glitch.md`
  - Issue title: `☕️ Infinite pasta glitch`
- Tech Brew scrambled email capture: `2026-07-14-1830-newsletter-big-tech-s-global-power-trip.md`
  - Email URL was placeholder `/issues/tk?...`; generic HTTP-200 not-found shell.
  - Derived canonical URL: `https://www.techbrew.com/issues/big-techs-global-power-trip`
  - Normalized source archive: `Sources/2026-07-14 - Big Tech's Global Power Trip.md`
- Brew Markets scrambled email capture: `2026-07-14-2022-newsletter-inflation-hands-warsh-a-win.md`
  - Email URL used uppercase path segment: `/issues/IBM-bank-earnings-inflation-warsh?...`; generic HTTP-200 not-found shell.
  - Lowercase canonical URL worked: `https://www.brewmarkets.com/issues/ibm-bank-earnings-inflation-warsh`
  - Normalized source archive: `Sources/2026-07-14 - Inflation Hands Warsh a Win.md`

## Extraction lessons

### Placeholder `/issues/tk` — derive title slug
When Tech Brew/Morning Brew/Brew Markets plain text says the provider scrambled the email and the URL is a placeholder like `/issues/tk`, do not downgrade to low-content/admin. Use the email H1/title to derive likely issue slugs and fetch the real page.

Slug rules that worked here:
- Lowercase title.
- Remove emoji/punctuation.
- Convert possessive apostrophe-s to `s` rather than `-s` (`Big Tech's` → `big-techs`).
- Collapse spaces to hyphens.
- Verify the extracted text is not the generic “We couldn't find that page” shell before ingesting.

### Case-sensitive issue paths — retry lowercase
A Brew Markets URL that looked specific (`/issues/IBM-bank-earnings-inflation-warsh`) still returned a generic not-found shell because the path was case-sensitive. Before deriving unrelated slugs or treating the body as unavailable, retry the same path lowercased. Preserve the failed raw URL in the source archive (`failed_url:`) and store the successful canonical URL as `online_url:`.

### Headless-safe fetching
Fetch HTML to a temporary file first, then parse locally. Avoid `curl ... | python` or other pipe-to-interpreter patterns in headless cron because they can trigger approval guards. Keep the saved page only as temporary working state; the durable archive is the normalized Markdown source in `Sources/`.

## Routing decisions — Morning Brew flagship

### Create durable pages when a short newsletter item has reusable structure
- **Strait of Hormuz Protection Fee** — create a finance/geopolitics concept page when a market-moving policy proposal ties shipping security, oil prices, insurance, and international law together.
  - Evidence captured: proposed **20% cargo-value** US naval escort fee, normal shipowner fees around **2%-3%**, IMO objection, crude above **$80/barrel**.
  - Route to `15 Finance & Economics MOC` and update `Economic Indicators`.
- **Restaurant Subscription Promotions** — create a business/consumer-brand concept when a restaurant promotion illustrates a repeatable loyalty/subscription pattern, not just a coupon.
  - Evidence captured: Olive Garden **13-week**, **$100**, **10,000-pass** Never-Ending Pasta Pass; prior **24,000** passes sold in “milliseconds”; break-even at about four chicken alfredo plates.
  - Route to `14 Business MOC`, near `CAVA Restaurant Growth Strategy`.
- **Disney Remake Saturation Risk** — create a culture/media concept when a box-office item exposes a repeatable IP/franchise-strategy risk.
  - Evidence captured: live-action *Moana* opened at **$95m global** vs **$350m+** cost, **$43m domestic** vs **$60m+** target, compressed nostalgia cycle vs Disney’s historical average 27-year remake wait.
  - Route to `17 Culture MOC`, near streaming/media notes.
- **Workplace Romance Decline** — create a workplace/society concept when survey data signals changing office norms.
  - Evidence captured: SHRM coworker dating **16%** vs Harris Poll **40%** in 2008; workplace crushes **22%** vs **49%** in 2024.
  - Route to `06 US Politics & Society MOC`, near workplace/gender/work-culture notes.

### Update existing pages for one-paragraph refreshes
- **Economic Indicators** — add market table/rates/oil/Bitcoin/SK Hynix signal, especially when oil/rates or jobs/inflation/market-breadth appear.
- **Morning Brew Newsletter Network** — add a concise issue-routing paragraph documenting what became pages and what stayed source-only.
- **Meta AI Capex Valuation Risk** — update rather than create a new Meta note when a one-line headline adds a larger capex figure (here: Bloomberg-reported **$40bn** boost, **$250bn** implied Louisiana campus cost, only **$50bn** publicly announced).
- **SK Hynix AI Memory Listing** — update rather than create a daily stock-move page when market table adds post-debut trading signal (here: **$152.35**, **-9.32%** in AI/Hormuz selloff).

## Routing decisions — Tech Brew “Big Tech's global power trip”
- **Data Center Noise Externalities** — update this existing data-center externalities page rather than create a new “data-center global power trip” page. Evidence: New York moratorium for data centers above **50MW**; Ireland data centers using **23%** of national electricity; Denmark pausing large connection requests with **14GW** queued; Chile wetland servers using **62%** of community power; hyperscaler emissions at about one-third of France; US consumers facing **$23bn** extra electricity costs through 2028; Meta Louisiana power capacity moving from **2GW** to **5GW**.
- **Meta AI Capex Valuation Risk** — update with the 2GW-to-5GW physical-capacity lens because it reinforces capex/ROIC concerns and ties Meta’s valuation note to grid, climate, and local-politics constraints.
- **AI Employee Accountability Gap** — update with the employee-credit/disclosure dimension: managers may over-credit AI for human work while employers devalue work once employees disclose bot assistance.
- **Morning Brew Newsletter Network** — record that Tech Brew issue routing can refresh existing AI infrastructure and AI workplace-governance pages without creating a generic newsletter issue page.

## Routing decisions — Brew Markets “Inflation hands Warsh a win”
- **IBM AI Infrastructure Spending Squeeze** — create a new public-company/entity note because IBM’s **25.21%** record selloff and infrastructure revenue **-7%** show a reusable AI-budget crowd-out pattern. Route through `14 Business MOC` and `15 Finance & Economics MOC`. Since IBM was not in `System/Stock Watchlist.md`, surface it as a watchlist candidate in the final summary instead of editing the watchlist.
- **Citigroup Turnaround Earnings Catalyst** — update the existing Citi note with operational follow-through: four of five divisions beat expectations, equities trading revenue **+45%**, profit **$5.8bn**, shares **-5.27%**.
- **Federal Reserve Kevin Warsh Chair Risks** — update the existing Warsh/Fed note with June CPI and testimony context: CPI **-0.4%** month-over-month, headline **3.5%**, core **2.6%** annualized, no-change odds rising from **58%** to **83%**, hike odds down from nearly **42%** to **16%**.
- **Economic Indicators** — update with the Brew Markets table: Nasdaq **26,107.01**, S&P **7,543.59**, Dow **52,508.27**, 10-year **4.585%**, Bitcoin **$64,445.52**, oil **$79.73**, CPI/Fed signal, and bank earnings breadth.

## Keep source-only
Sponsor copy, ads/disclosures, games, holiday trivia, word-of-day, referral blocks, product recommendations, generic newsletter-network promo, and short one-line headline recaps stay in the source archive unless they connect to an existing durable page.

## Infrastructure pattern
- Archive with normalized name `YYYY-MM-DD - Source Title.md`; preserve the raw Inbox filename in `original_filename`.
- For scrambled emails, also preserve the raw Inbox capture as `Sources/<stem>.inbox-original.md` when the normalized source archive contains the fetched online issue.
- Add `## Pages Updated` to the source archive listing all pages created or updated.
- Update all touched page rows in `wiki-index.md`; increment `page_count` for newly created `Notes/*.md` pages.
- Append one `wiki-log.md` ingest entry per source.
- Verify: Inbox empty, source archive exists, preserved raw original exists when applicable, new note files exist, MOC links exist, index rows exist, log entry exists, and touched frontmatter parses as valid YAML.
