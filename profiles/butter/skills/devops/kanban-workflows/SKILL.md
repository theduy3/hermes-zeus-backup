---
name: kanban-workflows
description: "Umbrella for Hermes Kanban orchestration and worker execution: decomposition, routing, lifecycle, anti-temptation rules, and worker pitfalls."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, orchestrator, worker, devops, task-routing, hermes]
---

# Kanban Workflows

Use this umbrella when operating a Hermes Kanban system, either as an orchestrator decomposing and routing work or as a worker executing assigned cards.

## Orchestrator role

- Decompose work into independently executable cards with acceptance criteria.
- Route work to the right lane/worker instead of doing implementation directly.
- Keep card scope small enough that completion and review are unambiguous.
- Track dependencies and blockers explicitly.

## Worker role

- Read the card, inspect required context, implement only the assigned scope, and update status with evidence.
- Follow the injected Kanban lifecycle when present; use this skill for pitfalls, examples, and edge cases that are too detailed for the system prompt.
- Report commands run, files changed, verification output, and blockers.

## Anti-temptation rule

An orchestrator should resist doing the work itself; a worker should resist widening scope. Escalate ambiguity rather than silently changing role or scope.

## Verification

A card is done only when acceptance criteria are met and backed by concrete artifacts: commits/diffs, logs, test output, deployed URLs, or a documented blocker.