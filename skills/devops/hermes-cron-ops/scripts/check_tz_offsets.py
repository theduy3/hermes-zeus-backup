#!/usr/bin/env python3
"""Diagnose Hermes cron timezone drift across profiles.

Checks two independent sources of truth:
  1. Each job's `next_run_at` UTC offset vs the config.yaml `timezone` offset
     (a mismatch means the scheduler localized the job to the wrong zone).
  2. Each live `hermes gateway run` process's HERMES_TIMEZONE env var vs its
     config.yaml `timezone` (a mismatch means the process was started before
     the tz change and never restarted -- the classic stale-tz trap).

Run: python3 scripts/check_tz_offsets.py
"""
import glob
import json
import os
import re
import subprocess
from datetime import datetime
from zoneinfo import ZoneInfo

HOME = os.path.expanduser("~/.hermes")
OFFSET_RE = re.compile(r"([+-]\d{2}:\d{2})$")


def config_tz(profile_home):
    path = os.path.join(profile_home, "config.yaml")
    try:
        import yaml
        cfg = yaml.safe_load(open(path, encoding="utf-8")) or {}
        tz = cfg.get("timezone", "")
        return tz.strip() if isinstance(tz, str) else ""
    except Exception:
        return ""


def expected_offset(tzname):
    try:
        z = ZoneInfo(tzname)
        off = datetime.now(z).utcoffset()
        total = int(off.total_seconds())
        sign = "+" if total >= 0 else "-"
        total = abs(total)
        return f"{sign}{total // 3600:02d}:{(total % 3600) // 60:02d}"
    except Exception:
        return "??:??"


def job_files():
    files = [os.path.join(HOME, "cron", "jobs.json")]
    files += glob.glob(os.path.join(HOME, "profiles", "*", "cron", "jobs.json"))
    return [f for f in files if os.path.exists(f)]


def main():
    print("=== JOB next_run_at OFFSETS vs CONFIG TIMEZONE ===")
    problems = 0
    for f in job_files():
        prof = "DEFAULT" if "/profiles/" not in f else f.split("/profiles/")[1].split("/")[0]
        home = HOME if prof == "DEFAULT" else os.path.join(HOME, "profiles", prof)
        tz = config_tz(home)
        exp = expected_offset(tz)
        try:
            data = json.load(open(f))
        except Exception as e:
            print(f"  {prof:8} ERR reading {f}: {e}")
            continue
        for j in data.get("jobs", []):
            nxt = j.get("next_run_at") or ""
            m = OFFSET_RE.search(nxt)
            off = m.group(1) if m else "??:??"
            flag = ""
            if off not in ("??:??",) and exp not in ("??:??",) and off != exp:
                flag = "  <-- OFFSET MISMATCH (job localized to wrong zone)"
                problems += 1
            print(f"  {prof:8} | {j.get('name', '?')[:34]:34} | cfg={tz or '(none)':17} exp={exp} got={off}{flag}")
    print()
    print("=== LIVE GATEWAY HERMES_TIMEZONE vs CONFIG ===")
    pids = subprocess.run(["pgrep", "-f", "hermes gateway run"],
                          capture_output=True, text=True).stdout.split()
    for pid in pids:
        try:
            env = open(f"/proc/{pid}/environ", "rb").read().decode(errors="ignore")
        except Exception:
            continue
        envmap = dict(kv.split("=", 1) for kv in env.split("\0") if "=" in kv)
        htz = envmap.get("HERMES_TIMEZONE", "")
        hhome = envmap.get("HERMES_HOME", HOME)
        ctz = config_tz(hhome)
        flag = ""
        if htz and ctz and htz != ctz:
            flag = f"  <-- STALE: process={htz} but config={ctz} (RESTART GATEWAY)"
            problems += 1
        elif not htz:
            flag = "  (no HERMES_TIMEZONE set; relies on cached config or server-local)"
        print(f"  pid={pid:8} home={hhome} | env={htz or '(none)':17} cfg={ctz or '(none)':17}{flag}")
    print()
    if problems:
        print(f"*** {problems} timezone problem(s) found. Restart gateways after fixing config. ***")
    else:
        print("All job offsets and gateway envs match configured timezones.")


if __name__ == "__main__":
    main()
