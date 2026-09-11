#!/usr/bin/env python3
"""Scan ALL Hermes cron jobs across default + every profile and report
provider-pin / blocked_config problems only.

For full "are crons working" health (dead free models, OOM, delivery, gateway),
run fleet_health.py in this directory instead — this scanner alone is not enough.

Usage: python3 audit_scan.py
"""
import json, glob, os

BASE = os.path.expanduser('~/.hermes')
files = [os.path.join(BASE, 'cron', 'jobs.json')]
files += sorted(glob.glob(os.path.join(BASE, 'profiles', '*', 'cron', 'jobs.json')))

left = 0
for f in files:
    scope = 'default' if '/profiles/' not in f else f.split('/profiles/')[1].split('/')[0]
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
        # script-shaped without prompt also skip when marked via script-only heuristic
        if j.get('script') and not j.get('prompt') and no_agent is not False:
            # leave alone unless explicitly agent
            if no_agent is True or (j.get('prompt') in (None, '') and j.get('script')):
                if no_agent is True:
                    continue
        if prov == 'openai-codex' or (prov is None and j.get('last_status') == 'blocked_config'):
            left += 1
            print(f"  PROBLEM [{scope}] {jid} | {str(j.get('name'))[:40]} | provider={prov} | last_status={j.get('last_status')}")

print(f"\nJobs still blocked by a missing provider: {left}")
print("0 = clean for provider-pin only. Run fleet_health.py for model/OOM/delivery classes.")
