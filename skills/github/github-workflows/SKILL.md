---
name: github-workflows
description: "Use when working with GitHub end-to-end: authentication, repository management, codebase inspection, issues, pull requests, CI, review, and merge workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [github, git, gh, pull-requests, issues, code-review, ci]
    related_skills: []
---

# GitHub Workflows

## Overview

This umbrella is the class-level GitHub operating guide. Use it for repository setup, auth, issue triage, PR lifecycle, code review, CI troubleshooting, release/repo management, and codebase inspection. The old per-action skills are retained as archived package references, but skill discovery should route through this single GitHub workflow entry.

## When to Use

- The user asks to clone, fork, create, inspect, configure, or release a repository.
- The user asks to create/triage issues or manage labels/assignees.
- The user asks to create, review, update, merge, or monitor a PR.
- The user asks for GitHub authentication setup or `gh`/git credential debugging.
- The user asks for codebase LOC/language inspection as part of repo work.

## Standard Setup

1. Run `git status` and identify the repository root before modifying anything.
2. Check authentication with `gh auth status` when GitHub API/PR/issue operations are needed; fall back to git-only operations or REST with explicit tokens when appropriate.
3. Use `gh repo view --json nameWithOwner,defaultBranchRef,viewerPermission` to confirm repo identity and permissions.
4. For destructive or publishing actions, verify branch, remote, and user intent.

## Workflow Sections

### Authentication
Prefer `gh auth status` and `gh auth login` for GitHub CLI workflows. For git-only environments, configure HTTPS tokens or SSH keys and verify with `git ls-remote` before attempting push/pull operations.

### Repository Management
Use `gh repo clone/create/fork/view/edit` and git remotes for repository lifecycle. For branch protection, secrets, and releases, use `gh api` when the CLI lacks a direct command.

### Codebase Inspection
Use lightweight LOC/language tools such as `pygount` or project-native tooling. Exclude vendor/build directories and report methodology with the numbers.

### Issues
Use `gh issue list/view/create/edit` for issue operations. Include labels, assignees, reproducible steps, expected/actual behavior, and links to related PRs when available.

### Pull Requests and CI
Use branches with focused commits, open PRs with a clear test plan, monitor CI with `gh pr checks`, and iterate until the PR is green or the blocker is explicit.

### Code Review
Review diffs before commenting. Prefer actionable findings with file/line references. For inline comments, use `gh api`/REST only after mapping positions correctly.

## Archived Package References

Former narrow skills absorbed into this umbrella are preserved under `references/<old-skill-name>/` with their original SKILL.md and support files intact.

## Common Pitfalls

- Acting in the wrong repository or on the wrong remote.
- Trusting local branch names without checking upstream/default branch.
- Posting review comments before verifying diff positions.
- Reporting CI success without checking the latest commit's checks.

## Verification Checklist

- [ ] Repo root, remote, branch, and auth state are verified.
- [ ] Any mutation has a visible handle: issue URL, PR URL, commit SHA, release URL, or API status.
- [ ] Final response includes commands run and real results, not inferred GitHub state.
