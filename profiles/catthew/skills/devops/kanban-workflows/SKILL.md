---
name: kanban-workflows
description: "Use when operating Hermes Kanban orchestration or worker flows: decomposing work, creating/claiming cards, reporting heartbeats, blocking, and handing off results."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [kanban, orchestration, workers, task-routing, hermes]
    related_skills: [coding-agent-delegation]
---

# Hermes Kanban Workflows

## Overview

This umbrella covers both sides of Hermes Kanban: orchestrators that decompose and route work, and workers that claim cards, execute bounded tasks, heartbeat, block, and report results. The core rule is role discipline: orchestrators coordinate; workers execute the card they claimed.

## When to Use

- A Hermes profile is operating as a Kanban orchestrator or worker.
- Work needs decomposition, dependency ordering, or multiple specialized workers.
- A worker needs guidance on claiming, status updates, blocking, or final summaries.

## Orchestrator Pattern

1. Understand the goal and constraints.
2. Sketch the task graph: independent tasks, dependencies, acceptance criteria, and handoff artifacts.
3. Create cards with clear owner expectations and enough context to execute without chat history.
4. Monitor board state and unblock workers with concise answers.
5. Integrate results and verify the final artifact.

## Worker Pattern

1. Claim only cards you can complete.
2. Read the full card and linked artifacts before acting.
3. Work in the assigned workspace/tenant; do not cross-contaminate paths or credentials.
4. Heartbeat when the task is long or state changes materially.
5. If blocked, state the precise missing input and the smallest useful next question.
6. Final summary should include artifacts, commands run, verification, and residual risks.

## Good Card Shape

- Goal: one bounded deliverable.
- Context: repo/path, relevant files, user constraints, prior attempts.
- Acceptance criteria: commands, tests, output format, evidence required.
- Dependencies and safety limits.

## Common Pitfalls

1. Orchestrator doing the work instead of routing/integrating.
2. Vague cards that require parent-chat context.
3. Block reports without an exact missing decision or artifact.
4. Treating board completion as proof without verification.

## Verification Checklist

- [ ] Cards have enough context and acceptance criteria.
- [ ] Workers stayed inside assigned workspaces/tenants.
- [ ] Blockers were specific and actionable.
- [ ] Final integration verified actual artifacts.
