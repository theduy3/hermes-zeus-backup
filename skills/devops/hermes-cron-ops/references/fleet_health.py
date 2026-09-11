#!/usr/bin/env python3
"""Fleet cron health matrix across default + every profile.

Classifies jobs beyond provider-pin issues. Use when the user asks whether
cronjobs are actually working.

Usage: python3 fleet_health.py
"""
from __future__ import annotations

import glob
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(os.path.expanduser("~/.hermes"))


def _jobs_files():
    yield "default", BASE / "cron" / "jobs.json"
    for path in sorted((BASE / "profiles").glob("*/cron/jobs.json")):
        yield path.parent.parent.name, path


def _classify(j: dict) -> str:
    enabled = j.get("enabled", True)
    paused = bool(j.get("paused_at") or j.get("state") == "paused")
    if not enabled or paused:
        return "PAUSED"
    err = str(j.get("last_error") or "")
    del_err = str(j.get("last_delivery_error") or "")
    status = j.get("last_status")
    low = err.lower()
    if "free period has ended" in low or "select a different model" in low:
        return "MODEL_DEAD"
    if status == "blocked_config" or "no codex credentials" in low:
        return "BLOCKED_CONFIG"
    if "-9" in err or "sigkill" in low:
        return "OOM_KILL"
    if "truncated" in low and "output length" in low:
        return "TRUNCATED"
    if del_err and ("unauthorized" in del_err.lower() or "rejected" in del_err.lower()):
        return "DELIVERY"
    if status == "ok" and not err and not del_err:
        return "OK"
    if status in (None, "pending") and not err:
        return "NEVER_PENDING"
    if status == "error" or err:
        return "ERROR"
    return "OTHER"


def _jid(j: dict) -> str:
    return str(j.get("job_id") or j.get("id") or "?")


def main() -> int:
    counts: Counter = Counter()
    by_class: dict[str, list] = defaultdict(list)
    vault_ok = (BASE.parts[0] == "/" and Path("/vault").is_dir()) or Path("/vault").is_dir()

    for scope, path in _jobs_files():
        if not path.exists():
            print(f"[{scope}] missing {path}")
            continue
        try:
            raw = json.loads(path.read_text())
        except Exception as e:
            print(f"[{scope}] parse err {e}")
            continue
        jobs = raw if isinstance(raw, list) else (raw.get("jobs") or [])
        for j in jobs:
            if not isinstance(j, dict):
                continue
            cls = _classify(j)
            counts[cls] += 1
            row = {
                "scope": scope,
                "id": _jid(j),
                "name": str(j.get("name") or "")[:48],
                "status": j.get("last_status"),
                "provider": j.get("provider"),
                "model": j.get("model"),
                "streak": j.get("failure_streak", 0),
                "workdir": j.get("workdir"),
                "error": (str(j.get("last_error"))[:160] if j.get("last_error") else None),
            }
            by_class[cls].append(row)

    total = sum(counts.values())
    print(f"TOTAL={total} vault_mounted={vault_ok}")
    print("COUNTS:", dict(counts))
    problem_order = [
        "MODEL_DEAD",
        "BLOCKED_CONFIG",
        "OOM_KILL",
        "TRUNCATED",
        "DELIVERY",
        "ERROR",
        "OTHER",
    ]
    for cls in problem_order:
        rows = by_class.get(cls) or []
        if not rows:
            continue
        print(f"\n## {cls} ({len(rows)})")
        for r in rows:
            print(
                f"  [{r['scope']}] {r['id'][:12]} {r['name']!s:48} "
                f"pin={r['provider']}/{r['model']} streak={r['streak']} status={r['status']}"
            )
            if r["error"]:
                print(f"      err: {r['error']}")
            if r.get("workdir"):
                print(f"      workdir={r['workdir']}")

    # workdir warnings for OK/pending jobs that need /vault when missing
    if not vault_ok:
        print("\n## VAULT_MISSING_WARN")
        for cls, rows in by_class.items():
            for r in rows:
                wd = r.get("workdir") or ""
                if str(wd).startswith("/vault"):
                    print(f"  [{r['scope']}] {r['id'][:12]} {r['name']} workdir={wd} class={cls}")

    bad = sum(counts[c] for c in problem_order if c in counts)
    print(f"\nAction-worthy failures: {bad}")
    print("0 action-worthy + gateways live = healthy fleet (still confirm cron status).")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
