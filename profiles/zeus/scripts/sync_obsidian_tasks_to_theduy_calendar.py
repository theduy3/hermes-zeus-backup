#!/usr/bin/env python3
"""Sync dated Obsidian tasks to Google Calendar: theduy calendar only.

Source: /vault/Tasks/tasks/*.md
Target: GOOGLE_CALENDAR_ID from Zeus .env, default duynt1989@gmail.com

Rules:
- Sync pending/in_progress/blocked dated tasks as all-day Google Calendar events.
- Never sync #catthew tasks (tags/frontmatter/body containing catthew).
- Never sync completed/done/cancelled/canceled tasks.
- Upsert by source file path using Google Calendar private extendedProperties.
- Remove stale Google events previously managed by this script when the source is
  completed/deleted/no longer eligible.
"""
from __future__ import annotations

import argparse
import hashlib
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
MANAGED_BY = "zeus-obsidian-task-sync"
TZ = ZoneInfo("America/Vancouver")

SKIP_STATUSES = {"completed", "done", "cancelled", "canceled"}
SYNC_STATUSES = {"pending", "in_progress", "blocked"}


def load_env_defaults() -> None:
    if not ENV_PATH.exists():
        return
    for raw in ENV_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


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
        key, value = raw.split(":", 1)
        fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm, parts[2]


def title_from(path: Path, body: str, fm: dict[str, str]) -> str:
    if fm.get("title"):
        return fm["title"].strip()
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("-", " ").title()


def clean_text(value: str) -> str:
    value = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", value)
    value = re.sub(r"\[\[([^\]]+)\]\]", r"\1", value)
    value = re.sub(r"`([^`]*)`", r"\1", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def has_catthew(fm: dict[str, str], body: str, path: Path) -> bool:
    haystack = "\n".join([
        path.name,
        fm.get("tags", ""),
        fm.get("company", ""),
        fm.get("source", ""),
        body[:4000],
    ]).lower()
    return "#catthew" in haystack or "catthew" in haystack


def parse_date(value: str) -> date | None:
    value = (value or "").strip()[:10]
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def task_hash(title: str, due: date, status: str, path: str) -> str:
    payload = json.dumps({"title": title, "due": due.isoformat(), "status": status, "path": path}, sort_keys=True)
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


@dataclass
class TaskEvent:
    path: Path
    title: str
    due: date
    status: str
    source_hash: str
    kind: str = "task"

    @property
    def key(self) -> str:
        return str(self.path)

    def event_body(self) -> dict:
        next_day = self.due + timedelta(days=1)
        label = "event" if self.kind == "event" else "task"
        description = (
            f"Obsidian {label}: {self.path}\n"
            f"Status: {self.status}\n"
            f"Type: {self.kind}\n"
            f"Managed by Zeus. Edit the Obsidian {label} for durable changes."
        )
        return {
            "summary": clean_text(self.title),
            "description": description,
            "start": {"date": self.due.isoformat()},
            "end": {"date": next_day.isoformat()},
            "transparency": "transparent",
            "extendedProperties": {
                "private": {
                    "managed_by": MANAGED_BY,
                    "source_path": str(self.path),
                    "source_hash": self.source_hash,
                    "source_type": self.kind,
                }
            },
        }


def load_tasks() -> dict[str, TaskEvent]:
    tasks: dict[str, TaskEvent] = {}
    for path in sorted(TASK_DIR.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        fm, body = parse_frontmatter(text)
        kind = (fm.get("type") or "task").strip().lower()
        if kind not in {"task", "event"}:
            continue
        status = (fm.get("status") or "pending").strip().lower()
        if status in SKIP_STATUSES or status not in SYNC_STATUSES:
            continue
        if has_catthew(fm, body, path):
            continue
        due = parse_date(fm.get("due_date") or fm.get("date") or "")
        if not due:
            continue
        title = title_from(path, body, fm)
        key = str(path)
        tasks[key] = TaskEvent(path, title, due, status, task_hash(title, due, status, key), kind)
    return tasks


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


def list_managed_events(service, calendar_id: str, years_back: int = 2, years_forward: int = 3) -> dict[str, dict]:
    now = datetime.now(TZ).date()
    time_min = datetime.combine(now.replace(year=now.year - years_back), datetime.min.time(), tzinfo=TZ).isoformat()
    time_max = datetime.combine(now.replace(year=now.year + years_forward), datetime.max.time(), tzinfo=TZ).isoformat()
    events: dict[str, dict] = {}
    page_token = None
    while True:
        resp = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            maxResults=2500,
            privateExtendedProperty=f"managed_by={MANAGED_BY}",
            pageToken=page_token,
        ).execute()
        for event in resp.get("items", []):
            priv = (event.get("extendedProperties") or {}).get("private") or {}
            source_path = priv.get("source_path")
            if source_path:
                events[source_path] = event
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return events


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--calendar", default="")
    args = parser.parse_args()

    load_env_defaults()
    calendar_id = args.calendar or os.getenv("GOOGLE_CALENDAR_ID") or DEFAULT_CALENDAR_ID
    tasks = load_tasks()

    service = build("calendar", "v3", credentials=credentials())
    cal_meta = service.calendarList().get(calendarId=calendar_id).execute()
    if cal_meta.get("accessRole") not in {"owner", "writer"}:
        raise SystemExit(f"No write access to {calendar_id}: {cal_meta.get('accessRole')}")

    existing = list_managed_events(service, calendar_id)
    created = updated = deleted = unchanged = 0

    for key, task in tasks.items():
        body = task.event_body()
        event = existing.get(key)
        if event is None:
            created += 1
            if not args.dry_run:
                service.events().insert(calendarId=calendar_id, body=body).execute()
            continue
        priv = (event.get("extendedProperties") or {}).get("private") or {}
        if priv.get("source_hash") == task.source_hash:
            unchanged += 1
            continue
        updated += 1
        if not args.dry_run:
            service.events().patch(calendarId=calendar_id, eventId=event["id"], body=body).execute()

    for key, event in existing.items():
        if key in tasks:
            continue
        deleted += 1
        if not args.dry_run:
            service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()

    prefix = "[dry-run] " if args.dry_run else ""
    print(
        f"{prefix}obsidian->theduy calendar: {created} created, {updated} updated, "
        f"{deleted} stale deleted, {unchanged} unchanged, {len(tasks)} eligible tasks; "
        f"calendar={calendar_id} ({cal_meta.get('summary')})"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
