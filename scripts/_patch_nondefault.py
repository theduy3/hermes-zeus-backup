import json, os
BASE=os.path.expanduser('~/.hermes')

# profile -> (jobs.json path, default nous model)
PROFILES = {
    'catthew': ('profiles/catthew/cron/jobs.json', 'tencent/hy3:free'),
    'thor':    ('profiles/thor/cron/jobs.json',    'tencent/hy3:free'),
    'wiki':    ('profiles/wiki/cron/jobs.json',    'tencent/hy3:free'),
    'zeus':    ('profiles/zeus/cron/jobs.json',    'tencent/hy3:free'),
}
# job_id -> profile
JOB2PROF = {
    'f1f1cdddc83e':'catthew',
    'f27f8a01f65a':'thor',
    'b92449d7f332':'wiki','ce61f73456fe':'wiki','e358e0a4cb18':'wiki',
    '1b7bcc26dda2':'wiki','2f8f46180850':'wiki','2346506d909a':'wiki',
    'e6711b998b07':'zeus','b83af24484d0':'zeus',
}

changed=[]
for jid, prof in JOB2PROF.items():
    rel, model = PROFILES[prof]
    p = os.path.join(BASE, rel)
    raw = json.load(open(p))
    jobs = raw.get('jobs') if isinstance(raw, dict) else raw
    for j in jobs:
        if not isinstance(j, dict): continue
        key = j.get('job_id') or j.get('id')
        if key != jid: continue
        old_prov, old_model = j.get('provider'), j.get('model')
        j['provider'] = 'nous'
        j['model'] = model
        # clear stale block state so scheduler re-validates cleanly
        if j.get('last_status') == 'blocked_config':
            j['last_status'] = 'pending'
        if j.get('last_error'):
            j['last_error'] = None
        if 'preflight_alerted' in j:
            j['preflight_alerted'] = False
        changed.append((prof, jid, old_prov, old_model, 'nous', model))
        break
    json.dump(raw, open(p,'w'), indent=1)

print("Patched (profile, job_id, old_provider, old_model -> new_provider/new_model):")
for c in changed:
    print(f"  {c[0]:8} {c[1]}  {str(c[2]):13}->{str(c[3]):15} => {c[4]}/{c[5]}")
print(f"\nTotal patched: {len(changed)}")
