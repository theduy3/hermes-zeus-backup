#!/usr/bin/env python3
import json
from datetime import datetime, timezone
with open('/tmp/wl_data.json') as f:
    data=json.load(f)
print('asof', data['asof_utc'])
ok=0; fail=[]
for r in data['rows']:
    if r['chart_ok'] and r['price'] is not None:
        ok+=1
        print(f"{r['t']}\t{r['price']}\t{r['chg']}\t{r.get('currency')}\t{r.get('last_ts')}")
    else:
        fail.append((r['t'], r.get('chart_err')))
print('OK', ok, 'FAIL', fail)
ts=[r['last_ts'] for r in data['rows'] if r.get('last_ts')]
if ts:
    t=max(ts)
    print('max ts', t, datetime.fromtimestamp(t, timezone.utc).isoformat())
