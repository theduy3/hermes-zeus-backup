# Hermes Operations Daily Summary

Template and data-gathering workflow for the `weekday-hermes-vault-summary` cron job. Distinct from the "Daily Briefing" (market/task/weather) — this is an operations health report.

## Target Path

```
<vault>/Notes/Hermes Daily Summaries/Hermes Daily Summary YYYY-MM-DD.md
```

## Data Gathering Commands

Run these in parallel where possible:

```bash
hermes status 2>&1
hermes doctor 2>&1
hermes cron list 2>&1
hermes mcp list 2>&1
hermes gateway status 2>&1
```

Supplemental:
```bash
df -h <vault-mount> | tail -1          # Disk space
ls ~/.hermes/sessions/ 2>/dev/null | wc -l  # Session count
ls -lt ~/.hermes/logs/ | head -5            # Recent logs
tail -30 ~/.hermes/logs/errors.log | grep -i "error\|fail\|timeout\|warn" | tail -15
hermes --version 2>&1
```

## Frontmatter

```yaml
---
tags: [hermes, daily, operations, automation]
type: synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - "[[Hermes Agent Setup and Operations]]"
  - "[[Hermes Operations Dashboard]]"
wiki_status: complete
---
```

## Content Sections

### 1. Summary
2-3 sentence high-level overview. Include: environment (macOS/VPS), model provider, gateway PID, cron job count & status, any critical alerts.

### 2. What Ran Today
Bullet list of each cron job with:
- Job name in **bold**
- Schedule
- Last run status (✓ or ✗)
- Last run timestamp

### 3. Health Signals
Categorized bullet list:
- **Good (✓):** model, gateway, config version, Python, MCP servers
- **Warning (⚠):** auth gaps, disk space, pending updates, errors in logs
- Contrast against previous day's state when possible

### 4. Next Actions
Actionable bullet list, prioritized:
- **Immediate:** critical issues needing same-day attention
- **Today:** non-critical but time-sensitive
- **This week:** maintenance items

### 5. Related Notes
Wikilinks to related vault pages:
- [[Hermes Agent Setup and Operations]]
- [[Hermes Operations Dashboard]]
- [[AI Agent Tooling MOC]]

## Pitfalls

- **Vault path mismatch:** The cron prompt may specify `/root/theduyvault` (VPS), but on macOS the vault lives at `/Users/theduy/theduyvault`. Use `mcp_obsidian_fs_list_allowed_directories` to discover the actual path, or probe `/Users/theduy/theduyvault` on macOS. Do NOT claim success writing to an unreachable path.
- **Overwriting existing:** This cron job may run multiple times per day. Always overwrite the existing file with fresh data — the note represents current state, not append-only.
- **Stale gateway PID:** The gateway PID changes across restarts. Always capture the current PID from `hermes gateway status`, don't copy from an earlier note.
- **Cron job last-run times are in UTC:** `hermes cron list` shows UTC times. The note title date should use local date. Convert mentally but don't alter the raw values in the note.
