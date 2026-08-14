import json, os
BASE=os.path.expanduser('~/.hermes')
f=os.path.join(BASE,'cron/jobs.json')
raw=json.load(open(f))
jobs = raw.get('jobs') if isinstance(raw, dict) else raw
MODEL='upstage/solar-pro4:free'  # default-profile Nous served model
TARGETS={'e83470683a90','c9c38ab77915','8f310c8f4baf','67d44bd30291','067ad023e2d9','12e5ce30563d'}
changed=[]
for j in jobs:
    if not isinstance(j,dict): continue
    key=j.get('job_id') or j.get('id')
    if key in TARGETS:
        old_prov,old_model=j.get('provider'),j.get('model')
        j['provider']='nous'; j['model']=MODEL
        if j.get('last_status')=='blocked_config': j['last_status']='pending'
        if j.get('last_error'): j['last_error']=None
        if 'preflight_alerted' in j: j['preflight_alerted']=False
        changed.append((key,old_prov,old_model))
json.dump(raw,open(f,'w'),indent=1)
print("Default-profile patched:")
for c in changed: print(f"  {c[0]}  {str(c[1]):13}->{str(c[2]):15} => nous/{MODEL}")
print("total:",len(changed))
