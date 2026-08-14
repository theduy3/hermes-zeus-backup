#!/usr/bin/env python3
"""Forward-only Charles (investments) capture for Life OS.

Records one dated, source-linked investment record into the Life OS
Markdown ledger (60-finance/events/YYYY-MM.md) via the Markdown-first
life_store.write(). Never backfills or invents data: records exactly
what is passed.

Charles operates UNDER Finance: it references Finance's liquidity/cash-
flow facts (see 60-finance/finance_summary.md) and never overwrites them.

Record kinds:
  position   - a held/intended position (ticker, qty, cost, thesis_id)
  thesis     - an investment thesis or view (id, statement, confidence)
  risk_rule  - a portfolio risk limit or constraint
  decision   - a buy/sell/hold decision with rationale
  watch      - a watchlist item / monitoring note

Usage:
  python3 charles_log.py --date 2026-08-13 --kind thesis \
      --id thesis-ai-infra --statement "AI infra capex durable thru 2027" \
      --confidence medium --source "Daily/2026-08-12-investment.md"

  python3 charles_log.py --date 2026-08-13 --kind position \
      --payload '{"ticker":"ORCL","qty":10,"cost_usd":1450,"thesis_id":"thesis-ai-infra"}'

All non-kind fields optional except --date and --kind. --id recommended
for thesis/risk_rule/decision so later records can reference them.
--payload is JSON for structured kinds; otherwise key fields are taken
from explicit flags.
"""
from __future__ import annotations
import argparse, json, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import life_store as s  # noqa: E402

KINDS = {"position", "thesis", "risk_rule", "decision", "watch"}

def main():
    ap = argparse.ArgumentParser(description="Forward-only Charles (investments) capture")
    ap.add_argument("--date", required=True, help="ISO date (YYYY-MM-DD), America/Toronto")
    ap.add_argument("--kind", required=True, choices=sorted(KINDS), help="record kind")
    ap.add_argument("--id", default=None, help="stable id for thesis/risk_rule/decision")
    ap.add_argument("--statement", default=None, help="thesis/risk_rule/decision text")
    ap.add_argument("--confidence", default=None, help="low|medium|high")
    ap.add_argument("--ticker", default=None, help="position/watch ticker")
    ap.add_argument("--qty", type=float, default=None, help="position quantity")
    ap.add_argument("--cost", type=float, default=None, help="position cost (USD)")
    ap.add_argument("--thesis-id", default=None, help="thesis this position/decision references")
    ap.add_argument("--payload", default=None, help="raw JSON for structured kinds")
    ap.add_argument("--source", action="append", default=None, help="vault source path this is derived from")
    ap.add_argument("--note", default=None)
    ap.add_argument("--event-id", default=None, help="override auto id (advanced)")
    ap.add_argument("--correct", default=None, help="event_id this record supersedes")
    args = ap.parse_args()

    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print(f"ERROR: bad --date {args.date!r}", file=sys.stderr); sys.exit(2)
    if args.kind not in KINDS:
        print(f"ERROR: bad --kind {args.kind!r}", file=sys.stderr); sys.exit(2)

    if args.payload:
        try:
            payload = json.loads(args.payload)
        except json.JSONDecodeError as e:
            print(f"ERROR: bad --payload JSON: {e}", file=sys.stderr); sys.exit(2)
        if not isinstance(payload, dict):
            print("ERROR: --payload must be a JSON object", file=sys.stderr); sys.exit(2)
    else:
        payload = {}
        if args.id: payload["id"] = args.id
        if args.statement: payload["statement"] = args.statement
        if args.confidence: payload["confidence"] = args.confidence
        if args.ticker: payload["ticker"] = args.ticker
        if args.qty is not None: payload["qty"] = args.qty
        if args.cost is not None: payload["cost_usd"] = args.cost
        if args.thesis_id: payload["thesis_id"] = args.thesis_id
        if args.note: payload["note"] = args.note

    if not payload:
        print("ERROR: no content provided (use --payload JSON or specific flags)", file=sys.stderr); sys.exit(2)

    # Charles references finance liquidity; tag provenance
    source_ids = tuple(args.source) if args.source else ("charles_self_report",)
    event_id = args.event_id or f"charles-{args.kind}-{args.date}" + (f"-{args.id}" if args.id else "")

    rec = s.write(
        "finance", args.kind, args.date, payload,
        event_id=event_id,
        supersedes=(args.correct,) if args.correct else (),
        source_ids=source_ids,
        estimated=False,
    )
    print(f"OK wrote event {rec['id']} (kind={args.kind}) -> 60-finance/events/{args.date[:7]}.md")
    print("payload:", rec["payload"])
    return 0

if __name__ == "__main__":
    sys.exit(main())
