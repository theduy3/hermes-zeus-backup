import os, glob, json
BASE=os.path.expanduser('~/.hermes')
files=[os.path.join(BASE,'cron/jobs.json')]+sorted(glob.glob(os.path.join(BASE,'profiles','*','cron','jobs.json')))
print("=== provider=None, no_agent=False jobs: status ===")
for f in files:
    scope='DEFAULT' if f.endswith('cron/jobs.json') else f.split('/profiles/')[1].split('/')[0]
    raw=json.load(open(f))
    jobs=raw if isinstance(raw,list) else (raw.get('jobs') or raw.get('job_list') or list(raw.values()))
    for j in jobs:
        if not isinstance(j,dict): continue
        if j.get('provider') is None and j.get('no_agent') is not True:
            print(f"[{scope}] {j.get('job_id')} | {str(j.get('name'))[:38]:38} | last_status={j.get('last_status')} | err={str(j.get('last_delivery_error'))[:40]}")
print("\n=== explicit openai-codex jobs: status ===")
for f in files:
    scope='DEFAULT' if f.endswith('cron/jobs.json') else f.split('/profiles/')[1].split('/')[0]
    raw=json.load(open(f))
    jobs=raw if isinstance(raw,list) else (raw.get('jobs') or raw.get('job_list') or list(raw.values()))
    for j in jobs:
        if not isinstance(j,dict): continue
        if j.get('provider')=='openai-codex':
            print(f"[{scope}] {j.get('job_id')} | {str(j.get('name'))[:38]:38} | last_status={j.get('last_status')} | err={str(j.get('last_delivery_error'))[:40]}")
