---
name: apple-reminders
description: Manage Apple Reminders via remindctl CLI (list, add, complete, delete).
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Reminders, tasks, todo, macOS, Apple]
prerequisites:
  commands: [remindctl]
---

# Apple Reminders

Use `remindctl` to manage Apple Reminders directly from the terminal. Tasks sync across all Apple devices via iCloud.

## Prerequisites

Primary path:
- **macOS** with Reminders.app
- Install: `brew install steipete/tap/remindctl`
- Grant Reminders permission when prompted
- Check: `remindctl status` / Request: `remindctl authorize`

Fallback path when `remindctl` is unavailable:
- Use AppleScript via `osascript`
- Example create command:
  ```bash
  osascript -e 'tell application "Reminders" to make new reminder at end of default list with properties {name:"Buy milk", due date:(current date)}'
  ```
- This creates a reminder in the default list and returns an `x-apple-reminder://...` id

## When to Use

- User mentions "reminder" or "Reminders app"
- Creating personal to-dos with due dates that sync to iOS
- Managing Apple Reminders lists
- User wants tasks to appear on their iPhone/iPad

## When NOT to Use

- Scheduling agent alerts → use the cronjob tool instead
- Calendar events → use Apple Calendar or Google Calendar
- Project task management → use GitHub Issues, Notion, etc.
- If user says "remind me" but means an agent alert → clarify first

## Quick Reference

### View Reminders

```bash
remindctl                    # Today's reminders
remindctl today              # Today
remindctl tomorrow           # Tomorrow
remindctl week               # This week
remindctl overdue            # Past due
remindctl all                # Everything
remindctl 2026-01-04         # Specific date
```

### Manage Lists

```bash
remindctl list               # List all lists
remindctl list Work          # Show specific list
remindctl list Projects --create    # Create list
remindctl list Work --delete        # Delete list
```

### Create Reminders

```bash
remindctl add "Buy milk"
remindctl add --title "Call mom" --list Personal --due tomorrow
remindctl add --title "Meeting prep" --due "2026-02-15 09:00"
```

### Complete / Delete

```bash
remindctl complete 1 2 3          # Complete by ID
remindctl delete 4A83 --force     # Delete by ID
```

### Output Formats

```bash
remindctl today --json       # JSON for scripting
remindctl today --plain      # TSV format
remindctl today --quiet      # Counts only
```

## Date Formats

Accepted by `--due` and date filters:
- `today`, `tomorrow`, `yesterday`
- `YYYY-MM-DD`
- `YYYY-MM-DD HH:mm`
- ISO 8601 (`2026-01-04T12:34:56Z`)

## Rules

1. When user says "remind me", clarify: Apple Reminders (syncs to phone) vs agent cronjob alert
2. Always confirm reminder content and due date before creating
3. Use `--json` for programmatic parsing
4. Before using `remindctl`, check whether it is installed with `command -v remindctl`
5. If `remindctl` is missing but Reminders.app is available, fall back to `osascript` instead of failing
