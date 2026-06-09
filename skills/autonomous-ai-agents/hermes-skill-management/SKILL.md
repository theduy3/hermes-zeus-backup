---
name: hermes-skill-management
description: "Use when installing, importing, repairing, authoring, exposing, or consolidating Hermes/OpenClaw/Claude-style skills and skill packages."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, skills, skill-installation, skill-authoring, slash-commands, curator]
    related_skills: [hermes-agent]
---

# Hermes Skill Management

## Overview

This umbrella covers the lifecycle of Hermes skill packages: installing community skills, repairing blocked or manual installs, authoring in-repo or user-local SKILL.md files, exposing skills as slash commands/shell wrappers, and consolidating narrow skills into class-level umbrellas.

## When to Use

- The user asks to install, import, repair, or verify a Hermes/OpenClaw/Claude-style skill.
- The user asks to author or edit SKILL.md packages.
- The user asks to expose a skill as a slash command or shell command.
- The user asks for skill-library curation, consolidation, archiving, or package integrity checks.

## Standard Workflow

1. Identify whether the skill is user-local, in-repo, bundled, or hub-installed.
2. Inspect the complete package, not only SKILL.md: `references/`, `templates/`, `scripts/`, and `assets/` can be required for correctness.
3. For installs, prefer the supported Hermes/hub path; use manual install only when blocked and explicitly authorized.
4. For authoring, follow Hermes frontmatter constraints: leading `---`, required `name` and `description`, concise trigger description, and non-empty body.
5. For consolidation, create or patch a class-level umbrella, re-home support packages safely, then archive absorbed narrow skills with `absorbed_into` metadata.

## Modes

### Installing Community Skills
Use the standard hub/import path first. If security scanning blocks an install and the user approves manual installation, inspect the package, preserve support files, then verify skill discovery in a fresh session or by file inspection.

### Authoring Skills
Write class-level instructions, not one-session bug logs. Include Overview, When to Use, actionable workflows, pitfalls, and verification. Move session-specific detail into `references/`, copyable starters into `templates/`, and reusable probes into `scripts/`.

### Slash Commands and Shell Wrappers
Expose only stable workflows. Ensure command wrappers call the correct Hermes profile/home and preserve arguments/quoting.

### Curator Consolidation
Judge overlap by maintainer shape: would a human want one umbrella with subsections? If yes, merge. Do not flatten packages with linked support files; copy/re-home the full package or keep it standalone.

## Archived Package References

Former narrow skills absorbed into this umbrella are preserved under `references/<old-skill-name>/` with original SKILL.md and support files intact.

## Common Pitfalls

- Treating usage counters as value signals.
- Deleting instead of archiving.
- Flattening SKILL.md while leaving linked support files behind.
- Creating narrow skills whose trigger is just one bug/session.

## Verification Checklist

- [ ] Skill package type and location are known.
- [ ] Support files and relative links were inspected before moving/archiving.
- [ ] Installation/authoring/curation result is verified by file inspection or skill discovery.
