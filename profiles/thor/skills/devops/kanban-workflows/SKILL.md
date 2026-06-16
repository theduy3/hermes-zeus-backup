---
name: kanban-workflows
description: "Use when operating Hermes Kanban-style work routing, including orchestrator decomposition and worker execution. Consolidates orchestrator and worker playbooks into one class-level workflow."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [kanban, orchestration, workers, devops, hermes]
    related_skills: [workspace-dispatch, ai-coding-agents]
---

# Kanban Workflows

## Overview

Use this umbrella for Hermes Kanban workflows: breaking missions into cards, routing work to worker profiles, enforcing worker lifecycle expectations, and collecting verified outputs. Detailed historical playbooks are preserved in:

- `references/kanban-orchestrator.md`
- `references/kanban-worker.md`

## When to Use

- The user asks to run or design a Kanban worker lane.
- A mission needs decomposition into cards with ownership and acceptance criteria.
- You need to explain orchestrator vs worker responsibilities.
- A worker has produced ambiguous, incomplete, or unverifiable output.

## Roles

### Orchestrator

- Convert a mission into small cards with explicit definitions of done.
- Assign each card to a suitable lane/worker.
- Prevent scope creep by splitting follow-ups into new cards.
- Verify outputs and integrate them into the parent mission.

### Worker

- Accept one card at a time.
- Gather local context before editing.
- Produce concrete artifacts and verification output.
- Report blockers early with evidence, not speculation.

## Operating Rules

1. Cards should be independently verifiable.
2. Workers should not silently broaden scope.
3. Orchestrators must not trust worker self-reports without handles, diffs, logs, or files.
4. Prefer small reversible changes over large ambiguous work dumps.
5. Preserve links between cards, artifacts, and verification output.

## Verification Checklist

- [ ] Each card has a clear owner and definition of done.
- [ ] Worker output includes concrete artifacts or command output.
- [ ] Integration was checked after worker completion.
- [ ] Follow-up work is tracked separately rather than hidden in the summary.
