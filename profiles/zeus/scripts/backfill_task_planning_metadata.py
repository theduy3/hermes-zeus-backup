#!/usr/bin/env python3
"""Backfill lightweight planning metadata into active theduyvault tasks."""
from __future__ import annotations

import re
from pathlib import Path

TASK_DIR = Path("/vault/Tasks/tasks")
FIELDS = ["time_block", "estimated_minutes", "energy", "priority", "company"]


def parse(text: str):
    if not text.startswith("---"):
        return {}, "", text
    parts = text.split("---", 2)
    fm = {}
    for line in parts[1].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, parts[1], parts[2]


def title(path: Path, body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("-", " ").title()


def infer_company(t: str, tags: str, name: str) -> str:
    s = f"{t} {tags} {name}".lower()
    if any(x in s for x in ["salonx", "salon360", "fluentcrm", "chatbot", "survey", "photos", "clients page", "clover"]): return "salonx"
    if any(x in s for x in ["sans souci", " ss ", "-ss", " ss-", "safe balance", "skip", "square", "ticketmaster"]): return "ss"
    if any(x in s for x in ["rivieres", "rivières", "3r", "le 3r"]): return "rivieres"
    if any(x in s for x in ["maily", "jessica"]): return "maily"
    if "charlesbourg" in s: return "charlesbourg"
    if any(x in s for x in ["victoria", "daycare", "sea star", "family", "baby"]): return "family"
    if any(x in s for x in ["cibc", "td ", "rbc", "bmo", "amex", "loan", "tax", "bank", "payment", "portfolio", "stock"]): return "finance"
    return "personal"


def infer_meta(t: str, tags: str, company: str):
    s = f"{t} {tags}".lower()
    if any(x in s for x in ["call", "phone"]): return "calls", "15", "low", "normal"
    if any(x in s for x in ["pay ", "payment", "bank", "cibc", "td ", "rbc", "bmo", "amex", "loan", "tax", "reimbursement", "square"]): return "finance", "20", "low", "high"
    if any(x in s for x in ["fix", "build", "create", "form", "website", "chatbot", "workflow", "photos", "clients page", "software", "menu"]): return "deep_work", "60", "high", "high"
    if any(x in s for x in ["review", "learning", "portfolio", "stock"]): return "review", "30", "medium", "normal"
    if any(x in s for x in ["daycare", "victoria", "doctor", "consultation", "flight", "arrive", "attend"]): return "family", "30", "medium", "high"
    if company in {"maily", "ss", "rivieres", "charlesbourg", "salonx"}: return "admin_batch", "30", "medium", "normal"
    return "admin_batch", "30", "medium", "normal"


def main() -> int:
    changed = 0
    for path in sorted(TASK_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        fm, raw, body = parse(text)
        if not raw or (fm.get("type") or "task").lower() != "task":
            continue
        status = (fm.get("status") or "pending").lower()
        if status in {"completed", "done", "cancelled", "canceled"}:
            continue
        ttl = title(path, body)
        tags = fm.get("tags", "")
        company = fm.get("company") or infer_company(ttl, tags, path.name)
        tb, est, energy, priority = infer_meta(ttl, tags, company)
        additions = {
            "time_block": fm.get("time_block") or tb,
            "estimated_minutes": fm.get("estimated_minutes") or est,
            "energy": fm.get("energy") or energy,
            "priority": fm.get("priority") or priority,
            "company": fm.get("company") or company,
        }
        missing = [(k, v) for k, v in additions.items() if k not in fm]
        if not missing:
            continue
        # Insert planning fields after status line when possible, else before frontmatter end.
        lines = raw.rstrip().splitlines()
        insert_at = len(lines)
        for i, line in enumerate(lines):
            if line.startswith("status:"):
                insert_at = i + 1
                break
        for k, v in reversed(missing):
            lines.insert(insert_at, f"{k}: {v}")
        new = "---\n" + "\n".join(lines) + "\n---" + body
        path.write_text(new, encoding="utf-8")
        changed += 1
        print(f"updated {path.name}: " + ", ".join(k for k, _ in missing))
    print(f"metadata backfill complete: {changed} file(s) updated")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
