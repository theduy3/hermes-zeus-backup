---
name: github-workflows
description: "Class-level GitHub workflow umbrella: auth, repositories, issues, PR lifecycle, PR review, releases, CI, and gh/API fallbacks."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, git, gh-cli, pull-requests, issues, code-review, repositories, ci]
---

# GitHub Workflows

Use this umbrella whenever a task involves GitHub or GitHub-backed project work: authenticating `gh`, cloning/forking/creating repos, managing issues, opening or updating PRs, reviewing PR diffs, checking CI, creating releases, or using GitHub's REST/GraphQL APIs as a fallback.

## Prerequisites

1. Prefer `gh` for authenticated GitHub operations; verify with `gh auth status` before assuming credentials work.
2. For raw REST/GraphQL calls, use `GH_TOKEN`/`GITHUB_TOKEN` and include explicit API versions where relevant.
3. For git transport problems, distinguish HTTPS token auth, SSH key auth, and `gh auth setup-git` credential-helper state.
4. Always inspect the live repo state before changing it: `git status`, `git remote -v`, branch, upstream, and open PR/issue context.

## Repository management

- Clone, fork, create, or inspect repositories with `gh repo ...` and `git remote -v`.
- Check default branch, visibility, topics, releases, secrets, and workflows before assuming repository layout.
- For release work, inspect existing tags/releases and avoid overwriting published artifacts unless explicitly requested.

## Authentication and transport

- Start with `gh auth status`; if `git push` fails independently, check whether git is using HTTPS credentials or SSH.
- Use `gh auth setup-git` after a successful login to align git credential helpers.
- For SSH, verify key presence and GitHub acceptance (`ssh -T git@github.com`) before editing remotes.

## Issues

- For issue creation, gather a concise title, problem statement, repro steps, expected/actual behavior, environment, labels, and assignees.
- Use templates when the repo has them; otherwise produce bug report / feature request structure inline.
- For triage, search existing issues first to avoid duplicates, then label and cross-link related work.

## Pull request lifecycle

1. Create a topic branch from a clean base.
2. Make focused commits with conventional commit-style subjects when useful.
3. Push branch and open PR with a body that explains motivation, implementation, tests, and risks.
4. Monitor CI with `gh pr checks` and fetch failing logs before retrying.
5. Update PR body/comments as facts change; do not claim tests passed unless run or CI confirms.

## Code review

- Review PRs from actual diffs (`gh pr diff`, `gh pr view --json ...`) and current file contents, not summaries alone.
- Separate blocking correctness/security issues from suggestions.
- When posting inline comments through REST, verify path and line positions against the PR diff hunk.
- Provide a short final verdict: approve/comment/request changes, with tests or evidence inspected.

## CI and troubleshooting

- Use `gh run list`, `gh run view --log-failed`, and workflow YAML inspection.
- Categorize failures as code, environment, dependency, secret, flake, or infrastructure before fixing.
- Re-run only when the failure is plausibly flaky or after a concrete fix.

## Fallback API pattern

When `gh` lacks a feature, call the GitHub REST/GraphQL API with `curl` or Python. Always include repo owner/name, endpoint, authentication source, HTTP status, and response body/error in your reasoning.
