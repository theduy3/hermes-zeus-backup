---
name: hermes-custom-endpoint
description: Use when adding a custom provider to Hermes Agent.
tags: [hermes, configuration, custom-provider, model-picker, troubleshooting]
---

# Hermes Custom Endpoint Setup

Guide for configuring custom OpenAI-compatible endpoints in Hermes Agent so they work correctly with the `/model` picker, credential resolution, and runtime provider selection.

## The Bare-Custom Trap

When you configure a custom endpoint only via inline `model` fields:

```yaml
model:
  default: orcarouter/auto
  provider: custom
  base_url: https://api.orcarouter.ai/v1
```

The `/model` picker will **not** show this provider or its models. The picker only enumerates providers declared in `providers:` (new-style dict) or `custom_providers:` (legacy list). A bare `provider: custom` with inline `base_url` is invisible to the picker UI.

**Symptoms:**
- `/model` (no args) opens the picker but the custom endpoint is absent
- `/model <name>` may still work (the runtime uses the inline base_url), but you can't browse available models
- `hermes model` CLI picker also won't list it

**Fix — declare as a named provider:**

```yaml
providers:
  orcarouter:
    api: https://api.orcarouter.ai/v1
    # api_key / key_env if required; omit for keyless endpoints

model:
  default: orcarouter/auto
  provider: orcarouter
```

After this, the `/model` picker shows the provider with its discovered models.

## Provider Declaration Forms

### New-style (`providers:` dict)

```yaml
providers:
  my-proxy:
    api: https://proxy.example.com/v1
    api_key: "..."        # or use key_env
    default_model: qwen3.8-27b-free
    # transport: openai_chat   # optional, defaults to openai_chat
    # api_mode: chat_completions  # optional
    # extra_body: {...}         # optional
    # extra_headers: {...}      # optional
    # discover_models: true     # default; set false to pin a model list
    # models:                   # explicit model list (allows per-model metadata)
    #   qwen3.8-27b-free:
    #     context_length: 16384
```

The provider key (`my-proxy`) becomes the provider slug. The picker shows it as `custom:my-proxy`.

### Legacy (`custom_providers:` list)

```yaml
custom_providers:
  - name: my-proxy
    base_url: https://proxy.example.com/v1
    api_key: "..."
    model: qwen3.8-27b-free
    provider_key: custom:my-proxy   # optional, for alias resolution
```

### Bare custom (inline, NOT recommended for picker visibility)

```yaml
model:
  provider: custom
  base_url: https://api.example.com/v1
  default: some-model
```

Works at runtime but invisible to `/model` picker. Use only for quick experiments.

## Model Picker Integration

- The picker calls `/v1/models` on custom endpoints to discover available models (when `discover_models: true` or no explicit `models:` list)
- Discovered models are cached to `custom_providers[]` in config.yaml after a successful probe (see `_save_discovered_models_to_config` in `hermes_cli/model_switch.py`)
- Set `discover_models: false` and declare `models:` explicitly to pin a known list and avoid probe failures on unreliable endpoints
- The picker deduplicates models that appear in both a custom endpoint and an aggregator (OpenRouter, etc.) — the custom endpoint's models win

## Credential Resolution Order

For a named custom provider, Hermes resolves credentials in this order:

1. `api_key` field in the provider entry
2. `key_env` or `api_key_env` field → environment variable (both field names are accepted; `api_key_env` is the one used by `runtime_provider.py`)
3. `key_cmd` field → shell command that outputs a token (for short-lived bearers)

The API key is never persisted in session state — only the provider slug and base_url survive across restarts.

## Runtime Resolution Path

When the agent makes a call with `provider: custom` or a named custom provider:

1. `runtime_provider.py:_get_named_custom_provider()` scans `providers:` dict first, then `custom_providers:` list
2. Matches by provider key/name/alias
3. Returns base_url, api_key, model, api_mode, extra_body, extra_headers
4. Falls back to bare custom trust path (inline `model.base_url`) only when no named entry matches

## Pitfalls

### Bare custom invisible to picker (most common)

When you configure a custom endpoint only via inline `model` fields:

```yaml
model:
  default: orcarouter/auto
  provider: custom
  base_url: https://api.orcarouter.ai/v1
```

The `/model` picker will **not** show this provider or its models. The picker only enumerates providers declared in `providers:` (new-style dict) or `custom_providers:` (legacy list). A bare `provider: custom` with inline `base_url` is invisible to the picker UI.

**Symptoms:**
- `/model` (no args) opens the picker but the custom endpoint is absent
- `/model <name>` may still work (the runtime uses the inline base_url), but you can't browse available models
- `hermes model` CLI picker also won't list it

**Fix — declare as a named provider in `providers:` dict (NOT `custom_providers:`):**

```yaml
providers:
  orcarouter:
    api: https://api.orcarouter.ai/v1
    api_key_env: ORCAROUTER_API_KEY

model:
  default: qwen/qwen3.8-27b-free
  provider: orcarouter
```

Note: the legacy `custom_providers:` list form does NOT reliably give picker visibility — always use the `providers:` dict for new setups.

After this, the `/model` picker shows the provider with its discovered models.

### Wrong credential field name

Using `api_key: ${ORCAROUTER_API_KEY}` or similar variable expansion does not work — Hermes does not expand env vars in YAML values. Use `api_key_env: ORCAROUTER_API_KEY` (or `key_env`) to point at the environment variable by name.
