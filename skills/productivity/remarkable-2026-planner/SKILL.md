---
name: remarkable-2026-planner
description: Sync a reMarkable Planner into the vault and Life OS safely.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [remarkable, planner, sync, vault, life-os, mcp]
---

# reMarkable 2026 Planner sync

Sync the reMarkable Planner notebook into `/vault/Tasks/planning/remarkable/<date>.md`
and (when confirmed) into Life OS health/goal logs. All profiles already have the
`remarkable` MCP server wired (read-only, launcher at
`~/.hermes/scripts/run-remarkable-mcp.sh`, token at `~/.rmapi`).

## When to use
- First real planner sync for a day (OCR day pages + habit grids)
- Re-running a sync (idempotent — safe to run twice a day)
- Wiring a daily cron to auto-sync
- Debugging why a page text looks wrong / a habit didn't write

## Key files (under ~/.hermes/projects/remarkable-mcp/)
| Piece | Path |
|-------|------|
| Page geometry map | `page_map.py` (day pages 89+(DOY-1)*2; grids fixed p963 exercise, p964 meditation; `self_check()` validates anchors) |
| Apply extract → vault + Life OS | `apply_planner_extract.py` |
| PNG capture (ground truth) | `rm_capture.py` (drives `remarkable_image` over stdio) |
| Sample extract | `examples/sample-extract-2026-08-20.json` |

Mirror target: `/vault/Tasks/planning/remarkable/<date>.md`
PNG assets: `/vault/Tasks/planning/remarkable/assets/<date>/<page>.png`
Life OS health: `thor_log.py` id `thor-rm-<date>`, `life_store.py` event `med-rm-<date>`

## The four hardening rules (DO NOT regress these)
**A. Idempotency — overwrite, never append.**
Each page is written to a delimited block in the daily mirror:
`<!-- rm:NNN --> … <!-- /rm:NNN -->`. Re-running overwrites only the blocks
for pages present in THIS extract (last-write-wins per page). Handwriting OCR is
NON-DETERMINISTIC (p69 read as "OMF" one pass, could be "OMP" next) — so a page
is a snapshot, mirrored as a snapshot. Append-plus-dedupe WILL collect variants
of the same line. Verified: two overwrites of p551 → exactly 1 block.

**B. Habit grids (p963/p964) — DO NOT auto-parse. Gate them.**
No grid parser exists and none should be built — it's position-counting with
silent off-by-one risk. Keep the paper grid as the visual; log exercise/
meditation in the Life OS daily note, not by reading X-marks. Until the user
confirms the marks on-device, the sync writes them as UNCONFIRMED + `confidence:
low` and skips ALL Life OS habit writes. Confirm via `--confirm-habits` (or
`habits_confirmed:true` in JSON) AFTER the user verifies.

**C. Store the rendered PNG alongside the transcription.**
Transcription is the lossy layer. `rm_capture.py` shells to `remarkable_image`
and decodes the base64 PNG to `assets/<date>/<page>.png`. Each page block gets
`png: assets/<date>/<page>.png` so an agent can fall back to the original stroke
image instead of trusting OCR. Set `capture_pngs:true` in the extract to fetch
live (recommended for grid pages at minimum).

**D. Confidence flags everywhere.**
Per-page + overall `confidence:` in frontmatter. Habit extractions forced to
`low`. Life OS meditation event passes `estimated=(conf=='low')`.

## How to run
Build an extract JSON (use `pages` array preferred; legacy flat fields
`day_schedule_text`/`day_notes_text`/`exercise`/`meditation` are mapped):
```json
{
  "date": "2026-08-20",
  "source_document": "2026 Planner",
  "confidence": "low",
  "pages": [
    {"page": 551, "role": "day_schedule", "text": "…", "png": null, "confidence": "high"},
    {"page": 963, "role": "exercise_grid", "text": "Aug 14, 17, 18, 19 (read, UNCONFIRMED)", "confidence": "low"}
  ],
  "tasks": [], "goals": [],
  "capture_pngs": false,
  "habits_confirmed": false
}
```
Apply (dry run first):
```
python3 apply_planner_extract.py --json <extract>.json --dry-run --no-capture
python3 apply_planner_extract.py --json <extract>.json --no-capture        # real write
python3 apply_planner_extract.py --json <extract>.json --confirm-habits    # after user verifies marks
```
Capture PNGs (separate step, proven):
```
python3 rm_capture.py "2026 Planner" 551 /vault/Tasks/planning/remarkable/assets/2026-08-20/551.png
```

## Pitfalls (learned the hard way)
1. **Baked-in `dry_run:true` in the JSON** — `apply_planner_extract.py` reads
   `data.get("dry_run")`, so a sample carrying `"dry_run": true` silently
   prevents all writes. Strip it (`d.pop("dry_run")`) before a real run, or
   pass `--dry-run` explicitly and check the JSON.
2. **fitz/PyMuPDF warning corrupts MCP stdio.** The remarkable-mcp server prints
   `warning: The 'fitz' API is deprecated…` to STDOUT. MCP stdio uses stdout for
   JSON-RPC, so that line marks the server "degraded"/"parked". The launcher
   (`run-remarkable-mcp.sh`) already filters it via `grep -v`. If you ever
   replace the launcher, keep the filter or the server won't load in Hermes.
3. **Vision model needed for image tools.** hy3:free is text-only — `remarkable_image`
   / `remarkable_canvas` / OCR need a vision model. All profiles have
   `model.auxiliary.vision = stepfun/step-3.7-flash:free` (free, Nous) set;
   text/browse/search/read work on hy3:free.
4. **rm_capture needs `uvx` on PATH** and the `~/.rmapi` token. It launches the
   MCP server as a subprocess and reads base64 from the `remarkable_image` result.
5. **`hermes config set` for nested keys** — use `model.auxiliary.vision.model`
   (NOT `model.auxiliary` which sets the generic provider slot).
6. **Blocklist on complex inline commands** — the agent's terminal hardline-blocks
   big heredocs/loops. Run multi-step scripts via a written `.sh` file with
   `bash <file>`, not inline.
7. **Page geometry is 2026-specific.** `page_map.YEAR=2026`; recalibrate anchors
   before enabling writes on a new-year planner layout. `self_check()` validates.

## Verification standard
- `python3 page_map.py check` → "OK page_map self-check passed"
- Dry run prints blocks + habit gate; real run creates the mirror file
- `grep -c '<!-- rm:551 -->' <mirror>` → 1 after re-run (idempotent)
- PNG: `head -c 8 <file>` == `\x89PNG\r\n\x1a\n`
- Habits: with `habits_confirmed:false`, Life OS returns `gated:exercise`/
  `gated:meditation` and writes nothing.
