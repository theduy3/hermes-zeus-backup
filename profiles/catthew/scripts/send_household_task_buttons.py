#!/usr/bin/env python3
"""Send Catthew household task cards with Telegram Done buttons.

Sources:
- /home/hermes/.hermes/profiles/catthew/tasks.md
- /home/hermes/.hermes/profiles/catthew/events.md
- Reads dated task sections like `## Thu, May 28`.
- Sends at most one pending task/event due today or overdue per run.
- Done button callback is ct:<task_id>; the Telegram gateway marks task
  lines as `- [x]` in tasks.md on click. Event cards are tracked in the registry.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime
from zoneinfo import ZoneInfo

PROFILE = pathlib.Path("/home/hermes/.hermes/profiles/catthew")
BASE = PROFILE / "task_buttons"
REGISTRY = BASE / "registry.json"
TASKS_FILE = PROFILE / "tasks.md"
EVENTS_FILE = PROFILE / "events.md"
ENV_FILES = [PROFILE / ".env", pathlib.Path("/home/hermes/.hermes/.env")]
CONFIG = PROFILE / "config.yaml"
DEFAULT_CHAT_ID = "-5249331607"  # Catthew - the Butler group

MONTHS = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def load_env_file(path: pathlib.Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def config_home_channel() -> str | None:
    if not CONFIG.exists():
        return None
    text = CONFIG.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        if line.startswith("TELEGRAM_HOME_CHANNEL:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'") or None
    return None


def post_telegram(token: str, method: str, payload: dict) -> dict:
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/{method}", data=data)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def today_local() -> date:
    tz_name = os.environ.get("TASK_BUTTON_TZ", "America/Vancouver")
    try:
        return datetime.now(ZoneInfo(tz_name)).date()
    except Exception:
        return date.today()


def parse_section_date(header: str, today: date) -> date | None:
    # Examples: "Thu, May 28", "May 28", "2026-05-28"
    text = header.strip().lstrip("#").strip()
    iso = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", text)
    if iso:
        try:
            return date.fromisoformat(iso.group(1))
        except ValueError:
            return None
    m = re.search(r"\b([A-Za-z]{3,9})\s+(\d{1,2})(?:,\s*(20\d{2}))?\b", text)
    if not m:
        return None
    month = MONTHS.get(m.group(1).lower())
    if not month:
        return None
    day = int(m.group(2))
    year = int(m.group(3)) if m.group(3) else today.year
    try:
        parsed = date(year, month, day)
    except ValueError:
        return None
    # If a December/January rollover is obvious, pick the nearer future/past year.
    if not m.group(3) and parsed.month == 1 and today.month == 12:
        parsed = date(today.year + 1, month, day)
    return parsed


def load_tasks(today: date) -> list[dict]:
    if not TASKS_FILE.exists():
        return []
    tasks: list[dict] = []
    current_due: date | None = None
    for lineno, raw in enumerate(TASKS_FILE.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        header = re.match(r"^##\s+(.+?)\s*$", raw)
        if header:
            current_due = parse_section_date(header.group(1), today)
            continue
        task = re.match(r"^\s*- \[ \]\s+(.+?)\s*$", raw)
        if not task or current_due is None or current_due > today:
            continue
        title = task.group(1).strip()
        source = "Household task" if current_due == today else f"Household task overdue {current_due.isoformat()}"
        tasks.append({"title": title, "due_date": current_due.isoformat(), "source": source, "line": lineno})
    today_tasks = [t for t in tasks if t["due_date"] == today.isoformat()]
    overdue = [t for t in tasks if t["due_date"] != today.isoformat()]
    overdue.sort(key=lambda t: (t["due_date"], t["title"].lower()), reverse=True)
    return sorted(today_tasks, key=lambda t: t["title"].lower()) + overdue


def event_within_date_range(text: str, today: date) -> bool:
    start_match = re.search(r"\bfrom\s+(20\d{2}-\d{2}-\d{2}|[A-Za-z]{3,9}\s+\d{1,2}(?:,\s*20\d{2})?)\b", text, re.I)
    if start_match:
        start = parse_section_date(start_match.group(1), today)
        if start and today < start:
            return False
    end_match = re.search(r"\b(?:through|until)\s+(20\d{2}-\d{2}-\d{2}|[A-Za-z]{3,9}\s+\d{1,2}(?:,\s*20\d{2})?)\b", text, re.I)
    if end_match:
        end = parse_section_date(end_match.group(1), today)
        if end and today > end:
            return False
    return True


def load_today_events(today: date) -> list[dict]:
    if not EVENTS_FILE.exists():
        return []
    events: list[dict] = []
    in_recurring = False
    for lineno, raw in enumerate(EVENTS_FILE.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        header = re.match(r"^##\s+(.+?)\s*$", raw)
        if header:
            in_recurring = header.group(1).strip().lower() == "recurring"
            continue
        item = re.match(r"^\s*-\s+(.+?)\s*$", raw)
        if not item or not in_recurring:
            continue
        text = item.group(1).strip()
        weekday_match = re.search(r"\bevery\s+([A-Za-z]+)\b", text, re.I)
        if not weekday_match:
            continue
        if WEEKDAYS.get(weekday_match.group(1).lower()) != today.weekday():
            continue
        if not event_within_date_range(text, today):
            continue
        events.append({
            "title": text,
            "due_date": today.isoformat(),
            "source": "Household event today",
            "line": lineno,
            "kind": "event",
        })
    return events


def main() -> int:
    for env in ENV_FILES:
        load_env_file(env)
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TASK_BUTTON_CHAT_ID") or os.environ.get("TELEGRAM_HOME_CHANNEL") or config_home_channel() or DEFAULT_CHAT_ID
    if not token:
        print("TELEGRAM_BOT_TOKEN missing", file=sys.stderr)
        return 1

    local_today = today_local()
    date_key = local_today.isoformat()
    tasks = load_today_events(local_today) + load_tasks(local_today)
    if not tasks:
        return 0

    BASE.mkdir(parents=True, exist_ok=True)
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    try:
        send_limit = max(1, int(os.environ.get("TASK_BUTTON_SEND_LIMIT", "1")))
    except ValueError:
        send_limit = 1

    sent = 0
    for task in tasks:
        title = task["title"]
        digest = hashlib.sha1(f"{date_key}\n{task.get('kind', 'task')}\n{title}\n{task['line']}".encode("utf-8")).hexdigest()[:16]
        existing = registry.get(digest, {})
        if existing.get("message_id") and existing.get("status") != "done":
            continue
        if existing.get("status") == "done":
            continue

        text = f"☐ {title}\nSource: {task['source']}"
        markup = json.dumps({"inline_keyboard": [[
            {"text": "✅ Done", "callback_data": f"ct:{digest}"},
            {"text": "More", "callback_data": f"ctm:{digest}"},
        ]]}, ensure_ascii=False)
        res = post_telegram(token, "sendMessage", {
            "chat_id": chat_id,
            "text": text,
            "reply_markup": markup,
            "disable_web_page_preview": "true",
        })
        message_id = res.get("result", {}).get("message_id")
        registry[digest] = {
            "id": digest,
            "date": date_key,
            "title": title,
            "text": title,
            "source": task["source"],
            "due_date": task["due_date"],
            "line": task["line"],
            "kind": task.get("kind", "task"),
            "status": "sent",
            "message_id": message_id,
        }
        sent += 1
        if sent >= send_limit:
            break

    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
