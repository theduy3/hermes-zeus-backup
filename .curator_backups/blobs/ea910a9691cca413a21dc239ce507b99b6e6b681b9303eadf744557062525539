# Pin vs stale drift_skip

`last_status=error` + `RuntimeError: [drift_skip] ... job is unpinned` is not proof the job is still unpinned.

## Check the record, not cron list

Read `~/.hermes/profiles/<p>/cron/jobs.json` (or default `~/.hermes/cron/jobs.json`). Look at `provider`, `model`, `provider_snapshot`, `model_snapshot`, `drift_alerted`.

If `provider` and `model` are already set (e.g. `nous` / `tencent/hy3:free`), the job is pinned. `cron_model_drift_axes` skips any axis with `job[axis]` set. Null snapshots on a pinned job are correct: `_compute_provider_model_snapshots` only snapshots unpinned axes.

## CLI edit of the same pin is a no-op

```
hermes -p <p> cron edit <id> --provider nous --model tencent/hy3:free
```

When those fields already match, Hermes reports “Updated job” but does not rewrite snapshots and does not clear `last_error` / `drift_alerted`. Do not treat that as healing the skip state.

## Clear stale skip display

The `cronjob` tool is default-only. After the user asked to change that profile, patch `jobs.json` with `cross_profile=True`:

- `last_status`: `pending`
- `last_error`: null
- `failure_streak`: 0
- drop `drift_alerted`

The scheduler re-reads disk each tick. No gateway restart.

## Verify

`cron_model_drift_axes(job, current_provider=..., current_model=...)` → `[]`.

Do not fire a household Telegram reminder just to prove the pin.

The error text “job stays skipped until pinned” means the guard re-evaluates at fire time. A leftover `last_error` does not latch a skip once the job is pinned.
