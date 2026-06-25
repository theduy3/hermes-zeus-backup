#!/usr/bin/env python3
"""One-shot travel context reset after Duy's Vancouver return flight."""
import json
import subprocess
import sys

TEXT = (
    "Duy has returned to Vancouver after Montreal/YUL trip; "
    "set active travel context back to Vancouver and timezone America/Vancouver (PDT) "
    "for trip-sensitive scheduling/briefings across all Hermes profiles."
)

cmd = ["/home/hermes/.hermes/scripts/sync_travel_context.py", "--text", TEXT]
proc = subprocess.run(cmd, text=True, capture_output=True, timeout=120)
if proc.returncode != 0:
    print(proc.stderr or proc.stdout or f"sync_travel_context failed with exit {proc.returncode}")
    sys.exit(proc.returncode)

try:
    payload = json.loads(proc.stdout)
except Exception:
    print(proc.stdout)
    sys.exit(1)

if not payload.get("ok"):
    print(proc.stdout)
    sys.exit(1)

# Success: stay silent so Duy is informed only if action is needed.
