---
name: github-workflows
description: "Use when managing GitHub work end-to-end: authentication, repositories, issues, PR branches, CI, code review, releases, and codebase inspection."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [github, gh, git, pull-requests, issues, code-review, repositories]
    related_skills: []
---

# GitHub Workflows

## Overview

This umbrella covers the full GitHub operating lifecycle. It consolidates auth, repository administration, issue triage, branch/PR flow, CI troubleshooting, PR review, and codebase inspection into one discoverable entry point while preserving detailed package references.

## When to Use

- Set up or repair GitHub authentication.
- Clone, create, fork, configure, release, or inspect repositories.
- Create, triage, label, assign, or close GitHub issues.
- Create branches/commits/PRs, monitor CI, and merge.
- Review local diffs or GitHub pull requests.
- Inspect LOC/language composition before planning or review.

## Workflow Map

1. **Auth first** — use the `github-auth` reference if `gh` or git credentials are uncertain.
2. **Repository context** — use `github-repo-management` for remotes, repo settings, releases, and API cheatsheets.
3. **Issue intake** — use `github-issues` templates and triage commands.
4. **Implementation PR** — use `github-pr-workflow` for branch, commit, push, CI, and merge lifecycle.
5. **Review gate** — use `github-code-review` and `requesting-code-review` for structured review.
6. **Codebase sizing** — use `codebase-inspection` for pygount/LOC summaries.

## Package References

Full source packages are copied under `references/source-packages/<old-skill>/`; start with the package matching the workflow phase above.

## Common Pitfalls

1. Do not assume `gh` auth; run a quick auth/status check before API or PR operations.
2. Always inspect current branch, remote, and diff before mutating git state.
3. For code review, ground comments in exact file/line evidence.

## Verification Checklist

- [ ] Auth and repo target verified.
- [ ] Current branch/diff/remote checked before pushing or reviewing.
- [ ] CI or final GitHub state verified after side effects.
