#!/usr/bin/env python3
"""Send one due-today Obsidian task card to Telegram per run.

Source of truth: /vault/Tasks/tasks/*.md. Uses the Zeus task button registry
with callback prefix zt:<digest>, so Done buttons update the original task file.
Overdue tasks are intentionally not dripped; Duy moves them himself while planning.
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
from dataclasses import dataclass
from datetime import date, datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Vancouver")
PROFILE = pathlib.Path("/home/hermes/.hermes/profiles/zeus")
TASK_DIR = pathlib.Path("/vault/Tasks/tasks")
REGISTRY = PROFILE / "task_buttons" / "registry.json"
CONFIG = PROFILE / "config.yaml"
ENV_FILES = [PROFILE / ".env", pathlib.Path("/home/hermes/.hermes/.env")]
SKIP_STATUSES = {"completed", "done", "cancelled", "canceled"}

@dataclass
class Task:
    path: pathlib.Path
    title: str
    due: date
    status: str
    tags: str
    company: str
    due_time: str = ""


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
    for line in CONFIG.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("TELEGRAM_HOME_CHANNEL:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'") or None
    return None


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm: dict[str, str] = {}
    for raw in parts[1].splitlines():
        if ":" not in raw or raw.startswith((" ", "\t", "-")):
            continue
        k, v = raw.split(":", 1)
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, parts[2]


def title_from(path: pathlib.Path, body: str, fm: dict[str, str]) -> str:
    if fm.get("title"):
        return fm["title"].strip()
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("-", " ").title()


def has_catthew(fm: dict[str, str], body: str, path: pathlib.Path) -> bool:
    hay = "\n".join([path.name, fm.get("tags", ""), fm.get("company", ""), body[:2000]]).lower()
    return "#catthew" in hay or "catthew" in hay


def load_tasks(today: date) -> list[Task]:
    out: list[Task] = []
    for path in sorted(TASK_DIR.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        fm, body = parse_frontmatter(text)
        kind = (fm.get("type") or "task").lower()
        if kind != "task":
            continue
        # Earnings are events/reminders, not actionable tasks; never send Done buttons for them.
        if (fm.get("source") or "").lower() == "nasdaq-earnings-calendar" or "earnings" in (fm.get("tags") or "").lower():
            continue
        status = (fm.get("status") or "pending").lower()
        if status in SKIP_STATUSES:
            continue
        if has_catthew(fm, body, path):
            continue
        due_txt = (fm.get("due_date") or fm.get("date") or "").strip()[:10]
        try:
            due = date.fromisoformat(due_txt)
        except ValueError:
            continue
        if due != today:
            continue
        due_time = (fm.get("due_time") or fm.get("time") or fm.get("start_time") or "").strip()
        if not due_time:
            m = re.search(r"(?im)^\s*(?:kickoff|start|due|time|date/time)\s*:\s*(.+)$", body)
            if m:
                due_time = m.group(1).strip()
        out.append(Task(path, title_from(path, body, fm), due, status, fm.get("tags", ""), fm.get("company", ""), due_time))
    return sorted(out, key=lambda t: (t.title.lower(), str(t.path)))


def load_json(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    except Exception:
        return {}


def save_json(path: pathlib.Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def post_telegram(token: str, method: str, payload: dict) -> dict:
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/{method}",
        data=urllib.parse.urlencode(payload).encode("utf-8"),
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def digest_for(task: Task) -> str:
    return hashlib.sha1(f"{task.title}\n{task.path}\n{task.due.isoformat()}".encode("utf-8")).hexdigest()[:16]


def already_sent_today(registry: dict, task: Task, today: str) -> bool:
    for entry in registry.values():
        if not isinstance(entry, dict):
            continue
        if entry.get("file_path") != str(task.path):
            continue
        if entry.get("status") == "done":
            return True
        if entry.get("status") == "sent" and entry.get("date") == today:
            return True
    return False


def main() -> int:
    dry = "--dry-run" in sys.argv
    for env in ENV_FILES:
        load_env_file(env)
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_HOME_CHANNEL") or config_home_channel() or "8446251233"
    if not token and not dry:
        print("TELEGRAM_BOT_TOKEN missing", file=sys.stderr)
        return 1
    if token is None:
        token = ""
    today = datetime.now(TZ).date()
    today_s = today.isoformat()
    registry = load_json(REGISTRY)
    for task in load_tasks(today):
        if already_sent_today(registry, task, today_s):
            continue
        digest = digest_for(task)
        label = "Due today"
        meta = f"\nCompany: {task.company}" if task.company else ""
        time_line = f"\nTime: {task.due_time}" if task.due_time else ""
        text = f"☐ {task.title}\n{label}{time_line}{meta}\nSource: Obsidian"
        if dry:
            print(f"would send: {task.title} ({task.path})")
            return 0
        markup = json.dumps({"inline_keyboard": [[
            {"text":"Done","callback_data":f"zt:{digest}"},{"text":"Delay","callback_data":f"delay:{digest}"},{"text":"Delete","callback_data":f"del:{digest}"},
        ]]}, ensure_ascii=False)
        res = post_telegram(token, "sendMessage", {"chat_id": chat_id, "text": text, "reply_markup": markup, "disable_web_page_preview": "true"})
        mid = res.get("result", {}).get("message_id")
        registry[digest] = {
            "id": digest,
            "date": today_s,
            "due_date": task.due.isoformat(),
            "title": task.title,
            "text": task.title,
            "source": "Obsidian",
            "file_path": str(task.path),
            "status": "sent",
            "message_id": mid,
            "odds": "",
        }
        save_json(REGISTRY, registry)
        print(f"sent: {task.title} message_id={mid}")
        return 0
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
# Auto handlers added: delay reply parses YYYY-MM-DD; delete removes file + syncs calendar
