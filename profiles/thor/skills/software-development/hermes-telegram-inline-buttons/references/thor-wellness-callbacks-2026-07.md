# Thor Wellness Callback Regression — 2026-07

## Symptom

Telegram reminder buttons labeled Log/More stopped working. Tapping buttons produced no wellness log update and no expanded More menu.

## Root cause pattern

The reminder scripts sent callback data directly through Telegram Bot API, for example:

```python
{"text": "✅ Log 500ml", "callback_data": "wl:water:500"}
{"text": "More", "callback_data": "wlm:water:500"}
```

But the active Telegram gateway adapter did not route `wl:` / `wlm:` inside `_handle_callback_query()`. Since those callbacks bypass the LLM and arrive only at the gateway, the adapter must handle them explicitly.

## Fix shape

Add a route before the generic `update_prompt` fallback:

```python
if data.startswith(("wl:", "wlm:", "wlb:")):
    await self._handle_wellness_log_callback(...)
    return
```

Then implement a handler that:

- validates authorization with `_is_callback_user_authorized(...)`
- parses `wl|wlm|wlb:<kind>:<amount>`
- answers every callback with `query.answer(...)`
- edits the keyboard for `More`/`Back`
- runs the profile log script for `Log`
- reports visible script errors instead of silently returning
- logs success with kind, amount, and user id

## Fake-query verification recipe

Use a temp `HERMES_HOME` so the test does not mutate real logs:

```bash
tmp=$(mktemp -d)
mkdir -p "$tmp/scripts"
cp ~/.hermes/profiles/thor/scripts/log_water_button.py "$tmp/scripts/"
HERMES_HOME="$tmp" ~/.hermes/hermes-agent/venv/bin/python - <<'PY'
import asyncio
from types import SimpleNamespace
from plugins.platforms.telegram.adapter import TelegramAdapter
from gateway.config import Platform

class Q:
    data = 'wl:water:250'
    from_user = SimpleNamespace(id='8446251233', first_name='Duy')
    message = SimpleNamespace(text='💧 Test water', date=None)
    def __init__(self):
        self.answers = []
        self.edits = []
    async def answer(self, text=None, **kw):
        self.answers.append(text)
    async def edit_message_text(self, **kw):
        self.edits.append(kw)
    async def edit_message_reply_markup(self, **kw):
        self.edits.append(kw)

async def main():
    a = TelegramAdapter.__new__(TelegramAdapter)
    a.platform = Platform.TELEGRAM
    a._is_callback_user_authorized = lambda *args, **kwargs: True
    q = Q()
    await a._handle_wellness_log_callback(
        q, q.data,
        query_chat_id='8446251233',
        query_chat_type='private',
        query_thread_id=None,
        query_user_name='Duy',
    )
    print('answers=', q.answers)
    print('edits=', q.edits)

asyncio.run(main())
PY
find "$tmp/logs" -type f -maxdepth 1 -print -exec sed -n '1,80p' {} \;
```

Expected proof:

- `answers=` includes `✅ Logged 250ml water`
- message edit removes/updates the keyboard
- temp food log contains the added water row and daily totals

## Activation step

After patching adapter code, run syntax verification first:

```bash
~/.hermes/hermes-agent/venv/bin/python -m py_compile ~/.hermes/hermes-agent/plugins/platforms/telegram/adapter.py
```

Then restart the relevant profile gateway. If approval blocks restart, report that the code is patched but not active until restart.
