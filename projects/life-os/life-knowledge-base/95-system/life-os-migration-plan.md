# Life OS migration plan — revised

Status: approved 2026-08-12; phased execution only. Every domain cutover remains gated by reconciliation and user review.
Updated: 2026-08-12
Timezone: America/Toronto

## Decision

Life OS will become the authoritative operating system for current personal context, plans, active health and nutrition tracking, current finance and investment context, goals, habits, projects, reviews, and profile coordination.

theduyvault remains the permanent source archive and general wiki: original documents, PDFs, statements, raw captures, newsletters, research, historical notes, daily journals, task archive, and evidence.

Do not literally move every vault file. Migrate only active, current, structured, decision-relevant, source-linked knowledge. Preserve originals in theduyvault and link to them from Life OS source records. Nothing is deleted during migration.

## Capture policy — revised

All new raw knowledge from Pixel, Samsung, email newsletters, web clips, PDFs, screenshots, voice-note transcriptions, and other devices continues to enter through:

`/vault/Inbox`

Flow:

```text
Devices / newsletters / captures
  -> /vault/Inbox
  -> Wiki: preserve, deduplicate, classify, archive, index
  -> theduyvault Notes / Sources / MOCs
  -> domain owner promotes only current, useful, source-linked conclusions to Life OS
```

Do not create a competing phone/newsletter Life OS inbox. Life OS `01-inbox/inbox.md` is reserved for deliberate direct personal-context captures that bypass the vault, and should normally be normalized quickly into the appropriate canonical Life OS record.

Raw material remains in theduyvault unless it changes what is true now, creates an active decision/constraint, becomes a goal/project/idea, or changes a current health/finance/investment protocol.

## Target architecture

```text
Life OS Markdown
  = current truth, plans, health, finance, investments, goals, habits,
    projects, reviews, current personal context, and correction history.

Life OS Tracker
  = operational UI/cache derived from Life OS Markdown: today checklist,
    explicit completions, selected metrics, goal/project views, trends.

theduyvault
  = original documents, historical notes, research library, daily journals,
    raw captures, newsletters, task archive, source evidence, and wiki.
```

One fact has one writable authority. Links, summaries, dashboards, and indexes are derived views, not competing records.

## Authority matrix

| Record | Writable authority | Evidence / derived view |
|---|---|---|
| Raw capture, newsletter, PDF, statement, screenshot | theduyvault Inbox then Sources/Notes | Life OS source record link only when promoted |
| Research note and broad reference material | theduyvault Notes/MOCs | Life OS resource/project link when current |
| Dated task and calendar commitment | `/vault/Tasks/` until an explicit future task cutover | Life OS goal/project context; tracker reference only |
| Current health/nutrition protocol and durable context | Life OS Markdown | Vault source + tracker cache |
| Explicit health/nutrition metric or habit completion | Life OS Markdown event/log | Tracker SQLite/dashboard |
| Current personal finance context and obligations | Life OS Markdown | Vault documents/sources |
| Investment posture, thesis, constraints, decisions | Life OS Markdown | Vault research + Finance constraints |
| Current goals, milestones, review cadence, projects | Life OS Markdown | Tracker views + vault task links |
| Vault taxonomy, archival, MOCs, deduplication | theduyvault | Wiki only |

## Profile contracts

| Profile | Owns in Life OS | Reads from theduyvault | Must not do |
|---|---|---|---|
| Wiki | Source links and migration candidates only | Inbox, Sources, Notes, MOCs, Daily | Write current Life OS summaries or tracker state autonomously |
| Thor | Health, wellness, nutrition, routines, explicit metrics | Health sources and legacy Thor CSV | Infer diagnoses or overwrite original evidence |
| Finance | Cash-flow context, obligations, financial goals, uncertainty | Statements, bills, financial source notes | Overwrite investment thesis or present unsourced balances as current |
| Charles | Investment posture, thesis, risk rules, decisions, investment projects | Research, watchlists, reports | Overwrite Finance liquidity/cash constraints |
| Zeus | Cross-domain priorities, daily plan, goal/project coordination | Vault Tasks and specialist outputs | Become a competing task authority |
| Catthew | Durable household/family context and active plans | Family/household evidence and tasks | Write non-family specialist domains |
| Butter | Current travel reward strategy and card rules | Travel and program sources | Override Finance payment/cash constraints |
| Default | Standards, conflict resolution, migration governance | All approved sources | Make unsupported specialist conclusions |

## Migration phases

### Phase 1 — Markdown authority hardening

Goal: ensure Life OS Markdown, not SQLite, is the true tracker source of truth before real data enters.

1. Add append-only dated Markdown ledgers under each domain:
   - `30-health/logs/YYYY-MM.md`
   - `40-nutrition/logs/YYYY-MM.md`
   - `60-finance/events/YYYY-MM.md`
   - `50-projects/events/YYYY-MM.md`
   - `70-goals/events/YYYY-MM.md`
2. Make each tracker write transaction:
   - validate request;
   - write canonical Markdown record first;
   - update current summary only if current state changes;
   - update/rebuild SQLite cache;
   - read back both records;
   - report conflict instead of overwriting.
