# Codex rate-limit from LLM-based gateway watchdogs

Use this reference when Hermes profiles all report provider auth/rate-limit errors and they share one `openai-codex` OAuth account.

## Durable pattern

A frequent watchdog cron such as `every 2m` must not run a full Hermes agent prompt on a premium model. Even a small health-check prompt can consume tens of thousands of tokens per run once skills/system context/log inspection are loaded. Across many profiles, this can exhaust a shared OpenAI Codex / ChatGPT team quota and surface in gateways as sanitized messages such as:

- `Provider authentication failed`
- `The model provider is rate-limiting requests`

Raw log signatures:

- `provider=openai-codex base_url=https://chatgpt.com/backend-api/codex model=gpt-5.5`
- `HTTP 429: The usage limit has been reached`
- `error.type: usage_limit_reached`
- `plan_type: team`
- `resets_at` / `resets_in_seconds`
- followed by fallback/title-generation messages such as `no Codex OAuth token found` or unrelated 401s from auxiliary providers

## Diagnosis checklist

1. List profiles and auth state:
   - `hermes profile list`
   - `hermes auth list`
   - `hermes -p <profile> auth list`
2. Check gateway/agent logs for 429s and sanitized provider errors:
   - `~/.hermes/logs/errors.log*`
   - `~/.hermes/profiles/<profile>/logs/errors.log*`
   - `~/.hermes/profiles/<profile>/logs/agent.log*`
3. Aggregate recent token usage by session/job from `agent.log` lines containing `API call #... provider=openai-codex ... total=...`.
4. Look for recurring `cron_<job_id>_...` sessions consuming large totals at high frequency.
5. Convert `resets_at` timestamps to UTC to know whether the quota window has already reopened.

## Immediate mitigation

- Pause or remove the runaway LLM cron job.
- Run `hermes auth reset openai-codex` after the reset window if Hermes has marked the credential exhausted.
- Do not interpret a sanitized gateway `Provider authentication failed` message as proof that the OAuth login is invalid; inspect raw logs first.

## Permanent fix

For gateway health/watchdog jobs:

- Prefer `no_agent=true` with a deterministic script that prints only when something is wrong.
- If reasoning is actually required, run it rarely (hourly/daily), pin a cheaper model/provider, and cap scope.
- Avoid `every 2m` agent jobs on `gpt-5.5` or any premium shared-quota model.
- Keep frequent checks as shell/Python status probes: process list, `hermes -p <profile> gateway status`, recent log grep, and restart commands if missing.

## Codex model downgrade gotchas

When reducing cron/profile cost for `openai-codex`, do not assume every listed Codex model works with the user's ChatGPT account. In practice, `gpt-5.4-nano` can be listed in Hermes metadata but fail at runtime with:

- `The 'gpt-5.4-nano' model is not supported when using Codex with a ChatGPT account.`

Safe sequence:

1. Smoke-test the candidate model before changing all profiles/jobs:
   - `hermes chat -q 'Reply exactly: ok' --provider openai-codex -m <model> -Q`
2. If `gpt-5.4-nano` is rejected, test `gpt-5.4-mini`; it is the smaller working Codex fallback observed on ChatGPT-backed Codex OAuth.
3. Only after a successful smoke test, update profile configs and cron job model pins.
4. Restart gateways after profile config changes so long-running gateway processes pick up the new default model. If restart approval is blocked or unavailable, report that disk config changed but running processes may still use the old model until restart.
5. Be careful testing paused cron jobs: triggering a paused job can leave it enabled/scheduled again depending on scheduler behavior. Re-check `enabled/state` after any `cronjob run` and pause it again if it is meant to remain disabled.

## Script-only watchdog shape

A good watchdog script should:

1. Iterate expected profile names.
2. Check for a running `hermes -p <profile> gateway run` process or use profile status.
3. Start only missing gateways.
4. Verify logs/status after restart.
5. Print nothing when all is healthy, so cron delivery stays silent.
6. Print a concise alert only on restart/failure.
