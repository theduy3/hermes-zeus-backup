#!/usr/bin/env python3
"""Send Zeus daily schedule reminders (brunch, company review, protein, exercise, pickup).

Runs as a no-agent cron. It stays silent except in configured reminder windows.
Schedule reminders are plain one-line messages without buttons or task lists;
task cards with Done buttons are handled separately by due_task_drip.py.
Specific-time events/tasks are intentionally not fed into Pomodoro reminders.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, time
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Vancouver")
PROFILE = pathlib.Path("/home/hermes/.hermes/profiles/zeus")
PLAN_DIR = pathlib.Path("/vault/Tasks/planning")
SCHEDULE_REGISTRY = PROFILE / "task_buttons" / "schedule_reminder_registry.json"
GENERATOR = PROFILE / "scripts" / "generate_daily_plan.py"
CONFIG = PROFILE / "config.yaml"
ENV_FILES = [PROFILE / ".env", pathlib.Path("/home/hermes/.hermes/.env")]

# Weekday work-day reminders. Windows are intentionally short; cron can run
# every 5 minutes and only one reminder per key/day will be sent.
WEEKDAY_WINDOWS = [
    {"key": "exercise", "start": "09:00", "end": "09:06", "heading": "9:00–10:00 Exercise", "title": "Exercise", "time": "9:00–10:00", "fallback": ["Morning exercise", "Drop Victoria at daycare first"]},
    {"key": "brunch", "start": "10:00", "end": "10:06", "heading": "10:00–10:30 Brunch", "title": "Brunch", "time": "10:00–10:30", "fallback": ["Brunch", "Water 2/6"]},
    {"key": "company", "start": "11:45", "end": "11:51", "heading": "11:45–12:15 Company Review", "title": "Company review", "time": "11:45–12:15", "fallback": ["Revenue/cash", "Staff/schedule", "Reviews/complaints", "Pick one follow-up"]},
    {"key": "protein", "start": "14:00", "end": "14:06", "heading": "", "title": "Protein", "time": "2:00", "fallback": ["Protein drink"]},
    {"key": "pickup", "start": "15:35", "end": "15:41", "heading": "3:35–3:45 Pickup Transition", "title": "Pickup transition", "time": "3:35–3:45", "fallback": ["Stop work", "Prepare to pick up Victoria"]},
]

# Weekends are intentionally silent for Zeus schedule reminders. Weekend task
# cards still come from due_task_drip.py when something is actually due.
WEEKEND_WINDOWS: list[dict] = []


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


def post_telegram(token: str, method: str, payload: dict) -> dict:
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/{method}",
        data=urllib.parse.urlencode(payload).encode("utf-8"),
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_time(s: str) -> time:
    h, m = [int(x) for x in s.split(":")]
    return time(h, m)


def windows_for(now: datetime) -> list[dict]:
    return WEEKEND_WINDOWS if now.weekday() >= 5 else WEEKDAY_WINDOWS


def current_window(now: datetime, force: str | None = None) -> dict | None:
    wins = windows_for(now)
    # Weekends are always silent. --force may select a weekday window for a
    # weekday test, but must not bypass the weekend policy.
    if now.weekday() >= 5:
        return None
    if force:
        return next((w for w in wins if w["key"] == force), None)
    t = now.time()
    for w in wins:
        if parse_time(w["start"]) <= t <= parse_time(w["end"]):
            return w
    return None


def ensure_plan(day: str, is_weekend: bool) -> pathlib.Path:
    path = PLAN_DIR / f"{day}.md"
    if not is_weekend and GENERATOR.exists():
        subprocess.run([sys.executable, str(GENERATOR), "--date", day], check=False, timeout=60, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return path


def section(text: str, heading: str) -> str:
    if not heading:
        return ""
    pat = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.M)
    m = pat.search(text)
    if not m:
        return ""
    start = m.end()
    n = re.search(r"^##\s+", text[start:], re.M)
    end = start + n.start() if n else len(text)
    return text[start:end].strip()


def clean_line(line: str) -> str:
    line = re.sub(r"^- \[[ xX]\]\s*", "", line.strip())
    line = re.sub(r"^[-*]\s*", "", line)
    line = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", line)
    line = re.sub(r"\[\[([^\]]+)\]\]", r"\1", line)
    line = re.sub(r"`[^`]*`", "", line)
    line = re.sub(r"\([^)]*\)", "", line)
    return re.sub(r"\s+", " ", line).strip(" -")


def load_json(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    except Exception:
        return {}


def save_json(path: pathlib.Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")



def main() -> int:
    force = None
    if "--force" in sys.argv:
        i = sys.argv.index("--force")
        force = sys.argv[i + 1] if i + 1 < len(sys.argv) else "setup"
    dry_run = "--dry-run" in sys.argv

    for env in ENV_FILES:
        load_env_file(env)
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_HOME_CHANNEL") or config_home_channel() or "8446251233"
    if not token and not dry_run:
        print("TELEGRAM_BOT_TOKEN missing", file=sys.stderr)
        return 1
    if token is None:
        token = ""

    now = datetime.now(TZ)
    win = current_window(now, force=force)
    if not win:
        return 0
    day = now.date().isoformat()
    key = f"{day}:{win['key']}"
    sent_registry = load_json(SCHEDULE_REGISTRY)
    if key in sent_registry and not force:
        return 0

    ensure_plan(day, now.weekday() >= 5)
    title = f"{win['time']} — {win['title']}"
    lines = [f"🗓 {title}"]
    if now.weekday() >= 5:
        lines += ["", "Family-first: keep it light."]
    text = "\n".join(lines)

    if dry_run:
        print(text)
        return 0

    res = post_telegram(token, "sendMessage", {"chat_id": chat_id, "text": text, "disable_web_page_preview": "true"})
    mid = res.get("result", {}).get("message_id")
    sent_registry[key] = {"message_id": mid, "sent_at": now.isoformat(), "title": title}
    save_json(SCHEDULE_REGISTRY, sent_registry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
