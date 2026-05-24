# Paperclip Manual Resolution and Repo Access Verification

Use this when a Paperclip issue is a documentation/access-verification task, the owning local agent run fails, or automation repeatedly recovers a stranded assignment.

## Pattern: inaccessible/private repo verification

For engineering setup verification tasks against a private repo:

1. Inspect the task file and nearby project docs first.
2. Try access without printing secrets:
   - verify the target repo URL
   - check whether `gh`/git can see it
   - test available token env var names only; never print values
   - search expected local checkout paths
3. If no source is accessible, complete the task as an access-verification result, not as code verification.
4. Report exactly one unblocker request class:
   - runtime GitHub access/token for Hermes/Paperclip
   - corrected repo URL
   - local checkout path
   - public README/source export
5. Do not invent stack, package-manager, build, test, Supabase, or deployment facts from inaccessible source.

## Pattern: reports as both local docs and Paperclip work products

For Paperclip project tasks, write deliverables in both locations when possible:

- local repo docs, e.g. `/home/hermes/wylios-paperclip/docs/<REPORT>.md`
- Paperclip managed `_default` work product folder for the project

Then include both paths in the Paperclip issue comment.

## Pattern: stranded assigned issue / adapter_failed recovery

Symptoms observed:

- `checkout` fails with HTTP/API 409 `Issue checkout conflict`
- issue status is `blocked` or `in_progress` but `blockedBy` is empty
- `blockerAttention.state` is `needs_attention` with no real blocker records
- active recovery action mentions `stranded_assigned_issue`
- latest run has `adapter_failed`
- issue status remains `in_progress` despite work being complete
- automation may re-lock/retry the task

Diagnosis sequence:

```bash
npx --yes paperclipai issue get <ISSUE-ID-OR-IDENTIFIER> --json
npx --yes paperclipai issue update --help
```

If the issue is a research/reporting/documentation task and checkout is conflicted, do not keep retrying checkout. Finish the work manually:

1. Read the issue JSON for project ID, managed folder, title, description, assignee, and current status.
2. Produce the deliverable in the local project docs folder.
3. Also write a short work-product copy into the Paperclip managed `_default` folder when one exists.
4. Add a concise issue comment with both paths and the key conclusion.
5. Mark the issue `done`.

Manual resolution sequence via CLI:

```bash
npx --yes paperclipai issue release <ISSUE-ID> --json
npx --yes paperclipai issue update <ISSUE-ID> \
  --status done \
  --assignee-agent-id <AGENT-ID> \
  --comment "Manual resolution: <summary>. Reports saved at <paths>." \
  --json
```

Manual resolution sequence via Paperclip API/curl when the task explicitly requires API calls through curl:

```bash
curl -s -X POST "$PAPERCLIP_API_BASE/issues/<ISSUE-ID>/release" \
  -H "Content-Type: application/json" \
  -d '{}'

curl -s -X POST "$PAPERCLIP_API_BASE/issues/<ISSUE-ID>/comments" \
  -H "Content-Type: application/json" \
  -d '{"body":"DONE: Manual resolution: <summary>. Reports saved at <paths>."}'

curl -s -X PATCH "$PAPERCLIP_API_BASE/issues/<ISSUE-ID>" \
  -H "Content-Type: application/json" \
  -d '{"status":"done"}'
```

Use `release` first to clear assignment/execution locks, then post a concise manual-resolution comment and update status. If an issue was already updated to `done` without release and Paperclip immediately starts a new automation run, inspect/release the active lock before doing more work; do not duplicate the deliverable.

## Safety notes

- If a tool/policy returns `BLOCKED: User denied. Do NOT retry.`, do not retry that exact command path.
- Never preserve credential values in reports, comments, skills, or memory. Replace credential values with `[REDACTED]` if encountered.
- Do not encode one-off missing credentials as a durable tool limitation; capture the fallback/reporting workflow instead.