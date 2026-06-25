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
import unicodedata
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


def time_from_task(fm: dict[str, str], body: str) -> str:
    """Return a concise due/kickoff time for task cards when present."""
    for key in ("due_time", "time", "start_time", "kickoff"):
        val = (fm.get(key) or "").strip()
        if val:
            return val
    for line in body.splitlines():
        m = re.match(r"^(Kickoff|Start|Due|Time):\s*(.+?)\s*$", line.strip(), re.IGNORECASE)
        if m:
            return m.group(2).strip()
    return ""


def note_field_from_body(body: str, label: str) -> str:
    for line in body.splitlines():
        m = re.match(r"^" + re.escape(label) + r":\s*(.+?)\s*$", line.strip(), re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return ""


def normalize_team(name: str) -> str:
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9]+", " ", ascii_name.lower()).strip()
    aliases = {
        "korea republic": "south korea",
        "south korea": "south korea",
        "cote d ivoire": "ivory coast",
        "c te d ivoire": "ivory coast",
        "ivory coast": "ivory coast",
        "usa": "united states",
        "u s a": "united states",
        "usmnt": "united states",
        "congo dr": "dr congo",
        "dr congo": "dr congo",
    }
    return aliases.get(value, value)


def split_world_cup_title(title: str) -> tuple[str, str] | None:
    # World Cup tasks are usually `Follow World Cup: A vs B`, but a few
    # team-specific cards were created as `Follow Korea Republic: A vs B`.
    m = re.match(r"^Follow\s+(?:World\s+Cup|[^:]+):\s*(.+?)\s+vs\s+(.+?)\s*$", title.strip(), re.IGNORECASE)
    if not m:
        return None
    return m.group(1).strip(), m.group(2).strip()


def current_market_value(market: dict, key: str = "odds") -> str:
    for bucket in ("current", "close", "open"):
        val = (market.get(bucket) or {}).get(key)
        if val not in (None, ""):
            return str(val)
    return ""


