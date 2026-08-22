# Cross-profile cron provider-audit & repair (missing provider)

Scenario: cron jobs (or a `blocked_config` alert) fail with
`provider credential missing: No Codex credentials stored`.

Root cause: jobs are pinned to `openai-codex` (no creds anywhere) OR have
`provider:null` and inherit the profile default provider (openai-codex) at runtime.

## Confirm the credential pool
```bash
hermes auth list
```
Look for which providers have stored tokens (nous, xai-oauth, openai-codex).
If `openai-codex` is absent, repoint jobs to a working provider rather than
repairing Codex auth.

## Reusable cross-profile scan + repair script
Save as a script (e.g. `~/.hermes/scripts/cron_provider_audit.py`) and run with
`python3`. Dry-run prints every Codex-blocked job; set `REPAIR=True` after
confirming scope to rewrite them to a chosen provider/model.

```python
import json, glob, os
BASE = os.path.expanduser('~/.hermes')
files = [os.path.join(BASE, 'cron/jobs.json')] + sorted(
    glob.glob(os.path.join(BASE, 'profiles', '*', 'cron', 'jobs.json')))
REPAIR = False                       # flip to True after a clean dry run
PROV, MODEL = 'nous', 'upstage/solar-pro4:free'  # per-profile default varies (see table)
hits = []
for f in files:
    scope = 'default' if f.endswith('cron/jobs.json') else f.split('/profiles/')[1].split('/')[0]
    raw = json.load(open(f))
    jobs = raw.get('jobs') if isinstance(raw, dict) else raw
    for j in jobs:
        if not isinstance(j, dict):
            continue
        p = j.get('provider')
        blocked = (p == 'openai-codex') or (
            p is None and j.get('last_status') == 'blocked_config'
            and j.get('no_agent') is not True)
        if blocked:
            hits.append((scope, j.get('job_id') or j.get('id'), p, j.get('model')))
            if REPAIR:
                j['provider'] = PROV
                j['model'] = MODEL
                if j.get('last_status') == 'blocked_config':
                    j['last_status'] = 'pending'
                if j.get('last_error'):
                    j['last_error'] = None
                if 'preflight_alerted' in j:
                    j['preflight_alerted'] = False
    if REPAIR:
        json.dump(raw, open(f, 'w'), indent=1)
for h in hits:
    print(h)
print('total Codex-blocked:', len(hits))
```

## Per-profile Nous model mapping (observed fleet — verify via each config.yaml)
| profile                                  | Nous default model        |
|------------------------------------------|---------------------------|
| default                                  | upstage/solar-pro4:free   |
| zeus / catthew / thor / wiki / butter / charles / finance | tencent/hy3:free |

Pin each job to its own profile's Nous default to match the already-working jobs.

## Silent-inheritance gotcha
`provider: null` does NOT avoid the block. The scheduler resolves null to the
profile default provider (openai-codex) → `blocked_config`. Always set the
provider explicitly when the default provider lacks credentials.

## Verification
- Re-run the scan with `REPAIR=False` → expect 0 hits.
- Live test: `hermes cron run --profile <p> <job_id>` → `Ran now: succeeded.`
- The scheduler reads `jobs.json` from disk each tick (inside the gateway
  process); no restart is needed after JSON edits.

## `cronjob` agent-tool limits (vs the real CLI)
- Reaches the DEFAULT profile only; other profiles need `hermes cron --profile <p>`
  or a direct `jobs.json` edit.
- `cronjob update` ignores `provider`/`model` ("No updates provided") → edit the
  JSON directly.
- `hermes cron list/run/edit` DO understand `--profile` and the `provider`/`model`
  fields — prefer the real CLI for non-default profiles.
