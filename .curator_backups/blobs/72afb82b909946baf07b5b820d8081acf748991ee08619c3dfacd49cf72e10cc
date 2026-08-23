#!/usr/bin/env python3
"""Scan ALL Hermes cron jobs across default + every profile and report
provider-pin problems. Reusable from any session. Prints a per-profile table
and a final count of jobs still blocked by a missing provider.

Usage: python3 audit_scan.py   (run from ~/.hermes or any cwd)
"""
import json, glob, os

BASE = os.path.expanduser('~/.hermes')
files = [os.path.join(BASE, 'cron', 'jobs.json')]
files += sorted(glob.glob(os.path.join(BASE, 'profiles', '*', 'cron', 'jobs.json')))

left = 0
for f in files:
    scope = 'default' if f.endswith('cron/jobs.json') else f.split('/profiles/')[1].split('/')[0]
    try:
        raw = json.load(open(f))
    except Exception as e:
        print(f"  [{scope}] parse err {e}")
        continue
    jobs = raw if isinstance(raw, list) else (raw.get('jobs') or raw.get('job_list') or list(raw.values()))
    for j in jobs:
        if not isinstance(j, dict):
            continue
        jid = j.get('job_id') or j.get('id')
        prov = j.get('provider')
        no_agent = j.get('no_agent')
        # LLM jobs only (skip script-only)
        if no_agent is True:
            continue
        if prov == 'openai-codex' or (prov is None and j.get('last_status') == 'blocked_config'):
            left += 1
            print(f"  PROBLEM [{scope}] {jid} | {str(j.get('name'))[:40]} | provider={prov} | last_status={j.get('last_status')}")

print(f"\nJobs still blocked by a missing provider: {left}")
print("0 = clean.")
