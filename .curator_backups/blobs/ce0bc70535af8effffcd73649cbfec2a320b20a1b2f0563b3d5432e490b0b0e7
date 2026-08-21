---
name: hermes-profile-model-config
description: Switch all Hermes profiles to a new model/provider in bulk.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, profiles, model, provider, config, nous, openai, deepseek]
---

# Hermes Profile Model Configuration

Use this when the user wants to change the model or provider for one or more Hermes profiles — especially bulk-switching all profiles to the same model/provider, or discovering what models are available from a given provider.

## When to Use

- User wants to switch all (or several) Hermes profiles to a new model or provider
- User asks to discover what models are available from a specific provider (Nous, OpenAI, DeepSeek, etc.)
- User wants to find free models on a platform and apply them to profiles
- User reports that a profile is using the wrong model or provider
- User wants to bulk-clear auxiliary models across profiles

Do NOT use for: single-profile one-off model changes that don't need discovery (just use `hermes config set` directly), or for gateway/platform setup (use `hermes-telegram-multi-profile`).

## What this covers

- Setting `model.default`, `model.provider`, `model.auxiliary`, and related fields in `config.yaml` per profile
- Discovering available models from any provider (Nous, OpenAI, DeepSeek, OpenRouter, etc.)
- Bulk-applying the same model to all profiles with a loop
- Verifying the change took effect across all profiles
- Provider-specific quirks: auth state, API access patterns, interactive vs. scriptable flows

## Quick reference: config keys

All model config lives under `model:` in `config.yaml`:

| Key | Purpose |
|-----|---------|
| `model.default` | Model ID string (e.g. `gpt-5.6-luna`, `tencent/hy3:free`) |
| `model.provider` | Provider name (e.g. `openai-codex`, `nous`, `deepseek`, `opencode-go`) |
| `model.auxiliary` | Secondary model for specific tasks (optional) |
| `model.base_url` | Custom API endpoint (for custom providers) |
| `model.api_key` | API key (usually in `.env` instead) |
| `model.max_output_tokens` | Max tokens per response |
| `model.parameters.reasoning_effort` | Reasoning effort level |

Set via `hermes config set model.<key> <value>` or edit `config.yaml` directly.

## Discovering available models

### Interactive (requires TTY)
```
hermes model
```
This opens an interactive picker. **Cannot be scripted** — it requires a PTY. Do not pipe input into it.

### Programmatic (no TTY needed)

For most providers, hit the provider's `/v1/models` endpoint directly:

```bash
# OpenAI-format providers (most use this)
curl -s "https://<provider-api>/v1/models" \
  -H "Authorization: Bearer <token>" | python3 -c "
import sys, json
for m in json.load(sys.stdin).get('data', []):
    print(m['id'], m.get('name',''))
"
```

**Provider endpoints:**
- **Nous:** `https://inference-api.nousresearch.com/v1/models` — may be Cloudflare-protected with auth headers; unauthenticated calls often work
- **OpenRouter:** `https://openrouter.ai/api/v1/models`
- **OpenCode Go:** via `hermes model --refresh` (interactive)

### Filtering for free models

Free models have `pricing.prompt == 0` AND `pricing.completion == 0` (as strings `"0"`), or `"synthesizedFreeVariant": true`:

```bash
curl -s "https://<provider>/v1/models" | python3 -c "
import sys, json
for m in json.load(sys.stdin).get('data', []):
    p = m.get('pricing', {})
    if p.get('prompt') == '0' and p.get('completion') == '0':
        print(m['id'], m.get('name',''), f\"ctx={m.get('context_length',0):,}\")
"
```

## Bulk-switching all profiles to a new model/provider

### Pattern

