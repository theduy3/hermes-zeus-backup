---
name: apple-platform-automation
description: Use when automating Apple/macOS personal productivity, messages, reminders, notes, Find My, or GUI workflows. Provides a single decision tree for native CLIs, AppleScript, and computer-use fallback.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [apple, macos, notes, reminders, imessage, findmy, computer-use]
    related_skills: []
---

# Apple Platform Automation

## Overview

This umbrella covers macOS/Apple workflows that used to be split across one-tool skills: Notes, Reminders, iMessage/SMS, Find My, and macOS GUI automation. Choose the most direct automation layer first, then fall back to AppleScript or visual computer-use when no CLI exists.

## When to Use

- The user asks to create, search, update, or summarize Apple Notes.
- The user asks to add/list/complete Apple Reminders.
- The user asks to send/read iMessage or SMS from macOS.
- The user asks to locate Apple devices, AirTags, or people through Find My.
- The user asks to operate a macOS app where no stable CLI/API exists.

## Decision Tree

1. Prefer a purpose-built CLI when installed: `memo` for Notes, `remindctl` for Reminders, `imsg` for Messages.
2. Use AppleScript/Shortcuts for simple app actions when the app exposes scriptable nouns.
3. Use visual computer-use for Finder/System Settings/Find My or GUI-only paths.
4. If running inside a Linux container or remote server, verify whether a macOS bridge exists before promising execution.

## Notes Workflow

- Use `memo` to create, search, and edit notes.
- Confirm the target folder/account when ambiguity could create duplicate personal/business notes.
- For large note edits, read the existing note first, prepare the replacement text, then write once.

## Reminders Workflow

- Use `remindctl` for list/add/complete/delete operations.
- Normalize natural-language dates before writing when the CLI is strict.
- For recurring tasks, state the recurrence explicitly and verify it after creation.

## Messages Workflow

- Use `imsg` for iMessage/SMS when available.
- Confirm recipient identity when multiple contacts match; do not send to a guessed phone/email.
- Keep messages plain-text unless the tool explicitly supports attachments.

## Find My Workflow

- Prefer explicit device/person names.
- Use AppleScript or GUI automation when no reliable CLI is available.
- Report timestamp and uncertainty; Find My locations may be stale.

## macOS Computer-Use Workflow

- Take a screenshot before each action batch.
- Use keyboard shortcuts and accessibility labels over fragile pixel clicks.
- After a write/send/delete action, verify the app state visually.

## Package Notes

The archived source packages preserve the original command details for `apple-notes`, `apple-reminders`, `imessage`, `findmy`, and `macos-computer-use`. Restore or consult them if a tool-specific command surface changes.

## Verification Checklist

- [ ] Confirmed this environment can access the relevant macOS app/tool.
- [ ] Used the most direct CLI/API available.
- [ ] Verified the post-action state before reporting success.
- [ ] Avoided guessing recipients, accounts, folders, or devices.
