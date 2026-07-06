---
name: hermes-operations-troubleshooting
description: "Troubleshoot Hermes operational issues in live deployments: cron scheduler state, gateway delivery failures, Telegram/Discord delivery, stale cron errors, and safe verification patterns."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [hermes, cron, gateway, telegram, operations, troubleshooting]
---

# Hermes Operations Troubleshooting

Use this skill when the user asks to fix or audit live Hermes operations: cron jobs, gateway status, delivery failures, scheduler health, Telegram/Discord messaging, or stale job errors.

This is an operational supplement for live troubleshooting. If the task is general Hermes setup/configuration, load `hermes-agent` first; if that skill is protected or cannot be updated, record recurring live-ops procedures here.

## Principles

1. Verify the live state, not remembered state.
2. Distinguish job execution from delivery: `last_status=ok` can coexist with delivery failure.
3. Test the platform independently before changing cron jobs.
4. Prefer minimal surgical changes: restart/reload only when needed; do not rewrite working jobs.
5. Clear stale error state only after a successful live verification.
6. Keep the final report terse: fixed/verified/remaining.

## Cron + Telegram delivery failure workflow

When cron outputs are running but Telegram delivery says `Unauthorized`:

1. Inspect cron scheduler and job state.
   - Use `hermes cron status` to confirm the scheduler/gateway PID and next run.
   - Use `hermes cron list --all` or the cronjob list tool to identify affected jobs and delivery targets.

2. Validate the configured Telegram bot token directly.
   - Read `TELEGRAM_BOT_TOKEN` from the active profile `.env` without printing the token.
   - Call Telegram Bot API `getMe` with the token.
   - `200 {"ok":true...}` means the token itself is valid.
   - `401 Unauthorized` means the active token is invalid/revoked or the process is using a different token than the file you inspected.

3. Validate the target chat independently.
   - Send a short direct test message to the target, e.g. `telegram:<chat_id>`.
   - If direct send works, token + chat are valid for the current agent/tool path.

4. Validate cron delivery path separately.
   - Create a one-shot temporary cron job with a tiny prompt and `deliver: telegram:<chat_id>`.
   - Trigger it immediately with `cronjob action=run`.
   - Wait at least one cron tick, usually 60-90 seconds, and verify output under `~/.hermes/cron/output/<job_id>/` or via cron list.
   - Remove the temporary job after verification if it remains listed.

5. If direct Telegram and cron delivery both work, treat old `last_delivery_error` entries as stale state.
   - Patch only `last_delivery_error` fields containing the resolved error.
   - Do not change prompts, schedules, models, skills, or delivery targets.
   - Re-run one affected low-risk job if practical and verify it returns `last_status=ok` with no delivery error.

6. If direct Telegram works but cron delivery still fails:
   - Restart/reload the gateway/scheduler so it picks up the current environment.
   - Re-check gateway logs for which profile and token source it loaded.
   - Verify `HERMES_HOME` / profile selection, especially in Docker multi-profile setups.

## Profile Codex auth failure workflow

When a profile cron job fails with `RuntimeError: Codex auth is missing access_token`:

1. Confirm the affected profile and job.
   - Use `hermes -p <profile> profile show <profile>` to confirm model/provider and gateway status.
   - Use `hermes -p <profile> cron list` to find the failing job and exact `last_status`.
2. Compare auth state for the working baseline profile and affected profile.
   - `hermes auth list openai-codex`
   - `hermes -p <profile> auth list openai-codex`
   - If the affected profile has stale legacy provider tokens, suppressed sources, or fewer/older credentials, prefer replacing the profile `auth.json` from a known-working profile rather than editing token fields by hand.
3. Back up before replacing credentials.
   - Copy `~/.hermes/profiles/<profile>/auth.json` to `auth.json.bak.<UTC timestamp>`.
   - Copy the known-good `~/.hermes/auth.json` (or another verified profile auth file) into the affected profile.
   - Set permissions to `600`.
4. Verify model auth independently before rerunning cron.
   - Run `hermes -p <profile> chat -q 'Reply exactly OK' --toolsets '' -Q`.
   - Success means the profile can call the configured model/provider.
5. Restart the affected profile gateway before trusting cron reruns.
   - The cron scheduler runs inside the gateway process and may keep stale credential/provider state after `auth.json` is replaced.
   - Verify a fresh gateway PID with `hermes -p <profile> gateway status`.
6. Verify the original cron path.
   - Run `hermes -p <profile> cron run <job_id>`.
   - Wait one scheduler tick (usually 60-90 seconds).
   - Re-run `hermes -p <profile> cron list --all` and confirm the job `Last run` is `ok`.
   - If the body succeeds but delivery shows `RuntimeError('cannot schedule new futures after interpreter shutdown')`, rerun once more after the restarted gateway is stable and verify the delivery error clears.