3. Add deterministic rebuild, reconciliation, backup/restore, interrupted-write, concurrency, correction, duplicate-ID, and provenance tests.
4. Remove test habit/metric/observation data before real use.

Exit criterion: deleting `tracker.sqlite3` and rebuilding from Markdown produces the same operational tracker state.

### Phase 2 — Migration registry and checkpoints

Create a non-sensitive migration manifest containing, per candidate:
- source path and source ID;
- owner profile;
- sensitivity classification;
- date range and date precision;
- proposed Life OS destination;
- status: `queued`, `imported`, `verified`, `cut_over`, or `archived`;
- reviewer and cutover date.

Create backup checkpoints for Life OS Markdown, tracker database, and legacy specialty logs. Never delete a vault source. Every promoted consequential claim receives a source link.

### Phase 3 — Thor health/wellness pilot

Migrate only bounded, reviewable material:
- retain the original Thor weight CSV as source evidence;
- create a Life OS source record linking to it;
- register weight as an optional metric;
- import explicit dated measurements exactly as recorded;
- migrate current routines, protocols, health context, and explicit metrics only;
- mark unsupported medical claims uncertain or exclude them;
- cut over future weight/energy/sleep/exercise/nutrition/habit records only after reconciliation;
- freeze the legacy CSV as a read-only legacy source after approved cutover.

Exit criterion: Thor can retrieve current context and trend history from Life OS, with each important historical value traceable to the legacy source.

### Phase 4 — Finance current-state migration

Create current, source-backed finance context:
- cash-flow constraints;
- recurring obligations;
- active liabilities;
- financial goals;
- known uncertainties;
- review cadence.

Keep statements, receipts, and original records in theduyvault. Import current, dated, sourced values—not complete transaction history. Future finance operating context writes to Life OS after source validation.

### Phase 5 — Charles investment migration

After Finance establishes current liquidity constraints, migrate:
- portfolio rules and risk limits;
- current investment posture;
- active theses;
- dated decisions and rationale;
- review triggers;
- active investment research projects.

Keep watchlists, articles, transcripts, reports, and research library in theduyvault. Charles references Finance constraints rather than duplicating them.

### Phase 6 — Goals, projects, and daily execution

Migrate goals, milestones, project context, review cadence, habits, and personal operating context to Life OS. Keep `/vault/Tasks/` as task authority initially because it already connects to calendar/reminders.

Zeus combines Life OS priorities with vault commitments and tracker habit state. A task-system cutover is optional and cannot begin until health, finance, and investment migrations pass reconciliation.

### Phase 7 — Catthew household/family migration

Migrate only current, privacy-appropriate household/family operating context:
- routines, household projects, active family goals, confirmed preferences, and practical logistics;
- source links to relevant vault material, without copying raw communications, photos, attachments, or sensitive biographies;
- `/vault/Tasks/` remains the authority for scheduled chores, errands, renewals, and calendar-linked commitments.

Catthew owns current household/family context but must not distribute child, spouse, household, health, location, or identity information beyond required private Life OS records without explicit approval.

### Phase 8 — Butter travel-rewards migration

After Finance current-state migration passes, migrate only:
- active card/rewards registry, with user-reported balances dated `as_of`;
- minimum-spend, annual-fee, expiry, retention, downgrade/cancel, and redemption decisions;
- active travel-rewards goals and projects; and
- source-linked trip/reward strategy.

Finance owns cash-flow, debt, payment obligations, and liquidity. Butter must read Finance constraints before recommending a card application, annual fee, large minimum spend, transfer, or paid positioning. Keep statements, booking confirmations, promos, screenshots, and research in theduyvault.

### Phase 9 — Wiki transition

Wiki remains theduyvault librarian. For an approved cut-over domain, Wiki adds a lightweight legacy marker or cross-reference where appropriate:
- `legacy_source: true`
- Life OS canonical path/ID
- last reviewed date

Wiki does not ingest Life OS private summaries into broad wiki collections without explicit approval.

### Phase 10 — Final cutover and legacy retirement

After each domain passes reconciliation and receives approval:
- profile writes new current context only to Life OS;
- legacy specialty logs become read-only evidence;
- old cron/report jobs read Life OS rather than independently maintained logs;
- no legacy log is disabled until backup, restore, and profile retrieval tests pass.

## Safety rules

- Never delete theduyvault content during migration.
- Never bulk-import Notes, Sources, or Daily folders.
- Migrate only active, current, source-linked, useful records.
- Preserve conflict/uncertainty; do not silently resolve it.
- Use exact dates when known and record approximate precision otherwise.
- Keep raw documents in theduyvault permanently.
- Never store credentials, payment authentication, recovery data, or other excluded secrets.
- Pause at every domain cutover for approval.

## Recommended approval sequence

1. Plan approved 2026-08-12. Begin Phases 1–2: harden Markdown authority, create registry/checkpoints, remove only tracker test data.
2. Gate: request approval of the Thor pilot only after Phase 1 passes its rebuild/reconciliation tests.
3. Gate: request approval of Finance, then Charles, with a review gate between them.
4. Gate: request approval of goals/daily execution, then Catthew, then Butter, then Wiki transition.

The next execution scope is Phases 1–2 only.
