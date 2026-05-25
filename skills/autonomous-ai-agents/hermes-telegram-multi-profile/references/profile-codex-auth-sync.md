# Profile Codex credential sync

Use this when multiple Hermes profiles are running, gateways are connected, but `hermes -p <profile> chat -q ...` fails with Codex credential/rate-limit errors while another profile works.

## Symptom

`hermes auth list openai-codex` may show different credentials per profile, for example:

- default: healthy `duynt1989@gmail.com`
- affected profiles: stale/rate-limited `kitty ... usage_limit_reached (429)`

Gateway status can still look healthy because platform connectivity is separate from model-provider auth.

## Fix pattern

1. Pick a known-good profile auth store, usually default:

```bash
DEFAULT_AUTH="$HOME/.hermes/auth.json"
```

2. Back up and copy it into every profile:

```bash
TS=$(date +%Y%m%d_%H%M%S)
DEFAULT_AUTH="$HOME/.hermes/auth.json"
for d in "$HOME/.hermes/profiles"/*; do
  [ -d "$d" ] || continue
  [ -f "$d/auth.json" ] && cp "$d/auth.json" "$d/auth.json.bak.$TS"
  cp "$DEFAULT_AUTH" "$d/auth.json"
  chmod 600 "$d/auth.json"
done
```

3. Verify auth state:

```bash
for p in default 3r alan butter catthew charles charlesbourg finance maily mira ss thor turing zeus; do
  arg=""; [ "$p" = default ] || arg="-p $p"
  echo "--- $p ---"
  hermes $arg auth list openai-codex | head -10
done
```

4. Run an actual model smoke test, not just gateway status:

```bash
for p in default 3r alan butter catthew charles charlesbourg finance maily mira ss thor turing zeus; do
  arg=""; [ "$p" = default ] || arg="-p $p"
  timeout 60s hermes $arg chat -Q -q "Reply exactly: OK-$p" 2>&1 | tail -8
 done
```

## Notes

- `hermes profile list` and `hermes gateway status` prove processes/platforms are up; they do not prove the model provider credential works.
- `auth.json` is profile-scoped. Removing a bad credential from one profile does not automatically update the others.
- Always create timestamped backups before overwriting profile auth stores.
