#!/usr/bin/env python3
"""Assign due_date=today to all no-date pending triage tasks."""
import re
from pathlib import Path

TASK_DIR = Path("/vault/Tasks/tasks")
TODAY = "2026-08-31"

DONE = {"completed", "done", "cancelled", "canceled"}


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None, None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, None, text
    return parts[1], parts[2], text


def has_specific_time(fm_raw: str, body: str) -> bool:
    fm = {}
    for line in fm_raw.splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    if any((fm.get(k) or "").strip() for k in ["due_time", "time", "start_time", "kickoff"]):
        return True
    return bool(
        re.search(r"(?im)^\s*(kickoff|start|due|time|date/time)\s*:", body)
        or re.search(r"(?im)^\s*- \*\*time:\*\*", body)
    )


def fm_dict(fm_raw: str) -> dict:
    fm = {}
    for line in fm_raw.splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def title_from(path: Path, body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


updated = []
skipped = []

for path in sorted(TASK_DIR.glob("*.md")):
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        skipped.append((path.name, f"read error: {e}"))
        continue

    fm_raw, body, _ = parse_frontmatter(text)
    if fm_raw is None:
        skipped.append((path.name, "no frontmatter"))
        continue

    fm = fm_dict(fm_raw)
    kind = (fm.get("type") or "task").lower()
    if kind != "task":
        continue
    status = (fm.get("status") or "pending").lower()
    if status in DONE:
        continue
    due = (fm.get("due_date") or "").strip()
    if due:
        continue
    if has_specific_time(fm_raw, body or ""):
        skipped.append((path.name, "specific time undated — left alone"))
        continue

    # Insert due_date after type: line if present, else after opening ---
    lines = fm_raw.splitlines(keepends=True)
    # Normalize: ensure we write due_date cleanly
    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line)
        if not inserted and re.match(r"^type\s*:", line):
            new_lines.append(f"due_date: {TODAY}\n")
            inserted = True
    if not inserted:
        # put near top after first blank-stripped content
        new_lines = [f"due_date: {TODAY}\n"] + lines

    new_text = "---" + "".join(new_lines)
    if not new_text.endswith("\n") and not (body or "").startswith("\n"):
        new_text += "\n"
    # reconstruct: --- + fm + --- + body
    # fm_raw may or may not have leading newline after ---
    if not fm_raw.startswith("\n"):
        fm_block = "\n" + "".join(new_lines)
    else:
        fm_block = "".join(new_lines)
        if not fm_block.startswith("\n"):
            fm_block = "\n" + fm_block

    # Rebuild carefully from original structure
    # Original: --- \n fm \n --- \n body
    orig_parts = text.split("---", 2)
    # orig_parts[0] is '' , [1] is fm_raw, [2] is body
    new_fm = fm_raw
    if re.search(r"(?m)^due_date\s*:", new_fm):
        skipped.append((path.name, "already has due_date after recheck"))
        continue

    if re.search(r"(?m)^type\s*:", new_fm):
        new_fm = re.sub(r"(?m)^(type\s*:.*)$", rf"\1\ndue_date: {TODAY}", new_fm, count=1)
    else:
        # prepend after leading newline
        if new_fm.startswith("\n"):
            new_fm = "\n" + f"due_date: {TODAY}\n" + new_fm.lstrip("\n")
        else:
            new_fm = f"\ndue_date: {TODAY}\n" + new_fm

    new_content = f"---{new_fm}---{orig_parts[2]}"
    path.write_text(new_content, encoding="utf-8")
    title = title_from(path, orig_parts[2])
    updated.append((path.name, title))

print(f"UPDATED={len(updated)}")
for name, title in updated:
    print(f"OK|{name}|{title}")
print(f"SKIPPED={len(skipped)}")
for name, reason in skipped:
    print(f"SKIP|{name}|{reason}")

# verify
still = 0
for path in sorted(TASK_DIR.glob("*.md")):
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        continue
    parts = text.split("---", 2)
    if len(parts) < 3:
        continue
    fm = fm_dict(parts[1])
    kind = (fm.get("type") or "task").lower()
    status = (fm.get("status") or "pending").lower()
    if kind != "task" or status in DONE:
        continue
    due = (fm.get("due_date") or "").strip()
    if not due and not has_specific_time(parts[1], parts[2]):
        still += 1
        print(f"STILL_NODATE|{path.name}")
print(f"REMAINING_NODATE={still}")