def format_world_cup_odds(title: str, due_date: str, body: str = "") -> str:
    """Fetch pre-game odds from ESPN/DraftKings for World Cup follow cards.

    Falls back to an `Odds:` line in the task note when ESPN has no market.
    For World Cup cards, return an explicit unavailable message instead of
    silently omitting odds, so every game card has an Odds line.
    """
    manual = note_field_from_body(body, "Odds")
    unavailable = "No listed ESPN/DraftKings market yet"
    teams = split_world_cup_title(title)
    if not teams or not due_date:
        return manual
    wanted = {normalize_team(teams[0]), normalize_team(teams[1])}
    try:
        base = date.fromisoformat(due_date[:10])
    except ValueError:
        return manual or unavailable
    candidates = [base, base + timedelta(days=1), base - timedelta(days=1)]
    try:
        for day in candidates:
            url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard?dates={day.strftime('%Y%m%d')}"
            data = json.loads(urllib.request.urlopen(url, timeout=12).read().decode("utf-8"))
            for event in data.get("events", []):
                comp = (event.get("competitions") or [{}])[0]
                competitors = comp.get("competitors") or []
                event_names = {normalize_team((c.get("team") or {}).get("displayName", "")) for c in competitors}
                if not wanted.issubset(event_names):
                    continue
                odds_list = comp.get("odds") or []
                odds = next((o for o in odds_list if isinstance(o, dict)), None)
                if not odds:
                    return manual or unavailable
                sides: dict[str, str] = {}
                for c in competitors:
                    team = c.get("team") or {}
                    sides[c.get("homeAway", "")] = team.get("shortDisplayName") or team.get("displayName") or ""
                ml = odds.get("moneyline") or {}
                spread = odds.get("pointSpread") or {}
                total = odds.get("total") or {}
                home = sides.get("home", "Home")
                away = sides.get("away", "Away")
                ml_home = current_market_value(ml.get("home") or {})
                ml_away = current_market_value(ml.get("away") or {})
                ml_draw = current_market_value(ml.get("draw") or {}) or str((odds.get("drawOdds") or {}).get("moneyLine") or "")
                sp_home_line = current_market_value(spread.get("home") or {}, "line")
                sp_home_odds = current_market_value(spread.get("home") or {})
                sp_away_line = current_market_value(spread.get("away") or {}, "line")
                sp_away_odds = current_market_value(spread.get("away") or {})
                over_line = current_market_value(total.get("over") or {}, "line")
                over_odds = current_market_value(total.get("over") or {})
                under_line = current_market_value(total.get("under") or {}, "line")
                under_odds = current_market_value(total.get("under") or {})
                provider = ((odds.get("provider") or {}).get("displayName") or (odds.get("provider") or {}).get("name") or "ESPN odds")
                parts = []
                if ml_home or ml_draw or ml_away:
                    parts.append(f"ML {home} {ml_home or 'n/a'} / Draw {ml_draw or 'n/a'} / {away} {ml_away or 'n/a'}")
                if sp_home_line or sp_away_line:
                    parts.append(f"Spread {home} {sp_home_line or 'n/a'} ({sp_home_odds or 'n/a'}) / {away} {sp_away_line or 'n/a'} ({sp_away_odds or 'n/a'})")
                if over_line or under_line:
                    parts.append(f"O/U {over_line or 'O n/a'} ({over_odds or 'n/a'}) / {under_line or 'U n/a'} ({under_odds or 'n/a'})")
                if parts:
                    return f"{provider}: " + "; ".join(parts)
                return manual or unavailable
    except Exception:
        return manual or unavailable
    return manual or unavailable


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
        due_time = time_from_task(fm, body)
        tasks.append({
            "title": title,
            "source": "Obsidian" if due == today else f"Obsidian overdue {due.isoformat()}",
            "file_path": str(path),
            "due_date": due.isoformat(),
            "due_time": due_time,
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

    # Re-drip unfinished cards daily until Duy taps Done.
    # A sent-but-not-done card should be suppressed only for the current day;
    # tomorrow it becomes eligible again. A done card remains suppressed.
    handled_by_file: dict[str, list[dict]] = {}
    for entry in registry.values():
        if isinstance(entry, dict):
            fp = str(entry.get("file_path") or "").strip()
            if fp:
                handled_by_file.setdefault(fp, []).append(entry)

    for idx, task in enumerate(tasks, 1):
        title = str(task.get("title") or task.get("text") or "").strip()
        if not title:
            continue
        source = str(task.get("source") or "").strip()
        file_path = str(task.get("file_path") or "").strip()
        due_date = str(task.get("due_date") or "").strip()
        due_time = str(task.get("due_time") or "").strip()
        odds = str(task.get("odds") or "").strip()
        prior_entries = handled_by_file.get(file_path, [])
        if any(e.get("status") == "done" for e in prior_entries):
            continue
        if any(
            e.get("status") == "sent"
            and (not e.get("due_date") or e.get("due_date") == due_date)
            and e.get("date") == date_key
            for e in prior_entries
        ):
            continue
        digest = hashlib.sha1(f"{title}\n{file_path}\n{due_date}".encode("utf-8")).hexdigest()[:16]
        existing = registry.get(digest, {})
        if existing.get("message_id") and existing.get("status") != "done" and existing.get("date") == date_key:
            continue
        if existing.get("status") == "done":
            continue
        if not odds and due_date and split_world_cup_title(title):
            body = ""
            try:
                if file_path:
                    body = pathlib.Path(file_path).read_text(encoding="utf-8", errors="replace")
            except Exception:
                body = ""
            odds = format_world_cup_odds(title, due_date, body)

        text = f"☐ {title}"
        if due_time:
            text += f"\nTime: {due_time}"
        if odds:
            text += f"\nOdds: {odds}"
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
            "due_date": due_date,
            "title": title,
            "text": title,
            "source": source,
            "file_path": file_path,
            "status": "sent",
            "message_id": message_id,
            "odds": odds,
        }
        sent += 1
        if sent >= send_limit:
            break

    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    # Keep stdout empty on success so no_agent cron stays silent.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
