---
name: autonomous-coding-agents
description: "Umbrella for delegating software work to external coding-agent CLIs such as Claude Code, Codex, and OpenCode."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [coding-agents, delegation, claude-code, codex, opencode, autonomous-development]
---

# Autonomous Coding Agents

Use this skill when the best path is to delegate implementation, refactoring, PR review, or repository work to an external autonomous coding CLI rather than doing every edit directly in the parent Hermes turn.

## Shared delegation pattern

1. Inspect the repo and task scope first; pass agents exact paths, commands, constraints, and expected artifacts.
2. Prefer isolated branches/worktrees for agents that edit files.
3. Give bounded, testable goals: what to change, what not to change, and how to verify.
4. Require the agent to report changed files, commands run, failures, and remaining risks.
5. Verify the agent's claims yourself with git diff, tests, and file reads before reporting success.

## Claude Code

Use for strong repository-wide coding, refactors, and PR work when the Claude Code CLI is installed and authenticated. It is a good default for complex feature implementation and multi-file cleanup.

## Codex

Use for OpenAI Codex CLI-based implementation or review when the user has configured Codex credentials. It is especially useful when the user specifically asks for Codex or when a Codex lane is part of a larger Kanban/agent workflow.

## OpenCode

Use when the OpenCode CLI is the available coding agent or when the work benefits from OpenCode's local workflow. Treat its output as untrusted until verified like any other subagent result.

## Verification discipline

Never proxy an agent's self-report as fact. Check git state, inspect diffs, run the requested tests or build, and only then summarize the result.