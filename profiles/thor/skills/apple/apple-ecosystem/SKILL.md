---
name: apple-ecosystem
description: "Use when operating Apple/macOS personal productivity tools from Hermes: Notes, Reminders, iMessage/SMS, Find My, and GUI automation. Provides routing, safety, verification, and app-specific subsections instead of separate one-tool skills."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [apple, macos, notes, reminders, imessage, findmy, computer-use]
    related_skills: []
---

# Apple Ecosystem Operations

## Overview

Use this umbrella whenever a task touches Apple services or a local macOS UI: Apple Notes, Reminders, Messages/iMessage/SMS, Find My device location, or GUI-level computer use. These tools share the same operating constraints: they usually require a macOS host, account state is user-specific, and actions may create visible personal data or send messages.

Detailed historical procedures from absorbed narrow skills are preserved under `references/`:

- `references/apple-notes.md`
- `references/apple-reminders.md`
- `references/imessage.md`
- `references/findmy.md`
- `references/macos-computer-use.md`

## When to Use

- The user asks to create, search, update, or summarize Apple Notes.
- The user asks to create, list, complete, or clean up Apple Reminders.
- The user asks to send/read iMessage or SMS through a macOS bridge.
- The user asks where an Apple device, AirTag, or Find My item is.
- A workflow requires macOS GUI automation rather than a direct API/CLI.

Do not use for generic Google/Notion/Airtable productivity work, or for non-Apple messaging platforms.

## Routing Guide

| Task class | Primary route | Key checks |
|---|---|---|
| Notes | `memo` CLI / Apple Notes bridge | Confirm target folder/account before destructive edits. |
| Reminders | `remindctl` / Reminders bridge | Clarify due date/list only when not inferable. |
| Messages | `imsg` / Messages bridge | Verify recipient identity before sending. |
| Find My | FindMy.app or configured CLI bridge | Report timestamp and accuracy; do not overstate live precision. |
| GUI automation | macOS computer-use tools | Prefer direct CLI/API first; GUI is slower and stateful. |

## Shared Safety Rules

1. Treat all Apple operations as personal-data operations.
2. Before sending a message or making a destructive edit, verify the target and content.
3. Prefer reading current state before writing so the final answer can cite what actually changed.
4. When a bridge command is unavailable, report the missing prerequisite instead of inventing state.
5. For location data, include source timestamp and uncertainty when available.

## Verification Checklist

- [ ] Confirmed the macOS/Apple bridge command exists before relying on it.
- [ ] Read current state before modifying user data.
- [ ] Verified created/edited/sent item after the write where possible.
- [ ] Included timestamps for messages, reminders, or locations.
