# Discord employee-agent gateway for Paperclip companies

Use this when the user wants to chat with Paperclip/Hermes company agents like employees in Discord, and optionally let the agents coordinate with each other.

## Recommended rollout

Start with one Discord-facing Hermes profile/bot, usually the CEO/dispatcher.

Flow:

```text
Discord owner -> CEO Hermes Discord profile -> Paperclip bridge/helper script -> Paperclip issue/comment/checkout -> Hermes local agents
```

Only add one bot per employee after the CEO bot is verified. Multiple employee bots require one Discord application/token per bot plus careful mention/loop controls.

## Discord profile environment

For the company Discord profile, write profile-local `.env` values, not the default profile env:

```env
DISCORD_BOT_TOKEN=<bot_token>
DISCORD_ALLOWED_USERS=<owner_discord_user_id>
DISCORD_GUILD_ID=<server_id>
DISCORD_ALLOWED_CHANNELS=<optional_comma_separated_channel_ids>
DISCORD_IGNORE_NO_MENTION=true
DISCORD_ALLOW_BOTS=mentions
```

Notes:
- `DISCORD_IGNORE_NO_MENTION=true` keeps the bot from replying to every channel message.
- `DISCORD_ALLOW_BOTS=mentions` lets employee bots hand off to each other only by explicit @mention.
- Avoid `DISCORD_ALLOW_BOTS=all` initially; it can create bot loops.
- If the gateway log says no user allowlists are configured, Discord messages may be denied even though the bot is connected.

## Discord Developer Portal checklist

For each bot/app:

1. Enable Bot capability.
2. Enable Message Content Intent.
3. Invite bot to the server with at least:
   - View Channels
   - Send Messages
   - Read Message History
   - Use Slash Commands
   - Create Public Threads / Send Messages in Threads if threads are used
4. Collect:
   - bot token
   - owner Discord user ID
   - server/guild ID
   - optional channel IDs

## Gateway setup checklist

1. Create or clone a Hermes profile for the company/bot.
2. Ensure the profile has its own `config.yaml` and `.env`; profiles with missing config/env may fall back to the default profile.
3. Put the Discord token and allowlist in the profile `.env`.
4. Add a short `SOUL.md` describing the company role, escalation rules, and Paperclip bridge path.
5. Generate and give the user the OAuth invite URL for each bot before expecting server/channel tests to work:

```text
https://discord.com/oauth2/authorize?client_id=<application_client_id>&permissions=397284672576&integration_type=0&scope=bot+applications.commands
```

6. Start/restart gateway with profile-scoped home:

```bash
HERMES_HOME=/home/hermes/.hermes/profiles/<profile> hermes -p <profile> gateway run
```

7. Verify logs show:

```text
Connected as <BotName>#<discriminator>
✓ discord connected
Channel directory built: <N> target(s)
```

8. Also verify guild membership. A bot token can validate and the gateway can connect while the bot is in zero guilds; in that state Discord tests cannot work. If the guild list/directory is empty, report the setup as "connected but not invited", provide the invite links, and wait for the owner to add the bots to the Discord server. After invitation, restart or re-poll each profile gateway and verify the target guild/channel appears.

9. Test in Discord by mentioning the bot:

```text
@BotName list <Company> Paperclip issues
```

## Agent-to-agent coordination rule

Use explicit mention-based handoffs only:

```text
@salonx-engineer please inspect WYL-16 and report blockers in #salonx-engineering.
```

The receiving agent should read/update Paperclip, then reply with WYL ID, status, blockers, and next step. Agents should not free-chat indefinitely.

## Local Paperclip UI over VPS/container

If Paperclip runs inside a VPS container bound to container localhost, `http://127.0.0.1:3100` on the user's laptop will not work directly. Use an SSH local-forward through the host, often on a different local port to avoid conflicts:

```bash
ssh -N -v \
  -i ~/.ssh/id_ed25519 \
  -o IdentitiesOnly=yes \
  -o ExitOnForwardFailure=yes \
  -L 3101:127.0.0.1:3100 \
  root@<vps_ip>
```

Then open:

```text
http://127.0.0.1:3101
```

For a shortcut, add an SSH config host such as:

```sshconfig
Host paperclip
  HostName <vps_ip>
  User root
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
  ExitOnForwardFailure yes
  LocalForward 3101 127.0.0.1:3100
```

Then run:

```bash
ssh -N paperclip
```
