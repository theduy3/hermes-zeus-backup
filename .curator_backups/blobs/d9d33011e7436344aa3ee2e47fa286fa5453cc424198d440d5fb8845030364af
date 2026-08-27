# Profile model audit & model-availability checks

## 1. Auditing current model config across all profiles

When the user asks "which model is each profile using" / "check the models per
profile", READ each profile's `config.yaml` — do not trust `hermes status`
(single-profile, hides aux/vision) or `hermes -p <p> status` (same gap). Parse
the YAML directly.

Reusable audit script (run via `terminal`, not execute_code — no approval gate):

```python
import glob, os, yaml
BASE=os.path.expanduser('~/.hermes')
files=[( 'default', os.path.join(BASE,'config.yaml') )]
for p in sorted(os.listdir(os.path.join(BASE,'profiles'))):
    cfg=os.path.join(BASE,'profiles',p,'config.yaml')
    if os.path.isfile(cfg): files.append((p, cfg))
for name, path in files:
    try:
        c=yaml.safe_load(open(path,encoding='utf-8')) or {}
    except Exception as e:
        print(f"{name:9} ERROR {e}"); continue
    m=c.get('model',{}) or {}
    aux=(m.get('auxiliary') or {})
    vis=(aux.get('vision') or {}) if isinstance(aux,dict) else {}
    default=m.get('default')
    cosmetic=m.get('name')                       # DISPLAY LABEL ONLY
    provider=m.get('provider')
    mot=m.get('max_output_tokens')
    vmodel=vis.get('model') if vis else None
    vprov=vis.get('provider') if vis else None
    flag=''
    if cosmetic and cosmetic!=default: flag=f"  <-- cosmetic name:{cosmetic} != default:{default}"
    print(f"{name:9} default={default} provider={provider} max_out={mot} vision={vmodel}@{vprov}{flag}")
```

### Pitfall: cosmetic `model.name` label

`model.name: gpt-5.6-luna` (seen on several profiles) is ONLY a display label.
The ACTIVE model is `model.default` (e.g. `tencent/hy3:free`). A naive audit that
reads `name` concludes the profile runs gpt-5.6-luna when it actually runs hy3.
Always report `model.default`, and flag when `name != default` so the user knows
the label is decorative.

### Pitfall: per-profile `max_output_tokens` divergence

Profiles can carry different `max_output_tokens` for the same `model.default`.
Observed: default=8192 vs all named profiles=128000. That silently caps the
default bot's reply length much shorter. Flag divergence in the audit.

## 2. Checking whether a model exists / is free on a provider

### When web tools + provider /v1/models are unavailable

`web_search`/`web_extract` need FIRECRAWL_API_KEY (absent → both fail). Provider
endpoints may be Cloudflare-blocked. Fallback: the bundled model catalog ships in
the hermes-agent checkout:

- Canonical bundled copy: `~/.hermes/hermes-agent/website/static/api/model-catalog.json`
- (A refreshed copy may also appear at `/tmp/model-catalog.json` after `hermes model`.)

Structure: `{ "providers": { "<provider>": { "metadata": {...}, "models": [ {"id": "...", "description": "...", "provider": "..."}, ... ] } } }`.

Parse for existence on a provider:

```python
import json
d=json.load(open('/home/hermes/.hermes/hermes-agent/website/static/api/model-catalog.json'))
for prov,v in d['providers'].items():
    ids=[m.get('id') for m in v.get('models',[])]
    if any('ox' in i.lower() or 'alpha' in i.lower() for i in ids):
        print(prov, [i for i in ids if 'ox' in i.lower() or 'alpha' in i.lower()])
```

### CRITICAL caveat: catalog ≠ free-tier truth

The catalog manifest does NOT encode which Nous models are free. The `nous`
provider's `metadata.note` states: "Free-tier gating is determined live via
Portal pricing (partition_nous_models_by_tier), not this manifest."

- A model present in the catalog is NOT necessarily free.
- The `description: "free"` field that appears on some entries (e.g.
  `openrouter/elephant-alpha`) belongs to the **openrouter** provider, not nous.
- Therefore "is <model> free on Nous?" CANNOT be answered from the catalog alone.
  It requires a live Nous Portal pricing check (`hermes model` / Portal). The
  catalog only answers "does this model ID exist on this provider."

### Pitfall: cosmetic label vs real model in availability answers

If a user asks "is <X> on Nous?", first confirm <X> is not itself a cosmetic
label. Example: a profile labeled `name: gpt-5.6-luna` does not mean "gpt-5.6-luna"
is the configured/active model — verify against `model.default`.
