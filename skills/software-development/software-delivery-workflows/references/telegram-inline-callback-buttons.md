# Telegram inline callback buttons in Hermes profile gateways

Use this when cron/script-only jobs send Telegram inline buttons directly via Bot API and the buttons do nothing.

## Diagnostic pattern

1. Inspect the sender scripts for `reply_markup` / `inline_keyboard` / `callback_data`.
2. Search the Telegram gateway adapter for handlers for those exact compact callback prefixes.
3. If callback data exists only in scripts and not in the gateway callback router, the root cause is missing central callback handling, not the cron job itself.
4. Check all profile-specific sender scripts, not just the profile where the user noticed the failure.

## Durable examples from current deployment

- Zeus task cards:
  - `zt:<task_id>` = Done
  - `ztm:<task_id>` = More
  - Registry: `/home/hermes/.hermes/profiles/zeus/task_buttons/registry.json`
  - Source task files constrained under `/vault/Tasks/tasks`
- Catthew household task cards:
  - `ct:<task_id>` = Done
  - `ctm:<task_id>` = More
  - Registry: `/home/hermes/.hermes/profiles/catthew/task_buttons/registry.json`
  - Source file: `/home/hermes/.hermes/profiles/catthew/tasks.md`
- Thor wellness buttons demonstrate the older working More pattern:
  - `wl:<kind>:<amount>` = Log/Done
  - `wlm:<kind>:<amount>` = More
  - Handler shape: parse `wlm:`, build details text, call `query.edit_message_text(...)`, and rebuild `InlineKeyboardMarkup` so buttons stay active.

## Implementation pattern

- Route compact callback prefixes early in `_handle_callback_query` before generic fallthrough.
- Use one handler per button class, not one-off code in each sender script.
- For `More`, treat it as non-destructive and match the old Thor wellness pattern unless the user explicitly asks for richer expansion:
  - button label should be plain `More`, not `⋯ More`;
  - edit the message text with concise details only;
  - do not expand full source-file notes/paths into the card by default;
  - preserve/rebuild the inline keyboard so `Done` and `More` stay active;
  - answer the callback with a short confirmation.
- For `Done`, treat it as committing:
  - authorize caller via existing callback authorization helper;
  - update the source of truth where applicable;
  - update the registry entry (`status`, `done_at`, `done_by`, source update flag);
  - edit the Telegram message and remove the keyboard.
- Keep profile file writes constrained to known safe roots/files.

## Verification checklist

- `python -m py_compile gateway/platforms/telegram.py`
- Import the adapter from the same venv the gateway uses.
- Exercise handler logic with a fake callback query against a temporary registry/source file.
- Restart/reload every affected profile gateway.
- Verify running profile gateway processes have the expected `HERMES_HOME` values.
- Tail gateway logs for `Connected to Telegram` / `Gateway running` after restart.

## Pitfall

Do not assume a button exists just because a sender script emits it. Telegram callback buttons require both sides: sender `callback_data` and a live gateway route for that exact prefix.