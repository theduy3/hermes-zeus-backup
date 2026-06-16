---
name: apple-ecosystem
description: "Use when operating Apple/macOS local apps and device services from Hermes: Notes, Reminders, iMessage/SMS, Find My, and GUI computer-use automation."
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

This umbrella covers Hermes workflows that operate Apple services and macOS apps through local CLIs, AppleScript, screenshots, or computer-use automation. Prefer it over narrow app-specific skills when the user asks for anything involving Apple Notes, Reminders, iMessage/SMS, Find My, or macOS GUI control.

## When to Use

- Create, search, edit, or organize Apple Notes.
- List, add, complete, or delete Apple Reminders.
- Send/read iMessages or SMS from a Mac.
- Locate devices/AirTags using Find My.
- Operate a macOS app with screenshots, AppleScript, or computer-use tools.

## Preconditions

1. Confirm the active environment is the Mac that has the relevant Apple account signed in.
2. Check whether the required helper exists before assuming it: `memo`, `remindctl`, `imsg`, AppleScript, screenshot capture, or computer-use tooling.
3. Treat local Apple data as sensitive. Avoid dumping full histories unless the user asked for them.

## App-Specific Playbooks

### Notes
Search before creating duplicates. For edits, read the current note first, patch only the requested content, and verify by reading it back.

### Reminders
List reminder lists when the target is ambiguous. Preserve due dates, recurrence, priority, and notes. Complete/delete only the item the user identified.

### iMessage/SMS
Resolve the recipient/chat before sending. Show a short draft and recipient when wording leaves room for a mis-send. Return only relevant excerpts for history lookup.

### Find My
Start with read-only methods. Prefer structured device names/statuses over screenshots in the final answer. Verify selected tab/device before reporting a location.

### macOS Computer Use
Use screenshots to ground each GUI action. Prefer app-native shortcuts/AppleScript when reliable; use clicks only when necessary. Re-screenshot after consequential actions.

## Common Pitfalls

1. Running Apple commands on Linux/VPS instead of a Mac host.
2. Assuming app state instead of reading/listing/capturing first.
3. Returning over-broad local data.
4. Mis-sending messages due to unresolved recipients.

## Verification Checklist

- [ ] Required helper/app was available in the active environment.
- [ ] Target account/list/chat/device was disambiguated.
- [ ] The action was verified after completion.
- [ ] Final response includes only the relevant outcome and blockers.
