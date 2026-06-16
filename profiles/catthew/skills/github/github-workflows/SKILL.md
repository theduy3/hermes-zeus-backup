---
name: github-workflows
description: Use when performing GitHub repository, authentication, issue, pull-request, review, CI, release, or codebase-inspection workflows with git, gh, or the GitHub API.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [github, git, gh, pull-requests, issues, code-review, repositories, ci]
    related_skills: []
---

# GitHub Workflows

## Overview

This umbrella covers the full GitHub operating class: authentication, repository management, issue triage, pull-request lifecycle, code review, CI troubleshooting, releases, and codebase inspection. Use labeled sections below rather than searching for narrow GitHub subskills.

## When to Use

- The user asks to clone, fork, create, inspect, or configure a GitHub repository.
- The user asks to create or triage issues, labels, assignments, milestones, or projects.
- The user asks to branch, commit, push, open a PR, update a PR, monitor CI, merge, or release.
- The user asks for PR/local-diff review or inline review comments.
- GitHub auth, token, SSH, `gh` login, or remote push/pull failures block work.
- The user asks for LOC/language/codebase composition stats.

## Global Operating Rules

1. Inspect current state before acting: `git status`, `git remote -v`, `git branch --show-current`, and `gh auth status` when `gh` is involved.
2. Prefer `gh` for GitHub-native actions; fall back to REST/GraphQL when the CLI lacks a feature.
3. Never fabricate PR URLs, CI results, review comments, issue numbers, or release IDs. Verify with tool output.
4. Keep secrets out of logs. Redact tokens and avoid writing credentials into repo files.
5. For destructive actions (force-push, delete branch, close issue, merge, release), make the scope explicit.

## Authentication and Remotes

- Diagnose in this order: git remote shape → credential helper/SSH config → `gh auth status` → token scopes.
- HTTPS PAT works without `gh`; SSH works when keys are installed and authorized.
- `gh` browser auth is easiest on interactive desktops; token auth is better for headless environments.

## Repository Management

- Clone/fork/create after confirming owner/repo and destination path.
- Preserve upstream/origin naming conventions when working on forks.
- For releases, verify tags and generated artifacts before publishing.

## Issues

- For new issues, gather title, problem statement, repro/acceptance criteria, labels, and assignee when available.
- For triage, read linked PRs/commits and recent comments before changing labels/status.
- Use templates for bugs/features when the repo has them.

## Pull Requests and CI

- Create a branch from the intended base, commit focused changes, push, then open/update the PR.
- Use structured PR bodies: summary, tests, risks, screenshots/logs when relevant.
- After opening/updating, check CI (`gh pr checks`, workflow runs) and report actual statuses.
- For CI failures, inspect logs before guessing; link failure to the likely file/change.

## Code Review

- Review the diff, not just file names.
- Prioritize correctness, security, data loss, migrations, concurrency, and test gaps.
- Distinguish blocking findings from nits.
- For inline comments, compute exact file/line positions from the PR diff and verify submission succeeded.

## Codebase Inspection

- Use language/LOC tools such as `pygount`, `cloc`, or `tokei` when available.
- Exclude generated/vendor/build directories unless the user explicitly wants total repository size.
- Report methodology and exclusions with the numbers.

## Common Pitfalls

1. **Assuming the target repo.** Always derive owner/repo from remotes or ask if no repo context exists.
2. **Skipping auth diagnosis.** Many GitHub failures are credential/scope issues, not git issues.
3. **Stopping at PR creation.** Verify the PR URL and CI state.
4. **Reviewing stale diffs.** Fetch/update the branch before review when remote state matters.

## Verification Checklist

- [ ] Repo, branch, remote, and auth state were checked.
- [ ] GitHub side effects have verified URLs/IDs/statuses.
- [ ] CI/review/issue/release outcomes are grounded in `gh`, git, or API output.
- [ ] The final response lists commands run, artifacts created, and remaining blockers.
