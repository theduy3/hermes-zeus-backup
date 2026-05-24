---
name: hermes-telegram-multi-profile
description: Set up multiple Hermes profiles, each with its own Telegram bot and macOS launchd gateway service, including the common authorization pitfall. Also covers mixed-platform setups (Telegram + Discord across profiles) and the --clone env seeding pattern.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, telegram, profiles, gateway, launchd, macos]
---

# Hermes Telegram multi-profile setup

Use this when a user wants separate Hermes Telegram bots for different companies, teams, or contexts on the same machine.

## What this solves

- One Hermes profile per company or specialist role
- One Telegram bot token per profile (or Discord, or both — see mixed-platform reference)
- One macOS launchd gateway service per profile
- Separate config, memory, sessions, and SOUL instructions per profile

> **Mixed-platform setup (Telegram + Discord in one session):** See `references/mixed-platform-setup.md` for the full phase-by-phase template.

## Important findings

1. `hermes profile create <name>` requires lowercase profile names matching `[a-z0-9][a-z0-9_-]{0,63}`.
2. Freshly created profiles may not have `config.yaml` or `.env` yet, even though `config path` and `config env-path` resolve to profile-specific locations.
3. If you want a new profile to inherit the current setup, copy the default `~/.hermes/config.yaml` and `~/.hermes/.env` into the profile directory, or create the profile with `--clone`/`--clone-from`.
4. Telegram gateways can appear connected but still never respond if no allowlist is configured.
5. The key log message for that failure mode is:
   - `No user allowlists configured. All unauthorized users will be denied.`
   - `Unauthorized user: <telegram_user_id>`
6. Fix that by setting either:
   - `TELEGRAM_ALLOWED_USERS=<your_telegram_user_id>` for restricted access, or
   - `GATEWAY_ALLOW_ALL_USERS=true` for open access.
7. Be extremely careful when inspecting or rewriting profile `.env` files that contain bot tokens. Do not round-trip `.env` content through tools that add display prefixes or redacted placeholders to output. In particular:
   - avoid copying `read_file` output back into `.env` files, because numbered prefixes like `123|...` can be written into the file and corrupt it
   - avoid relying on redacted search output to reconstruct `TELEGRAM_BOT_TOKEN` values
   - prefer direct shell/Python reads of the actual file contents when validating token presence or length
8. If a token value has been replaced by a redacted placeholder in the file or in captured output, it is not recoverable from that output; ask the user to provide the real token again.
9. On flaky Telegram networks, increasing Hermes Telegram HTTP timeouts can improve gateway stability. Useful env overrides:
   - `HERMES_TELEGRAM_HTTP_CONNECT_TIMEOUT=20`
   - `HERMES_TELEGRAM_HTTP_READ_TIMEOUT=60`
   - `HERMES_TELEGRAM_HTTP_WRITE_TIMEOUT=60`
   - `HERMES_TELEGRAM_HTTP_POOL_TIMEOUT=20`
10. After restarting a profile gateway, `gateway status` can briefly show a stale `LastExitStatus` even while the new process is still starting. Verify success from the profile log, not launchd status alone. The decisive success lines are:
   - `Application started`
   - `Connected to Telegram (polling mode)`
   - `✓ telegram connected`
11. When testing whether a restored bot token is valid, do not trust only a previous `InvalidToken` line in the log tail. Always check the newest log lines after the restart; an older failure can still be visible above a later successful connection.
12. **API key requirement**: Gateway profiles need the model provider's API key in their `.env`. If using `deepseek-v4-pro` via OpenRouter, set `OPENROUTER_API_KEY=...` in each profile's `.env`. If using DeepSeek directly, set `DEEPSEEK_API_KEY=...`. Without the key, gateways will respond with "No LLM provider configured" errors even though the profile's config.yaml has the correct model/provider.
13. **Cross-platform profiles**: Profiles can mix Telegram and Discord on the same machine. Each profile's `.env` determines which platforms it connects to — set `TELEGRAM_BOT_TOKEN` for Telegram, `DISCORD_BOT_TOKEN` for Discord, or both for a profile on both platforms. Gateway services are per-profile and per-platform-agnostic.

## Recommended macOS workflow

### 1. Create profiles

```bash
hermes profile create maily
hermes profile create charlesbourg
hermes profile create 3r
hermes profile create ss
```

