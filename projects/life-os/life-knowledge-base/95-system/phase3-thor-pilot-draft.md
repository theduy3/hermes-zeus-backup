# Phase 3 — Thor health/wellness pilot (DRAFT, awaiting approval)

Status: DRAFT — executed only after explicit user approval of this document.
Parent plan: `95-system/life-os-migration-plan.md` (Phase 3).
Authorized mechanism: Phases 1–2 are complete and verified (see changelog 2026-08-13).

## Hard prerequisite (blocker)
The legacy Thor weight CSV specified by the plan does **not** currently exist in
`/home/hermes/.hermes` or `/vault`. Before any import, the source must be located
or provided. The pilot cannot run without a real, traceable source.

- Expected: `thor_weight.csv` with at least `date` and `weight_kg` columns, plus
  any energy/sleep/exercise rows if present.
- Acceptable locations: provided by the user, or found under a Thor profile/source path.

## Scope (bounded, reviewable)
Import ONLY the following, and ONLY after the source is present:
1. Retain the original Thor weight CSV as source evidence — never delete it; freeze
   it read-only after cutover.
2. Create a Life OS source record under `30-health/` linking to the CSV (with the
   source path, date range, and date precision).
3. Register `weight` as an optional metric (kind=numeric, unit=kg) in the ledger,
   domain `health`.
4. Import explicit dated measurements exactly as recorded (no inference, no rounding
   beyond the source precision).
5. Migrate current routines, protocols, health context, and explicit metrics only.
6. Mark any unsupported medical claims as uncertain or exclude them.

## Out of scope (strict)
- No diagnosis inference.
- No overwriting of original evidence.
- No finance/investment/household/rewards data.
- No bulk import of notes, sources, or daily folders.

## Execution steps (to run only when approved + source present)
1. Place/freeze the CSV; record its absolute path as the source of truth.
2. Write `30-health/logs/YYYY-MM.md` append-only event blocks via `life_store.write`
   (domain=`health`, kind=`metric`/`observation`, with `source_ids=['src-thor-weight']`).
3. Update `30-health/health_summary.md` with current protocol context + source link.
4. Run `rebuild()` + `reconcile()`; assert `ok=True`.
5. Build a verification report: each imported value traceable to a line in the CSV.

## Exit criterion (from plan)
Thor can retrieve current context and trend history from Life OS, with each
important historical value traceable to the legacy source.

## Reconciliation gate
- `reconcile()['ok'] == True` after import.
- CSV line count (minus header) == active imported measurement count.
- No `cache_only` or `ledger_only` discrepancies.

## Reviewer / cutover
- Cut over future weight/energy/sleep/exercise/nutrition/habit records ONLY after
  the above passes and the user approves the verification report.
- Then freeze the legacy CSV as a read-only legacy source.
