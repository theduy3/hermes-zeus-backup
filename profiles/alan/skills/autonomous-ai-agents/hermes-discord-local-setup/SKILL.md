---
name: hermes-discord-local-setup
description: Set up Hermes Agent as a local Discord bot on macOS, including credential wiring, launchd service install, and the common privileged-intents failure mode.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, discord, gateway, macos, launchd]
---

# Hermes Discord local setup

Use this when a user wants Hermes to run as a Discord bot on their local Mac.

## What this solves

- Configure Hermes with a Discord bot token and allowlist
- Install and run the Hermes gateway as a macOS launchd service
- Verify the bot is actually connected
- Diagnose the common Discord privileged-intents failure

## Required values

- `DISCORD_BOT_TOKEN`
- `DISCORD_ALLOWED_USERS` (the user's Discord user ID)
- Optional: `DISCORD_HOME_CHANNEL`
- Optional but usually required in practice: a Discord server to invite the bot into

## Preflight checks

Run:

```bash
hermes status --all
hermes doctor
```

Confirm:
- `discord.py` is installed
- Hermes reports Discord as not configured or configured
- Gateway manager on macOS is `launchd`

Useful repo docs:
- `website/docs/user-guide/messaging/discord.md`
- `website/docs/reference/environment-variables.md`

## Minimal local configuration

Write these into `~/.hermes/.env`:

```env
DISCORD_BOT_TOKEN=...
DISCORD_ALLOWED_USERS=123456789012345678
# Optional
# DISCORD_HOME_CHANNEL=123456789012345678
```

If editing programmatically, preserve the rest of `.env` and replace existing keys in place rather than rewriting the whole file from partial/redacted output.

## Start the gateway on macOS

```bash
hermes gateway install --force
hermes gateway start
hermes gateway status
```

## Verification standard

Check all of these, not just one:

```bash
hermes status --all
hermes gateway status
```

And inspect live state:

```bash
python3 - <<'PY'
from pathlib import Path
p=Path.home()/'.hermes'/'gateway_state.json'
print(p.read_text(errors='ignore') if p.exists() else 'missing')
PY
```

Success looks like:
- `hermes status --all` shows `Discord       ✓ configured`
- gateway service shows running under launchd
- `gateway_state.json` contains something like:
  - `gateway_state: running`
  - `platforms.discord.state: connected`

Also verify credentials are present without printing secrets:

```bash
python3 - <<'PY'
from pathlib import Path
p=Path.home()/'.hermes'/'.env'
vals={}
for line in p.read_text(errors='ignore').splitlines():
    if '=' in line and not line.lstrip().startswith('#'):
        k,v=line.split('=',1); vals[k]=v
print('DISCORD_BOT_TOKEN present', bool(vals.get('DISCORD_BOT_TOKEN')))
print('DISCORD_ALLOWED_USERS', vals.get('DISCORD_ALLOWED_USERS'))
print('DISCORD_HOME_CHANNEL', vals.get('DISCORD_HOME_CHANNEL','MISSING'))
PY
```

## Common failure mode: PrivilegedIntentsRequired

A very common Discord failure is:
- gateway starts
- token is present
- but logs show `PrivilegedIntentsRequired`
- Hermes reports `discord failed to connect`

Typical error evidence in `~/.hermes/logs/gateway.error.log`:
- `discord.errors.PrivilegedIntentsRequired`
- `Timeout waiting for connection to Discord`
- `Gateway failed to connect any configured messaging platform: discord: failed to connect`

Fix in Discord Developer Portal:
1. Open the app's **Bot** page
2. Under **Privileged Gateway Intents**, enable:
   - `Message Content Intent`
   - `Server Members Intent`
3. Save changes
4. Restart Hermes gateway:

```bash
hermes gateway restart
hermes gateway status
```

Then re-check `gateway_state.json` until Discord shows connected.

## If the user has no Discord server yet

They can still finish setup by:
1. Creating a new Discord server
2. Inviting the bot with scopes `bot` and `applications.commands`
3. Using a permission integer such as `274878286912`
4. Testing by mentioning the bot in a server channel or DMing it

Invite URL format:

```text
https://discord.com/oauth2/authorize?client_id=APP_ID&scope=bot+applications.commands&permissions=274878286912
```

## Behavioral notes

- In server channels, Hermes responds when mentioned by default
- DMs do not require mention
- If `DISCORD_HOME_CHANNEL` is unset, proactive messages are not configured

## Reporting template

When done, report:
- whether Discord is configured
- whether gateway service is running
- PID if available
- whether `gateway_state.json` shows Discord connected
- whether `DISCORD_HOME_CHANNEL` is set or missing
