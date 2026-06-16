---
name: ai-coding-agents
description: "Use when delegating software work to autonomous coding CLIs such as Claude Code, Codex, or OpenCode. Covers agent selection, prompt packaging, execution supervision, verification, and PR handoff."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [autonomous-agents, coding, claude-code, codex, opencode, delegation]
    related_skills: [subagent-driven-development, github-pr-workflow]
---

# AI Coding Agents

## Overview

Use this umbrella for class-level delegation of coding tasks to external autonomous coding agents. The old tool-specific skills are preserved as detailed references:

- `references/claude-code.md`
- `references/codex.md`
- `references/opencode.md`

The shared workflow is more important than the CLI brand: package context precisely, constrain side effects, run the agent in an isolated workspace, verify its output yourself, and only then report success.

## When to Use

- A coding task is large enough to benefit from an independent coding agent.
- The user explicitly asks to use Claude Code, Codex, OpenCode, or a similar ACP/CLI agent.
- You need parallel implementations, independent code review, or a PR-ready patch.

Do not use when a direct edit is faster, when the task requires user interaction mid-run, or when you cannot verify the produced artifact.

## Agent Selection

| Agent | Best fit | Watch-outs |
|---|---|---|
| Claude Code | Large refactors, feature implementation, PR preparation | Can make broad edits; constrain scope and verify diffs. |
| Codex | Focused coding tasks and CLI-friendly patch work | Provide exact files, tests, and expected command output. |
| OpenCode | Alternative coding agent / review path | Verify installed command and auth before dispatch. |

## Delegation Workflow

1. Inspect the repo and gather the minimum context: task, relevant files, failing tests, constraints, style conventions.
2. Give the agent a self-contained prompt with success criteria and forbidden areas.
3. Run in a controlled worktree or branch when possible.
4. After completion, inspect `git diff`, run tests/linters/builds, and fix or reject weak changes.
5. Summarize only verified work; never trust a child agent's self-report without checking handles, files, or command output.

## Verification Checklist

- [ ] Agent command exists and auth is configured.
- [ ] Prompt includes scope, tests, and definition of done.
- [ ] Diff reviewed manually after the agent exits.
- [ ] Required tests/builds actually ran and their output was checked.
- [ ] User-facing summary separates agent claims from verified facts.
