---
name: autonomous-coding-agents
description: "Use when delegating implementation, review, or persistent work to autonomous coding agents: Claude Code, Codex, OpenCode, Hermes subagents, or Kanban workers/orchestrators."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agents, delegation, codex, claude-code, opencode, kanban, worktrees]
    related_skills: []
---

# Autonomous Coding Agents

## Overview

This umbrella covers the class of workflows where another agent or persistent worker does coding/review work: Claude Code CLI, OpenAI Codex CLI, OpenCode, Hermes `delegate_task`, and Kanban orchestrator/worker lanes. Choose the backend based on user preference, installed tools, task scope, and required persistence.

## When to Use

- The user asks to delegate coding, PR review, implementation, or debugging to an agent CLI.
- The task has independent workstreams that can be parallelized.
- Work should continue through a Kanban board or dedicated worker profile.
- A review/implementation loop benefits from a separate context.

Do not use this when a single direct tool call or a small local edit is faster and safer.

## Backend Decision Tree

1. Use Hermes `delegate_task` for synchronous subtasks that fit within this turn and need isolated context.
2. Use Claude Code, Codex, or OpenCode CLI only when installed and explicitly suitable for the repo/task.
3. Use background processes with completion notifications for long bounded CLI agent runs.
4. Use Kanban orchestration when work must persist beyond the current turn or involve multiple worker profiles.

## Operating Rules

- Pass full context: repo path, branch, failing command output, constraints, expected deliverable, and response language.
- Require verifiable handles for side effects: files changed, PR URL, issue URL, branch name, test output.
- Verify the child/agent's claims yourself before telling the user the work succeeded.
- Keep one source of truth for task state; do not mix ad-hoc delegation with Kanban unless the board is updated.

## Backend Notes

### Claude Code
Useful for feature implementation and PR work where Claude Code is configured. Use print mode for bounded tasks and PTY/background sessions for interactive workflows.

### Codex
Useful for implementation/review tasks, batch worktrees, and PR review when Codex CLI is configured. Prefer non-interactive one-shot invocations for bounded tasks.

### OpenCode
Useful for coding and PR review when OpenCode is the available local agent. Resolve the binary first and run with explicit repo context.

### Kanban
Use orchestrator skills for decomposition and workers for claimed cards. Respect profile/tenant isolation and provide summaries/metadata that let the board recover state.

## Archived Package References

Former narrow backend skills absorbed into this umbrella are preserved under `references/<old-skill-name>/` with original package contents intact.

## Common Pitfalls

- Delegating without enough context, causing agents to guess.
- Reporting a child agent's self-report as verified truth.
- Starting long-running agents without `notify_on_complete=true`.
- Doing the work yourself while pretending to orchestrate a Kanban lane.

## Verification Checklist

- [ ] Backend availability was checked.
- [ ] Delegated prompt included complete context and constraints.
- [ ] Agent output was independently verified where possible.
- [ ] Final result includes concrete artifacts and real execution/test output.
