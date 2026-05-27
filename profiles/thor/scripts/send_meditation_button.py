#!/usr/bin/env python3
"""Send Thor meditation reminder with a Telegram inline Done button.

Used by no-agent cron jobs. Sends directly via Telegram Bot API and prints
nothing on success so cron stays silent (message is already delivered).
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

CHAT_ID = os.environ.get("THOR_TELEGRAM_CHAT_ID", "8446251233")
TEXT = os.environ.get("THOR_MEDITATION_REMINDER_TEXT", "🧘 Meditation check")
MINUTES = os.environ.get("THOR_MEDITATION_MINUTES", "20")


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def main() -> int:
    hermes_home = Path(os.environ.get("HERMES_HOME", "/home/hermes/.hermes/profiles/thor"))
    load_env(hermes_home / ".env")
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("TELEGRAM_BOT_TOKEN missing", file=sys.stderr)
        return 1

    payload = {
        "chat_id": CHAT_ID,
        "text": TEXT,
        "reply_markup": json.dumps({
            "inline_keyboard": [[
                {"text": f"✅ Log {MINUTES} min", "callback_data": f"wl:meditation:{MINUTES}"}
            ]]
        }),
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except Exception as exc:
        print(f"Telegram send failed: {exc}", file=sys.stderr)
        return 1
    try:
        parsed = json.loads(body)
    except Exception:
        parsed = {"ok": False, "raw": body}
    if not parsed.get("ok"):
        print(f"Telegram send rejected: {body}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
