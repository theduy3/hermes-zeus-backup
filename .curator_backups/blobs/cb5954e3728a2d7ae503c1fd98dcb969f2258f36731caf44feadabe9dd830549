# Weekly Hermes ops audit pattern

Use this reference when auditing Hermes operational health across gateways, MCP servers, cron jobs, and configuration drift in a scheduled/no-user-present context.

## Scope

Audit live state, not remembered state:

- `hermes --version`
- `hermes status --all`
- `hermes doctor`
- `hermes config check`
- `hermes profile list`
- `hermes gateway status`
- `hermes cron status`
- `hermes cron list --all`
- `hermes mcp list`

For every profile under `~/.hermes/profiles/<profile>/`, also run:

- `hermes -p <profile> gateway status`
- `hermes -p <profile> cron status`
- `hermes -p <profile> cron list --all`
- `hermes -p <profile> mcp list`
- `hermes -p <profile> auth list openai-codex` when model/auth errors appear

## Cron-job execution caveat

Scheduled cron agents may be denied arbitrary Python execution via `execute_code` even when normal tools are available. Do not encode this as a permanent tool limitation. In cron audits, prefer regular `terminal`, `search_files`, and `read_file` tool calls, or small `python3 - <<'PY'` snippets through `terminal` when shell approval permits.

## Multi-profile drift checks

1. **Gateway process isolation**
   - Inspect `ps` for all `hermes ... gateway run` processes.
   - Check each `/proc/<pid>/environ` for `HERMES_HOME`.
   - Default gateway should use `~/.hermes`; profile gateways should use `~/.hermes/profiles/<profile>`.

2. **Token collision without exposing secrets**
   - Read `.env` files and print only short SHA-256 prefixes for `TELEGRAM_BOT_TOKEN` / `DISCORD_BOT_TOKEN`.
   - Flag duplicate token fingerprints across profiles.
   - Also verify each profile has both `.env` and `config.yaml`.

3. **Zombie PID / stale lock conflict**
   - When logs say `Telegram bot token already in use (PID X)`, check `/proc/<pid>/stat`.
   - `STAT Z` means a zombie process; treat this as a stale conflict and restart/reap the owning supervisor/container rather than assuming a live duplicate gateway.
   - Compare against current `gateway.lock` files; healthy locks should reference live gateway PIDs.

4. **API server port conflicts**
   - If profile logs show `Api_Server Port 8642 already in use`, identify the listener via `/proc/net/tcp*` socket inode lookup or `ss -ltnp` if available.
   - Usually only one gateway can own the default API server port. Recommend disabling `api_server` on non-default profiles or assigning unique ports per profile.

## Cron health interpretation

- `last_status=ok` means the job completed; it does not prove delivery worked.
- `last_delivery_error` can persist after a later successful run. Treat it as stale only after a successful delivery verification or a subsequent job run with no delivery error.
- Parse each profile's `cron/jobs.json` to find non-OK `last_status`, non-empty `last_error`, non-empty `last_delivery_error`, and paused jobs.
- If a job failed with provider auth errors but `auth list` now looks healthy, report it as “rerun to verify; re-auth only if still failing” rather than immediately rewriting credentials.

## Log scanning

Search recent logs modified in the last week under:

- `~/.hermes/logs/`
- `~/.hermes/profiles/*/logs/`

Useful patterns:

```text
TimedOut|ConnectError|polling conflict|Unauthorized|RuntimeError|Traceback|failed|error|Port .* in use|token already in use|Codex auth|missing access_token|429|RateLimit|Broken pipe|Timed out
```

Prefer action-worthy current/recent findings over old historical noise.

## Reporting style

For scheduled weekly ops reports, keep output concise and action-only:

- State the affected component/profile/job.
- Quote the exact symptom or error in one line.
- Give the next action.
- Suppress healthy inventory unless it matters for contrast.
