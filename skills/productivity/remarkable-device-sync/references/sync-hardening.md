# Sync hardening — reMarkable planner mirror

Captured 2026-08-20. The production `apply_planner_extract.py` lives at
`~/.hermes/projects/remarkable-mcp/apply_planner_extract.py`. This note
documents the three hardening decisions and WHY, so a future session doesn't
reintroduce the bugs.

## A. Idempotency — overwrite, never append

Problem: a twice-daily sync re-reads pages the morning run already captured.
Appending + deduping FAILS because handwriting OCR is non-deterministic — a
page read as "OMF" one pass may come back "OMP" the next, so a content hash
never matches and variants accumulate.

Fix: each page is written inside a delimited block in the daily mirror:

    <!-- rm:551 --> …transcription… <!-- /rm:551 -->

`replace_blocks()` overwrites only the blocks for pages present in THIS run
(last-write-wins per page). Pages absent from this run are left untouched.
The whole file is regenerated only on first creation; subsequent runs patch
blocks in place. Verified: two overwrites of page 551 → exactly ONE block,
final has the later text.

## B. Habit grids (p963/p964) — confirmation gate, no positional parse

The exercise/meditation grids are 14×27 X-marks with no text anchors. Reading
them is pure position-counting and an off-by-one is silent. We do NOT build a
grid parser.

- Grid marks are written into the mirror as UNCONFIRMED + `confidence:low`.
- Life OS habit writes (thor_rm-<date>, med-rm-<date>) are SKIPPED unless the
  run passes `--confirm-habits` (or `habits_confirmed:true`).
- The sync prints the marks read so the user can verify them on the device
  before anything downstream consumes them.

If a user ever wants positional parsing, treat it as low-confidence and gate
it behind manual confirm — never auto-write to Life OS.

## C. Store the rendered PNG next to the transcription

The OCR text is the lossy layer. Each page block can carry
`png: assets/<date>/<page>.png` — a rendered stroke image captured via the MCP
`remarkable_image` tool. An agent hitting ambiguous text can fall back to the
original image instead of trusting the reading. Capture driver: `scripts/rm_capture.py`.

## D. Confidence flags

Per-page `confidence:` + overall frontmatter `confidence:`. Habit extractions
forced to `low`. Life OS meditation event passes `estimated=` based on
confidence so downstream agents know not to trust low-confidence health data.

## Verification recipe (reproducible)
```
cd ~/.hermes/projects/remarkable-mcp
# dry run shows habit gate firing, no Life OS writes:
python3 apply_planner_extract.py --json examples/sample-extract-2026-08-20.json --dry-run --no-capture
# real write (habits gated):
python3 apply_planner_extract.py --json /tmp/real-extract.json --no-capture
# re-run → still one <!-- rm:NNN --> block per page (idempotency)
grep -c '<!-- rm:551 -->' /vault/Tasks/planning/remarkable/2026-08-20.md
# capture ground-truth PNG:
python3 rm_capture.py "2026 Planner" 551 /vault/Tasks/planning/remarkable/assets/2026-08-20/551.png
```
