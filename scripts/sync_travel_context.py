#!/home/hermes/.hermes/hermes-agent/venv/bin/python3
"""Synchronize active travel destination/timezone across Hermes profiles.

Usage:
  /home/hermes/.hermes/scripts/sync_travel_context.py --location Montreal --timezone America/Toronto --label EDT
  /home/hermes/.hermes/scripts/sync_travel_context.py --text "I have arrived in Montreal EDT"

This updates every profile config timezone, profile memory travel context, and known
profile cron schedules so reminders/briefings follow the active destination timezone.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, available_timezones

import yaml

try:
    from croniter import croniter
except Exception:  # pragma: no cover
    croniter = None

ROOT = Path("/home/hermes/.hermes")
PROFILES_ROOT = ROOT / "profiles"
TRAVEL_FILE = ROOT / "travel_context.json"

TZ_ALIASES = {
    "EDT": "America/Toronto",
    "EST": "America/Toronto",
    "ET": "America/Toronto",
    "PDT": "America/Vancouver",
    "PST": "America/Vancouver",
    "PT": "America/Vancouver",
    "MDT": "America/Denver",
    "MST": "America/Denver",
    "CDT": "America/Chicago",
    "CST": "America/Chicago",
    "UTC": "UTC",
}
TZ_LABELS = sorted(TZ_ALIASES, key=len, reverse=True)
TZ_NAMES = [
    "America/Vancouver",
    "America/Toronto",
    "America/New_York",
    "America/Los_Angeles",
    "America/Edmonton",
    "America/Denver",
    "America/Chicago",
]
CITY_TZ = {
    "montreal": "America/Toronto",
    "montréal": "America/Toronto",
    "laval": "America/Toronto",
    "quebec": "America/Toronto",
    "québec": "America/Toronto",
    "toronto": "America/Toronto",
    "new york": "America/New_York",
    "vancouver": "America/Vancouver",
    "richmond": "America/Vancouver",
    "burnaby": "America/Vancouver",
    "surrey": "America/Vancouver",
    "calgary": "America/Edmonton",
    "edmonton": "America/Edmonton",
    "los angeles": "America/Los_Angeles",
    "san francisco": "America/Los_Angeles",
    "seattle": "America/Los_Angeles",
}

# Known personal recurring jobs where earlier travel handling encoded Eastern time
# by shifting cron expressions while profile timezone stayed Pacific. Once the
# profile timezone itself is switched, normalize these to destination-local wall time.
KNOWN_LOCAL_SCHEDULES: dict[str, dict[str, str]] = {
    "zeus": {
        "Daily Morning Briefing - Personal Tasks": "15 6 * * *",
        "Daily Evening Briefing - Task Status": "0 21 * * *",
        "Individual Obsidian Task Done Button Drip": "*/10 8-23 * * *",
    },
    "catthew": {
        "Daily Morning Briefing": "0 7 * * *",
        "Individual Household Task Done Button Drip": "*/10 8-23 * * *",
    },
}

PROFILE_NAMES = ["default"] + [p.name for p in sorted(PROFILES_ROOT.iterdir()) if p.is_dir()]


def profile_home(profile: str) -> Path:
    return ROOT if profile == "default" else PROFILES_ROOT / profile


def infer(text: str, location: str | None, timezone: str | None, label: str | None) -> tuple[str, str, str]:
    raw = text or ""
    loc = location or ""
    tz = timezone or ""
    lab = label or ""

    if not tz:
        for token, zone in TZ_ALIASES.items():
            if re.search(rf"\b{re.escape(token)}\b", raw, re.I):
                tz = zone
                lab = lab or token.upper()
                break
    if not loc:
        m = re.search(r"(?:arrived in|arrive in|travel(?:ing)? to|going to|in)\s+([A-Za-zÀ-ÿ .'-]+?)(?:\s+(?:EDT|EST|ET|PDT|PST|PT|MDT|MST|CDT|CST|UTC)\b|$)", raw, re.I)
        if m:
            loc = m.group(1).strip(" .")
    if not tz and loc:
        key = loc.lower().strip()
        tz = CITY_TZ.get(key, "")
    if tz in TZ_ALIASES:
        tz = TZ_ALIASES[tz]
    if tz not in available_timezones():
        raise SystemExit(f"Invalid/unknown timezone: {tz!r}. Use IANA like America/Toronto or alias EDT/PDT.")
    now = datetime.now(ZoneInfo(tz))
    if not lab:
        lab = now.tzname() or tz
    return loc or "unspecified destination", tz, lab


def update_config(profile: str, tz: str) -> bool:
    path = profile_home(profile) / "config.yaml"
    cfg: dict[str, Any] = {}
    if path.exists():
        cfg = yaml.safe_load(path.read_text()) or {}
    old = cfg.get("timezone")
    cfg["timezone"] = tz
    path.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return old != tz


def replace_or_append_memory(profile: str, line: str) -> None:
    memdir = profile_home(profile) / "memories"
    memdir.mkdir(parents=True, exist_ok=True)
    path = memdir / "MEMORY.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = [ln for ln in text.splitlines() if not ln.startswith("Active travel context:")]
    if lines and lines[-1].strip():
        lines.append("§")
    lines.append(line)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def localize_text(value: str, tz: str, label: str) -> str:
    out = value
    for name in TZ_NAMES:
        out = out.replace(name, tz)
    out = re.sub(r"\bPacific Time\b", label, out)
    out = re.sub(r"\bPacific timezone\b", f"{label} timezone", out)
    out = re.sub(r"\bPacific\b", label, out)
    out = re.sub(r"\b(?:PST/PDT|PDT/PST)\b", label, out)
    # Replace previous travel labels when switching again later (EDT -> PDT, etc.).
    # Keep generic ET/PT words out of this pass to avoid corrupting normal prose.
    for old_label in ["EDT", "EST", "PDT", "PST", "MDT", "MST", "CDT", "CST"]:
        if old_label != label:
            out = re.sub(rf"\b{old_label}\b", label, out)
    return out


def recompute_next(schedule: dict[str, Any], tz: str, last_run_at: str | None = None) -> str | None:
    now = datetime.now(ZoneInfo(tz))
    kind = schedule.get("kind")
    if kind == "cron" and croniter is not None:
        return croniter(schedule["expr"], now).get_next(datetime).isoformat()
    if kind == "interval":
        return (now + timedelta(minutes=int(schedule.get("minutes", 1)))).isoformat()
    if kind == "once":
        return schedule.get("run_at")
    return None


def update_crons(profile: str, tz: str, label: str) -> list[str]:
    path = profile_home(profile) / "cron" / "jobs.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    jobs = data.get("jobs", data if isinstance(data, list) else [])
    changed: list[str] = []
    for job in jobs:
        if not isinstance(job, dict):
            continue
        name = job.get("name", "")
        new_name = localize_text(name, tz, label)
        if new_name != name:
            job["name"] = new_name
            name = new_name
            changed.append(f"{name}: name label")
        prompt = job.get("prompt")
        if isinstance(prompt, str):
            new_prompt = localize_text(prompt, tz, label)
            if new_prompt != prompt:
                job["prompt"] = new_prompt
                changed.append(f"{name}: prompt timezone text")
        sched = job.get("schedule")
        if isinstance(sched, dict):
            # Normalize known jobs to destination-local wall time.
            base_name = name.replace(label, "Pacific")
            override = KNOWN_LOCAL_SCHEDULES.get(profile, {}).get(base_name) or KNOWN_LOCAL_SCHEDULES.get(profile, {}).get(name)
            if override and sched.get("kind") == "cron" and sched.get("expr") != override:
                sched["expr"] = override
                sched["display"] = override
                job["schedule_display"] = override
                changed.append(f"{name}: schedule -> {override}")
            nxt = recompute_next(sched, tz, job.get("last_run_at"))
            if nxt:
                job["next_run_at"] = nxt
    if changed:
        if isinstance(data, dict):
            data["updated_at"] = datetime.now(ZoneInfo(tz)).isoformat()
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        tmp.replace(path)
    return changed


def append_soul_instruction(profile: str) -> bool:
    path = profile_home(profile) / "SOUL.md"
    if not path.exists():
        return False
    marker = "## Cross-profile travel/timezone sync"
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return False
    block = f"""

