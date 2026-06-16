---
name: apple-ecosystem-automation
description: "Umbrella for macOS and Apple ecosystem automation: Notes, Reminders, iMessage/SMS, Find My, and background desktop control."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [apple, macos, notes, reminders, imessage, findmy, computer-use, automation]
---

# Apple Ecosystem Automation

Use this skill for user requests involving Apple-native data or macOS UI control: Apple Notes, Reminders, iMessage/SMS, Find My devices/AirTags, or background computer-use actions.

## Safety and prerequisites

- Confirm the task is intended for the local macOS account and has permission to access the relevant app/data.
- Prefer dedicated CLIs when available; use background desktop control only when APIs/CLIs cannot accomplish the task.
- For messages and reminders, show exact content and recipient/list when ambiguity would create external side effects.

## Apple Notes

Use the memo CLI pattern for creating, searching, and editing notes. Preserve note titles and user organization; avoid broad destructive edits without explicit confirmation.

## Apple Reminders

Use the remindctl pattern for listing, adding, completing, and deleting reminders. Record list names, due dates, recurrence, and priority explicitly.

## iMessage/SMS

Use the imsg CLI pattern to send and receive iMessages/SMS. Resolve contacts carefully and treat message sending as an external side effect requiring clear target/content.

## Find My

Use Find My automation for locating devices or AirTags. Report timestamps and uncertainty; location data can be stale.

## macOS computer use

Use background screenshots, mouse, keyboard, scroll, and drag only when CLI/API routes are unavailable. Avoid stealing focus or changing Spaces when the background-control tooling supports non-invasive operation.