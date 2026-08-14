# Forward-only capture script skeleton

Proven pattern for `tracker/<domain>_log.py`. Replace `<DOMAIN>` and fields.
Each domain script calls `life_store.write(...)` (Markdown-first; rebuilds SQLite
cache automatically). The CLI MUST reject empty payloads and bad dates BEFORE
calling write(), so no blank/fake events can be created.

```python
#!/usr/bin/env python3
import argparse, sys
from datetime import datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import life_store as s

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="YYYY-MM-DD (America/Toronto)")
    ap.add_argument("--field", type=float, default=None)   # one per real metric
    ap.add_argument("--note", default=None)
    ap.add_argument("--event-id", default=None)
    ap.add_argument("--correct", default=None, help="event_id this supersedes")
    args = ap.parse_args()

    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print(f"ERROR: bad --date {args.date!r}", file=sys.stderr); sys.exit(2)

    payload = {}
    if args.field is not None: payload["field"] = args.field
    if args.note: payload["note"] = args.note
    if not payload:
        print("ERROR: no value provided", file=sys.stderr); sys.exit(2)

    # Auto-id: plain `<domain>-<date>` for new events; when correcting an
    # existing event, the superseded id is invalid for reuse, so suffix -vN
    # to guarantee a DISTINCT id (else append_event raises "duplicate event id").
    if args.event_id:
        event_id = args.event_id
    elif args.correct:
        n = 2
        while True:
            cand = f"<domain>-{args.date}-v{n}"
            if cand != args.correct:
                break
            n += 1
        event_id = cand
    else:
        event_id = f"<domain>-{args.date}"
    rec = s.write("<DOMAIN>", "observation", args.date, payload,
                  event_id=event_id,
                  supersedes=(args.correct,) if args.correct else (),
                  source_ids=("<domain>_self_report",), estimated=False)
    print(f"OK wrote {rec['id']}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Post-write verification (mandatory)
```python
import life_store as s
print(s.reconcile())          # must be {'ok': True, ...}
```
Then update `<domain>/summary.md` (current-state, source-linked),
`migration-registry.md` (status -> cut_over), `changelog.md`, and
`life_store.checkpoint('phase<N>-<slug>-<date>')`.

## Regression gate
`python3 -m unittest tests.test_life_store` must stay OK after any change.
