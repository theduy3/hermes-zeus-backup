# Morning Briefing Pipeline Setup

Set up 2026-05-18 for Duy (Vancouver, true PST = UTC-8).

## Architecture

```
Catthew (family butler)          Zeus (personal assistant)
  5AM PST (13:00 UTC)              5:15AM PST (13:15 UTC)
  ↓→ family group chat             ↓→ Duy's Telegram DM
  (telegram:-5249331607)           (telegram:8446251233)
```

## Catthew Job — c729ba85e251

- **Profile:** catthew
- **Schedule:** `0 13 * * *` (13:00 UTC = 5AM PST = 6AM local during PDT)
- **Deliver:** origin → group chat "Catthew the Butler" (-5249331607)
- **Prompt includes:** family memory check, grocery-list.md, tasks.md, chores.md
- **Sign-off:** "At your service."

## Zeus Job — e6711b998b07

- **Profile:** zeus
- **Schedule:** `15 13 * * *` (13:15 UTC = 5:15AM PST = 6:15AM local during PDT)
- **Deliver:** telegram (home channel = 8446251233)
- **Skills:** obsidian (for vault task reading)
- **Prompt includes:**
  1. Read Catthew's latest output from `/home/hermes/.hermes/profiles/catthew/cron/output/c729ba85e251/`
  2. From Catthew section (2-3 household task bullets)
  3. Stocks (>2% movers + VIX/TNX)
  4. Obsidian tasks (overdue/today/this-week)
  5. Headlines (Morning Brew + finance)
  6. Weather (Vancouver BC, Laval QC, Quebec QC)
  7. Sagittarius horoscope
- **enabled_toolsets:** ["web", "memory", "skills", "terminal", "file"]

## Key Details

- **True PST** — user explicitly chose UTC-8 year-round, not local clock. During summer, runs at 6AM local.
- **Cross-profile reads** — Zeus reads Catthew's output via filesystem path; `context_from` does not work across profiles.
- **Duplicate cleanup** — removed Catthew job f0185ba512ba (5AM local to DM) since it conflicted with this pipeline.
- **15-min gap** between jobs ensures Catthew's output file is written before Zeus reads it.
