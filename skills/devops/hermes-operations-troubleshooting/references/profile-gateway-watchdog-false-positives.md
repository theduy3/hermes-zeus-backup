# Profile gateway watchdog false positives

Use this note when a Hermes profile gateway watchdog reports profile issues like `current startup log issue: Could not parse your authentication token` even though Telegram gateways appear to be running.

## Symptom

A no-agent watchdog reports:

```text
Hermes profile watchdog found issues:
- catthew: current startup log issue: Could not parse your authentication token
- thor: current startup log issue: Could not parse your authentication token
- zeus: current startup log issue: Could not parse your authentication token
```

But live verification shows:

```text
hermes gateway status  # all profile PIDs running
latest startup window contains Connected to Telegram / ✓ telegram connected
profile chat smoke test returns OK
profile_gateway_watchdog.py emits nothing after restart/current window
```

## Root cause pattern

`gateway.log` can contain multiple subsystems because cron scheduling and model calls run inside the gateway process. A line like:

```text
WARNING agent.conversation_loop: ... provider=openai-codex ... HTTP 401: Could not parse your authentication token
ERROR cron.scheduler: Job '<name>' failed ... Could not parse your authentication token
```

is a cron/model-auth failure, not necessarily a gateway startup failure. A watchdog that scans the latest `Starting Hermes Gateway` window for the raw string `Could not parse your authentication token` will misclassify cron job failures as gateway startup issues.

## Correct diagnostic sequence

1. Verify process state by environment, not argv alone:
   - inspect gateway PIDs and `/proc/<pid>/environ`
   - profile gateway must have `HERMES_HOME=~/.hermes/profiles/<profile>`
2. Inspect only the latest startup window for true gateway symptoms:
   - `polling conflict`
   - `token already in use`
   - `Port 8642 already in use`
   - fatal platform startup errors before a successful connect
3. Treat `Could not parse your authentication token` as model/cron-auth unless the surrounding log context is a gateway startup/auth path.
4. If the same startup window later contains `Connected to Telegram`, `✓ telegram connected`, and `Gateway running`, do not keep earlier generic auth strings as active gateway failures.
5. Verify model auth separately:
   - `HERMES_HOME=<profile-home> hermes -p <profile> chat -Q -q 'Reply OK only'`
6. Run the watchdog script directly. A healthy no-agent watchdog should print nothing.

## Watchdog design rule

Keep gateway and model/cron auth monitors separate:

- **Gateway watchdog:** missing PID, wrong `HERMES_HOME`, Telegram polling conflict, token already in use, port conflict, platform startup failure.
- **Cron/model auth watchdog:** job name/profile, provider/model, HTTP 401/429/auth error, last_status.

Do not put generic `agent.conversation_loop` or `cron.scheduler` auth strings in a gateway-startup problem list unless the alert label explicitly says cron/model auth.

## Minimal smoke tests

```bash
# Gateway health
hermes gateway status
for p in catthew thor zeus; do
  HERMES_HOME=/home/hermes/.hermes/profiles/$p hermes -p $p gateway status
  HERMES_HOME=/home/hermes/.hermes/profiles/$p hermes -p $p chat -Q -q 'Reply OK only'
done

# Watchdog should stay silent when healthy
python3 /home/hermes/.hermes/scripts/profile_gateway_watchdog.py
```
