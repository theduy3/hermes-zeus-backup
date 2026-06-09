# Profile slash command cache refresh

Use this when a user-installed or user-invocable skill (for example `/last30days`) exists on disk in a profile but Telegram replies that the slash command is unknown.

## Durable lesson

Slash command availability is determined from each profile's skill library at gateway startup. Copying or installing a `user-invocable: true` skill into `~/.hermes/profiles/<profile>/skills/` is not enough if that profile gateway is already running; restart the profile gateway so it rescans commands.

Telegram's Bot API menu limit can also hide valid commands: logs may say `Telegram menu: 30 commands registered, N hidden`. Hidden commands can still work by typing them directly if the gateway has discovered them.

## Verification probe

Run this per profile before and after restart. It checks local command discovery without sending a Telegram message:

```bash
for p in default butter catthew charles finance thor zeus; do
  if [ "$p" = default ]; then H="$HOME/.hermes"; else H="$HOME/.hermes/profiles/$p"; fi
  printf '%s: ' "$p"
  HERMES_HOME="$H" ~/.hermes/hermes-agent/venv/bin/python3 - <<'PY'
from agent.skill_commands import scan_skill_commands, build_skill_invocation_message
cmds = scan_skill_commands()
msg = build_skill_invocation_message('/last30days', 'Rocket Labs') if '/last30days' in cmds else None
print('OK' if msg and 'Rocket Labs' in msg else 'MISSING')
PY
done
```

Expected output for a ready profile: `OK`.

## Log signals

Before refresh, profile logs may show:

```text
Unrecognized slash command /last30days from telegram — replying with unknown-command notice
```

After restart, look for current timestamped startup lines:

```text
Starting Hermes Gateway...
Active profile: <profile>
Telegram menu: 30 commands registered, N hidden (over 30 limit)
Connected to Telegram (polling mode)
✓ telegram connected
Gateway running with 1 platform(s)
```

## Restart pattern on VPS/container supervisor setups

If profile gateways are managed by a local supervisor script, kill only the profile gateway PIDs and let the supervisor restart them. Then verify with process list and the latest profile logs. Do not rely on stale log tails from before the restart.
