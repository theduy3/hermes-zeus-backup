---
name: kanban-workflows
description: "Use when operating Hermes Kanban workflows as orchestrator or worker: decomposition, card lifecycle, worker summaries, heartbeats, blockers, tenant isolation, and stuck-card recovery."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [kanban, orchestration, workers, devops, hermes]
    related_skills: [hermes-agent]
---

# Kanban Workflows

## Overview

This umbrella combines the Hermes Kanban orchestrator and worker playbooks. The injected runtime guidance remains authoritative at execution time; use this skill for pitfalls, patterns, and examples.

## When to Use

- Decompose a multi-step job into Kanban cards.
- Act as a Kanban worker and need workspace/heartbeat/blocker conventions.
- Recover stuck workers or clarify summaries/metadata.

## Roles

### Orchestrator
Route work through the board when persistence, parallelism, or independent worker ownership matters. Decompose into bounded cards and avoid doing the work yourself.

### Worker
Respect workspace isolation, claim only appropriate cards, report useful heartbeats, and return summaries with evidence/metadata.

## Verification Checklist

- [ ] Correct role selected: orchestrator or worker.
- [ ] Board/card state checked before action.
- [ ] Completion summary includes concrete artifacts, tests, and blockers.
