# Migration registry

This registry tracks candidates; it is not a destination for raw source content.

## Status values

`queued` → `imported` → `verified` → `cut_over` → `archived`

A status change needs a source link, reviewer, and date. No source is deleted.

## Foundation (Phases 1–2, executed 2026-08-13)

The mechanism itself is established: Life OS Markdown is the authoritative tracker
source; SQLite is a rebuildable cache; backup/restore, interrupted-write, concurrency,
provenance, correction, reconciliation, and checkpoint tests pass; a baseline
checkpoint exists under `verification/checkpoints/`. No personal data has been
migrated. Each downstream candidate below remains `queued` behind its approval gate.

## Candidates (all gated, none imported yet)

| id | owner_profile | sensitivity | source_path | date_range | target_path | status | reviewer | notes |
|---|---|---|---|---|---|---|---|---|
| cand-thor-health | Thor | low-medical | forward-only self-report (no historical backfill) | 2026-08-13→ | `30-health/logs/`, `30-health/health_summary.md` | cut_over | Hermes (2026-08-13) | Forward-only live tracking started 2026-08-13; first event `thor-2026-08-13`. Legacy CSV template remains empty (no data existed). Future readings append via `tracker/thor_log.py`. |
| cand-finance-current | Finance | financial | forward-only self-report (2026-08-13) | 2026-08-13→ | `60-finance/events/`, `60-finance/finance_summary.md` | cut_over | Hermes (2026-08-13) | Forward-only live capture started 2026-08-13; events `fin-2026-08-13` + superseding `fin-2026-08-13-v2` (added monthly cash-out: rent $2,050 @ 1483 Homer St). Charles may now begin. |
| cand-charles-invest | Charles | financial | theduyvault Daily/*-investment.md (source evidence) + user-supplied theses/positions | current | `60-finance/charles.md`, `60-finance/events/` | queued | — | Phase 5 mechanism built (charles_log.py); source index links vault watchlists as evidence. Awaiting user's real positions/theses/risk rules. |
| cand-goals-projects | Zeus / Default | private | user-supplied goals/projects + `/vault/Tasks/` (task authority) | current | `70-goals/`, `50-projects/` | queued | — | Phase 6 mechanism built (life_log.py). Awaiting user's real goals/projects. Vault Tasks stays task authority. |
| cand-catthew-house | Catthew | private-family | household/family evidence (vault) | current | household/family Life OS records | queued | — | Phase 7; no child/spouse/identity beyond required |
| cand-butter-rewards | Butter | financial | travel/rewards sources (vault) | current | rewards Life OS records | queued | — | Phase 8; after Finance current state |
| cand-wiki-transition | Wiki | archival | theduyvault MOCs/Notes | historical | legacy cross-references | queued | — | Phase 9; read-only legacy markers only |

## Rules

- Never delete theduyvault content during migration.
- Migrate only active, current, source-linked, useful records.
- Preserve conflict/uncertainty; do not silently resolve it.
- Use exact dates when known; record approximate precision otherwise.
- Every promoted consequential claim receives a source link.
- No legacy log is disabled until backup, restore, and profile retrieval tests pass.