If the requested names contain capitals, normalize to lowercase first.

**Pitfall: `--clone` copies .env with placeholder values.** The cloned `.env` from `--clone` inherits the parent's config but may have commented-out or redacted tokens (`TELEGRAM_BOT_TOKEN=***`). You MUST explicitly set the real token after cloning — do not assume the clone brought a working token. Use a script to safely patch tokens:

```bash
python3 - <<'PY'
from pathlib import Path
profiles = {"alan": "TOKEN_HERE", "mira": "TOKEN_HERE"}
base = Path.home() / ".hermes" / "profiles"
TELEGRAM_USER_ID = "8446251233"
for name, token in profiles.items():
    env = base / name / ".env"
    lines = env.read_text().splitlines()
    new = []
    saw_tok = saw_auth = False
    for line in lines:
        if line.startswith("TELEGRAM_BOT_TOKEN="):
            new.append(f"TELEGRAM_BOT_TOKEN={token}"); saw_tok = True
        elif line.startswith("TELEGRAM_ALLOWED_USERS="):
            new.append(f"TELEGRAM_ALLOWED_USERS={TELEGRAM_USER_ID}"); saw_auth = True
        elif line.startswith("DISCORD_BOT_TOKEN=") or line.startswith("DISCORD_ALLOWED_USERS="):
            new.append(f"# {line}")  # comment out cross-platform tokens
        else:
            new.append(line)
    if not saw_tok: new.append(f"TELEGRAM_BOT_TOKEN={token}")
    if not saw_auth: new.append(f"TELEGRAM_ALLOWED_USERS={TELEGRAM_USER_ID}")
    env.write_text("\n".join(new) + "\n")
PY
```

### 2. Seed each profile with config and env

```bash
for p in maily charlesbourg 3r ss; do
  cp ~/.hermes/config.yaml ~/.hermes/profiles/$p/config.yaml
  cp ~/.hermes/.env ~/.hermes/profiles/$p/.env
done
```

If you do not want to copy the active profile manually, prefer:

```bash
hermes profile create <name> --clone
```

### 3. Set a unique Telegram bot token per profile

Edit each profile env file:

- `~/.hermes/profiles/maily/.env`
- `~/.hermes/profiles/charlesbourg/.env`
- `~/.hermes/profiles/3r/.env`
- `~/.hermes/profiles/ss/.env`

Set:

```env
TELEGRAM_BOT_TOKEN=<bot_token>
```

Do not leave all profiles sharing the same inherited token.

### 4. Authorize the intended Telegram user(s)

Restricted mode:

```env
TELEGRAM_ALLOWED_USERS=123456789
```

Multiple IDs can be added per Hermes conventions if needed; verify formatting in the current version.

Open mode instead:

```env
GATEWAY_ALLOW_ALL_USERS=true
```

### 5. Customize the profile persona/instructions

Edit each profile's `SOUL.md`:

- `~/.hermes/profiles/<profile>/SOUL.md`

Recommended template:
- professional
- concise
- scoped only to that company
- avoids mixing context from other profiles
- asks clarifying questions only when needed
- gives result-first responses for operational work

Better approach when the profile is for a real business:
- research the company's public website first
- add grounded business context to `SOUL.md` such as:
  - brand name
  - location
  - phone/email guidance
  - main service categories
  - tone/positioning
  - language preference (for example French-first with English fallback)
  - booking/policy priorities
- if the website contains inconsistent public information, encode that caution into the profile instructions so the bot does not confidently repeat contradictory details
  - examples: conflicting hours, conflicting deposit rules, inconsistent phone/email display

This makes the Telegram bot act like a company-specific front-desk assistant instead of a generic Hermes profile.

### 6. Install profile-scoped gateway services on macOS

```bash
maily gateway install --force
charlesbourg gateway install --force
3r gateway install --force
ss gateway install --force
```

Hermes creates profile-specific launchd plists like:
- `~/Library/LaunchAgents/ai.hermes.gateway-maily.plist`
- `~/Library/LaunchAgents/ai.hermes.gateway-charlesbourg.plist`

### 7. Restart after config or SOUL changes

```bash
maily gateway restart
charlesbourg gateway restart
3r gateway restart
ss gateway restart
```

### 8. Verify status

