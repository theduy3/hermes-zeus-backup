# Execution monitoring and follow-up issue handoff

Use this when a Paperclip company setup moves from package/import work into live issue execution.

## Pattern

1. After creating or assigning a follow-up issue, immediately fetch it with `issue get <id> --json` or the company-local helper script.
2. Treat `status: in_progress` plus `executionRunId` as a successful handoff to the Paperclip agent, even if no work products exist yet.
3. If the issue was auto-started, do not attempt a second checkout; a later conflict may only mean the issue is already running.
4. Poll the issue after a short delay and summarize only stable fields:
   - identifier
   - status
   - executionRunId
   - activeRecoveryAction kind
   - completedAt
   - workProducts count
5. Keep import/package validation separate from live execution monitoring. Re-run `company import --dry-run --yes --json` after local package/doc/script changes to ensure the portable package still validates.
6. If the follow-up issue creates an external user task, write it into `/vault/Tasks/tasks/<kebab-title>.md` using the user's Tasks frontmatter convention, not into the working directory.

## Terse status format

```text
Done:
- Created <issue-id>: <title>
- assigned: <agent-slug>
- project: <project-slug>
- status: <status>
- run: <executionRunId>
- Obsidian task: <path>
- import dry-run: errors: [], warnings: []

Monitor:
<helper-script> get <issue-id>
```

## Pitfall

Do not present a newly created follow-up issue as complete just because it has an execution run. Use `in_progress` / `running` language until `completedAt` or `status: done` verifies completion.