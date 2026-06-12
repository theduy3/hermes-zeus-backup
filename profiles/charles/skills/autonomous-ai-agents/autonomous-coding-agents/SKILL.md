---
name: autonomous-coding-agents
description: "Use when delegating software tasks to external autonomous coding CLIs such as Claude Code, Codex, or OpenCode, including one-shot tasks, PR reviews, worktrees, and long-running agent sessions."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agents, coding, delegation, claude-code, codex, opencode, worktrees]
    related_skills: [hermes-agent]
---

# Autonomous Coding Agents

## Overview

This umbrella covers running external coding-agent CLIs from Hermes. Provider-specific packages remain under `references/source-packages/`; use this skill to choose the orchestration pattern, then open the provider reference for exact flags.

## When to Use

- Delegate implementation, bug fixing, refactors, or PR review to an autonomous coding CLI.
- Run multiple independent agents in parallel, usually in separate worktrees.
- Start a long-running interactive coding agent and monitor it safely.

Do not use this when Hermes `delegate_task` is sufficient and the user did not request an external CLI.

## Agent Choices

### Claude Code
Best for high-context coding, PR review, and projects with CLAUDE.md conventions. Watch for PTY requirements and interactive prompts.

### Codex
Best for OpenAI Codex CLI one-shot implementation, batch PR reviews, and worktree-based parallel fixes. Use non-interactive/background patterns for long runs.

### OpenCode
Best where OpenCode is installed and its binary resolution/session-cost controls are desired.

## Orchestration Pattern

1. Verify the CLI exists and auth/config is ready.
2. Snapshot git state and create/choose an isolated worktree for side-effecting work.
3. Give the agent a bounded, self-contained prompt with acceptance checks.
4. Run with Hermes-tracked terminal/background process, not shell-disowned jobs.
5. Inspect diff, run tests, and review before reporting success.

## Package References

Full source packages are copied under `references/source-packages/claude-code/`, `codex/`, and `opencode/`.

## Verification Checklist

- [ ] CLI availability/auth checked.
- [ ] Worktree or branch isolation chosen.
- [ ] Final diff and tests reviewed by Hermes, not blindly trusted from agent self-report.
