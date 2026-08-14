import json, glob, os, datetime

BASE = os.path.expanduser('~/.hermes')

# ---- 1. Which providers have stored credentials (auth.json) ----
print("=== STORED PROVIDER CREDENTIALS (auth.json) ===")
try:
    auth = json.load(open(os.path.join(BASE, 'auth.json')))
    provs = auth.get('providers', {})
    for name, v in provs.items():
        info = []
        if isinstance(v, dict):
            if 'access_token' in v and v.get('access_token'):
                info.append('access_token=SET')
            if 'refresh_token' in v and v.get('refresh_token'):
                info.append('refresh_token=SET')
            if 'tokens' in v and isinstance(v['tokens'], dict) and v['tokens'].get('access_token'):
                info.append('tokens.access_token=SET')
            exp = v.get('expires_at') or (v.get('tokens', {}) or {}).get('expires_at')
            if exp:
                info.append(f'expires_at={exp}')
        print(f"  {name:14} -> {', '.join(info) if info else 'NO USABLE CRED'}")
except Exception as e:
    print("  auth.json err:", e)

# ---- 2. Enumerate ALL cronjobs across default + sub-profiles ----
print("\n=== ALL CRONJOBS (provider pin audit) ===")
files = [os.path.join(BASE, 'cron/jobs.json')]
files += sorted(glob.glob(os.path.join(BASE, 'profiles', '*', 'cron', 'jobs.json')))
target = 'e6711b998b07'
for f in files:
    scope = 'DEFAULT' if f == os.path.join(BASE, 'cron/jobs.json') else f.split('/profiles/')[1].split('/')[0]
    try:
        raw = json.load(open(f))
    except Exception as e:
        print(f"  [{scope}] parse err {e}"); continue
    # normalize to list
    if isinstance(raw, list):
        jobs = raw
    elif isinstance(raw, dict):
        jobs = raw.get('jobs') or raw.get('job_list') or list(raw.values())
    else:
        jobs = []
    for j in jobs:
        if not isinstance(j, dict):
            continue
        jid = j.get('job_id') or j.get('id')
        if jid == target:
            print("  >>> FOUND TARGET JOB", jid, "in", scope)
        prov = j.get('provider')
        mdl = j.get('model')
        flag = '  <-- PINNED openai-codex' if prov == 'openai-codex' else ''
        print(f"  [{scope}] {jid} | {str(j.get('name','?'))[:40]:40} | prov={str(prov):14} | model={mdl} | enabled={j.get('enabled')} | no_agent={j.get('no_agent')}{flag}")