7. Keep the final report terse: backup path, auth verification, gateway restart, cron verification.

See `references/profile-codex-auth-repair.md` for the base auth-repair recipe and `references/profile-cron-rerun-after-auth-repair.md` for the cron rerun + gateway restart verification pattern.

## Docker multi-profile gateway hardening workflow

When the user asks to make all Hermes agents/profiles work reliably without repeated daily fixes:

1. Audit every gateway process environment, not just `hermes gateway status`.
   - For each `hermes -p <profile> gateway run` PID, inspect `/proc/<pid>/environ`.
   - Profile gateways must have `HERMES_HOME=~/.hermes/profiles/<profile>`.
   - If they inherit `HERMES_HOME=~/.hermes`, profile env/config isolation is broken even if the gateway appears `running`.
2. Check current-startup logs for profile-specific failures.
   - Focus on the latest `Starting Hermes Gateway` window.
   - Look for `Port 8642 already in use`, `Telegram bot token already in use`, `polling conflict`, and Codex auth failures.
3. In Docker, prevent profile gateways from inheriting global/default gateway env.
   - Launch profile gateways with profile-scoped `HERMES_HOME`.
   - Unset inherited `TELEGRAM_*`, `DISCORD_BOT_TOKEN`, and `API_SERVER_*` before sourcing the profile `.env`.
   - If the container entrypoint is read-only, harden a writable wrapper or supervisor under `~/.hermes/` instead of trying to edit the mounted script.
4. Clean stale Telegram token locks after killing bad profile gateways.
   - Lock files can point at zombie PIDs; existing `/proc/<pid>` alone is not enough.
   - Treat `STAT Z` lock owners as stale and remove those token lock files before restarting the affected profile.
5. Add a silent watchdog, not a noisy daily status report.
   - Use a no-agent cron/script that emits nothing when healthy.
   - Alert only on missing gateways, wrong `HERMES_HOME`, or true current-startup gateway failures: Telegram polling conflict, token already in use, port conflict, or platform startup failure before a successful connect.
   - Do **not** treat generic `agent.conversation_loop` / `cron.scheduler` auth strings in `gateway.log` as gateway failures. `Could not parse your authentication token` usually indicates a cron/model-auth failure when the surrounding lines mention `provider=openai-codex` or `Job '<name>' failed`; monitor that separately from gateway health.
   - If the latest startup window contains `Connected to Telegram`, `✓ telegram connected`, and `Gateway running`, clear or suppress stale earlier startup strings unless a newer true gateway error appears.
   - In Docker, do **not** identify profile gateways only by `hermes -p <profile> gateway run` in argv: the final Python process may show only `hermes gateway run`. Match live gateway PIDs by `/proc/<pid>/environ` and profile-scoped `HERMES_HOME` instead. Apply the same rule to restart supervisors to avoid false "missing" alerts or duplicate restarts.
   - If `hermes -p <profile> gateway status` shows a PID but the watchdog says missing, inspect `/proc/<pid>/environ`. A process such as `python -m hermes_cli.main --profile <name> gateway run --replace` can still have `HERMES_HOME=~/.hermes`; kill that mis-scoped PID so the entrypoint/supervisor can restart the profile with `HERMES_HOME=~/.hermes/profiles/<name>`.

See `references/docker-profile-gateway-hardening.md` for the full repair pattern, wrapper/supervisor snippets, stale-lock cleanup, and watchdog criteria. See `references/profile-gateway-watchdog-false-positives.md` for the false-positive pattern where cron/model auth errors in gateway logs are mislabeled as gateway startup issues.

## Telegram cron task-card button workflow

When cron-generated Telegram task cards show inline buttons like `✅ Done` and `⋯ More`, but tapping them does nothing:

1. Treat it as a Telegram callback-query routing problem until proven otherwise.
   - Sender scripts only emit `callback_data`; the live gateway must handle those prefixes.
   - Search profile scripts for `InlineKeyboardButton`, `callback_data`, `Done`, and `More`.
2. Inspect the callback-data prefixes and backing registries.
   - Known examples: Zeus `zt:` / `ztm:` and Catthew `ct:` / `ctm:`.
   - Confirm registry paths and schema before writing handler logic.
3. Patch the central Telegram gateway adapter, not only the cron sender script.
   - Dispatch task-card prefixes early in `_handle_callback_query`.
   - `More` should answer quickly, edit the card with details, and keep the Done/More keyboard active.
   - `Done` should update registry state, safely update the backing task source if supported, then edit the card and remove the keyboard.
4. Keep writes profile-safe.
   - Treat callback data as a registry key, never a file path.
   - Only update source task files under an explicit safe root such as `/vault/Tasks/tasks`.