```bash
hermes profile list
maily gateway status
charlesbourg gateway status
3r gateway status
ss gateway status
```

## Log locations

Per-profile logs live under:

- `~/.hermes/profiles/<profile>/logs/gateway.log`
- `~/.hermes/profiles/<profile>/logs/gateway.error.log`

Useful checks:

```bash
tail -n 80 ~/.hermes/profiles/maily/logs/gateway.log
tail -n 80 ~/.hermes/profiles/maily/logs/gateway.error.log
```

## Troubleshooting checklist

### Bot reads messages but does not reply

Check logs first. If you see unauthorized-user warnings, the fix is allowlisting, not reinstalling the gateway.

### `config.yaml` or `.env` missing in a new profile

Seed them from the default profile or recreate the profile with `--clone`.

On a VPS/container, this can happen even when `hermes profile list` shows the profile exists. A practical repair is:

```bash
for p in maily charlesbourg 3r ss; do
  mkdir -p ~/.hermes/profiles/$p
  cp ~/.hermes/config.yaml ~/.hermes/profiles/$p/config.yaml
  cp ~/.hermes/.env ~/.hermes/profiles/$p/.env
  # Then edit ~/.hermes/profiles/$p/.env and set that profile's own TELEGRAM_BOT_TOKEN.
done
```

If copying from the default profile, clear or replace the inherited `TELEGRAM_BOT_TOKEN` immediately so all bots do not share the same token.

### Running profile bots on a VPS/container instead of macOS

When the user wants the profile Telegram bots to respond from the VPS, inspect the live environment first:

```bash
hostname
command -v hermes
hermes --version
hermes profile list
ps -ef | grep -E 'hermes.*gateway|gateway.*hermes' | grep -v grep || true
systemctl --user list-units --type=service --all 2>/dev/null | grep -i hermes || true
```

Verify the import/API mismatch before changing code:

```bash
cd ~/.hermes/hermes-agent
source venv/bin/activate
python - <<'PY'
from tools.registry import discover_builtin_tools, registry
import model_tools
print('OK import')
PY
```

If profiles exist but show `missing config, no .env`, seed config/env as above, then set the per-profile Telegram tokens. Validate each token without exposing it:

```bash
python3 - <<'PY'
import json, urllib.request
from pathlib import Path
for p in ['maily','charlesbourg','3r','ss']:
    tok = ''
    for line in (Path.home()/'.hermes/profiles'/p/'.env').read_text(errors='ignore').splitlines():
        if line.startswith('TELEGRAM_BOT_TOKEN='):
            tok = line.split('=', 1)[1]
    with urllib.request.urlopen(f'https://api.telegram.org/bot{tok}/getMe', timeout=15) as r:
        data = json.load(r)
    res = data.get('result') or {}
    print(p, data.get('ok'), res.get('username'), res.get('id'))
PY
```

If the VPS/container has no usable `systemctl` (for example PID 1 is `tini`), `hermes gateway install` may not be useful. Start profile gateways as tracked background processes instead:

```bash
hermes -p maily gateway run
hermes -p charlesbourg gateway run
hermes -p 3r gateway run
hermes -p ss gateway run
```

Then verify:

```bash
for p in maily charlesbourg 3r ss; do
  hermes -p "$p" gateway status
 done
ps -ef | grep -E 'hermes -p (maily|charlesbourg|3r|ss) gateway run' | grep -v grep || true
```

If `hermes gateway install` says service installation is not needed because the agent is running inside Docker/container mode, treat the container runtime as the real service manager. In locked-down containers you may also find:
- PID 1 is `tini` or another minimal init
- `systemctl` is unavailable or useless
- startup files like `/home/hermes/entrypoint.sh` are on a read-only filesystem

In that situation, if you cannot change the container's startup command or restart policy directly, create a local cron watchdog that periodically checks the profile gateways and restarts any missing ones. Example prompt for a local cron job:

- inspect `hermes -p <profile> gateway status` for `maily`, `charlesbourg`, `3r`, and `ss`
- if any profile is not running, start it with `hermes -p <profile> gateway run`
- verify status again and summarize which were restarted

This is a practical fallback for persistence when you cannot modify Docker Compose / `docker run --restart ...` / entrypoint wiring from inside the container.