```bash
# 1. Set on main profile
hermes config set model.default <model-id>
hermes config set model.provider <provider>
hermes config set model.auxiliary ""   # clear if not wanted

# 2. Set on all sub-profiles
for p in $(ls ~/.hermes/profiles/ | grep -v '^\.'); do
  hermes config set model.default <model-id> --profile $p
  hermes config set model.provider <provider> --profile $p
  hermes config set model.auxiliary "" --profile $p
done

# 3. Verify
for p in $(ls ~/.hermes/profiles/ | grep -v '^\.'); do
  echo "=== $p ==="
  hermes -p $p status 2>&1 | grep -E "Model:|Provider:"
done
```

### Important notes

- **Discover profiles dynamically** — don't hardcode the list. Profiles can be added over time.
- **`hermes model` cannot be scripted** — use `hermes config set` instead.
- **Gateway profiles need a restart** after config changes for bots to pick up the new model:
  ```
  hermes -p <profile> gateway restart
  ```
- **Clear auxiliary models** if the new provider doesn't support them, or if you want a clean single-model setup.
- **Auth state matters** — the target provider must have valid credentials. Check with `hermes auth list <provider>`.

### Nous Research

- Auth: OAuth via `hermes auth add nous --type oauth`
- Token storage: `~/.hermes/shared/nous_auth.json`
- Inference endpoint: `https://inference-api.nousresearch.com/v1`
- **Cloudflare protection:** Auth'd API calls may return `403 Error 1010: browser_signature_banned`. Unauthenticated calls to `/v1/models` often succeed.
- Token expiry: Tokens have a limited lifetime. When `hermes auth list nous` shows `device_code exhausted`, re-import with `hermes auth add nous --type oauth --no-browser`.
- Free models available: `tencent/hy3:free`, `stepfun/step-3.7-flash:free`, `upstage/solar-pro4:free`, `poolside/laguna-s-2.1:free`, `poolside/laguna-xs-2.1:free`
- **Full discovery and switching guide:** See `references/nous-free-models.md` for the complete free-model landscape, model comparison table, auth troubleshooting, and verified curl-based discovery commands.

### OpenAI Codex

- Auth: OAuth via `hermes auth add openai-codex`
- Models: `gpt-5.6-luna`, `gpt-5.5`, etc.
- Rate limits apply per account

### DeepSeek

- API key in env: `DEEPSEEK_API_KEY`
- Models: `deepseek-v4-flash`, `deepseek-v4-pro`, etc.

### OpenCode Go

- API key in env
- Endpoint configurable via `model.base_url`

## Verification standard

Before declaring success:
1. Confirm the main profile shows the correct model and provider: `hermes status`
2. Confirm each sub-profile: `hermes -p <name> status`
3. For gateway profiles (Telegram/Discord bots), restart the gateway and check logs
4. Run a smoke test if needed: `hermes -p <profile> chat -Q -q "Reply exactly: OK-<profile>"`

## Pitfalls

1. **`hermes model` is interactive-only.** Do not attempt to script it with pipes, redirects, or background execution. Use `hermes config set` for programmatic changes.

2. **Cloudflare blocks auth'd Nous API calls.** If you get `403 Error 1010`, drop the auth header and try unauthenticated. The models endpoint is publicly reachable in many setups.

3. **Stale Nous OAuth tokens.** Tokens expire and enter an exhausted state. Re-import with `hermes auth add nous --type oauth --no-browser`. If still stale, a browser OAuth flow is needed.

4. **Auxiliary model mismatch.** Profiles with an `auxiliary` set may still route certain tasks to it. Clear it unless intentionally keeping a secondary model.

5. **Hardcoded profile lists.** Always discover profiles dynamically with `ls ~/.hermes/profiles/` — new profiles won't be in a hardcoded loop.

6. **Config changes need session restart.** Changes to `config.yaml` take effect on next session start. Gateway profiles need an explicit `gateway restart`.

7. **Profile with .env but no config.yaml falls back to main token.** This is a silent failure mode — every profile should have its own `config.yaml`.

## Related skills

- `hermes-telegram-multi-profile` — multi-profile setup, gateway management, token per profile
- `hermes-agent` — general Hermes CLI and configuration reference
