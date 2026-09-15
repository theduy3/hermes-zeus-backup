---
name: cron-artifact-reporting
description: Tool-only reporting from Hermes cron/session artifacts when Python helpers or approval-gated shell scripts are unavailable in headless runs.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, cron, reporting, sessions, artifacts, headless]
---

# Cron Artifact Reporting

Use this when summarizing Hermes activity, cron output, session history, or operational status from a scheduled/headless job, especially when arbitrary Python execution or shell heredocs may be blocked by approval policy.

This skill complements broader activity-recap workflows. Its focus is the fallback path: produce a grounded report using ordinary Hermes tools only.

## Workflow

1. Establish the local reporting date/time with a safe `terminal` date command when allowed.
2. Check scheduler state with `hermes cron list` and, for named profiles that may own work, `hermes --profile <profile> cron list`.
3. Discover artifacts with `search_files(target="files")` instead of custom glob scripts:
   - default profile: `/home/hermes/.hermes/cron/output`
   - named profiles: `/home/hermes/.hermes/profiles`
   - session transcripts: `/home/hermes/.hermes/sessions`
4. If results are truncated, paginate with `offset` rather than treating the first page as complete.
5. Search for hard failures with `search_files(output_mode="files_only")` on patterns like `^## Error$`, `HTTP 429`, `HTTP 401`, `usage limit`, `Failed to`, `Permission denied`, `not writable`, `Unauthorized`, `Traceback`, and `ERROR`.
6. Read only representative outputs and useful line ranges with `read_file()`. Large agent cron outputs often embed the full prompt and loaded skills; jump near the final `## Response`/`## Error` section when line counts are known.
7. Re-scan near the end when co-scheduled jobs may have completed while you were reading earlier outputs.
8. For multi-profile evening recaps, use the concrete checklist in `references/2026-07-29-multi-profile-evening-recap.md`: named-profile cron lists, pagination when profile output discovery truncates, representative `wiki` jobs, and late co-scheduled output handling.

## Headless approval fallback

In cron mode, `execute_code` may be blocked because it can run arbitrary local Python. Terminal heredocs such as `python3 - <<'PY' ... PY` can also be left `pending_approval` with no user present. Do not stop the report there.

Fallback sequence:

1. Use `search_files(target="files")` for artifact discovery.
2. Use `search_files(target="content")` for failure/error probes.
3. Use `hermes --profile <name> cron list` to identify scheduled jobs, last-run status, and delivery failures.
4. Use `read_file()` on selected output files and line offsets to extract final responses.
5. Summarize from verified files and scheduler state, explicitly noting any current job still running or not yet due.

## Classification cautions

- Script/no-agent jobs may have no `## Response`; `**Status:** silent (empty output)` usually means a successful no-alert run, not a failed response.
- Whole-file searches for `[SILENT]` are misleading because prompts often include the literal delivery instruction. Inspect only the final response section when classifying silent vs substantive outputs.
- Do not call the currently running recap job missing just because its output markdown is not written yet; the file is created after the final response.
- Delivery failures in `cron list` are first-class blockers even when output files exist.
- Environment/setup warnings should be reported as current blockers, not turned into permanent claims that a tool never works.

## Model changes and unpinned cron jobs

When a profile's global model changes, inspect enabled agent jobs for `model_snapshot` / `provider_snapshot` values that differ from the new defaults. An unpinned job should follow the profile defaults, but Hermes may fail closed on snapshot drift rather than silently changing paid inference. Preserve the job as unpinned while refreshing its derived snapshots through the supported cron update path: temporarily set `--model <current-model> --provider <current-provider>`, then clear both with `--model '' --provider ''`. Verify the resulting record has `model: None`, `provider: None`, and current `model_snapshot` / `provider_snapshot`. Do not hand-edit `jobs.json` unless the supported CLI cannot perform the operation.

## Vault-writing cron jobs

For a cron job that must save output to Obsidian, attach the `obsidian` skill and include an explicit vault path, write-and-verify instruction, and exact-error fallback. Ensure the job has the required `terminal` and `file` toolsets. Keep the report's normal scheduler output behavior separate from the vault artifact. When composing a shell command that passes a prompt containing backticks, avoid unquoted command substitution: use a safely quoted argument or a file-based update, otherwise backticks may be executed by the shell and silently remove path text. Verify the stored prompt and attached skill after updating.

## Output style

For daily recaps, keep three concise sections:

1. What got done
2. Failures / blockers
3. Top next actions

Quantify when possible, but prefer exact verified outcomes over broad inferred counts when tool-only aggregation limits precision.
