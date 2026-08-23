# Stale drift_skip after an already-pinned job

See `hermes-cron-ops` `references/stale-drift-skip-pin.md` for the full recipe.

Short form: `cron list` showing last-run `drift_skip` can be stale. If `jobs.json` already has `provider` + `model` set, the next fire will not skip. `hermes cron edit` with the same provider/model is a no-op. Clear `last_status` / `last_error` / `drift_alerted` on the profile `jobs.json` (`cross_profile=True` after the user asked). Confirm with `cron_model_drift_axes` → `[]`.
