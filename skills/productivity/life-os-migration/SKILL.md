---
name: life-os-migration
version: 1
author: hermes-curator
license: MIT
description: Gated no-fabrication migration from theduyvault to Life OS.
metadata:
  hermes:
    tags: [life-os, theduyvault, migration, personal-knowledge-base, tracker]
    related_skills: [hermes-encrypted-secrets, life-knowledge-base, life-tracker]
---

# Life OS ↔ theduyvault migration

## When to use
- User says "continue the migration", "resume Life OS migration <phase>", "start live Thor/Finance/Goals tracking", or wants to advance any migration phase.
- Any work touching Life OS personal-context data where the source of truth may be theduyvault.

## Architecture (the non-negotiable model)
- **theduyvault (`/vault`)** = permanent SOURCE ARCHIVE: original docs, research, daily logs, newsletters, raw device captures. NEVER deleted during migration.
- **Life OS (`/home/hermes/.hermes/projects/life-os/life-knowledge-base`)** = CURRENT TRUTH: health, finance, investments, goals, habits, projects, reviews, current personal context.
- **Tracker (`/home/hermes/.hermes/projects/life-os/tracker`)** = operational cache, REBUILDABLE from Life OS Markdown via `life_store.rebuild()`. SQLite is NOT the authority.
- Rule: **one fact = one writable authority.** Everything else links or derives. Migrate only current, sourced, useful records — not full history.

## HARD RULE — no fabrication
- Never invent readings, balances, metrics, or history. A phase runs ONLY when (a) user approves AND (b) a REAL, traceable source exists (pasted values, a CSV with ≥1 real row, or a vault source file).
- If no real data exists, build the capture MECHANISM (forward-only script) and pause — do not record placeholder/fake data. Confirmed by user: "I have no data yet" → defer, leave empty template.
- Epistemic labeling: every captured claim is `self_report` (user-supplied) unless derived from a vault source file (then `source_ids` points at it).

## Resume mechanics (always do this first)
1. `session_search` for "migration theduyvault life-os" / "Life OS migration phases" — prior sessions hold the plan, changelog, and gate state.
2. Read the Life OS control files (they are the source of truth for WHERE YOU LEFT OFF):
   - `life-knowledge-base/95-system/changelog.md` — what was done + deferrals + decision rules.
   - `life-knowledge-base/95-system/migration-registry.md` — per-candidate status (`queued`→`imported`→`verified`→`cut_over`→`archived`).
   - `life-knowledge-base/agent_rules.md` — authority/privacy/capture rules.
3. Inspect current state: `find life-knowledge-base/<domain> -type f`, check `finance_summary.md`/`health_summary.md` ("No X data captured" = untouched), check `verification/checkpoints/`.

## Gated phase order (from the approved plan)
1. **Foundation/hardening** (DONE) — Markdown authority, rebuildable cache, tests, baseline checkpoint.
2. **Migration registry + checkpoint** (DONE) — candidates queued, baseline checkpoint created.
3. **Thor health/wellness pilot** (CUT_OVER, forward-only) — `tracker/thor_log.py` records daily `self_report` events.
4. **Finance current state** — `tracker/finance_log.py` records dated finance snapshot. GATED on real numbers.
5. **Charles investments** — after Finance liquidity set.
6. **Goals/projects/execution** — vault Tasks stays authority initially.
7. **Catthew household/family** — privacy-limited. 8. **Butter rewards**. 9. **Wiki transition** (read-only legacy markers).

Advance ONE phase at a time; each later phase may depend on an earlier one (Charles depends on Finance).

## Forward-only capture pattern (the proven technique)
- Each domain has a `tracker/<domain>_log.py` CLI that calls `life_store.write(domain, kind, selected_date, payload, event_id=..., source_ids=('thor_self_report',), estimated=False)`.
- CLI MUST reject empty payloads and bad dates (exit 2) before calling `write()` — so no accidental blank events.
- After writing: run `life_store.reconcile()` → must be `ok:True` (ledger count == cache count, sha matches).
- Update the domain `summary.md` to current-state, source-linked. Update `migration-registry.md` (status → `cut_over`) and `changelog.md`.
- Create a new checkpoint: `life_store.checkpoint('phase<N>-<slug>-<date>')`.
- Run the full unittest suite (`python3 -m unittest tests.test_life_store`) as a regression gate after any code change.

See `references/forward_capture.md` for the script skeleton and `references/phases.md` for the full gated plan text.

## Pitfalls
- **Don't edit `config.yaml` or `.env` via patch/write_file tools** — they refuse (security guard). For config use `hermes config set <dotted.key> <value>`; for `.env` use a terminal `python3` script. (Credential-specific; see `hermes-encrypted-secrets`.)
- **Reconcile before declaring done** — a write that doesn't rebuild the cache is silently broken. Always check `reconcile().ok`.
- **Don't backfill history the user doesn't have** — forward-only is the safe default when source data is absent.
- **theduyvault is read-only for migration** — copy/link, never move or delete.
- **CORRECTING a prior event needs a DISTINCT `--event-id`.** Using `--correct <old_id>` but letting `--event-id` fall back to the auto `<domain>-<date>` REUSES the superseded event's id → `ValueError: duplicate event id` from `append_event`. When correcting, pass an explicit new id (e.g. `--event-id fin-2026-08-13-v2`, `-v3`, ...). The skeleton in `references/forward_capture.md` now auto-suffixes `-vN` when `--correct` is set and no `--event-id` given. Also: `--correct` adds the old id to `supersedes` but does NOT copy the old payload — the new event carries ONLY the fields you pass, so the domain `summary.md` must be rewritten to merge both events into current state.
- **Session continuity**: the migration spans many sessions; the changelog + registry ARE the memory. Read them before acting; don't re-ask the user what phase they're on.
