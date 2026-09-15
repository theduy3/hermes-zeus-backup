# Life OS migration — full gated plan (approved)

Target architecture:
- Life OS = current truth: plans, health, finance, investments, goals, habits,
  projects, reviews, current personal context.
- theduyvault = original documents, historical notes, research library, daily
  journals, raw captures, task archive, source evidence.
- Tracker = operational UI/cache derived from Life OS Markdown.

Phase order (advance one at a time; later phases may depend on earlier):
1. Foundation/hardening — Markdown write authority, append-only dated ledgers,
   every tracker write updates Markdown first then rebuilds SQLite, deterministic
   rebuild/reconcile/backup/restore tests, remove test data.
   EXIT CRITERION: deleting tracker.sqlite3 and rebuilding from Markdown yields
   the same operational state (reconcile.ok == True).
2. Migration registry — one manifest per source (path, owner profile, sensitivity,
   date range, target note, status queued->imported->verified->cut_over->archived).
   Nothing deleted from theduyvault. Every claim source-linked. Baseline checkpoint.
3. Thor pilot (health/wellness) — forward-only live tracking; no backfill.
   CUT_OVER 2026-08-13 (first event thor-2026-08-13).
4. Finance current state — liquid CAD, monthly in/out, liabilities, goals,
   uncertainties, review cadence. Current values only, not full history.
   GATED on real numbers.
5. Charles investments — after Finance liquidity set: portfolio rules, risk limits,
   theses, decisions, review triggers. References Finance; never overwrites it.
6. Goals/projects/execution — vault Tasks stays authority initially.
7. Catthew household/family — privacy-limited (no child/spouse/identity beyond required).
8. Butter rewards — after Finance current state.
9. Wiki transition — read-only legacy cross-reference markers only.

Profile routing (raw vault -> Life OS write when):
Wiki=never autonomous (source links only); Thor=health/protocol/metric change;
Finance=obligation/state/decision change; Charles=thesis/risk/decision change;
Zeus=cross-domain priority/goal/project change; Catthew=household/family change;
Butter=card/reward strategy change; Default=resolves routing/conflicts.

Hard rule: do NOT fabricate data. Pilot/capture runs only with approval AND a real
traceable source. Inbox remains the sole raw-capture funnel; newsletters/research
stay in theduyvault as evidence.
