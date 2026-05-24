# Paperclip local automation before Discord

Use this pattern when a user asks whether Discord is required, or asks to finish Paperclip/Hermes automation before messaging-platform setup.

## Decision rule

Discord is optional. Do not block company setup on Discord unless the user specifically wants chat-based operations now.

Required local automation path:

1. Paperclip server running and healthy, typically `http://127.0.0.1:3100/api/health`.
2. Company imported and verified by ID.
3. Agents imported with `adapterType: hermes_local`.
4. A company-local bridge/helper script pins company/project/agent IDs and wraps Paperclip CLI/API operations.
5. Smoke tests verify the helper without Discord.
6. A local operating doc lists the exact commands.

## Recommended helper verbs

A minimal useful helper should support:

- `health` — GET Paperclip health endpoint.
- `smoke` — verify health, company, agents, open issues, dashboard in one command.
- `company` — get pinned company.
- `agents` — list company agents.
- `open` — list non-done issues only, summarized.
- `list` — list/filter issues by status, agent, project, text match.
- `get <issue>` — inspect one issue.
- `create` — create issue with pinned company/project/agent IDs.
- `comment` — add issue comment.
- `checkout` — assign/start issue for an agent.
- `release` — clear stuck locks/recovery states.
- `done` — mark manually complete with a verification comment.
- `dashboard` and `activity` — quick operations overview.

## Verification checklist

Run and verify:

```bash
python3 -m py_compile /path/to/company/scripts/<bridge>.py
/path/to/company/scripts/<bridge>.py smoke
/path/to/company/scripts/<bridge>.py open
/path/to/company/scripts/<bridge>.py dashboard
/path/to/company/scripts/<bridge>.py get <KNOWN-ISSUE-ID>
npx --yes paperclipai company import /path/to/company --dry-run --yes --json
```

Success criteria:

- Paperclip health returns `status: ok`.
- Company ID/name/prefix match expected values.
- Agents count matches package and all are `hermes_local`.
- Open issue summary is readable and does not dump huge issue descriptions by default.
- Known issue read works.
- Package dry-run has empty `errors` and no unexplained warnings.

## Reporting style for this user

Keep output terse:

- changed paths
- verification results
- commands to use now
- remaining blocker/status note, if any

Do not over-explain Discord. Say: local automation is required; Discord is only an optional input/output layer.