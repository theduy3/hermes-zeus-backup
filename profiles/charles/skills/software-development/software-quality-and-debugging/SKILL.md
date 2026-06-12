---
name: software-quality-and-debugging
description: "Use when improving software correctness and maintainability: systematic debugging, TDD, debugpy/pdb, Node inspector, pre-commit review, simplification, and spike experiments."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [debugging, testing, tdd, code-review, refactoring, spike]
    related_skills: []
---

# Software Quality and Debugging

## Overview

This umbrella captures recurring class-level software engineering practices rather than separate micro-skills for each quality gate. Tool/language-specific packages are preserved under `references/source-packages/`.

## When to Use

- Debug a bug from first principles.
- Add or repair tests using RED-GREEN-REFACTOR.
- Use Python `pdb`/`debugpy` or Node inspector/CDP.
- Request or perform pre-commit code review.
- Simplify recent code changes with parallel reviewers.
- Run throwaway spikes to validate approaches before implementation.

## Practice Map

- **Systematic debugging:** understand root cause before fixing.
- **TDD:** write/observe failing test, implement, refactor.
- **Python debugging:** `pdb`, post-mortem, debugpy attach.
- **Node debugging:** `node inspect`, CDP, profiles, Vitest under debugger.
- **Review:** diff, static checks, tests, independent review, fix loop.
- **Simplification:** parallel critique and cleanup.
- **Spike:** bounded experiment with explicit verdict.

## Verification Checklist

- [ ] Reproduction or failing test captured before fix when debugging.
- [ ] Appropriate debugger/test/review reference opened for exact commands.
- [ ] Final code path verified with tests or concrete execution.
