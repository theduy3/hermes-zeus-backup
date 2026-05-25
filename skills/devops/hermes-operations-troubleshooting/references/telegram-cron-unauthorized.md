# Telegram cron Unauthorized delivery pattern

Session pattern captured from a resolved Hermes cron incident.

## Symptoms

- Cron scheduler running and jobs firing.
- Active jobs show `last_status = ok`.
- Several jobs show `last_delivery_error = delivery error: Telegram send failed: Unauthorized`.
- Affected jobs may include a mix of `deliver: origin` and explicit `deliver: telegram:<chat_id>`.

## Diagnosis sequence that worked

1. Listed cron jobs and confirmed execution was healthy.
2. Inspected active profile `.env` for Telegram settings without exposing the token.
3. Called Telegram Bot API `getMe` with the configured token.
   - Result: `200 OK`, proving the token was valid at the time of diagnosis.
4. Sent a direct Telegram test message to the configured chat ID.
   - Result: success, proving current token + chat delivery path worked.
5. Created and ran a temporary one-shot cron job with `deliver: telegram:<chat_id>` and a tiny prompt.
   - Output file appeared under `~/.hermes/cron/output/<job_id>/`, proving cron execution path worked.
6. Re-ran one affected low-risk job.
   - Result: `last_status=ok` and no new delivery error.
7. Cleared stale `last_delivery_error` fields containing the resolved `Telegram send failed: Unauthorized` error.
8. Re-listed cron jobs to verify all active jobs were `ok` with no Telegram delivery warnings.

## Key lesson

If Telegram token validation, direct send, cron test delivery, and an affected job rerun all succeed, old `last_delivery_error` values can be stale operational state rather than an active failure. Clear only the resolved error fields after verification.

## Safe patch pattern

Use JSON parsing rather than broad text replacement:

```python
from pathlib import Path
import json
p = Path('/home/hermes/.hermes/cron/jobs.json')
data = json.loads(p.read_text())
for job in data.get('jobs', []):
    if job.get('last_delivery_error') and 'Telegram send failed: Unauthorized' in job['last_delivery_error']:
        job['last_delivery_error'] = None
p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
```

Do not alter prompts, schedules, skills, models, or delivery targets while clearing stale error state.
