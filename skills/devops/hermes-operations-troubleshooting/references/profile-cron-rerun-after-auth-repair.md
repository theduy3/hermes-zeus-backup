# Profile cron rerun after Codex auth repair

Use when a profile cron job fails with OpenAI Codex `401 token_expired`, the profile's `hermes -p <profile> chat -q 'Reply exactly OK'` fails, but a baseline/default profile succeeds.

## Pattern

1. Compare auth state:
   ```bash
   hermes auth list openai-codex
   hermes -p <profile> auth list openai-codex
   ```
2. Back up and replace stale profile auth from a known-good profile:
   ```bash
   TS=$(date -u +%Y%m%dT%H%M%SZ)
   cp ~/.hermes/profiles/<profile>/auth.json ~/.hermes/profiles/<profile>/auth.json.bak.$TS
   cp ~/.hermes/auth.json ~/.hermes/profiles/<profile>/auth.json
   chmod 600 ~/.hermes/profiles/<profile>/auth.json
   ```
3. Verify profile model auth outside cron:
   ```bash
   hermes -p <profile> chat -q 'Reply exactly OK' --toolsets '' -Q
   ```
4. Restart the affected profile gateway before trusting cron reruns. The scheduler runs inside the gateway process and may keep stale credential/provider state until restart.
   - Find profile PID with `hermes -p <profile> gateway status`.
   - Kill/restart via the configured supervisor, or start the profile gateway with profile-scoped `HERMES_HOME`.
   - Verify `hermes -p <profile> gateway status` shows a fresh running PID.
5. Rerun the affected jobs:
   ```bash
   hermes -p <profile> cron run <job_id>
   ```
6. Wait at least one scheduler tick (60–90s), then verify:
   ```bash
   hermes -p <profile> cron list --all
   ```
   Confirm `Last run ... ok` and no `Delivery failed` line.

## Pitfalls

- A successful direct `hermes -p <profile> chat` only proves the CLI path uses fresh auth; the already-running gateway scheduler may still fail with old auth until restarted.
- `cron run` only schedules the job for the next tick. Always wait and inspect `Last run`.
- If the first rerun after gateway restart shows the job body succeeded but delivery failed with `RuntimeError('cannot schedule new futures after interpreter shutdown')`, rerun once more after the fresh gateway is stable and verify delivery clears.
- Do not report success after only triggering the jobs; report success only after `Last run ... ok` is observed for each requested job.