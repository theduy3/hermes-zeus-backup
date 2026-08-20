# Orcarouter Model Picker Diagnosis

Session: 2026-08-18. User's Hermes Agent config had orcarouter set up as a bare custom endpoint (inline `model.provider: custom` + `model.base_url`). The `/model` picker showed no orcarouter option — only the provider choice appeared with zero models.

## Root Cause

Config was:

```yaml
model:
  default: qwen/qwen3.8-27b-free
  provider: orcarouter
  api_mode: chat_completions
  max_output_tokens: 8192
```

Plus `.env` had `ORCAROUTER_API_KEY=sk-orc...`. There was NO `providers:` dict entry and NO `custom_providers:` list entry. The provider name `orcarouter` was just sitting in `model.provider` with no corresponding provider definition anywhere.

The `/model` picker inventory (`hermes_cli/inventory.py` → `build_models_payload` → `list_authenticated_providers`) only enumerates providers from:

- `providers:` dict (new-style, keyed by provider name)
- `custom_providers:` list (legacy)

A bare `model.provider: orcarouter` with no matching entry in either collection is invisible to the picker. The user saw "orcarouter" as a provider choice but no models under it.

## What Still Works

The runtime provider resolution (`runtime_provider.py:_get_named_custom_provider`) does NOT fall back to bare custom when the provider name is non-empty but unmatched — it only falls back to bare custom trust path (`model.base_url`) when `model.provider: custom`. With `model.provider: orcarouter` and no provider definition, the config is effectively broken: no models to browse, and calls may fail with "unknown provider" at runtime.

## Fix Applied

Added to `providers:` dict:

```yaml
providers:
  orcarouter:
    api: https://api.orcarouter.ai/v1
    api_key_env: ORCAROUTER_API_KEY
    default_model: qwen/qwen3.8-27b-free
    discover_models: true
```

Changed model section to:

```yaml
model:
  default: qwen/qwen3.8-27b-free
  provider: orcarouter
```

This made orcarouter appear in the `/model` picker with 191 discovered models.

## Verification (confirmed working)

```bash
# 1. Confirm picker inventory shows the provider with models
cd ~/.hermes/hermes-agent && python3 -c "
from hermes_cli.inventory import load_picker_context, build_models_payload
ctx = load_picker_context()
payload = build_models_payload(ctx, probe_custom_providers=True, for_picker=True)
for p in payload['providers']:
    if 'orcarouter' in str(p.get('slug', '')):
        print(f\"{p['slug']}: {p.get('name')} — {len(p.get('models', []))} models\")
        for m in (p.get('models') or [])[:5]:
            print(f'  - {m}')
"
# Output: orcarouter: orcarouter — 191 models
#   - orcarouter/free
#   - orcarouter/fusion
#   ...

# 2. Probe the endpoint directly
curl -s https://api.orcarouter.ai/v1/models | python3 -c "
import json, sys
data = json.load(sys.stdin)
if isinstance(data, list):
    print(f'Total models: {len(data)}')
    for m in data[:10]:
        print(f'  - {m.get(\"id\", m.get(\"name\", str(m)))}')
"
# Output: Total models: 191
```

## Key Finding: `providers:` dict vs `custom_providers:` list

The `custom_providers:` **list** form did NOT give picker visibility in this session. Only the `providers:` **dict** form worked. When creating a new custom provider, always use:

```yaml
providers:
  my-endpoint:
    api: https://example.com/v1
    api_key_env: MY_KEY
```

NOT:

```yaml
custom_providers:
  - name: my-endpoint
    base_url: https://example.com/v1
    api_key: "..."
```

## Available Models

Orcarouter serves 191 models including:

- `orcarouter/free`, `orcarouter/fusion`, `orcarouter/fusion-flash`, `orcarouter/fusion-mini`
- Anthropic Claude family (haiku-4.5, sonnet-4.5/4.6, opus-4.5/4.6/4.7/4.8, opus-5)
- Qwen family (qwen3.8-27b-free, qwen3.6-27b, qwen3-32b, qwen3-coder, etc.)
- DeepSeek, Llama, GLM, MiniMax, Kimi, and more

## Code References

- `hermes_cli/inventory.py:load_picker_context()` — builds the ConfigContext from disk config; bare `model.provider` with no matching `providers:` entry does NOT create a user provider
- `hermes_cli/inventory.py:build_models_payload()` — calls `list_authenticated_providers()` which only emits rows for providers in `providers:` dict or `custom_providers:` list
- `hermes_cli/runtime_provider.py:_get_named_custom_provider()` — scans `providers:` dict first, then `custom_providers:` list; does NOT fall back to bare custom when provider name is non-empty but unmatched
- `hermes_cli/runtime_provider.py` lines 2126-2149 — credential resolution checks both `key_env` and `api_key_env` field names
- `agent/auxiliary_client.py` line 6487 — also checks both `key_env` and `api_key_env` for custom entries
