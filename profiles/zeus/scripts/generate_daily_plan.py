#!/usr/bin/env python3
"""Generate Duy's time-blocked daily plan from theduyvault tasks.

Writes /vault/Tasks/planning/YYYY-MM-DD.md using the approved schedule:
- no work before 9AM
- brunch 10:00-10:30
- pickup transition 3:35-3:45, Victoria/family after 3:45
- rotating company review: SalonX Mon, SS Tue, Rivieres Wed, Maily Thu, Charlesbourg Fri
- weekends: no company review; use Investment Portfolio Review instead
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Vancouver")
TASK_DIR = Path("/vault/Tasks/tasks")
PLAN_DIR = Path("/vault/Tasks/planning")

COMPANY_BY_WEEKDAY = {
    0: ("SalonX", "salonx"),
    1: ("Sans Souci / SS", "ss"),
    2: ("Ongles Rivieres", "rivieres"),
    3: ("Ongles Maily", "maily"),
    4: ("Ongles Charlesbourg", "charlesbourg"),
}

# Time blocks are no longer hardcoded; generate_plan() emits a lightweight skeleton.

@dataclass
class Task:
    path: Path
    title: str
    due: str = ""
    status: str = "pending"
    tags: str = ""
    time_block: str = ""
    estimated_minutes: int = 30
    energy: str = "medium"
    priority: str = "normal"
    company: str = ""
    body: str = ""
    kind: str = "task"
    specific_time: bool = False
    sort_due: date = field(default_factory=lambda: date.max)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, str]:
    if not text.startswith("---"):
        return {}, "", text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, "", text
    raw = parts[1]
    fm: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, raw, parts[2]


def title_from(path: Path, body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("-", " ").title()


def infer_company(title: str, tags: str, path: Path) -> str:
    s = f"{title} {tags} {path.name}".lower()
    if any(x in s for x in ["salonx", "salon360", "fluentcrm", "chatbot", "survey", "photos", "clients page"]):
        return "salonx"
    if any(x in s for x in ["sans souci", " ss ", "-ss", " ss-", "safe balance", "skip", "square", "ticketmaster"]):
        return "ss"
    if any(x in s for x in ["rivieres", "rivières", "3r", "le 3r"]):
        return "rivieres"
    if any(x in s for x in ["maily", "jessica"]):
        return "maily"
    if any(x in s for x in ["charlesbourg"]):
        return "charlesbourg"
    if any(x in s for x in ["victoria", "daycare", "sea star", "family", "baby"]):
        return "family"
    if any(x in s for x in ["cibc", "td ", "rbc", "bmo", "amex", "loan", "tax", "bank", "payment", "portfolio", "stock"]):
        return "finance"
    return "personal"


def infer_time_block(title: str, tags: str, company: str) -> tuple[str, int, str, str]:
    s = f"{title} {tags}".lower()
    if any(x in s for x in ["call", "phone"]):
        return "calls", 15, "low", "normal"
    if any(x in s for x in ["pay ", "payment", "bank", "cibc", "td ", "rbc", "bmo", "amex", "loan", "tax", "reimbursement", "square"]):
        return "finance", 20, "low", "high"
    if any(x in s for x in ["fix", "build", "create", "form", "website", "chatbot", "workflow", "photos", "clients page", "software", "menu"]):
        return "deep_work", 60, "high", "high"
    if any(x in s for x in ["review", "learning", "portfolio", "stock"]):
        return "review", 30, "medium", "normal"
    if company in {"maily", "ss", "rivieres", "charlesbourg", "salonx"}:
        return "admin_batch", 30, "medium", "normal"
    if any(x in s for x in ["daycare", "victoria", "doctor", "consultation", "flight", "arrive", "attend"]):
        return "family", 30, "medium", "high"
    return "admin_batch", 30, "medium", "normal"


def has_specific_time(fm: dict[str, str], body: str) -> bool:
    if any((fm.get(k) or "").strip() for k in ["due_time", "time", "start_time", "kickoff"]):
        return True
    return bool(re.search(r"(?im)^\s*(kickoff|start|due|time|date/time)\s*:", body) or re.search(r"(?im)^\s*- \*\*time:\*\*", body))


def load_tasks(today: date, horizon: int = 14) -> list[Task]:
    tasks: list[Task] = []
    if not TASK_DIR.exists():
        return tasks
    end = today + timedelta(days=horizon)
    for path in sorted(TASK_DIR.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"WARN: skipping unreadable task {path}: {exc}")
            continue
        fm, _, body = parse_frontmatter(text)
        kind = (fm.get("type") or "task").lower()
        if kind not in {"task", "event"}:
            continue
        status = (fm.get("status") or "pending").lower()
        if status in {"completed", "done", "cancelled", "canceled"}:
            continue
        due_txt = (fm.get("due_date") or "").strip()[:10]
        sort_due = date.max
        include = False
        if due_txt:
            try:
                sort_due = date.fromisoformat(due_txt)
                include = sort_due <= end
            except ValueError:
                include = False
        else:
            # Include no-date tasks only for triage, not hard scheduling.
            include = True
        if not include:
            continue
        title = title_from(path, body)
        tags = fm.get("tags", "")
        company = fm.get("company") or infer_company(title, tags, path)
        tb, est, energy, priority = infer_time_block(title, tags, company)
        tasks.append(Task(
            path=path,
            title=title,
            due=due_txt,
            status=status,
            tags=tags,
            time_block=fm.get("time_block") or tb,
            estimated_minutes=int(fm.get("estimated_minutes") or est),
            energy=fm.get("energy") or energy,
            priority=fm.get("priority") or priority,
            company=company,
            body=body,
            kind=kind,
            specific_time=has_specific_time(fm, body) or kind == "event",
            sort_due=sort_due,
        ))
    return tasks


def priority_key(t: Task) -> tuple:
    pmap = {"urgent": 0, "high": 1, "normal": 2, "low": 3}
    overdue = 0 if t.sort_due < date.today() else 1
    return (pmap.get(t.priority, 2), overdue, t.sort_due, -t.estimated_minutes, t.title.lower())


def pick(tasks: list[Task], predicate, minutes: int, used: set[Path], max_items: int = 3) -> list[Task]:
    picked: list[Task] = []
    remaining = minutes
    for t in sorted([x for x in tasks if x.path not in used and predicate(x)], key=priority_key):
        if len(picked) >= max_items:
            break
        if t.estimated_minutes <= remaining or not picked:
            picked.append(t)
            used.add(t.path)
            remaining -= min(t.estimated_minutes, remaining)
    return picked


def review_for_day(d: date) -> tuple[str, str, str]:
    if d.weekday() >= 5:
        return "Investment Portfolio Review", "finance", "investment"
    company_name, company_slug = COMPANY_BY_WEEKDAY[d.weekday()]
    return "Company Review", company_name, company_slug


def sea_star_closed(tasks: list[Task], day: date) -> bool:
    """A Sea Star closure means Victoria stays home; there is no pickup handoff."""
    return any(
        t.sort_due == day
        and "sea star" in t.title.lower()
        and "daycare closed" in t.title.lower()
        for t in tasks
    )


def md_task(t: Task) -> str:
    due = f" due {t.due}" if t.due else " no date"
    meta = f"`{t.time_block}` `{t.company}` {t.estimated_minutes}m"
    return f"- [ ] [[{t.path.stem}|{t.title}]] ({due}) {meta}"


def generate_plan(day: date, write: bool = True) -> str:
    tasks = load_tasks(day)
    review_label, review_target, review_slug = review_for_day(day)
    daycare_closed = sea_star_closed(tasks, day)
    used: set[Path] = set()

    review_related = [t for t in tasks if t.company == review_slug and not t.specific_time]
    timed_today = [t for t in sorted(tasks, key=priority_key) if (t.specific_time or t.kind == "event") and t.sort_due == day]
    today_tasks = [t for t in sorted(tasks, key=priority_key) if t.kind == "task" and t.due and t.sort_due == day and not t.specific_time]
    # Schedule reminders should not pull overdue tasks; Duy moves overdue items himself while planning.
    schedulable = lambda t: t.kind == "task" and bool(t.due) and not t.specific_time and t.sort_due >= day
    top3 = pick(today_tasks or tasks, lambda t: schedulable(t) and t.priority in {"urgent", "high", "normal"} and t.time_block != "family", 180, used, 3)
    p1 = pick(tasks, lambda t: schedulable(t) and t.time_block == "deep_work" and t.energy == "high", 25, used, 1)
    p2 = pick(tasks, lambda t: schedulable(t) and t.time_block == "deep_work", 25, used, 1)
    p3 = pick(tasks, lambda t: schedulable(t) and t.time_block == "deep_work", 25, used, 1)
    p4 = pick(tasks, lambda t: schedulable(t) and t.time_block == "deep_work", 25, used, 1)
    p5 = pick(tasks, lambda t: schedulable(t) and t.time_block in {"admin_batch", "calls", "finance"}, 25, used, 2)
    p6 = pick(tasks, lambda t: schedulable(t) and t.time_block in {"deep_work", "review"}, 25, used, 1)
    p7 = pick(tasks, lambda t: schedulable(t) and t.time_block in {"deep_work", "review"}, 25, used, 1)
    no_date = [t for t in sorted(tasks, key=priority_key) if t.kind == "task" and not t.due and not t.specific_time][:5]
    next7 = [t for t in sorted(tasks, key=priority_key) if t.kind == "task" and t.due and day < t.sort_due <= day + timedelta(days=7) and t.path not in used][:8]

    lines = [
        "---",
        "type: daily-plan",
        f"date: {day.isoformat()}",
        "status: planned",
        "---",
        f"# Daily Plan — {day.isoformat()}",
        "",
        "## Constraints",
        "- Before 9:00 AM — family / baby; no work task cards.",
        "- 10:00–10:30 AM — brunch; protected.",
    ]
    if day.weekday() >= 5:
        lines += [
            "- Weekend is family-first; no work schedule blocks.",
            "- Specific-time events/tasks stay fixed.",
            "- 3:45 PM onward — Victoria / family; only urgent fixed reminders.",
        ]
    else:
        lines += [
            "- No fixed deep-work / Pomodoro blocks; work flexibly between 10:30 AM and 3:35 PM.",
            "- Specific-time events/tasks stay fixed.",
            "- 3:35–3:45 PM — pickup transition; stop work.",
            "- 3:45 PM onward — Victoria / family; only urgent fixed reminders.",
        ]
    lines += ["", "## Fixed"]
    # Victoria pickup is a weekday handoff, except when Sea Star is closed and
    # Victoria stays home. Weekends also do not invent a pickup appointment.
    if day.weekday() < 5 and not daycare_closed:
        lines += ["- 3:45 PM — Pick up Victoria / family transition"]
    lines += [md_task(t) for t in timed_today] if timed_today else []
    lines += ["", "## Today Tasks"]
    lines += [md_task(t) for t in today_tasks] or ["- None"]
    lines += ["", "## Top 3"]
    lines += [md_task(t) for t in top3] or ["- [ ] Pick from Today Tasks"]

    if day.weekday() >= 5:
        lines += [f"", f"## 11:45–12:15 {review_label}", f"Focus: {review_target}", "", "Checklist:"]
        lines += ["- [ ] Review portfolio allocation / concentration", "- [ ] Check watchlist and earnings dates", "- [ ] Review macro / rates / market notes", "- [ ] Note any cash needs or rebalance candidates", "- [ ] Pick one follow-up action if needed."]
        if review_related:
            lines += ["", "Related tasks:"] + [md_task(t) for t in review_related[:5]]
        lines += ["", "## Weekend Notes", "- No work schedule blocks on weekends.", "- Keep family-first; handle only fixed or truly important items."]
        lines += ["", "## Tomorrow / Next 7 Days"] + ([md_task(t) for t in next7] or ["- None"])
        lines += ["", "## No-Date Triage — max 5"] + ([md_task(t) for t in no_date] or ["- None"])
        content = "\n".join(lines) + "\n"
        if write:
            PLAN_DIR.mkdir(parents=True, exist_ok=True)
            (PLAN_DIR / f"{day.isoformat()}.md").write_text(content, encoding="utf-8")
        return content

    lines += ["", "## 9:00–10:00 Exercise", "Morning block — after dropping Victoria at daycare.", ""]
    lines += ["## 10:00–10:30 Brunch", "Protected.", ""]
    lines += [f"## 11:45–12:15 {review_label}", f"Focus: {review_target}", "", "Checklist:"]
    if review_label == "Investment Portfolio Review":
        lines += ["- [ ] Review portfolio allocation / concentration", "- [ ] Check watchlist and earnings dates", "- [ ] Review macro / rates / market notes", "- [ ] Note any cash needs or rebalance candidates", "- [ ] Pick one follow-up action if needed."]
    else:
        lines += ["- [ ] Cash / revenue abnormal?", "- [ ] Staff / schedule issue?", "- [ ] Customer reviews / complaints?", "- [ ] Supplies / equipment / vendor / software?", "- [ ] Pick one follow-up action if needed."]
    if review_related:
        lines += ["", "Related tasks:"] + [md_task(t) for t in review_related[:5]]
    if not daycare_closed:
        lines += ["", "## 3:35–3:45 Pickup Transition", "- [ ] Stop work; prepare to pick up Victoria", ""]
        lines += ["## 3:45 PM — Pick up Victoria / family transition"]
    lines += ["## Tomorrow / Next 7 Days"] + ([md_task(t) for t in next7] or ["- None"])
    lines += ["", "## No-Date Triage — max 5"] + ([md_task(t) for t in no_date] or ["- None"])
    content = "\n".join(lines) + "\n"
    if write:
        PLAN_DIR.mkdir(parents=True, exist_ok=True)
        (PLAN_DIR / f"{day.isoformat()}.md").write_text(content, encoding="utf-8")
    return content


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD; default today in America/Vancouver")
    ap.add_argument("--tomorrow", action="store_true")
    ap.add_argument("--print", action="store_true")
    args = ap.parse_args()
    day = datetime.now(TZ).date()
    if args.tomorrow:
        day += timedelta(days=1)
    if args.date:
        day = date.fromisoformat(args.date)
    content = generate_plan(day, write=True)
    if args.print:
        print(content)
    else:
        print(f"wrote /vault/Tasks/planning/{day.isoformat()}.md")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
