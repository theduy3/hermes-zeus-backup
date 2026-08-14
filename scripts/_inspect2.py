import json, os
BASE=os.path.expanduser('~/.hermes')
def load(p):
    return json.load(open(p))
f=os.path.join(BASE,'profiles/zeus/cron/jobs.json')
raw=load(f)
print("zeus jobs.json TYPE:", type(raw).__name__)
if isinstance(raw, dict):
    print("zeus top keys:", list(raw.keys())[:10])
jobs = raw if isinstance(raw,list) else (raw.get('jobs') or raw.get('job_list') or list(raw.values()))
print("zeus job count:", len(jobs))
for j in jobs:
    if not isinstance(j,dict): continue
    jid = j.get('job_id') or j.get('id')
    if jid=='e6711b998b07':
        print("\n=== FOUND e6711b998b07 ===")
        print("keys:", list(j.keys()))
        print(json.dumps(j, indent=1)[:1600])
        break
else:
    print("e6711b998b07 NOT found in zeus jobs.values(); checking raw dict keys")
    if isinstance(raw, dict):
        for k,v in raw.items():
            if 'e6711b' in str(k) or 'e6711b' in str(v):
                print("raw key match:", k)
