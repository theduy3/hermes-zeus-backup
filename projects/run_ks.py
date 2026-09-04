#!/usr/bin/env python3
import json, subprocess, sys
r = subprocess.run([sys.executable, "/home/hermes/.hermes/projects/yh_ks_scrape.py"], capture_output=True, text=True, timeout=180)
open("/tmp/ks_out.json","w").write(r.stdout)
open("/tmp/ks_err.txt","w").write(r.stderr)
print("EXIT", r.returncode)
print("stdout_len", len(r.stdout), "stderr_len", len(r.stderr))
if r.stderr:
    print("STDERR_HEAD", r.stderr[:500])
try:
    d=json.loads(r.stdout)
except Exception as e:
    print("JSON fail", e, r.stdout[:500])
    sys.exit(1)
ok=sum(1 for t,v in d.items() if v.get('fwd_pe') is not None)
err=sum(1 for t,v in d.items() if 'error' in v)
print('fwd_ok',ok,'err',err,'total',len(d))
for t in sorted(d):
    v=d[t]
    print(t, {k:v.get(k) for k in ['fwd_pe','peg','roe','roa','fcf','ocf','pm','error','html_len']})
