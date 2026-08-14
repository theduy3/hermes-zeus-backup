# Weekly ops audit — 2026-07-20

## Context
Scheduled weekly audit of Hermes operational health: gateways, MCP servers, cron jobs, and configuration drift. Final report requested only action-worthy findings.

## Durable checks that mattered

- Verified live gateway state across default + profiles and inspected `/proc/<pid>/environ` for profile-scoped `HERMES_HOME`. All profile gateway PIDs were correctly scoped; default status still reported all PIDs together, so `/proc` remained the source of truth.
- Tested configured MCP servers directly with `hermes -p <profile> mcp test agentmemory`; enabled `agentmemory` connected and exposed 8 tools on butter, catthew, charles, finance, thor, and zeus.
- Validated Telegram bot health with redacted `getMe` checks for every profile after seeing July 16–17 network flap logs. Tokens were valid; logs showed polling restarted, so this was a recovered network flap, not auth breakage.
- Read latest cron output bodies rather than relying on `last_status=ok`.

## Action-worthy findings surfaced

1. **Nightly GitHub backup silently did no backup despite cron `ok`.**
   - Latest output said `~/.hermes/.env` lacked `GITHUB_TOKEN`; no files were staged/committed/pushed.
   - `git status --short` showed many local-only changes, so this was operationally important, not just an optional missing credential.
   - Reporting pattern: affected job, exact missing env var, impact, and next action to add repo-scoped Contents read/write token.

2. **Hermes install was far behind upstream.**
   - `hermes --version` reported `854 commits behind`; report as maintenance-window action, not an immediate in-cron update.

3. **Recovered Telegram network flaps.**
   - Logs showed `TimedOut`, `Bad Gateway`, fallback IP failures, and a transient polling conflict; live `getMe` checks passed for every profile.
   - Report as recovered network instability with proxy/host monitoring action if repeated, not as a token/auth issue.

4. **External-source cron degradation can be acceptable when fallback succeeds.**
   - Catthew Save-On-Foods official page returned `403 Forbidden`, but job found SmartCanucks fallback and determined promo active.
   - Report as “manual app verification before shopping” rather than cron failure.

## False positives avoided

- Missing optional provider/API keys from `doctor` were not treated as action-worthy unless tied to an active job or requested capability.
- Catthew Google Workspace `setup.py --check` showed partial auth missing non-calendar scopes, but the morning briefing only needed Calendar and did not state degradation in the final response. Do not report missing Workspace scopes unless the job purpose depends on those scopes or the latest `## Response` says calendar/workspace data was unavailable.
- Cron response keyword scans can match prompts or loaded skills; inspect only `## Response` before reporting.
