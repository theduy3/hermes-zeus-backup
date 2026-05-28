#!/usr/bin/env python3
"""Send Thor daily exercise reminder with YouTube link."""
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

CHAT_ID = os.environ.get("THOR_TELEGRAM_CHAT_ID", "8446251233")
TEXT = os.environ.get(
    "THOR_EXERCISE_REMINDER_TEXT",
    "🏃 3PM exercise time\nhttps://youtu.be/Jo1eWJ0YNnA?si=xnAMcODqvYy1oyde",
)
VIDEO_URL = os.environ.get("THOR_EXERCISE_URL", "https://youtu.be/Jo1eWJ0YNnA?si=xnAMcODqvYy1oyde")


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


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
            "inline_keyboard": [[{"text": "▶️ Start exercise", "url": VIDEO_URL}]]
        }),
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=data, method="POST")
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