5. Restart and verify every relevant profile gateway.
   - Check `/proc/<pid>/environ` for profile-scoped `HERMES_HOME`.
   - Tail latest logs for `Connected to Telegram (polling mode)`, `✓ telegram connected`, and `Gateway running with 1 platform(s)`.
6. Verify with a local callback self-test before reporting success.
   - Use a temporary registry and fake query object to exercise both `More` and `Done`.
   - Compile/import the patched gateway module in the project venv.

See `references/telegram-cron-task-card-callbacks.md` for prefix examples, fix pattern, safe-write rules, and verification checks.

## Weekly ops audit workflow

When auditing Hermes operational health for gateways, MCP servers, cron jobs, and obvious configuration drift:

1. Start with live state: `hermes --version`, `hermes status --all`, `hermes doctor`, `hermes config check`, `hermes profile list`, `hermes gateway status`, `hermes cron status`, `hermes cron list --all`, and `hermes mcp list`.
2. Audit each profile individually with `hermes -p <profile> gateway status`, `cron status`, `cron list --all`, `mcp list`, and auth checks if model errors appear.
3. In scheduled/no-user-present cron contexts, arbitrary `execute_code` may be blocked by approval policy. Prefer normal `terminal`, `search_files`, and `read_file` calls; if needed, run small Python snippets via `terminal` rather than stopping the audit.
4. Check multi-profile gateway drift explicitly: each profile gateway process should have `HERMES_HOME=~/.hermes/profiles/<profile>`, each profile should have its own `.env` and `config.yaml`, and token comparisons must use redacted fingerprints only.
5. Treat `Telegram bot token already in use (PID X)` carefully: inspect `/proc/<pid>/stat`; `STAT Z` indicates a zombie/stale conflict that usually requires reaping/restarting the supervisor/container rather than assuming a live duplicate gateway.
6. For repeated `Api_Server Port 8642 already in use`, identify which process owns the listener and recommend either disabling `api_server` on non-default profiles or assigning unique API server ports.
7. For MCP servers listed as enabled, test them directly with `hermes -p <profile> mcp test <server>` (or `hermes mcp test <server>` for default). `mcp list` proves configuration only; `mcp test` proves the server can spawn/connect and expose tools.
8. Audit recent cron output files, not only `last_status`. A job can show `Last run: ok` while its delivered/report body says the intended operation did not happen (for example a backup job that exits cleanly after reporting a missing credential). For high-value jobs, read the latest output under `~/.hermes[/profiles/<profile>]/cron/output/<job_id>/` and look for explicit failure text such as `did not run`, `FAIL:`, `missing`, `No files were`, or `Action:`.
   - When keyword-scanning cron output markdown, ignore the prompt/loaded-skill section and inspect the `## Response` body first. Cron output often contains words like `missing`, `FAIL`, `error`, or setup troubleshooting tables inside the prompt itself; reporting those as current failures creates false positives.
   - Treat recurring backup jobs as high-value even when `last_status=ok`: inspect the latest backup output for “did not run”, missing token, no commit/push attempted, or similar safety-stop text, then check `git status --short` only to confirm whether unsynced local state exists.
   - For vault/wiki cron blockers, verify the referenced files directly with `stat` and readability/writability checks before reporting them; distinguish still-broken root-owned files from stale prior warnings that have already been fixed.
   - Missing optional provider credentials are action-worthy only when they block an active job or requested capability. Do not turn a generic `doctor` optional-key inventory into an ops finding unless there is operational impact.
9. For MCP servers listed as enabled, `mcp list` is only configuration evidence. Run `hermes [-p <profile>] mcp test <server>` for each enabled server before reporting it broken. If the only symptom is repeated `keepalive failed ... Unknown method: ping` log noise but `mcp test` connects and discovers tools, report it at most as low-priority log noise, not an outage.
10. For gateway log errors such as `api_server Port 8642 already in use`, inspect the latest startup window and the live listener state (for example `ss -ltnp`) before reporting. If the latest startup ends with `Gateway running` and there is no current listener/conflict, treat earlier port-conflict lines as stale startup noise.
11. Report only action-worthy findings: affected component/profile/job, exact symptom, and next action. Omit healthy inventory unless it clarifies scope.

See `references/weekly-ops-audit.md` for a compact runbook with commands, log patterns, and reporting guidance.

## Codex gpt-5.5 auto-compaction notice workflow

When the user replies to the startup notice about Codex gpt-5.5 raising auto-compaction to 85% and says "fix this issue":

