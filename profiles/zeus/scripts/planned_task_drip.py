#!/usr/bin/env python3
"""Send time-blocked block reminders from /vault/Tasks/planning/YYYY-MM-DD.md.

Silent unless the current Vancouver time is inside an approved card window.
Block reminders are plain Telegram messages without task buttons. Task cards
with Done buttons are sent separately by due_task_drip.py from source task notes.
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
PLAN_REGISTRY = PROFILE / "task_buttons" / "plan_drip_registry.json"
GENERATOR = PROFILE / "scripts" / "generate_daily_plan.py"
CONFIG = PROFILE / "config.yaml"
ENV_FILES = [PROFILE / ".env", pathlib.Path("/home/hermes/.hermes/.env")]

BLOCK_WINDOWS = [
    {"key": "setup", "start": "09:00", "end": "09:09", "heading": "9:00–9:10 Daily Setup", "kind": "summary"},
    {"key": "deep1", "start": "09:10", "end": "09:19", "heading": "9:10–10:00 Deep Work 1", "kind": "tasks"},
    {"key": "deep2", "start": "10:30", "end": "10:39", "heading": "10:30–11:45 Deep Work 2", "kind": "tasks"},
    {"key": "company", "start": "11:45", "end": "11:54", "heading": "11:45–12:15 Company Review", "kind": "company"},
    {"key": "admin", "start": "12:15", "end": "12:24", "heading": "12:15–12:45 Admin / Finance Batch", "kind": "tasks"},
    {"key": "deep3", "start": "13:00", "end": "13:09", "heading": "1:00–2:15 Deep Work 3", "kind": "tasks"},
    {"key": "shutdown", "start": "14:15", "end": "14:24", "heading": "2:15–2:35 Shutdown", "kind": "shutdown"},
]


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
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/{method}", data=urllib.parse.urlencode(payload).encode("utf-8"))
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_time(s: str) -> time:
    h, m = [int(x) for x in s.split(":")]
    return time(h, m)


def current_window(now: datetime, force: str | None = None) -> dict | None:
    if force:
        return next((w for w in BLOCK_WINDOWS if w["key"] == force), None)
    if now.weekday() >= 5:
        return None
    t = now.time()
    for w in BLOCK_WINDOWS:
        if parse_time(w["start"]) <= t <= parse_time(w["end"]):
            return w
    return None


def ensure_plan(day: str) -> pathlib.Path:
    path = PLAN_DIR / f"{day}.md"
    # Regenerate at each card window so newly-added due tasks are pulled from
    # theduyvault and assigned to the next compatible block.
    if GENERATOR.exists():
        subprocess.run(
            [sys.executable, str(GENERATOR), "--date", day],
            check=False,
            timeout=60,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    return path


def section(text: str, heading: str) -> str:
    pat = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.M)
    m = pat.search(text)
    if not m:
        return ""
    start = m.end()
    n = re.search(r"^##\s+", text[start:], re.M)
    end = start + n.start() if n else len(text)
    return text[start:end].strip()


def top3(text: str) -> list[str]:
    sec = section(text, "Top 3")
    return [clean_task_line(l) for l in sec.splitlines() if l.strip().startswith("- [")][:3]


def clean_task_line(line: str) -> str:
    line = re.sub(r"^- \[[ xX]\]\s*", "", line.strip())
    line = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", line)
    line = re.sub(r"\[\[([^\]]+)\]\]", r"\1", line)
    line = re.sub(r"`[^`]*`", "", line)
    return re.sub(r"\s+", " ", line).strip()


def extract_task_refs(sec: str) -> list[dict]:
    refs: list[dict] = []
    for line in sec.splitlines():
        if not line.strip().startswith("- ["):
            continue
        m = re.search(r"\[\[([^\]|]+)\|([^\]]+)\]\]", line)
        if m:
            stem, title = m.group(1), m.group(2)
        else:
            title = clean_task_line(line)
            stem = ""
        path = pathlib.Path("/vault/Tasks/tasks") / f"{stem}.md" if stem else pathlib.Path("")
        refs.append({"title": title, "file_path": str(path) if stem and path.exists() else "", "raw": line})
    return refs


def load_json(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    except Exception:
        return {}


def save_json(path: pathlib.Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def send_block_reminder(token: str, chat_id: str, heading: str, refs: list[dict]) -> int | None:
    lines = [f"Block: {heading}"]
    if refs:
        lines += [""] + [f"☐ {ref['title']}" for ref in refs[:3]]
    else:
        lines += ["", "☐ Use this block for the planned work."]
    text = "\n".join(lines)
    res = post_telegram(token, "sendMessage", {"chat_id": chat_id, "text": text, "disable_web_page_preview": "true"})
    return res.get("result", {}).get("message_id")


def main() -> int:
    force = None
    if "--force" in sys.argv:
        i = sys.argv.index("--force")
        force = sys.argv[i + 1] if i + 1 < len(sys.argv) else "setup"
    for env in ENV_FILES:
        load_env_file(env)
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_HOME_CHANNEL") or config_home_channel() or "8446251233"
    if not token:
        print("TELEGRAM_BOT_TOKEN missing", file=sys.stderr)
        return 1
    now = datetime.now(TZ)
    win = current_window(now, force=force)
    if not win:
        return 0
    day = now.date().isoformat()
    plan_path = ensure_plan(day)
    if not plan_path.exists():
        return 0
    plan = plan_path.read_text(encoding="utf-8", errors="replace")
    preg = load_json(PLAN_REGISTRY)
    key = f"{day}:{win['key']}"
    if key in preg and not force:
        return 0

    sent_any = False
    if win["kind"] == "summary":
        items = top3(plan)
        text = "Today’s Plan\n" + "\n".join(f"{i+1}. {x}" for i, x in enumerate(items))
        text += "\n\nProtected: brunch 10:00–10:30; pickup transition 3:35–3:45."
        res = post_telegram(token, "sendMessage", {"chat_id": chat_id, "text": text})
        preg[key] = {"message_id": res.get("result", {}).get("message_id"), "sent_at": now.isoformat()}
        sent_any = True
    elif win["kind"] == "company":
        sec = section(plan, win["heading"])
        company = next((l.split(":",1)[1].strip() for l in sec.splitlines() if l.startswith("Company:")), "Company")
        text = f"Company Review — {company}\n11:45–12:15\n\n☐ Cash / revenue abnormal?\n☐ Staff / schedule issue?\n☐ Customer reviews / complaints?\n☐ Supplies / equipment / vendor / software?\n☐ Pick one follow-up action if needed."
        res = post_telegram(token, "sendMessage", {"chat_id": chat_id, "text": text})
        preg[key] = {"message_id": res.get("result", {}).get("message_id"), "sent_at": now.isoformat()}
        sent_any = True
    elif win["kind"] == "shutdown":
        text = "Shutdown — 3:35–3:45\n☐ Mark completed tasks Done\n☐ Move unfinished tasks\n☐ Capture next actions\n☐ Stop by 3:35 for pickup transition"
        res = post_telegram(token, "sendMessage", {"chat_id": chat_id, "text": text})
        preg[key] = {"message_id": res.get("result", {}).get("message_id"), "sent_at": now.isoformat()}
        sent_any = True
    else:
        refs = extract_task_refs(section(plan, win["heading"]))
        mid = send_block_reminder(token, chat_id, win["heading"], refs)
        if mid:
            preg[key] = {"message_id": mid, "sent_at": now.isoformat()}
            sent_any = True
    if sent_any:
        save_json(PLAN_REGISTRY, preg)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
