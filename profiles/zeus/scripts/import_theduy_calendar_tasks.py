#!/usr/bin/env python3
"""Import explicitly-prefixed theduy Google Calendar events into Obsidian tasks.

Rule: Only events from `theduy calendar` whose summary starts with `Task:` or
`TODO:` become Obsidian tasks. Normal appointments stay calendar-only.

The importer:
- reads Google Calendar `duynt1989@gmail.com` by default;
- ignores events managed by Zeus's Obsidian->calendar mirror;
- ignores #catthew/catthew events;
- creates/updates `/vault/Tasks/tasks/*.md` with Google event metadata;
- marks imported Google events with private extendedProperties so re-runs are
  idempotent.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

PROFILE = Path("/home/hermes/.hermes/profiles/zeus")
TASK_DIR = Path("/vault/Tasks/tasks")
TOKEN_PATH = PROFILE / "google_token.json"
ENV_PATH = PROFILE / ".env"
DEFAULT_CALENDAR_ID = "duynt1989@gmail.com"
TZ = ZoneInfo("America/Vancouver")
IMPORTER = "zeus-calendar-task-import"
OBSIDIAN_MIRROR = "zeus-obsidian-task-sync"
PREFIX_RE = re.compile(r"^\s*(task|todo)\s*:\s*(.+)$", re.I)


def load_env_defaults() -> None:
    if not ENV_PATH.exists():
        return
    for raw in ENV_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def credentials() -> Credentials:
    if not TOKEN_PATH.exists():
        raise SystemExit(f"Missing Google token: {TOKEN_PATH}")
    payload = json.loads(TOKEN_PATH.read_text(encoding="utf-8"))
    scopes = payload.get("scopes") or payload.get("scope") or ["https://www.googleapis.com/auth/calendar"]
    if isinstance(scopes, str):
        scopes = scopes.split()
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), scopes)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        normalized = json.loads(creds.to_json())
        normalized.setdefault("type", "authorized_user")
        normalized["scopes"] = scopes
        TOKEN_PATH.write_text(json.dumps(normalized, indent=2), encoding="utf-8")
    if not creds.valid:
        raise SystemExit("Google token invalid")
    return creds


def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80] or "calendar-task"


def yaml_quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def parse_date_from_event(event: dict) -> tuple[str, str | None]:
    start = event.get("start") or {}
    if start.get("date"):
        return start["date"], None
    dt = start.get("dateTime")
    if not dt:
        return datetime.now(TZ).date().isoformat(), None
    parsed = datetime.fromisoformat(dt.replace("Z", "+00:00")).astimezone(TZ)
    return parsed.date().isoformat(), parsed.strftime("%H:%M %Z")


def parse_tags(text: str) -> list[str]:
    tags = []
    for raw in re.findall(r"#([A-Za-z0-9_-]+)", text or ""):
        tag = raw.lower()
        if tag not in tags:
            tags.append(tag)
    return tags


def has_catthew(summary: str, description: str) -> bool:
    hay = f"{summary}\n{description}".lower()
    return "#catthew" in hay or "catthew" in hay


def existing_task_for_event(event_id: str) -> Path | None:
    needle = f"google_event_id: {event_id}"
    for path in TASK_DIR.glob("*.md"):
        try:
            if needle in path.read_text(encoding="utf-8", errors="ignore"):
                return path
        except OSError:
            continue
    return None


def unique_path(title: str, event_id: str) -> Path:
    base = slugify(title)
    path = TASK_DIR / f"{base}.md"
    if not path.exists():
        return path
    existing = existing_task_for_event(event_id)
    if existing:
        return existing
    short = re.sub(r"[^a-z0-9]", "", event_id.lower())[:8]
    return TASK_DIR / f"{base}-{short}.md"


def build_task(path: Path, title: str, due_date: str, due_time: str | None, tags: list[str], event: dict) -> str:
    tags = [t for t in tags if t and t != "catthew"]
    if "calendar" not in tags:
        tags.append("calendar")
    body_desc = (event.get("description") or "").strip()
    html = event.get("htmlLink", "")
    event_id = event.get("id", "")
    lines = [
        "---",
        "type: task",
        f"due_date: {due_date}",
    ]
    if due_time:
        lines.append(f"due_time: {yaml_quote(due_time)}")
    lines += [
        f"tags: [{', '.join(tags)}]",
        "status: pending",
        "time_block: admin_batch",
        "estimated_minutes: 30",
        "energy: medium",
        "priority: normal",
        "company: personal",
        f"google_calendar_id: {DEFAULT_CALENDAR_ID}",
        f"google_event_id: {event_id}",
        f"calendar_imported_by: {IMPORTER}",
        "---",
        "",
        f"# {title}",
        "",
        f"Imported from Google Calendar event: {event_id}",
    ]
    if html:
        lines.append(f"Calendar: {html}")
    if due_time:
        lines.append(f"Time: {due_date} {due_time}")
    if body_desc:
        lines += ["", "## Calendar notes", "", body_desc]
    lines.append("")
    return "\n".join(lines)


@dataclass
class ImportCandidate:
    event: dict
    title: str
    due_date: str
    due_time: str | None
    tags: list[str]
    path: Path


def list_events(service, calendar_id: str, days_back: int, days_forward: int) -> list[dict]:
    today = datetime.now(TZ).date()
    time_min = datetime.combine(today - timedelta(days=days_back), datetime.min.time(), tzinfo=TZ).isoformat()
    time_max = datetime.combine(today + timedelta(days=days_forward), datetime.max.time(), tzinfo=TZ).isoformat()
    events = []
    page_token = None
    while True:
        resp = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            maxResults=2500,
            orderBy="startTime",
            pageToken=page_token,
        ).execute()
        events.extend(resp.get("items", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return events


def candidates(events: list[dict]) -> list[ImportCandidate]:
    out = []
    for event in events:
        if event.get("status") == "cancelled":
            continue
        priv = ((event.get("extendedProperties") or {}).get("private") or {})
        if priv.get("managed_by") == OBSIDIAN_MIRROR:
            continue
        summary = event.get("summary") or ""
        m = PREFIX_RE.match(summary)
        if not m:
            continue
        description = event.get("description") or ""
        if has_catthew(summary, description):
            continue
        title = m.group(2).strip()
        if not title:
            continue
        due_date, due_time = parse_date_from_event(event)
        tags = parse_tags(summary + "\n" + description)
        path = unique_path(title, event.get("id", ""))
        out.append(ImportCandidate(event, title, due_date, due_time, tags, path))
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--calendar", default="")
    parser.add_argument("--days-back", type=int, default=30)
    parser.add_argument("--days-forward", type=int, default=365)
    args = parser.parse_args()

    load_env_defaults()
    calendar_id = args.calendar or os.getenv("GOOGLE_CALENDAR_ID") or DEFAULT_CALENDAR_ID
    service = build("calendar", "v3", credentials=credentials())
    meta = service.calendarList().get(calendarId=calendar_id).execute()
    TASK_DIR.mkdir(parents=True, exist_ok=True)

    created = updated = unchanged = marked = 0
    found = candidates(list_events(service, calendar_id, args.days_back, args.days_forward))
    for c in found:
        content = build_task(c.path, c.title, c.due_date, c.due_time, c.tags, c.event)
        exists = c.path.exists()
        same = exists and c.path.read_text(encoding="utf-8", errors="ignore") == content
        if same:
            unchanged += 1
        elif exists:
            updated += 1
            if not args.dry_run:
                c.path.write_text(content, encoding="utf-8")
        else:
            created += 1
            if not args.dry_run:
                c.path.write_text(content, encoding="utf-8")

        priv = ((c.event.get("extendedProperties") or {}).get("private") or {})
        if priv.get("managed_by") != IMPORTER or priv.get("obsidian_path") != str(c.path):
            marked += 1
            if not args.dry_run:
                patch = {
                    "extendedProperties": {
                        "private": {
                            **priv,
                            "managed_by": IMPORTER,
                            "obsidian_path": str(c.path),
                        }
                    }
                }
                service.events().patch(calendarId=calendar_id, eventId=c.event["id"], body=patch).execute()

    prefix = "[dry-run] " if args.dry_run else ""
    print(
        f"{prefix}theduy calendar -> Obsidian tasks: {created} created, {updated} updated, "
        f"{unchanged} unchanged, {marked} calendar events marked, {len(found)} importable; "
        f"calendar={calendar_id} ({meta.get('summary')})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
