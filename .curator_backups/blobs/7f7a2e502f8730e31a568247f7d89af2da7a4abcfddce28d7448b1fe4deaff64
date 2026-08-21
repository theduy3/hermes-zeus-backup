# Planner extract → apply_planner_extract.py

```bash
python3 ~/.hermes/projects/remarkable-mcp/apply_planner_extract.py \
  --json extract.json [--dry-run] [--no-tasks] [--no-lifeos]
```

Sample: `~/.hermes/projects/remarkable-mcp/examples/sample-extract-2026-08-20.json`

## JSON (date required)

```json
{
  "date": "YYYY-MM-DD",
  "source_document": "2026 Planner",
  "pages_read": [551, 552, 69, 963, 964],
  "day_schedule_text": "...",
  "day_notes_text": "...",
  "tasks": [{"title": "...", "done": false, "due": "YYYY-MM-DD", "notes": "...", "skip_vault_task": true}],
  "goals": [{"title": "...", "area": "health", "status": "active", "note": "..."}],
  "exercise": {"done": true, "minutes": 45, "note": "..."},
  "meditation": {"done": true, "minutes": 10, "note": "..."},
  "raw_ocr": {"963": "..."},
  "confidence": "high|medium|low"
}
```

## Writes
| Output | Path / id |
|---|---|
| Mirror | `/vault/Tasks/planning/remarkable/<date>.md` |
| New tasks | `/vault/Tasks/tasks/rm-planner-<date>-<slug>.md` |
| Exercise | Life OS `thor-rm-<date>` via thor_log.py |
| Meditation | Life OS `med-rm-<date>` health observation |
| Goals | life_log.py `--kind goal` |

## Rules
- No inventing done/minutes from vague ink — raw_ocr only
- `skip_vault_task` when vault already has the item
- Same event id re-run needs supersede/correct
- All values OCR self_report
