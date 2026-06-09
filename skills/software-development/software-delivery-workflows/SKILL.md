---
name: software-delivery-workflows
description: "Use when planning, spiking, debugging, testing, reviewing, or instrumenting software changes from idea through verified delivery."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [software-development, planning, debugging, tdd, review, debugpy, node-inspect]
    related_skills: []
---

# Software Delivery Workflows

## Overview

This umbrella covers the class-level lifecycle for making reliable software changes: write a plan when useful, run spikes to validate uncertainty, debug systematically, drive changes with tests, inspect Python/Node runtime state when needed, and request/perform code review before delivery.

## When to Use

- The user asks for a plan, implementation strategy, or architecture breakdown.
- A bug requires root-cause debugging rather than guess-and-patch.
- A change should be driven by RED/GREEN/REFACTOR tests.
- Python or Node runtime debugging is needed.
- A pre-commit or pre-PR review is needed.

## Lifecycle

1. **Plan** when scope is ambiguous or the user asks for plan mode. Keep tasks bite-sized and path-specific.
2. **Spike** when a technical choice or feasibility question is uncertain. Throw away spike code unless explicitly promoted.
3. **Debug systematically**: reproduce, inspect, hypothesize, test the hypothesis, then patch.
4. **Test-drive changes** when behavior can be specified. Start with a failing test and only then implement.
5. **Instrument runtime** with `pdb`/`debugpy` for Python or `node inspect`/Chrome DevTools Protocol for Node when static inspection is insufficient.
6. **Review before delivery**: check diff, run quality gates, scan for security issues, and incorporate reviewer feedback.

## Debugging Modes

### Python
Use `pdb` for local breakpoints/post-mortem debugging and `debugpy`/DAP for attaching to running processes or test sessions.

### Node.js
Use `node inspect`, `--inspect`, CDP scripts, heap snapshots, and CPU profiles for runtime issues, especially UI/TUI or browser-adjacent code.

### Root Cause Discipline
Never patch symptoms without a reproduction and a plausible mechanism. If a command/test fails, preserve the real output in the final report.

## Archived Package References

Former narrow skills absorbed into this umbrella are preserved under `references/<old-skill-name>/` with original SKILL.md and support files intact.

## Common Pitfalls

- Writing implementation before clarifying the expected behavior.
- Calling a spike result production-ready without verification.
- Skipping the RED step in TDD.
- Treating static code review as a substitute for tests.

## Verification Checklist

- [ ] The workflow selected matches the task risk and scope.
- [ ] Reproduction/test command output is captured when relevant.
- [ ] Changes are verified with real execution before reporting success.
