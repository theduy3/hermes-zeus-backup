# Discord employee-agent setup for Paperclip companies

Use this when the user wants to chat with company agents like employees in Discord, and optionally let agents coordinate with each other.

## Recommended architecture

Start with one Discord-facing CEO/dispatcher bot/profile, then add separate employee bots only after the command loop is proven useful.

Initial flow:

```text
Discord user → CEO Hermes Discord profile → Paperclip helper script/CLI/API → Paperclip issue/comment/checkout → Hermes/Paperclip worker agent
```

Benefits:
- fewer Discord applications/tokens to manage
- less risk of bot-to-bot loops
- one clear owner approval point
- Paperclip remains the source of truth for work/status

Add separate bots later for product, engineering, GTM, sales, and research only if the user explicitly wants per-employee personalities/accounts.

## Discord profile setup checklist

1. Create a Hermes profile for the company bot, e.g. `wylios-ceo`.
2. Ensure the profile has its own `config.yaml` and `.env`.
3. Put the Discord bot token in the profile `.env`:

```env
DISCORD_BOT_TOKEN=<token>
DISCORD_ALLOWED_USERS=<owner_discord_user_id>
DISCORD_GUILD_ID=<server_id>
DISCORD_ALLOWED_CHANNELS=<comma_separated_channel_ids_optional>
DISCORD_IGNORE_NO_MENTION=true
DISCORD_ALLOW_BOTS=mentions
```

4. If using one trusted company channel and the user wants plain messages without @mention, add:

```env
DISCORD_FREE_RESPONSE_CHANNELS=<channel_id>
```

5. Restart the profile gateway with profile-scoped home:

```bash
HERMES_HOME=/home/hermes/.hermes/profiles/<profile> hermes -p <profile> gateway run
```

6. Verify logs show:

```text
[Discord] Connected as <BotName>#NNNN
✓ discord connected
Channel directory built: N target(s)
```

## Discord Developer Portal requirements

- Bot capability enabled
- MESSAGE CONTENT INTENT enabled
- Bot invited to the server with permissions:
  - View Channels
  - Send Messages
  - Read Message History
  - Use Slash Commands
  - Create Public Threads / Send Messages in Threads if using threads

## Mention pitfalls

Discord can autocomplete roles before bot users. If the message content contains a role mention such as:

```text
<@&1234567890> list issues
```

then the user mentioned a role, not the bot. Hermes may ignore it because the actual bot user was not mentioned.

Fix options:
- Tell the user to mention the actual bot user, e.g. `@Wylios-CEO`, not the role.
- Or put the channel ID in `DISCORD_FREE_RESPONSE_CHANNELS` so no mention is needed in that channel.

## Bot-to-bot coordination

For multiple employee bots, use mention-based handoffs only:

```text
@salonx-engineer please inspect WYL-16 and report blockers in #salonx-engineering.
```

Recommended setting:

```env
DISCORD_ALLOW_BOTS=mentions
```

Avoid `DISCORD_ALLOW_BOTS=all` at first; it can create loops. Each agent should mention another bot only for a specific handoff and should include the WYL issue ID/status in the response.

## Operational rule

Keep Paperclip as the source of truth:
- Discord is the chat/interface layer.
- Paperclip issues/comments/work products are the durable record.
- The company-local helper script should pin company/project/agent IDs and wrap issue list/create/comment/checkout/release/done.
