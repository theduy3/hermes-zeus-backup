---
name: life-tracker
description: "Use when reading today, habits, goals, or private life data."
version: 1.0.0
tags: [habits, goals, metrics, private]
---
# Life Tracker

## Workflow
Use the local tracker at `/home/hermes/.hermes/projects/life-os/tracker`. Read current state before correction/deletion. Use the separate bearer credential only from its permission-600 secrets file; never reveal it.

Only log explicit completed/occurred reports. Preserve exact values, selected date, units, description, and estimated flag. Ask one focused question when missing detail materially changes a value. After writes/corrections, read the API back and report date, record, estimate status, and aggregate.

## Semantics
Scheduled habit days only count in completion rates; pauses/skips/unscheduled days are not failures. Missing metric values follow metric definitions. Never infer goal progress from elapsed time or activity volume.

## Verification
- [ ] Read before destructive change
- [ ] Validate schedule/type/range
- [ ] Read back API result
- [ ] Update Markdown authority if durable context changed
