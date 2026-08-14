#!/usr/bin/env python3
"""Forward-only Thor health/wellness capture for Life OS.

Records one dated self-report reading into the Life OS Markdown ledger
(30-health/logs/YYYY-MM.md) via the Markdown-first life_store.write().
Never backfills or invents data: it records exactly what is passed.

Usage:
  python3 thor_log.py --date 2026-08-13 --weight-kg 72.4 --energy 7 \
      --sleep-hours 7.5 --exercise-minutes 30 --note "morning walk"

All fields optional except --date. Missing fields are simply not recorded.
Each call writes ONE event (kind=observation) with an id derived from the
date + a short slug, so re-running the same date+slug is rejected as a dup
(use --event-id to override, or --correct <old_id> to supersede).

Provenance: source_ids points at a self-report marker so the reading is
traceable. Non-negotiable: no fabricated values.
"""
from __future__ import annotations
import argparse, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import life_store as s  # noqa: E402

def main():
    ap = argparse.ArgumentParser(description="Forward-only Thor health capture")
    ap.add_argument("--date", required=True, help="ISO date of the reading (YYYY-MM-DD), America/Toronto")
    ap.add_argument("--weight-kg", type=float, default=None)
    ap.add_argument("--energy", type=int, default=None, help="energy 1-10")
    ap.add_argument("--sleep-hours", type=float, default=None)
    ap.add_argument("--exercise-minutes", type=int, default=None)
    ap.add_argument("--note", default=None)
    ap.add_argument("--event-id", default=None, help="override auto id (advanced)")
    ap.add_argument("--correct", default=None, help="event_id this reading supersedes")
    args = ap.parse_args()

    # validate date
    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print(f"ERROR: bad --date {args.date!r} (need YYYY-MM-DD)", file=sys.stderr); sys.exit(2)

    payload = {}
    if args.weight_kg is not None: payload["weight_kg"] = args.weight_kg
    if args.energy is not None: payload["energy_1to10"] = args.energy
    if args.sleep_hours is not None: payload["sleep_hours"] = args.sleep_hours
    if args.exercise_minutes is not None: payload["exercise_minutes"] = args.exercise_minutes
    if args.note: payload["note"] = args.note

    if not payload:
        print("ERROR: no reading provided (pass at least one of --weight-kg/--energy/--sleep-hours/--exercise-minutes/--note)", file=sys.stderr); sys.exit(2)

    # deterministic id: thor-<date> (one forward reading per day; --event-id overrides)
    event_id = args.event_id or f"thor-{args.date}"
    source_ids = ("thor_self_report",)

    rec = s.write(
        "health", "observation", args.date, payload,
        event_id=event_id,
        supersedes=(args.correct,) if args.correct else (),
        source_ids=source_ids,
        estimated=False,
    )
    print(f"OK wrote event {rec['id']} -> 30-health/logs/{args.date[:7]}.md")
    print("payload:", rec["payload"])
    return 0

if __name__ == "__main__":
    sys.exit(main())
