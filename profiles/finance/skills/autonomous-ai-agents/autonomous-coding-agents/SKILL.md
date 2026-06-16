---
name: autonomous-coding-agents
description: Use when delegating coding or review work to external autonomous coding CLIs such as Claude Code, Codex, or OpenCode. Covers prompt packaging, PTY/background execution, verification, and result integration.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agents, coding, claude-code, codex, opencode, delegation]
    related_skills: []
---

# Autonomous Coding Agents

## Overview

This umbrella covers using external coding-agent CLIs as workers. Treat each agent as an implementation assistant, not an authority: give it bounded instructions, isolate its workspace, collect a verifiable diff or artifact, then run your own tests and review.

## When to Use

- A coding task is large enough to benefit from an independent worker.
- You need a second-pass implementation, review, simplification, or spike.
- The user explicitly asks to use Claude Code, Codex, OpenCode, or another coding CLI.
- Work can be verified from files, tests, logs, PRs, or other durable handles.

## Agent Selection

- Claude Code: strong for multi-file implementation and refactors; handle interactive prompts carefully.
- Codex CLI: good for focused one-shot patches and background coding tasks.
- OpenCode: useful for feature work and PR review when installed/configured.
- Hermes `delegate_task`: use for isolated subagent reasoning when external CLIs are unnecessary or unavailable.

## Operating Modes

### One-shot mode

Use for bounded tasks with a clear output: describe the repo, files, constraints, tests to run, and expected deliverable. Capture stdout/stderr and inspect the diff.

### Interactive/PTTY mode

Use a PTY only when the CLI requires interactive prompts. Submit approvals intentionally; do not leave an interactive agent waiting silently.

### Background mode

Use background sessions for long bounded jobs and set completion notification. Poll logs before acting on results.

## Prompt Contract

Every worker prompt should include:

- Goal and non-goals.
- Repository path and branch constraints.
- Files/modules likely involved.
- Required tests/lints/build commands.
- Output format: summary, changed files, verification run, blockers.
- Instruction not to commit/push unless explicitly requested.

## Integration Workflow

1. Snapshot `git status` and relevant tests before delegation.
2. Run the worker with the narrowest sufficient scope.
3. Inspect changed files and command output.
4. Run verification yourself.
5. Fix or revert worker mistakes before reporting success.

## Pitfalls

- Do not trust a worker's self-report without reading the diff and running tests.
- Do not run multiple agents in the same worktree unless their scopes cannot conflict.
- Do not let an external CLI make remote side effects unless the user asked for them.
- Do not paste secrets into agent prompts.

## Verification Checklist

- [ ] Worker output includes a concrete diff/artifact or blocker.
- [ ] You inspected the resulting files.
- [ ] Required tests/lints/builds were run by you or their failure is reported.
- [ ] No unexpected commits, pushes, or secrets were introduced.