Warn the user that manually started gateway processes may not survive VPS/container restart unless a process manager is added later.

Also warn that Telegram polling bots should not run from two machines with the same tokens at once. Stop the old Mac gateways before relying on the VPS bots. **Diagnostic signal:** persistent `polling conflict (1/3)` in the gateway log despite unique tokens and clean webhook state strongly suggests another machine is polling the same token. See `hermes-agent` skill → `references/gateway-troubleshooting.md` for the 7-step diagnostic workflow including external-process detection via direct Python getUpdates long-poll.

### All bots accidentally share one Telegram bot

Inspect each profile `.env` and ensure `TELEGRAM_BOT_TOKEN` differs per profile.

**Silent token sharing via missing config.yaml:** A profile with its own `.env` (unique token) but NO `config.yaml` will silently fall back to the main `~/.hermes/.env` token. All such profiles end up fighting over the same bot. The fix: every profile must have its own `config.yaml` — copy from default:
```bash
cp ~/.hermes/config.yaml ~/.hermes/profiles/<name>/config.yaml
```

**Silent token sharing via unset HERMES_HOME:** On Docker/VPS, the `entrypoint.sh` must set `HERMES_HOME` per profile before launching the gateway, or every profile gateway inherits the main `.env` token:
```bash
# Correct:
HERMES_HOME="$profile_dir" hermes -p "$name" gateway run >> "$log_dir/gateway.log" 2>&1 &

# Wrong (all profiles silently share the default token):
hermes -p "$name" gateway run >> "$log_dir/gateway.log" 2>&1 &
```

### Persona changes not reflected

Restart that profile's gateway after editing `SOUL.md`.

## Mixed-platform setups (Telegram + Discord)

Profiles can mix platforms — some on Telegram, some on Discord, some on both. The gateway handles this automatically based on which tokens are present in each profile's `.env`.

### Platform token rules

- `TELEGRAM_BOT_TOKEN` present → gateway connects to Telegram
- `DISCORD_BOT_TOKEN` present → gateway connects to Discord
- Both present → gateway connects to both platforms
- Neither present → gateway starts with cron only (no messaging)

### Migrating a profile from Telegram to Discord

1. Edit the profile `.env` — comment out `TELEGRAM_BOT_TOKEN` and `TELEGRAM_ALLOWED_USERS`
2. Set `DISCORD_BOT_TOKEN=<token>` and `DISCORD_ALLOWED_USERS=<user_id>`
3. Restart the gateway: `hermes -p <profile> gateway restart`

Do NOT leave stale `TELEGRAM_BOT_TOKEN` in the file when migrating — the gateway will try to connect to Telegram with an old/invalid token and log failures.

### Discord token validation

**Validate Discord tokens with `curl` before starting gateways — Python urllib returns false-negatives.**

```bash
for name in charlesbourg:TOKEN maily:TOKEN; do
  n="${name%%:*}"; t="${name#*:}"
  echo -n "$n: "
  curl -s -H "Authorization: Bot $t" "https://discord.com/api/v10/users/@me" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'✓ {d[\"username\"]}')"
done
```

- JSON with `username` + `bot: true` → valid
- `{"message": "401: Unauthorized"}` → bad token
- Python `urllib` returning HTTP 403/1010 on a valid token → false negative, switch to curl

Also ensure each Discord bot app has **Privileged Gateway Intents** enabled:
- Message Content Intent ✓
- Server Members Intent ✓

### Gateway log timestamp pitfall

When checking connectivity, always look at the **most recent** log entries. Old gateway logs (from days/weeks ago when the profile had different tokens) can mislead. Use timestamps:

```bash
# Only show today's entries
grep "$(date +%Y-%m-%d)" ~/.hermes/profiles/<name>/logs/gateway.log | grep -E "✓|✗|Connected|failed"
```

## Verification standard

Before declaring success:
1. Confirm each profile exists in `hermes profile list`.
2. Confirm each profile has its own platform token (Telegram or Discord, never shared).
3. Validate Discord tokens via the REST API before starting gateways (see reference above).
4. Confirm allowlist or open-access setting is present per profile.
5. Confirm each gateway service is loaded and profile-scoped.
6. Check ONLY today's log timestamps for connectivity — ignore old entries.
7. Ask the user to send a message to each bot to verify end-to-end.
