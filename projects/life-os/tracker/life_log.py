#!/usr/bin/env python3
"""Forward-only Goals / Projects capture for Life OS.

Records one dated, source-linked goal or project record into the Life OS
Markdown ledger via the Markdown-first life_store.write(). Never backfills
or invents data: records exactly what is passed.

NOTE: /vault/Tasks/ remains the AUTHORITY for actionable dated tasks.
Life OS stores the strategic "why", milestones, and project context.
This tool writes goal/project context only.

Usage:
  # Goal
  python3 life_log.py --date 2026-08-13 --kind goal \
      --id goal-fin-buffer --title "Build $10k liquid buffer" \
      --area finance --status active --review-date 2026-09-13 \
      --note "Supports mortgage + salon cash flow resilience"

  # Project
  python3 life_log.py --date 2026-08-13 --kind project \
      --id proj-salon360 --title "Salon360 ops improvement" \
      --status active --phase planning --next-action "..." \
      --goal-id goal-fin-buffer

All non-id fields optional except --date and --kind.
"""
from __future__ import annotations
import argparse, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import life_store as s  # noqa: E402

KINDS = {"goal", "project"}

def main():
    ap = argparse.ArgumentParser(description="Forward-only Goals/Projects capture")
    ap.add_argument("--date", required=True, help="ISO date (YYYY-MM-DD), America/Toronto")
    ap.add_argument("--kind", required=True, choices=sorted(KINDS), help="goal or project")
    ap.add_argument("--id", required=True, help="stable id, e.g. goal-fin-buffer / proj-salon360")
    ap.add_argument("--title", default=None)
    ap.add_argument("--area", default=None, help="goal area: finance|health|business|personal|...")
    ap.add_argument("--status", default=None, help="active|paused|done|blocked|archived")
    ap.add_argument("--phase", default=None, help="project phase")
    ap.add_argument("--next-action", default=None)
    ap.add_argument("--goal-id", default=None, help="project -> goal link")
    ap.add_argument("--review-date", default=None, help="YYYY-MM-DD")
    ap.add_argument("--note", default=None)
    ap.add_argument("--source", action="append", default=None, help="vault source path")
    ap.add_argument("--event-id", default=None, help="override auto id (advanced)")
    ap.add_argument("--correct", default=None, help="event_id this record supersedes")
    args = ap.parse_args()

    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print(f"ERROR: bad --date {args.date!r}", file=sys.stderr); sys.exit(2)
    if args.kind not in KINDS:
        print(f"ERROR: bad --kind {args.kind!r}", file=sys.stderr); sys.exit(2)

    payload = {"id": args.id}
    if args.title: payload["title"] = args.title
    if args.area: payload["area"] = args.area
    if args.status: payload["status"] = args.status
    if args.phase: payload["phase"] = args.phase
    if args.next_action: payload["next_action"] = args.next_action
    if args.goal_id: payload["goal_id"] = args.goal_id
    if args.review_date: payload["review_date"] = args.review_date
    if args.note: payload["note"] = args.note

    source_ids = tuple(args.source) if args.source else ("life_self_report",)
    event_id = args.event_id or f"{args.kind}-{args.id}-{args.date}"

    rec = s.write(
        args.kind, args.kind + "s", args.date, payload,
        event_id=event_id,
        supersedes=(args.correct,) if args.correct else (),
        source_ids=source_ids,
        estimated=False,
    )
    print(f"OK wrote event {rec['id']} (kind={args.kind}) -> {args.kind}s/events/{args.date[:7]}.md")
    print("payload:", rec["payload"])
    return 0

if __name__ == "__main__":
    sys.exit(main())
