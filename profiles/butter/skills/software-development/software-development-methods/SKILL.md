---
name: software-development-methods
description: "Umbrella for coding-process methods: spikes, TDD, systematic debugging, code review, simplification, and language debugger workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [software-development, debugging, tdd, code-review, refactoring, spike, testing]
---

# Software Development Methods

Use this umbrella when the task is primarily about how to conduct software work rather than a specific external platform: validating an idea, debugging, test-driving a change, reviewing code, simplifying code, or attaching a debugger.

## Spike experiments

Before committing to an uncertain design, build the smallest throwaway experiment that answers the risk question. Keep spikes isolated, time-boxed, and delete or clearly label throwaway artifacts.

## Test-driven development

For well-scoped behavior changes, follow RED-GREEN-REFACTOR: write or update a failing test first, make the minimal implementation pass, then clean up while keeping tests green.

## Systematic debugging

Do not patch symptoms first. Reproduce the bug, localize the failing layer, form hypotheses, instrument or inspect evidence, then apply the smallest fix and verify regression coverage.

## Pre-commit / requested code review

Review actual diffs and changed files. Check correctness, security, data loss, concurrency, migrations, tests, and backward compatibility. Auto-fix only mechanical low-risk issues unless asked.

## Simplification and cleanup

When recent code feels over-complex, identify redundant abstractions, unused paths, needless indirection, and unclear naming. Preserve behavior with tests or snapshot comparisons before refactoring.

## Debugger workflows

- Python: use pdb/debugpy for breakpoints, post-mortem debugging, and remote DAP-style inspection.
- Node.js: use `--inspect` and Chrome DevTools Protocol tooling for breakpoints, heap/runtime state, and async call inspection.

## Verification

Every method ends with concrete evidence: tests, build, reproduced failure now passing, diff inspection, or a clearly stated blocker.