---
name: software-quality-debugging
description: Use when validating, debugging, reviewing, simplifying, or test-driving software changes. Consolidates systematic debugging, TDD, review, spike, simplification, and language debugger workflows.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [debugging, testing, tdd, review, refactor, spike, quality]
    related_skills: []
---

# Software Quality and Debugging

## Overview

This umbrella covers the engineering workflows that improve confidence before or after code changes: root-cause debugging, test-driven development, pre-commit review, simplification/refactoring, exploratory spikes, and debugger use for Python or Node.js.

## When to Use

- A bug needs root-cause analysis before fixing.
- A change should be developed with tests first.
- The user asks for a code review, quality gate, or pre-commit check.
- Recent changes should be simplified or split.
- You need a throwaway experiment to validate feasibility.
- Runtime behavior requires `pdb`, `debugpy`, `node inspect`, or Chrome DevTools Protocol.

## Core Decision Tree

1. Unknown failure: use systematic debugging before editing.
2. New behavior: use TDD when expected behavior can be specified.
3. Risky or unclear design: run a spike, record the verdict, then discard or promote learnings.
4. Finished implementation: run review and quality gates.
5. Bloated diff: simplify/refactor with tests guarding behavior.
6. Runtime-only mystery: attach a debugger and inspect live state.

## Systematic Debugging

- Reproduce the issue first.
- Gather evidence from logs, tests, stack traces, and minimal examples.
- Form one hypothesis at a time and falsify it with a targeted probe.
- Only patch after the root cause is understood.

## Test-Driven Development

- RED: write or expose a failing test for the intended behavior.
- GREEN: implement the smallest fix that passes.
- REFACTOR: improve structure while keeping tests green.
- Never claim TDD if the test did not fail first.

## Review and Quality Gates

- Inspect the diff, not just the final files.
- Run relevant tests/lints/type checks/security scans.
- Separate must-fix defects from optional style improvements.
- Verify generated files and lockfiles are intentional.

## Simplification

- Preserve behavior with tests before refactoring.
- Remove dead abstractions and duplicated logic.
- Prefer small, reversible edits.
- Re-run the same verification after cleanup.

## Spikes

- Time-box the experiment.
- Keep spike code separate or clearly disposable.
- End with a verdict: validated, partial, invalidated, or inconclusive.
- Promote only the minimal proven pieces.

## Debuggers

- Python: use `pdb` for local stepping and `debugpy` for remote/DAP-style attaches.
- Node.js: use `node inspect`, `--inspect`, or CDP scripting for live process introspection.
- Debuggers are evidence tools; still encode the fix in tests.

## Verification Checklist

- [ ] Failure or target behavior is clearly stated.
- [ ] Evidence supports the selected fix or design.
- [ ] Tests/lints/builds were run and results recorded.
- [ ] Debug/spike artifacts were cleaned up or documented.
