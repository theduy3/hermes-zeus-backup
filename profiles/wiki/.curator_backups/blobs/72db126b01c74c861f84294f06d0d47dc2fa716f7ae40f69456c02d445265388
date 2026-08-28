# Cron stale model-pin 404 (wiki profile, 2026-08-27)

## Symptom

Manual/scheduled fire of `vault-wiki-ingest` (and potentially sibling agent jobs) failed immediately with:

```text
HTTP 404: Model 'hy3-free' not found.
The requested model does not exist in our configuration or OpenRouter catalog.
```

No wiki work ran. Chat session was healthy on **grok-4.5** / **xai-oauth**.

## Root cause

Per-job pins in `cron/jobs.json`, not the live chat model:

| Field | Stale value |
|-------|-------------|
| `model` | `tencent/hy3:free` |
| `provider` | `nous` |

Resolved name surfaced as missing **`hy3-free`**. Profile `config.yaml` also listed `fallback_providers: [{provider: nous, model: hy3-free}]` — same dead id family.

## Fix that worked

```bash
# Clear pin so job inherits model.default / model.provider
hermes cron edit <job_id> --model '' --provider ''

# Confirm
python3 -c "import json; j=json.load(open('$HERMES_HOME/cron/jobs.json')); ..."

# Rerun
# cronjob(action='run', job_id=...)
```

Cleared on wiki profile for: `vault-today`, `vault-process`, `vault-wiki-ingest`, `vault-wiki-lint`, `vault-tonight`, `stock-watchlist-last30days-weekly`. Script-only jobs (`no_agent: true`) already had null model.

After clear + manual run, `vault-wiki-ingest` completed ok (~8m) and delivered a normal ingest summary.

## Operator notes

- Session model ≠ job model when pins exist.
- Empty string on `--model` / `--provider` clears pins (`hermes cron edit --help`).
- Prefer clearing pins over re-pinning free/nous models unless the user confirms a live catalog id.
- On one pin failure, sweep other agent jobs on the same profile.