{marker}
When Duy tells this profile his travel destination, current location, arrival, or timezone (for example: "I have arrived in Montreal EDT"), treat it as global Hermes context. Immediately run:

`/home/hermes/.hermes/scripts/sync_travel_context.py --text "<Duy's exact message>"`

This updates timezone, travel context memory, and timezone-sensitive cron schedules for default plus all named profiles. After it succeeds, reply tersely with the destination/timezone and say all profiles were synced. Do not update only this profile.
"""
    try:
        path.write_text(text.rstrip() + block, encoding="utf-8")
    except PermissionError:
        # Some profile SOUL.md files are mounted/owned by another UID. Do not let
        # a non-writable instruction file block timezone/config/memory/cron sync.
        return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", default="")
    ap.add_argument("--location", default="")
    ap.add_argument("--timezone", default="")
    ap.add_argument("--label", default="")
    args = ap.parse_args()
    location, tz, label = infer(args.text, args.location or None, args.timezone or None, args.label or None)
    now = datetime.now(ZoneInfo(tz))
    line = f"Active travel context: destination {location}; timezone {tz} ({label}); set {now.strftime('%Y-%m-%d')}. Apply trip-sensitive schedules, briefings, reminders, dates, and local-time wording across all profiles until Duy changes it."
    context = {"location": location, "timezone": tz, "label": label, "updated_at": now.isoformat(), "profiles": PROFILE_NAMES}
    TRAVEL_FILE.write_text(json.dumps(context, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    report = []
    for profile in PROFILE_NAMES:
        cfg_changed = update_config(profile, tz)
        replace_or_append_memory(profile, line)
        soul_changed = append_soul_instruction(profile)
        cron_changes = update_crons(profile, tz, label)
        report.append({
            "profile": profile,
            "config_timezone_changed": cfg_changed,
            "soul_instruction_added": soul_changed,
            "cron_changes": cron_changes,
        })
    print(json.dumps({"ok": True, "location": location, "timezone": tz, "label": label, "profiles": report}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
