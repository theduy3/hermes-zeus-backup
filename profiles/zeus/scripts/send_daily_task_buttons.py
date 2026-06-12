#!/usr/bin/env python3
"""Send Zeus individual Obsidian task cards with Telegram Done buttons.

Source: /vault/Tasks/tasks/*.md
- Reads each task's YAML frontmatter directly from the Obsidian vault.
- Sends one Telegram card per pending/in_progress task due today or overdue.
- Done button callback is zt:<task_id>; the Telegram gateway marks the source
  vault file's YAML frontmatter as `status: completed` on click.
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
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

BASE = pathlib.Path("/home/hermes/.hermes/profiles/zeus/task_buttons")
INPUT = BASE / "today_tasks.json"
REGISTRY = BASE / "registry.json"
VAULT_TASKS = pathlib.Path("/vault/Tasks/tasks")
ENV_FILES = [pathlib.Path("/home/hermes/.hermes/profiles/zeus/.env"), pathlib.Path("/home/hermes/.hermes/.env")]
CONFIG = pathlib.Path("/home/hermes/.hermes/profiles/zeus/config.yaml")


def load_env_file(path: pathlib.Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        os.environ.setdefault(key, val)


def config_home_channel() -> str | None:
    if not CONFIG.exists():
        return None
    text = CONFIG.read_text(encoding="utf-8", errors="ignore")
    # Avoid PyYAML dependency in cron script; this config value is a simple scalar.
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


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, ""
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, ""
    fm_text = parts[1]
    fm: dict[str, str] = {}
    for raw in fm_text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, val = line.split(":", 1)
        fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm, parts[2]


def title_from_body(path: pathlib.Path, body: str) -> str:
    for line in body.splitlines():
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return path.stem.replace("-", " ").strip().title()


def add_months(d: date, months: int) -> date:
    month_index = d.month - 1 + months
    year = d.year + month_index // 12
    month = month_index % 12 + 1
    month_lengths = [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return date(year, month, min(d.day, month_lengths[month - 1]))


def next_recurring_due(due: date, recurrence: str, today: date, grace_days: int = 2) -> date:
    """Roll stale recurring tasks forward after a short grace window.

    A pending recurring task remains visible on its due date and the next day.
    Once it is 2+ days old, it disappears and advances to the next scheduled
    occurrence so it can reappear later.
    """
    recurrence = recurrence.strip().lower()
    if not recurrence or due > today - timedelta(days=grace_days):
        return due
    if recurrence == "daily":
        step = lambda x: x + timedelta(days=1)
    elif recurrence == "weekly":
        step = lambda x: x + timedelta(days=7)
    elif recurrence in {"bi-weekly", "biweekly", "fortnightly"}:
        step = lambda x: x + timedelta(days=14)
    elif recurrence == "monthly":
        step = lambda x: add_months(x, 1)
    elif recurrence == "quarterly":
        step = lambda x: add_months(x, 3)
    elif recurrence in {"annually", "annual", "yearly"}:
        step = lambda x: add_months(x, 12)
    else:
        return due
    while due <= today - timedelta(days=grace_days):
        due = step(due)
    return due


def update_due_date(path: pathlib.Path, old_due: date, new_due: date) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    updated = re.sub(r"(?m)^due_date:\s*" + re.escape(old_due.isoformat()) + r"\s*$", f"due_date: {new_due.isoformat()}", text, count=1)
    if updated != text:
        path.write_text(updated, encoding="utf-8")


def load_vault_tasks(today: date) -> list[dict]:
    if not VAULT_TASKS.exists():
        return []
    tasks: list[dict] = []
    for path in sorted(VAULT_TASKS.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        fm, body = parse_frontmatter(text)
        if (fm.get("type") or "task").strip().lower() != "task":
            continue
        status = (fm.get("status") or "pending").strip().lower()
        if status in {"completed", "done", "cancelled", "canceled"}:
            continue
        due_text = (fm.get("due_date") or "").strip()
        if not due_text:
            continue
        try:
            due = date.fromisoformat(due_text[:10])
        except ValueError:
            continue
        if due > today:
            continue
        recurrence = (fm.get("recurrence") or "").strip()
        if recurrence:
            next_due = next_recurring_due(due, recurrence, today)
            if next_due != due:
                update_due_date(path, due, next_due)
                due = next_due
            if due > today:
                continue
        title = title_from_body(path, body)
        tasks.append({
            "title": title,
            "source": "Obsidian" if due == today else f"Obsidian overdue {due.isoformat()}",
            "file_path": str(path),
            "due_date": due.isoformat(),
        })
    # Priority: today's tasks first, then overdue tasks newest-first, then title.
    tasks.sort(key=lambda t: (
        0 if t.get("due_date") == today.isoformat() else 1,
        t.get("due_date", "9999-99-99") if t.get("due_date") == today.isoformat() else "",
        t.get("title", "").lower(),
    ))
    overdue = [t for t in tasks if t.get("due_date") != today.isoformat()]
    overdue.sort(key=lambda t: (t.get("due_date", "0000-00-00"), t.get("title", "").lower()), reverse=True)
    today_tasks = [t for t in tasks if t.get("due_date") == today.isoformat()]
    return today_tasks + overdue


def main() -> int:
    for env in ENV_FILES:
        load_env_file(env)
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_HOME_CHANNEL") or config_home_channel() or "8446251233"
    if not token:
        print("TELEGRAM_BOT_TOKEN missing", file=sys.stderr)
        return 1
    local_today = today_local()
    date_key = local_today.isoformat()
    try:
        tasks = load_vault_tasks(local_today)
    except Exception as exc:
        print(f"vault task scan failed: {exc}", file=sys.stderr)
        tasks = []

    if not tasks:
        return 0

    BASE.mkdir(parents=True, exist_ok=True)
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    sent = 0
    try:
        send_limit = max(1, int(os.environ.get("TASK_BUTTON_SEND_LIMIT", "1")))
    except ValueError:
        send_limit = 1

    for idx, task in enumerate(tasks, 1):
        title = str(task.get("title") or task.get("text") or "").strip()
        if not title:
            continue
        source = str(task.get("source") or "").strip()
        file_path = str(task.get("file_path") or "").strip()
        digest = hashlib.sha1(f"{date_key}\n{title}\n{file_path}".encode("utf-8")).hexdigest()[:16]
        existing = registry.get(digest, {})
        if existing.get("message_id") and existing.get("status") != "done":
            continue
        if existing.get("status") == "done":
            continue

        text = f"☐ {title}"
        if source:
            text += f"\nSource: {source}"
        markup = json.dumps({"inline_keyboard": [[
            {"text": "✅ Done", "callback_data": f"zt:{digest}"},
            {"text": "More", "callback_data": f"ztm:{digest}"},
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
            "source": source,
            "file_path": file_path,
            "status": "sent",
            "message_id": message_id,
        }
        sent += 1
        if sent >= send_limit:
            break

    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    # Keep stdout empty on success so no_agent cron stays silent.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
