---
name: apple-ecosystem-automation
description: "Use when operating macOS Apple ecosystem surfaces: Notes, Reminders, iMessage/SMS, Find My, or GUI-only Apple apps through computer-use automation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [apple, macos, notes, reminders, imessage, findmy, computer-use]
    related_skills: []
---

# Apple Ecosystem Automation

## Overview

This umbrella covers class-level workflows for Apple services that are only available from a macOS host or Apple-authenticated CLI: Notes, Reminders, Messages/iMessage, Find My, and GUI-only app automation. Treat each service as a labeled mode under one macOS capability class instead of separate micro-skills.

## When to Use

- The user asks to create/search/update Apple Notes or Reminders.
- The user asks to send or inspect iMessage/SMS from a Mac.
- The user asks to locate Apple devices, AirTags, or Find My items.
- The user needs browser/computer-use style interaction with macOS apps.

Do not use this for cloud productivity services such as Google Workspace, Notion, Airtable, or Microsoft/Teams.

## Prerequisite Checks

1. Confirm this session has access to the user's macOS machine or an SSH target where the relevant CLI exists.
2. Check for the service CLI before acting: `memo` for Notes, `remindctl` for Reminders, `imsg` for Messages, and AppleScript/Peekaboo-style tooling for Find My/UI automation.
3. Prefer dry listing/search commands before mutating notes, reminders, or messages.
4. Never invent message delivery, note IDs, or device locations; report the exact command output or a blocker.

## Modes

### Notes
Use the `memo` CLI for create/search/edit flows. Search first when updating an existing note. Preserve note titles and avoid destructive rewrites unless the user explicitly asked for replacement.

### Reminders
Use `remindctl` for list/add/complete/delete. Normalize natural-language due dates conservatively and echo the parsed date/time before destructive changes when ambiguity matters.

### Messages / iMessage
Use `imsg` where available. Verify the recipient and transport (iMessage vs SMS) before sending. Keep message text plain unless the CLI supports attachments and the user requested media.

### Find My
Use AppleScript, screenshots, or computer-use tooling to query Find My when no direct API exists. Treat coordinates and addresses as live observations that require verification from the UI or tool output.

### macOS Computer Use
For GUI-only flows, capture the screen, identify the active window, then perform one small action at a time. Re-capture after each action rather than assuming state.

## Archived Package References

Former narrow skills absorbed into this umbrella are preserved under `references/<old-skill-name>/` with their original SKILL.md and any support files intact.

## Common Pitfalls

- Running Apple-specific commands on a Linux Hermes host with no macOS bridge.
- Assuming iCloud web access is equivalent to local Apple CLI access.
- Marking reminders complete or sending messages without first verifying the target item/person.
- Treating Find My screenshots as precise telemetry; always label uncertainty.

## Verification Checklist

- [ ] Required CLI or GUI automation path exists.
- [ ] Target note/reminder/person/device was verified before mutation.
- [ ] Final response includes real command/UI output or explicitly states the blocker.
