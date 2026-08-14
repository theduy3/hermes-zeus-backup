# Weekly ops audit example — 2026-07-13

Use this as a compact example of how to interpret a multi-profile Hermes weekly ops audit without over-reporting healthy inventory.

## What was checked

- `hermes --version`, `hermes status --all`, `hermes doctor`, `hermes config check`
- Default and per-profile `gateway status`, `cron status`, `cron list --all`, and `mcp list`
- Profile gateway process environments via `/proc/<pid>/environ` to verify profile-scoped `HERMES_HOME`
- Enabled MCP servers with `hermes -p <profile> mcp test <server>`
- Recent gateway/error logs for Telegram conflicts, auth failures, reconnect loops, and startup errors
- Latest cron output markdown, reading only the `## Response` body for degraded-mode/failure text
- Nightly backup output and git status to distinguish a real backup failure from normal post-backup churn

## Interpretation patterns learned

### Recovered Telegram network flap

Observed many profiles logging `telegram.error.TimedOut`, `httpx.ConnectError`, fallback-IP attempts, and reconnects in the same short window. Do not immediately classify this as bot-token auth failure or duplicate gateway conflict.

Verification pattern:

1. Confirm gateways are still running.
2. Check latest log lines for `Telegram polling resumed after network error`.
3. Validate each profile token with Telegram `getMe`, printing only bot username and a redacted fingerprint.
4. If all tokens validate and polling resumed, report as a recovered outbound/network flap. Recommended action: monitor recurrence and consider VPS outbound connectivity/proxy investigation.

### Cron `last_status=ok` can still mean degraded output

Examples from this audit:

- A household briefing job returned `ok` but said Google Calendar was not connected, so it used local notes only. This is action-worthy because the job explicitly loaded Google Workspace and expected calendar events.
- A sale-check job returned `ok` but reported `HTTP 403 Forbidden` and `Unable to verify`; action is to add a fallback source or browser-capable verification path.
- Portfolio/finance reports returned `ok` while noting unresolved symbols or missing structured source data; report these as data-quality/input issues, not cron failures.

Always read the `## Response` body before reporting. Ignore errors/pitfalls appearing only in the injected prompt or loaded skill text.

### MCP list vs MCP test

`mcp list` proves configuration only. For each enabled server, run `hermes -p <profile> mcp test <server>`. In this audit, `agentmemory` was enabled and testable on several profiles; default/wiki simply had no MCP servers configured, which is not an outage.

### Backup verification

For the nightly GitHub backup, inspect the latest output markdown. A successful report should include the midnight timezone self-check, commit hash, push status, and secret-safety checks. Normal `git status --short` churn after a successful backup is not itself a backup failure; compare against the latest backup output before alerting.

## Reporting style

Return only action-worthy findings with:

- component/profile/job
- exact symptom
- next action

Do not include healthy inventory unless needed to explain scope or rule out a likely false positive.
