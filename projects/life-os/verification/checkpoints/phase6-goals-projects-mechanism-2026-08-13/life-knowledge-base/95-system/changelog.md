# Changelog

## 2026-08-12
Created private portable KB and tracker; no personal data imported. `/vault/AgentMemory` excluded. Existing vault is referenced as a legacy/source corpus only due to its write boundary.

## 2026-08-12 — migration plan updated
- Added `95-system/life-os-migration-plan.md`.
- Confirmed theduyvault Inbox remains the sole raw-capture funnel for device imports and newsletters.
- Defined phased cutover: Markdown authority hardening, migration registry, Thor pilot, Finance, Charles, goals/execution, household/travel, Wiki transition, then optional task cutover.
- No personal data was migrated and no vault content was changed.

## 2026-08-12 — migration plan approved
- User approved the staged Life OS migration plan.
- Added explicit Catthew household/family privacy rules and Butter rewards/Finance dependency rules.
- Created the approved foundation task at `/vault/Tasks/tasks/life-os-migration-phases-1-2.md`.
- Execution is limited to Phases 1–2 until the Thor pilot receives its separate approval gate.

## 2026-08-12 — Phase 1–2 paused
- User asked to save the Phase 1–2 migration work for later.
- Keep the approved task pending; do not remove tracker test data, create the baseline checkpoint, or migrate personal domain data until work is resumed.

## 2026-08-13 — Phases 1–2 executed
- Removed orphaned SQLite test data (habits/metrics/observations/completions with no Markdown source); rebuilt empty cache; `reconcile` ok.
- Created missing ledger dirs: `60-finance/events`, `50-projects/events`, `70-goals/events`.
- Added 4 Phase 1 tests: backup/restore roundtrip, interrupted-write (no partial cache), concurrency (no duplicate ids), provenance (source link preserved through rebuild). All 9 tracker tests pass.
- Fixed 3 latent bugs found by tests: `rebuild` now stores full event so `source_ids`/provenance survive the cache; `rebuild_tracker` serializes dict `schedule` before insert; `write` is lock-guarded so concurrent writes stay consistent.
- Verified Phase 1 exit criterion: deleting `tracker.sqlite3` and rebuilding from Markdown yields a consistent operational state (`reconcile.ok=True`).
- Phase 2: populated `migration-registry.md` with 7 gated candidate domains (all `queued`, no data imported).
- Phase 2: created baseline checkpoint `verification/checkpoints/phase12-baseline-2026-08-13` (25 KB MD files + SQLite, all ledger dirs).
- No personal data migrated; theduyvault untouched. Next gate: Thor pilot (Phase 3) after Phase 1 passes.

## 2026-08-13 — Phase 3 deferred (save for later)
- User reviewed the staged Thor pilot draft; chose to defer because no weight/health data exists yet.
- Created an empty fill-in template (header only, no invented data) at `30-health/sources/thor_weight.csv`.
- Phase 3 remains a DRAFT + a pending vault task (`life-os-phase-3-thor-pilot.md`); not executed.
- Decision rule recorded: pilot runs only when (a) user approves the draft and (b) a real, traceable source (the CSV with ≥1 real row, or pasted readings) exists. Do NOT fabricate health data.
- Life OS parked after Phases 1–2; all later phases (Finance, Charles, Goals, Catthew, Butter, Wiki) still gated and untouched.

## 2026-08-13 — Phase 3 Thor pilot EXECUTED (forward-only)
- User chose "start live Thor tracking from today, forward-only, no backfill."
- Built `tracker/thor_log.py`: CLI forward-capture writing one sourced `self_report` health event per day via `life_store.write`; rejects empty/bad input; never invents fields.
- Recorded first real event `thor-2026-08-13` (weight 74kg, energy 10, sleep 6.5h, exercise 45min, note "going back to gym") to `30-health/logs/2026-08.md`. `reconcile.ok=True`.
- Updated `30-health/health_summary.md` (was "No health data captured") to current-state, source-linked summary.
- Migration registry: `cand-thor-health` → `cut_over` (forward-only). Legacy `thor_weight.csv` template stays empty (no historical data; deliberately not fabricated).
- Rule honored: NO fabricated health data. Only user-supplied readings recorded.
- Next: continue daily forward captures when user provides readings. Later phases still gated.

