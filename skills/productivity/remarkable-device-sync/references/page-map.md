# 2026 Planner page map

Code: `~/.hermes/projects/remarkable-mcp/page_map.py`
```bash
python3 ~/.hermes/projects/remarkable-mcp/page_map.py check
python3 ~/.hermes/projects/remarkable-mcp/page_map.py YYYY-MM-DD
```

## Formulas (1-based, year 2026)

| Layer | Pages | Formula |
|---|---|---|
| Year | 2–3 | 2 calendar, 3 goals |
| Quarter Q=1..4 | 4–11 | `2+2Q`, `3+2Q` |
| Month M=1..12 | 12–35 | `10+2M`, `11+2M` |
| Week W ISO | 36–88 | `35+W` |
| Day DOY | 89–818 | schedule `89+(DOY−1)×2`; notes +1 |
| Exercise | 963 | fixed grid |
| Meditation | 964 | fixed grid |

## Anchors (self-checked)
- p2 year calendar
- p69 = Week 34
- p550 = 2026-08-19 notes
- p551 = 2026-08-20 schedule (notes 552)

## Daily sync set
Always: day schedule+notes, week page, 963, 964.
Also: month on Mondays and day=1; quarter on Q starts; year early January.
Timezone for "today": America/Toronto unless user overrides.
