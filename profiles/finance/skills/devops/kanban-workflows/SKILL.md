---
name: kanban-workflows
description: Use when orchestrating or executing Hermes Kanban board work, including decomposition, worker behavior, claims, summaries, metadata, and blocked-card handling.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [kanban, orchestration, workers, delegation, devops]
    related_skills: []
---

# Kanban Workflows

## Overview

This umbrella covers both sides of Hermes Kanban work: the orchestrator that decomposes/routs work through a board and the worker that claims, executes, updates, blocks, and summarizes cards. The central rule is role discipline: orchestrators coordinate; workers execute their claimed card.

## When to Use

- A task should be decomposed across a Kanban board rather than done inline.
- You are acting as an orchestrator assigning or sequencing work.
- You are acting as a worker claiming/executing a card.
- A card is blocked, stale, ambiguous, or missing useful metadata.

## Orchestrator Playbook

- Decompose work into independently claimable cards with clear definitions of done.
- Avoid doing worker tasks yourself; update the board and let workers execute.
- Sequence cards by dependency, not by convenience.
- Include enough context for a worker with no chat history to start safely.

## Worker Playbook

- Claim only cards you can actually execute.
- Inspect workspace and instructions before editing.
- Keep updates concise: status, evidence, blockers, next handoff.
- Include changed files, commands run, results, and artifact handles in the final summary.

## Blocked Work

Good block reasons include missing credentials, ambiguous scope, failing prerequisite, unavailable service, or conflicting repo state. A blocker should say exactly what decision or resource is needed.

## Metadata Shape

A useful card/summary includes: goal, repo/path, constraints, owner, dependencies, verification command, artifact URL/path, and completion criteria.

## Pitfalls

- Orchestrator temptation: solving the task instead of routing it.
- Worker temptation: broadening scope beyond the card.
- Silent failure: not updating the board when blocked.
- Weak handoff: summary lacks evidence or file paths.

## Verification Checklist

- [ ] Card scope and definition of done are explicit.
- [ ] Role boundaries were followed.
- [ ] Board state reflects current truth.
- [ ] Completion/blocker summary includes actionable evidence.
