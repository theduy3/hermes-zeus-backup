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
| cand-thor-health | Thor | low-medical | legacy Thor weight CSV (located at Phase 3 gate) | current | `30-health/logs/`, `30-health/health_summary.md` | queued | — | Phase 3; freeze legacy CSV read-only after cutover |
| cand-finance-current | Finance | financial | theduyvault Finance statements/sources | current | `60-finance/events/`, `60-finance/finance_summary.md` | queued | — | Phase 4; current values only, not full history |
| cand-charles-invest | Charles | financial | theduyvault research/watchlists | current | `60-finance/` investment section | queued | — | Phase 5; after Finance liquidity set |
| cand-goals-projects | Zeus / Default | private | `/vault/Tasks/`, Life OS summaries | current | `70-goals/`, `50-projects/` | queued | — | Phase 6; vault Tasks stays authority initially |
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
