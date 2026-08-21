---
name: remarkable-device-sync
description: "Use when wiring reMarkable MCP or planner habit sync."
version: 1.0.0
author: Hermes Agent (curator)
license: MIT
metadata:
  hermes:
    tags: [remarkable, mcp, planner, habits, telegram, life-os, vault]
    category: productivity
    related_skills: [external-mcp-integrations, native-mcp, life-tracker, life-knowledge-base]
---

# reMarkable ↔ Hermes (MCP + planner sync)

Class playbook for (1) wiring reMarkable as an MCP library Hermes can query from Telegram/CLI, and (2) structured sync of the **2026 Planner** into theduyvault + Life OS without inventing data.

Companion MCP install notes also live under `external-mcp-integrations` / `references/remarkable-mcp.md` when that skill is available.

## When to use

- Install or debug SamMorrowDrums (or other) reMarkable MCP on Hermes
- Telegram/CLI questions about reMarkable notebooks
- Daily planner sync: goals, tasks, **exercise** (p963), **meditation** (p964)
- User notes that Telegram already surfaces vault Tasks — feed that authority, do not fork a second task system

## Authority split

| Content | Authority |
|---|---|
| Dated actionable tasks | `/vault/Tasks/` |
| Daily plan cards | `/vault/Tasks/planning/` |
| Planner OCR mirrors | `/vault/Tasks/planning/remarkable/YYYY-MM-DD.md` |
| Exercise / meditation observations | Life OS `30-health/` (`thor_log` / health observation) |
| Strategic goals context | Life OS `70-goals/` (`life_log.py`) |
| Freeform notebook Q&A | Live MCP read only (no auto bulk copy) |

**Never invent** habit completions, minutes, or tasks. Ambiguous OCR → `raw_ocr` in the mirror only; skip Life OS habit fields.

## MCP install (cloud / remote Hermes)

1. Connect subscription required (not a Claude sub).
2. Code: https://my.remarkable.com/device/desktop/connect
3. Register as gateway OS user:
   ```bash
   uvx --from git+https://github.com/SamMorrowDrums/remarkable-mcp \
     remarkable-mcp --register CODE
   ```
4. Add server (default profile = Telegram):
   ```bash
   hermes mcp add remarkable \
     --command uvx \
     --args --from git+https://github.com/SamMorrowDrums/remarkable-mcp remarkable-mcp \
     --connect-timeout 120
   ```
   If `~/.rmapi` not visible to gateway: `--env REMARKABLE_TOKEN=...`
5. Restart gateway / new session — tools do not hot-inject mid-chat.
6. Smoke: status → browse/search → read/image a known page.

Prefer **SamMorrowDrums**. Skip remarkable-brain-style Anthropic-hardwired extractors when user is OpenAI-only. USB mode only if this host can reach the tablet.

See `references/mcp-setup.md`.

## 2026 Planner page map

Code: `~/.hermes/projects/remarkable-mcp/page_map.py`  
`python3 …/page_map.py YYYY-MM-DD` · `…/page_map.py check`

| Layer | Formula |
|---|---|
| Year 2–3 | calendar=2, goals=3 |
| Quarter Q | `2+2Q`, `3+2Q` |
| Month M | `10+2M`, `11+2M` |
| Week W | `35+W` |
| Day | schedule `89+(DOY−1)×2`, notes +1 |
| Exercise | **963** fixed |
| Meditation | **964** fixed |

Anchors: p2 year cal; p69=W34; p550=Aug19 notes; p551=Aug20 schedule. Date context: America/Toronto unless overridden.

Daily pull minimum: day schedule+notes, week page, 963, 964. Month on Mondays/1st; quarter/year on quarter/year starts.

Detail: `references/page-map.md`.

## Planner sync pipeline

```
page_map → MCP read/OCR pages → extract JSON (confident fields only)
  → apply_planner_extract.py [--dry-run]
       ├─ mirror: /vault/Tasks/planning/remarkable/<date>.md
       ├─ new tasks only: /vault/Tasks/tasks/rm-planner-… (skip if already in vault)
       └─ Life OS: thor-rm-<date>, med-rm-<date>, optional life_log goals
```

```bash
python3 ~/.hermes/projects/remarkable-mcp/apply_planner_extract.py \
  --json /path/to/extract.json --dry-run
```

Extract schema: `references/extract-schema.md`  
Sample: `~/.hermes/projects/remarkable-mcp/examples/sample-extract-2026-08-20.json`

### Extraction rules

- Exercise/meditation: clear mark/minutes for **that date** on grids only
- Tasks: explicit actions; set `skip_vault_task: true` when vault already has them
- Goals: only when year/quarter/month goal pages were read; strategic → Life OS, not task spam
- Epistemic: OCR `self_report`; re-run same event id needs supersede/correct

## Telegram Q&A (rest of notes)

1. MCP status → browse/search/recent
2. read/image (+ OCR/vision as needed)
3. Answer with notebook name, path, page, short quote
4. Commitments questions → also check `/vault/Tasks` + Life OS (Telegram's existing surface)

## Cron (only after smoke)

Load this skill; Toronto date; page_map + MCP + apply; short digest (habits, new tasks, ambiguities). Optional silent tick if extract hash unchanged. Do not enable until cloud auth works.

## Pitfalls

- Connect missing; USB on remote host; wrong profile; no gateway restart
- Tokens in chat/git; full-library OCR in cron
- Duplicate vault tasks; inventing habit done from scribbles
- Conflating live Q&A with structured planner apply

## Verification

- [ ] `page_map.py check` OK
- [ ] MCP status OK on Telegram profile
- [ ] Dry-run apply produces expected paths
- [ ] Real apply only after confident extract
- [ ] Non-planner Q&A cites page without vault spam

## Related

- Project handoff: `~/.hermes/projects/remarkable-mcp/RESUME.md`
- Session: @session:default/20260820_183206_0f8a25
- Overlap: session-created `remarkable-2026-planner` is user-owned and duplicates this class — prefer this curator skill; `hermes curator adopt remarkable-2026-planner` if keeping both