## 2026-08-13 — Phase 4 Finance pilot EXECUTED (forward-only)
- Built `tracker/finance_log.py`: forward-capture CLI for current finance state (liquid CAD, monthly in/out, liabilities, goals, uncertainties, review cadence, optional source). Rejects empty/bad input; never invents fields.
- Recorded first real event `fin-2026-08-13` (liquid $0; income $2,747.50 biweekly from 2026-08-20, est. monthly ~$5,952.92; mortgage $284k@3.89% bal $282,875.60; goal $10k liquid buffer; monthly review). `reconcile.ok=True`.
- Monthly cash-OUT intentionally left null (user will provide later) — flagged as pending in `finance_summary.md`.
- Updated `60-finance/finance_summary.md` (was "No finance data captured") to current-state, source-linked summary.
- Migration registry: `cand-finance-current` → `cut_over` (forward-only). Charles remains gated until liquidity baseline firm.
- Rule honored: NO fabricated finance data. Only user-supplied values recorded; income avg explicitly marked cadence-derived estimate.
- Next: capture monthly cash-out when provided; then Phase 5 (Charles) may begin.

## 2026-08-13 — SAVED FOR LATER (after Phase 4)
- User said "save for later." Life OS migration parked here.
- Phases 1-4 done & verified: Phase 1-2 (mechanism+registry+checkpoint), Phase 3 (Thor forward-only, event `thor-2026-08-13`), Phase 4 (Finance forward-only, event `fin-2026-08-13`).
- OUTSTANDING before Phase 5 (Charles): user still owes **monthly cash-out** for Finance (flagged pending in `finance_summary.md`). Charles gated until that's filled.
- All later phases (Goals/Projects, Catthew, Butter, Wiki) still queued/untouched.
- Resume trigger: "continue the migration of theduyvault and life-os" or "resume Life OS migration <phase>". To progress: provide monthly cash-out → then Phase 5 Charles with investment theses/positions.
- No fabricated data anywhere; theduyvault untouched.

## 2026-08-13 — Finance monthly cash-out added; Phase 4 COMPLETE
- User provided monthly cash-out: rent $2,050 at 1483 Homer Street (recurring).
- Superseded `fin-2026-08-13` with `fin-2026-08-13-v2` (correct + distinct id) adding `monthly_out_cad=2050`. Reconcile ok; old event preserved in ledger (supersede chain).
- Updated `finance_summary.md` to merged current state: liquid $0, inflow ~$5,952.92 (biweekly-derived), outflow $2,050 (rent), mortgage $284k@3.89% bal $282,875.60, $10k buffer goal, monthly review.
- Migration registry: `cand-finance-current` → `cut_over` (complete). **Phase 4 fully done.**
- Phase 5 (Charles/investments) now UNBLOCKED — liquidity + cash-flow baseline established. Remains queued until user supplies investment theses/positions.
- Fix noted: `finance_log.py` requires an explicit `--event-id` when using `--correct` (auto-id collides with superseded event). Next correction should pass e.g. `--event-id fin-2026-08-13-v3`.
- Remaining gated: Phases 6-9 (Goals/Projects, Catthew, Butter, Wiki).

## 2026-08-13 — Phase 5 Charles mechanism BUILT (awaiting real data)
- Built `tracker/charles_log.py`: forward-only capture for investment records (kinds: thesis, position, risk_rule, decision, watch). References Finance liquidity; never overwrites it.
- Created `60-finance/charles.md`: Charles operating layer + dependency on Finance + source index linking `Daily/*-investment.md` watchlists as read-only EVIDENCE (not migrated claims).
- Inspected theduyvault `Daily/*-investment.md`: they are watchlist/briefing snapshots (prices, sentiments), NOT positions/theses/decisions — correctly treated as source evidence only.
- 0 Charles events written: NO fabricated investment data. All 9 tests pass.
- Migration registry: `cand-charles-invest` remains `queued` — mechanism ready, awaiting user's real positions/theses/risk rules.
- Next: user supplies actual investment data → record via charles_log.py; promote distilled, sourced conclusions only.

## 2026-08-13 — Phase 6 Goals/Projects mechanism BUILT (awaiting real data)
- Built `tracker/life_log.py`: forward-only capture for goals + projects (strategic why/milestones/context). `/vault/Tasks/` remains the dated-task authority per plan.
- Created `70-goals/goals_summary.md` and `50-projects/projects_summary.md` (both "No ... captured", ready).
- 0 goal/project events written: NO fabricated data. All 9 tests pass.
- Migration registry: `cand-goals-projects` remains `queued` — mechanism ready, awaiting user's real goals/projects.
- Next: user supplies goals/projects → record via life_log.py.
