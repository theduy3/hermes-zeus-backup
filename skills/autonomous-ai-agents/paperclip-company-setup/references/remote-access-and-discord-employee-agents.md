# Remote Paperclip access + Discord employee agents

Use this when Paperclip is running inside a VPS/container and the user wants to access the UI from a local laptop or operate the company through Discord agents.

## Remote UI access pattern

If Paperclip is bound to `127.0.0.1:3100` on a VPS/container, `http://127.0.0.1:3100` on the user's laptop points to the laptop, not the VPS.

Preferred access path:

```bash
ssh -N \
  -i ~/.ssh/id_ed25519 \
  -o IdentitiesOnly=yes \
  -o ExitOnForwardFailure=yes \
  -L 3101:127.0.0.1:3100 \
  root@<vps-ip>
```

Then open locally:

```text
http://127.0.0.1:3101
```

Use a non-default local port like `3101` when `3100` is already bound locally.

Mac SSH shortcut:

```sshconfig
Host paperclip
  HostName <vps-ip>
  User root
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
  ExitOnForwardFailure yes
  LocalForward 3101 127.0.0.1:3100
```

Then:

```bash
ssh -N paperclip
```

Pitfall: do not include markdown fences/language labels like `sshconfig` in `~/.ssh/config`; OpenSSH treats them as invalid keywords.

## Host vs container SSH pitfall

A Hermes profile may run inside Docker while SSH to `<user>@<vps-ip>` lands on the VPS host. Adding a key to `/home/hermes/.ssh/authorized_keys` inside the container does not enable login to a host user unless that user also exists on the host.

If host user does not exist, either:

```bash
adduser hermes
mkdir -p /home/hermes/.ssh
printf '%s\n' '<public-key>' > /home/hermes/.ssh/authorized_keys
chown -R hermes:hermes /home/hermes/.ssh
chmod 700 /home/hermes/.ssh
chmod 600 /home/hermes/.ssh/authorized_keys
```

or use root SSH for the tunnel if root login/key auth is already available:

```bash
mkdir -p /root/.ssh
printf '%s\n' '<public-key>' >> /root/.ssh/authorized_keys
chmod 700 /root/.ssh
chmod 600 /root/.ssh/authorized_keys
```

## Discord employee-agent architecture

For a Paperclip company, start with one Discord bot/profile as a dispatcher/CEO before creating one bot per employee.

Phase 1:

```text
User in Discord → wylios-ceo Hermes Discord profile → Paperclip bridge script → Paperclip issues/agents
```

Phase 2, only after the CEO bot works:

```text
wylios-ceo
salonx-product
salonx-engineer
salonx-gtm
salonx-sales
salonx-research
```

Each employee bot needs its own Discord application/token and Hermes profile.

Recommended Discord env for multi-agent safety:

```env
DISCORD_BOT_TOKEN=<token>
DISCORD_ALLOWED_USERS=<owner_discord_user_id>
DISCORD_ALLOWED_CHANNELS=<comma_separated_channel_ids_optional>
DISCORD_IGNORE_NO_MENTION=true
DISCORD_ALLOW_BOTS=mentions
```

Important:
- `DISCORD_IGNORE_NO_MENTION=true` keeps bots from replying to every channel message.
- `DISCORD_ALLOW_BOTS=mentions` lets agents talk to each other only when directly mentioned.
- Avoid `DISCORD_ALLOW_BOTS=all` initially; it can create bot loops.
- Keep Paperclip as the task/control plane; Discord is the conversation/interface layer.

Recommended channels:

```text
WYLIOS HQ
  #wylios-command
  #wylios-paperclip
  #salonx-product
  #salonx-engineering
  #salonx-gtm
  #salonx-sales
  #salonx-research
  #wylios-archive
```

Required from the user before wiring Discord:
- Discord bot token(s)
- Owner Discord user ID
- Server/guild ID
- Channel IDs, if channel allowlisting is desired

Discord Developer Portal reminders:
- Enable Bot capability.
- Enable Message Content Intent.
- Invite with View Channels, Send Messages, Read Message History, Use Slash Commands, and thread permissions if threads will be used.
