# Nous Platform Free Models — Discovery and Switching

Specifics for discovering and switching Hermes profiles to free models on the Nous Research inference platform.

## The Nous free model landscape

Free models on the Nous platform are not Nous-owned models — they are models from other providers (Tencent, StepFun, Upstage, Poolside) that Nous hosts and offers at $0 pricing. They are identified by:

- `pricing.prompt == "0"` AND `pricing.completion == "0"`, OR
- `"synthesizedFreeVariant": true` in the model object

## Fetching the model list

The Nous inference API (`https://inference-api.nousresearch.com/v1/models`) is behind Cloudflare. Two access patterns exist:

### Unauthenticated (works in most cases)
```bash
curl -s "https://inference-api.nousresearch.com/v1/models" | python3 -c "
import sys, json
for m in json.load(sys.stdin).get('data', []):
    p = m.get('pricing', {})
    if p.get('prompt') == '0' and p.get('completion') == '0':
        mid = m.get('id','')
        name = m.get('name','')
        ctx = m.get('context_length', 0)
        print(f'{mid}  |  {name}  |  ctx={ctx:,}')
"
```

### With auth header (may be blocked by Cloudflare)
```bash
curl -s "https://inference-api.nousresearch.com/v1/models" \
  -H "Authorization: Bearer $TOKEN" | ...
```
If this returns `403 Error 1010: Access denied / browser_signature_banned`, fall back to the unauthenticated approach above.

## Known free models (as of 2026-08)

| Model ID | Name | Context | Modalities | Benchmark highlights |
|----------|------|---------|------------|---------------------|
| `tencent/hy3:free` | Tencent: Hy3 | 262K | text→text | 295B MoE, 21B active, Elo 1228, ranked #39 overall |
| `stepfun/step-3.7-flash:free` | StepFun: Step 3.7 Flash | 262K | text+image+video→text | 196B MoE, ~11B active, multimodal, Elo 1175 |
| `upstage/solar-pro4:free` | Upstage: Solar Pro 4 | 524K | text→text | Elo 41.6 intel, 52.7 coding, 33.6 agentic, 524K context |
| `poolside/laguna-s-2.1:free` | Poolside: Laguna S 2.1 | varies | varies | Smaller model, less-proven |
| `poolside/laguna-xs-2.1:free` | Poolside: Laguna XS 2.1 | varies | varies | Smallest free option |

### Choosing a free model

- **Best all-rounder:** `tencent/hy3:free` — highest Elo, strong across all categories
- **Best context window:** `upstage/solar-pro4:free` — 524K tokens, familiar if already using Solar
- **Multimodal needed:** `stepfun/step-3.7-flash:free` — handles text, image, and video input

## Applying to profiles

```bash
# Main profile
hermes config set model.default tencent/hy3:free
hermes config set model.provider nous
hermes config set model.auxiliary ""

# All sub-profiles
for p in $(ls ~/.hermes/profiles/ | grep -v '^\.'); do
  hermes config set model.default tencent/hy3:free --profile $p
  hermes config set model.provider nous --profile $p
  hermes config set model.auxiliary "" --profile $p
done
```

## Nous OAuth token management

- Token file: `~/.hermes/shared/nous_auth.json`
- Re-import when exhausted: `hermes auth add nous --type oauth --no-browser --label "nous-free"`
- Token expiry: tokens have a lifetime; check `expires_at` in the JSON. When `hermes auth list nous` shows `device_code exhausted`, re-import.
- If re-import doesn't fix it, a browser-based OAuth flow is needed: `hermes auth add nous --type oauth` (without `--no-browser`) in an interactive session.

## Verification

```bash
hermes status   # main profile
for p in $(ls ~/.hermes/profiles/ | grep -v '^\.'); do
  echo "=== $p ===" && hermes -p $p status 2>&1 | grep -E "Model:|Provider:"
done
```

All profiles should show the chosen model ID and `Provider: Nous`.
