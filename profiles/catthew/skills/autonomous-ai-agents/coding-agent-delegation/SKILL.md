---
name: coding-agent-delegation
description: Use when delegating coding, review, refactor, or PR tasks to external autonomous coding CLIs such as Claude Code, Codex, OpenCode, or similar agent processes.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agents, coding, delegation, claude-code, codex, opencode, pr-review]
    related_skills: [subagent-driven-development]
---

# Coding Agent Delegation

## Overview

This umbrella covers launching and supervising external autonomous coding agents. The class-level pattern is the same across Claude Code, Codex, OpenCode, and future agent CLIs: choose the right runtime mode, give a bounded task, isolate the workspace, capture outputs, verify changes yourself, and never treat an agent self-report as proof.

## When to Use

- A coding task is large enough to benefit from an independent agent pass.
- The user asks specifically to use Claude Code, Codex, OpenCode, or another installed coding CLI.
- You need an external reviewer for a PR/diff.
- You want parallel implementation/review/refactor workstreams with isolated contexts.

Do not use for small edits where direct file tools are faster, or for tasks requiring interactive user clarification inside the child process.

## Common Workflow

1. Inspect repo state and define the task boundary.
2. Choose the agent CLI that is installed/configured and appropriate for the task.
3. Prefer one-shot/print mode for bounded work. Use PTY/tmux/background only for long interactive sessions.
4. Provide explicit constraints: files, tests, acceptance criteria, forbidden side effects, branch policy.
5. Capture the transcript/output and changed files.
6. Independently verify: read diff, run tests/lint/build, inspect generated artifacts.
7. Summarize what the agent changed and what you verified.

## Claude Code Notes

- Best for broad coding tasks and PR-oriented implementation/review when `claude` is configured.
- Prefer non-interactive print mode for most tasks.
- For interactive PTY sessions, handle trust/setup prompts explicitly and keep a transcript.

## Codex Notes

- Best for OpenAI Codex CLI workflows, one-shot implementation, and PR review.
- Background mode is appropriate for long bounded tasks; use notify-on-complete and inspect logs before trusting results.
- Pass concise but complete repo context; Codex does not know the parent conversation unless you include it.

## OpenCode Notes

- Resolve the binary path first; installations may expose `opencode` differently.
- Use one-shot mode for implementation and review.
- Interactive sessions need PTY/background handling and careful log capture.

## Prompt Shape

Include:

- Goal and non-goals.
- Exact repo path and branch expectations.
- Files/modules likely involved.
- Acceptance tests/commands to run.
- Output contract: summary, changed files, commands run, blockers.
- Safety constraints: no secrets, no force-push, no unrequested dependency churn.

## Common Pitfalls

1. **Trusting self-reports.** Always verify artifacts yourself.
2. **Giving unbounded prompts.** Agents wander without file/test constraints.
3. **Losing logs.** Use background process tracking or transcript capture for long runs.
4. **Context starvation.** Child agents do not inherit the chat; pass required context.
5. **Parallel write collisions.** Use separate worktrees/branches for concurrent agents.

## Verification Checklist

- [ ] Agent CLI availability/auth was checked.
- [ ] Workspace/branch isolation was appropriate for the task.
- [ ] Diff was reviewed by Hermes after the child completed.
- [ ] Tests/lint/build or other acceptance checks were actually run.
- [ ] Final report distinguishes agent claims from verified facts.
