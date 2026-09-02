#!/usr/bin/env python3
import re
import sys
from pathlib import Path

# Avoid polluted sitecustomize / broken inspect if present
sys.path = [p for p in sys.path if "generation-" not in p and ".hermes-runtime" not in p]

TASK_DIR = Path("/vault/Tasks/tasks")


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm = {}
    for line in parts[1].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, parts[2]


def title_from(path, body):
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("-", " ").title()


def infer_company(title, tags, path):
    s = f"{title} {tags} {path.name}".lower()
    if any(x in s for x in ["salonx", "salon360", "fluentcrm", "chatbot", "survey", "photos", "clients page"]):
        return "salonx"
    if any(x in s for x in ["sans souci", " ss ", "-ss", " ss-", "safe balance", "skip", "square", "ticketmaster"]):
        return "ss"
    if any(x in s for x in ["rivieres", "rivières", "3r", "le 3r"]):
        return "rivieres"
    if any(x in s for x in ["maily", "jessica"]):
        return "maily"
    if "charlesbourg" in s:
        return "charlesbourg"
    if any(x in s for x in ["victoria", "daycare", "sea star", "family", "baby"]):
        return "family"
    if any(x in s for x in ["cibc", "td ", "rbc", "bmo", "amex", "loan", "tax", "bank", "payment", "portfolio", "stock"]):
        return "finance"
    return "personal"


def infer_time_block(title, tags, company):
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


def has_specific_time(fm, body):
    if any((fm.get(k) or "").strip() for k in ["due_time", "time", "start_time", "kickoff"]):
        return True
    return bool(
        re.search(r"(?im)^\s*(kickoff|start|due|time|date/time)\s*:", body)
        or re.search(r"(?im)^\s*- \*\*time:\*\*", body)
    )


tasks = []
for path in sorted(TASK_DIR.glob("*.md")):
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        continue
    fm, body = parse_frontmatter(text)
    kind = (fm.get("type") or "task").lower()
    if kind not in {"task", "event"}:
        continue
    status = (fm.get("status") or "pending").lower()
    if status in {"completed", "done", "cancelled", "canceled"}:
        continue
    due_txt = (fm.get("due_date") or "").strip()[:10]
    title = title_from(path, body)
    tags = fm.get("tags", "")
    company = fm.get("company") or infer_company(title, tags, path)
    tb, est, energy, priority = infer_time_block(title, tags, company)
    priority = fm.get("priority") or priority
    time_block = fm.get("time_block") or tb
    estm = int(fm.get("estimated_minutes") or est)
    energy = fm.get("energy") or energy
    specific = has_specific_time(fm, body) or kind == "event"
    tasks.append(
        {
            "title": title,
            "due": due_txt,
            "status": status,
            "tags": tags,
            "time_block": time_block,
            "estimated_minutes": estm,
            "energy": energy,
            "priority": priority,
            "company": company,
            "kind": kind,
            "specific_time": specific,
            "file": path.name,
        }
    )

pmap = {"urgent": 0, "high": 1, "normal": 2, "low": 3}
no_date = [t for t in tasks if t["kind"] == "task" and not t["due"] and not t["specific_time"]]
no_date.sort(key=lambda t: (pmap.get(t["priority"], 2), -t["estimated_minutes"], t["title"].lower()))
print(f"count={len(no_date)}")
for i, t in enumerate(no_date, 1):
    print(
        f"{i}|{t['priority']}|{t['company']}|{t['time_block']}|{t['estimated_minutes']}m|{t['title']}|{t['file']}|{t['tags']}"
    )
spec = [t for t in tasks if t["kind"] == "task" and not t["due"] and t["specific_time"]]
print(f"SPEC_COUNT={len(spec)}")
for t in spec:
    print(f"SPEC|{t['title']}|{t['file']}")
