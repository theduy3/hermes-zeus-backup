---
name: hermes-telegram-inline-buttons
description: Build, debug, and verify Hermes Telegram inline keyboard buttons and callback handlers, especially buttons sent by cron/no-agent scripts.
---

# Hermes Telegram Inline Buttons

Use this when Telegram buttons in Hermes messages do not respond, keep spinning, fail to log, or need Log/More/Done actions. This includes buttons sent by normal Hermes messages and buttons sent directly through the Telegram Bot API by cron/no-agent scripts.

## Core pattern

Telegram inline buttons work only when both sides agree:

1. **Sender emits callback data** in `reply_markup.inline_keyboard[*].callback_data`.
2. **Gateway registers a callback handler** for that callback-data prefix.
3. **Handler acknowledges the callback** with `query.answer(...)` so Telegram stops the spinner.
4. **Handler performs the side effect** (log, edit, script, approval, etc.).
5. **Gateway process is restarted** after adapter/source-code changes.

A common failure mode: cron/no-agent scripts send buttons directly via Telegram Bot API, but the live Hermes gateway adapter does not recognize their callback prefix. Telegram accepts the tap, but Hermes silently returns and no action happens.

## Debug workflow

1. **Read the sender script**
   - Find the exact `callback_data` values being emitted.
   - Example patterns: `wl:water:500`, `wlm:water:500`, `wl:protein:50`.

2. **Read the live Telegram adapter**
   - Search the active Hermes source for the callback prefix.
   - In profile deployments this is often under:
     - `~/.hermes/hermes-agent/plugins/platforms/telegram/adapter.py`
   - Confirm `_handle_callback_query()` routes the prefix before the generic fallback/return.

3. **Inspect gateway logs**
   - Look for button-specific success logs, callback errors, or complete absence of callback logs.
   - Absence of logs for a known prefix usually means the prefix is not handled or returns silently.

4. **Patch the root handler, not the reminder text**
   - Add an explicit prefix route, e.g. `if data.startswith(("wl:", "wlm:")):`.
   - Always call `query.answer(...)` for success and errors.
   - Prefer visible errors like `❌ Logger missing` over silent failure.

5. **Handle More buttons as keyboard edits**
   - `More` should usually call `query.edit_message_reply_markup(...)` to replace the keyboard with expanded options.
   - Add a `Back` callback when useful.

6. **Run deterministic verification before restarting**
   - Compile the edited file: `python -m py_compile path/to/adapter.py`.
   - Use a fake callback query object to directly invoke the new handler with sample `callback_data`.
   - Verify the expected side effect on a temp `HERMES_HOME` when possible.

7. **Restart the gateway**
   - Source edits do not affect the already-running Telegram gateway until restart.
   - If restart requires user approval, tell the user the code is patched but activation is pending restart.

## Implementation checklist

- [ ] Prefix route exists in `_handle_callback_query()`.
- [ ] Unauthorized users are rejected with `query.answer(...)`.
- [ ] Invalid callback data is answered visibly.
- [ ] All code paths call `query.answer(...)`.
- [ ] Side-effect scripts are launched with the correct `HERMES_HOME`.
- [ ] Script paths are profile-safe; avoid hardcoding another profile.
- [ ] Success removes or updates stale keyboards when appropriate.
- [ ] Gateway restart is performed or clearly reported as pending.

## Pitfalls

- **Silent return = broken UX.** If `_handle_callback_query()` reaches a fallback `return` without answering, Telegram shows a spinner and the user sees “button not working.”
- **No-agent cron scripts bypass the normal agent.** They can send buttons directly, but only the always-running gateway can receive callbacks.
- **A successful patch is not active until restart.** Always verify source syntax first, then restart the gateway.
- **Do not guess from memory.** Inspect the live sender script and live adapter, because callback prefixes drift over time.
- **Avoid capturing transient network issues as durable rules.** Network reconnects can block polling temporarily, but missing callback routing is a code/config mismatch and should be fixed in the handler.

## Reference

- See `references/thor-wellness-callbacks-2026-07.md` for the Thor wellness Log/More regression pattern and a fake-query verification recipe.
