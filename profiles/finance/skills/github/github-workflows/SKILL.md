---
name: github-workflows
description: Use when working with GitHub repositories, authentication, issues, pull requests, code review, releases, repository metadata, or repo-level inspection. Consolidates gh CLI, git, and REST API workflows.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [github, git, gh, pull-requests, issues, code-review, repositories]
    related_skills: []
---

# GitHub Workflows

## Overview

This umbrella covers the GitHub lifecycle: authentication, repository management, issue work, branch/commit/PR flow, code review, CI follow-up, and codebase inspection. Prefer `gh` when authenticated, fall back to git and REST with explicit tokens when needed.

## When to Use

- The user asks to clone, fork, create, inspect, or configure repositories.
- The user asks to create/triage/update GitHub issues.
- The user asks to create, update, review, merge, or monitor a pull request.
- GitHub authentication, remotes, tokens, SSH keys, or `gh` login are blocking work.
- You need LOC/language/codebase inspection as part of repo triage.

## Prerequisite Checks

1. Run `git status` in the repo before changing files.
2. Check `gh auth status` before GitHub API actions; if unavailable, use git remote URLs and REST with a configured token.
3. Identify repo owner/name from `gh repo view --json nameWithOwner` or `git remote -v`.
4. Before destructive actions, confirm the target branch/repo.

## Authentication

- Prefer `gh auth login` or existing `GH_TOKEN`/`GITHUB_TOKEN`.
- For git-only auth, verify fetch/push with the remote before assuming credentials work.
- Never print tokens. Use environment variables or credential helpers.

## Repository Management

- Clone/fork/create repos with `gh repo` when possible.
- Inspect remotes, default branch, visibility, releases, and branch protection before modifying repo configuration.
- For releases, verify tag existence and uploaded assets.

## Issues

- Use issue templates for bug reports and feature requests.
- Include reproduction steps, expected/actual behavior, environment, and acceptance criteria.
- When triaging, check labels, assignees, linked PRs, duplicates, and project fields.

## Pull Request Lifecycle

1. Create a topic branch from the intended base.
2. Make minimal commits with meaningful messages.
3. Run tests/lints before pushing.
4. Open PR with a concise summary and test plan.
5. Monitor CI and address review comments.
6. Merge only when checks and approvals meet repo policy.

## Code Review

- Review local diffs before push and PR diffs before submitting comments.
- Separate correctness, security, maintainability, performance, and test coverage findings.
- Prefer actionable comments with file/line context and suggested patches.

## Codebase Inspection

- Use language/LOC tools such as `pygount` only as a high-level signal.
- Exclude generated, vendored, build, and dependency directories.
- Use inspection output to prioritize review; do not treat LOC as quality evidence.

## Verification Checklist

- [ ] Authenticated target repo and current branch are known.
- [ ] `git status` is clean or intentional changes are explained.
- [ ] GitHub actions are verified with `gh`/API output, not assumed.
- [ ] PR/issue/release URLs or IDs are reported when created.
