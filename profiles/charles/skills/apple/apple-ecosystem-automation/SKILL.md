---
name: apple-ecosystem-automation
description: "Use when operating Apple/macOS user-facing apps and services from Hermes: Notes, Reminders, Messages, Find My, and GUI automation. Choose the subsection for the target app/tool and preserve app-specific safety rules."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [apple, macos, automation, notes, reminders, messages, findmy, computer-use]
    related_skills: []
---

# Apple Ecosystem Automation

## Overview

This is the umbrella for Apple/macOS-facing automation. Use it when the user asks Hermes to act through local Apple apps, macOS UI automation, or Apple-service CLIs. The old one-app skills are preserved under `references/source-packages/` so app-specific command syntax and safety notes remain available without fragmenting skill discovery.

## When to Use

- Create, search, or edit Apple Notes.
- Add, list, or complete Apple Reminders.
- Send, search, or receive iMessage/SMS through local macOS tooling.
- Track Apple devices/AirTags through Find My.
- Drive macOS GUI flows with computer-use/screenshot/action loops.

Do not use this for non-Apple productivity systems such as Google Workspace, Notion, or Airtable.

## Subsections

### Notes (`apple-notes`)
Use `memo` for create/search/edit. Confirm the local tool is installed and avoid pretending cloud access exists when the Mac-side bridge is unavailable.

### Reminders (`apple-reminders`)
Use `remindctl` for add/list/complete. Preserve natural-language due dates but verify what the CLI actually stored.

### Messages (`imessage`)
Use the local `imsg` bridge. Treat messages as external side effects: identify recipient precisely and avoid sending without explicit user intent.

### Find My (`findmy`)
Prefer reliable UI/screenshot automation when no stable API exists. Report uncertainty in locations and timestamps.

### macOS Computer Use (`macos-computer-use`)
Use the canonical observe-act-verify loop: capture screen, take one targeted action, capture again, and stop before risky irreversible changes.

## Package References

Full source packages are copied under `references/source-packages/<old-skill>/`.

## Common Pitfalls

1. Apple automation often depends on the user's Mac session, permissions, and logged-in Apple ID; verify availability before acting.
2. Do not conflate local CLI access with cloud/API access.
3. Messaging and GUI actions have user-visible side effects; keep scope explicit.

## Verification Checklist

- [ ] Confirmed the relevant local tool/app bridge exists.
- [ ] Used the app-specific reference package for exact commands.
- [ ] Verified the resulting note/reminder/message/location/UI state when possible.
