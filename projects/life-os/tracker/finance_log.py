#!/usr/bin/env python3
"""Forward-only Finance current-state capture for Life OS.

Records one dated, source-linked snapshot of CURRENT personal finance
state into the Life OS Markdown ledger (60-finance/events/YYYY-MM.md)
via the Markdown-first life_store.write(). Never backfills or invents
data: it records exactly what is passed.

Usage:
  python3 finance_log.py --date 2026-08-13 \
      --liquid-cad 50000 --monthly-in 12000 --monthly-out 9000 \
      --liability "mortgage: 350000 @ 4.2%" \
      --goal "build 3mo emergency buffer" \
      --uncertainty "salon revenue seasonal" \
      --review-cadence "monthly" \
      --note "Q3 review"

All fields optional except --date. Missing fields are simply not recorded.
Each call writes ONE event (kind=observation, domain=finance).

Provenance: source_ids=("finance_self_report",). Non-negotiable: no
fabricated values. Amounts are self-reported, not bank-verified unless a
source file is supplied via --source.
"""
from __future__ import annotations
import argparse, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import life_store as s  # noqa: E402

def main():
    ap = argparse.ArgumentParser(description="Forward-only Finance capture")
    ap.add_argument("--date", required=True, help="ISO date of the snapshot (YYYY-MM-DD), America/Toronto")
    ap.add_argument("--liquid-cad", type=float, default=None, help="total liquid CAD available")
    ap.add_argument("--monthly-in", type=float, default=None, help="avg monthly inflow CAD")
    ap.add_argument("--monthly-out", type=float, default=None, help="avg monthly outflow CAD")
    ap.add_argument("--liability", action="append", default=None, help="active liability, repeatable (e.g. 'mortgage: 350k @ 4.2%')")
    ap.add_argument("--goal", action="append", default=None, help="current financial goal, repeatable")
    ap.add_argument("--uncertainty", action="append", default=None, help="known uncertainty, repeatable")
    ap.add_argument("--review-cadence", default=None, help="e.g. monthly, quarterly")
    ap.add_argument("--note", default=None)
    ap.add_argument("--source", default=None, help="optional source file/path this snapshot is derived from")
    ap.add_argument("--event-id", default=None, help="override auto id (advanced)")
    ap.add_argument("--correct", default=None, help="event_id this snapshot supersedes")
    args = ap.parse_args()

    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print(f"ERROR: bad --date {args.date!r} (need YYYY-MM-DD)", file=sys.stderr); sys.exit(2)

    payload = {}
    if args.liquid_cad is not None: payload["liquid_cad"] = args.liquid_cad
    if args.monthly_in is not None: payload["monthly_in_cad"] = args.monthly_in
    if args.monthly_out is not None: payload["monthly_out_cad"] = args.monthly_out
    if args.liability: payload["liabilities"] = list(args.liability)
    if args.goal: payload["goals"] = list(args.goal)
    if args.uncertainty: payload["uncertainties"] = list(args.uncertainty)
    if args.review_cadence: payload["review_cadence"] = args.review_cadence
    if args.note: payload["note"] = args.note

    if not payload:
        print("ERROR: no finance value provided (pass at least one field)", file=sys.stderr); sys.exit(2)

    event_id = args.event_id or f"fin-{args.date}"
    source_ids = ("finance_self_report",)
    if args.source:
        source_ids = source_ids + (args.source,)

    rec = s.write(
        "finance", "observation", args.date, payload,
        event_id=event_id,
        supersedes=(args.correct,) if args.correct else (),
        source_ids=source_ids,
        estimated=False,
    )
    print(f"OK wrote event {rec['id']} -> 60-finance/events/{args.date[:7]}.md")
    print("payload:", rec["payload"])
    return 0

if __name__ == "__main__":
    sys.exit(main())
