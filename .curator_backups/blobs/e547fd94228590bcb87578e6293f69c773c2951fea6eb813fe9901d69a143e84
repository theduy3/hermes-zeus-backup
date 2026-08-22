# Telegram cron task card callback buttons

Use this reference when Telegram inline buttons on cron-generated task cards are visible but tapping `✅ Done` or `⋯ More` does nothing.

## Symptom

- Cron sender script successfully posts a task card with inline keyboard buttons.
- Telegram receives taps, but no card update happens and no source task/registry state changes.
- Slash commands may work normally; this is a callback-query handling problem, not a slash-command discovery problem.

## Root cause pattern

Cron sender scripts only emit `callback_data`; they do not receive button taps. The active Telegram gateway process must have a callback-query handler for every callback-data prefix used by those scripts.

Known task-card prefixes from this incident:

- Zeus daily task cards:
  - `zt:<digest>` = Done
  - `ztm:<digest>` = More/actions menu
  - `ztx:<digest>` = Modify selected
  - `ztd:<digest>` = Delete/dismiss card
  - registry: `~/.hermes/profiles/zeus/task_buttons/registry.json`
- Catthew household task cards:
  - `ct:<digest>` = Done
  - `ctm:<digest>` = More/actions menu
  - `ctx:<digest>` = Modify selected
  - `ctd:<digest>` = Delete/dismiss card
  - registry: `~/.hermes/profiles/catthew/task_buttons/registry.json`

If future profiles add task cards, inspect their sender scripts for new `callback_data` prefixes and add matching gateway dispatch/config.

## Fix pattern

1. Inspect sender scripts and registry files.
   - Search profile scripts for `InlineKeyboardButton`, `callback_data`, `Done`, and `More`.
   - Confirm the registry schema: digest key, title/text/source/file path/status/message ID fields.
2. Patch the central Telegram gateway adapter, not the cron script.
   - Dispatch recognized prefixes early in `_handle_callback_query` before generic update-prompt handlers.
   - Answer callbacks quickly so Telegram does not show a spinner.
   - For `More`, edit the message with expanded task details plus action choices (`Done`, `Modify`, `Delete`, `Back`).
   - For `Modify`, mark the registry entry `modify_requested` and edit the card with reply instructions so the user can send the desired change.
   - For `Delete`, mark the registry entry `deleted`, edit the Telegram card to a deleted confirmation, and remove the keyboard.
   - For `Done`, update registry state, update the backing task source if safe, then edit the Telegram card and remove the keyboard.
3. Keep file writes profile-safe.
   - For Obsidian task markdown, only write inside the expected task root, e.g. `/vault/Tasks/tasks`.
   - Reject paths outside the safe root even if they appear in a registry entry.
   - Do not trust callback data as a file path; treat it only as a registry key.
4. Restart every profile gateway that should load the patched adapter.
   - Verify process `HERMES_HOME` for each profile from `/proc/<pid>/environ`.
   - Tail current gateway logs for `Connected to Telegram (polling mode)`, `✓ telegram connected`, and `Gateway running with 1 platform(s)`.

## Verification pattern

- Compile/import check the modified gateway module in the Hermes venv.
- Smoke-test prefix config and live registry loading without printing secrets.
- Use a temporary registry + fake Telegram query object to exercise:
  - `More` edits text and preserves keyboard.
  - `Done` changes registry status to `done` and updates backing task state.
- After restart, verify all intended profile gateways are running with the correct profile-scoped `HERMES_HOME`.

## Pitfalls

- Do not assume a visible Telegram button has a live handler; inline keyboards can be sent by one process and handled by another.
- Do not patch only one profile's sender script when the callback handler is missing centrally.
- Do not claim success after code changes alone; the running gateway processes must be restarted and verified.
- Static type diagnostics about optional Telegram imports can be noisy in this repo; runtime compile/import checks in the project venv are the decisive smoke tests unless the diagnostics point to newly introduced syntax/import errors.