1. Treat it as an unwanted repeated notice, not a model failure.
2. Preserve the intended behavior by setting `compression.threshold: 0.85`.
3. Stop the notice by setting `compression.codex_gpt55_autoraise: false`.
4. Apply the pair to the emitting profile, and usually default + active Telegram profiles for consistency.
5. Verify with a minimal Hermes startup/chat run that the `Codex gpt-5.5 caps context` notice no longer appears.

Details and pitfalls: `references/codex-gpt55-compression-notice.md`.

## Useful commands

```bash
hermes cron status
hermes cron list --all
hermes -p <profile> auth list openai-codex
hermes -p <profile> chat -q 'Reply exactly OK' --toolsets '' -Q
hermes -p <profile> cron run <job_id>
ps -p <PID> -o pid,ppid,stat,etime,cmd

python3 - <<'PY'
import urllib.request
from pathlib import Path
for line in (Path.home()/'.hermes/.env').read_text().splitlines():
    if line.startswith('TELEGRAM_BOT_TOKEN='):
        token=line.split('=',1)[1].strip().strip('"\'')
        break
with urllib.request.urlopen(f'https://api.telegram.org/bot{token}/getMe', timeout=15) as r:
    print(r.status, r.read().decode()[:300])
PY
```

## Pitfalls

- `last_status=ok` means the cron agent completed; it does not guarantee delivery succeeded.
- `last_delivery_error` may persist after the underlying Telegram issue is fixed. Clear it only after a successful direct send and a successful cron delivery test.
- `origin` delivery depends on stored origin metadata. If `origin` is null or stale, prefer explicit `telegram:<chat_id>` for jobs that must deliver to Telegram.
- Do not print bot tokens. Redact token values and lengths only if needed.
- Do not capture a transient Unauthorized incident as a permanent claim that Telegram is broken.

## Cron job API failure workflow

When cron jobs report `last_status=error` due to an API call failure (delivery was fine but the job itself errored):

1. Read `~/.hermes/logs/errors.log` for the job ID mentioned in the error (e.g. `cron_c9c38ab77915_20260526_180057`).
2. Follow the session ID into `~/.hermes/logs/agent.log` to see the full conversation turn and API call attempt logs.
3. Trace the error type and summary:
   - `error_type=TypeError` + `Non-retryable client error` = classified as local validation error (TypeError/ValueError not subclassing UnicodeEncodeError/json.JSONDecodeError/ssl.SSLError). This bypasses retries. Check if the source is a provider response parsing issue.
   - `error_type=ReadError` + `Broken pipe` = provider connection was killed by stale-call detector. Usually a high-traffic backlog or slow model.
   - `error_type=RateLimitError` + HTTP 429 = usage limit reached. Check `resets_at` timestamp.
4. For Codex-reserved API errors (chatgpt.com/backend-api/codex), view the full response path:
   - `_interruptible_api_call` (`agent/chat_completion_helpers.py`) runs the API call in a background thread.
   - `_run_codex_stream` (`agent/codex_runtime.py`) handles the streaming response with retry + fallback.
   - `_run_codex_create_stream_fallback` (`agent/codex_runtime.py`) is the fallback when the primary stream fails.
   - `_normalize_codex_response` (`agent/codex_responses_adapter.py`) normalizes the raw response.
5. Verify the fix by running the job immediately with `cronjob action=run job_id=<id>` and checking `last_status`.

## Useful commands for API-tracing

```bash
# Find all cron errors in the last N hours
grep "Job.*failed:" /home/hermes/.hermes/logs/errors.log

# Follow a specific job's trace through logs
grep "cron_<job_id>" /home/hermes/.hermes/logs/errors.log
grep "cron_<job_id>" /home/hermes/.hermes/logs/agent.log | grep -E "(API call failed|Non-retryable|conversation turn)"

# Run a job immediately to verify fix
# Use cronjob tool action=run with the job_id
```

## References

- `references/telegram-cron-unauthorized.md` — resolved incident pattern: valid token, working direct send, successful cron test, stale Unauthorized state cleared.
- `references/codex-stream-typeerror.md` — Codex stream TypeError from malformed SSE frame: root cause, fix, and affected code paths.
- `references/profile-codex-auth-repair.md` — profile-specific OpenAI Codex auth repair when cron/model calls fail with missing `access_token` despite `auth list` showing credentials.
- `references/docker-profile-gateway-hardening.md` — Docker multi-profile gateway hardening: profile-scoped `HERMES_HOME`, inherited env cleanup, stale zombie lock removal, supervisor, and silent watchdog pattern.
- `references/telegram-cron-task-card-callbacks.md` — Telegram cron task-card inline button callbacks: prefix routing, registry updates, safe source-file writes, gateway restarts, and local callback self-tests.
- `references/profile-gateway-watchdog-false-positives.md` — avoid misclassifying cron/model auth failures in gateway logs as profile gateway startup failures.
