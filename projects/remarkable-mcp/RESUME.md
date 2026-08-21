---
type: handoff
status: cloud-connected-telegram-needs-new-session
session: "@session:default/20260820_183206_0f8a25"
updated: 2026-08-20
---

# Resume: reMarkable MCP + Planner sync

## Live status
- Cloud token registered at `~/.rmapi` (chmod 600)
- Hermes MCP server **remarkable** enabled (read-only)
- Launcher: `~/.hermes/scripts/run-remarkable-mcp.sh`
- `hermes mcp test remarkable` → 8 tools, connected
- Library smoke: **7 documents**, folder `The Economist`
- Planner resolved: **`2026 Planner`** (match rule: any title containing `Planner`)
- Search/read of planner content works (cover + year calendar text seen)

## User rules locked in
1. Auth code used (one-time; do not reuse)
2. Planner notebook = any name containing **Planner** (2026/2027/2028…)
   - `page_map.pick_planner_document()` prefers working year, else newest year in title
   - Page geometry still calibrated for **2026** layout; recalibrate before habit writes on a new-year layout

## Paths
| Piece | Path |
|---|---|
| Page map | `~/.hermes/projects/remarkable-mcp/page_map.py` |
| Apply extract | `~/.hermes/projects/remarkable-mcp/apply_planner_extract.py` |
| Skill | `remarkable-2026-planner` |
| Mirror target | `/vault/Tasks/planning/remarkable/YYYY-MM-DD.md` |
| Life OS exercise | `thor_log.py` id `thor-rm-<date>` |
| Life OS meditation | event `med-rm-<date>` |

## Telegram
MCP tools inject on **new** gateway sessions after restart. Ask in Telegram:
- "list my remarkable notebooks"
- "read today's 2026 Planner schedule page"
- "search remarkable for …"

## Next (optional)
1. First real planner sync for today (OCR exercise/meditation grids 963/964 + day pages)
2. Daily cron digest → Telegram
3. When 2027 Planner appears: confirm page anchors before enabling habit auto-write
