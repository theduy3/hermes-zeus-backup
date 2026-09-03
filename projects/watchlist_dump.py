#!/usr/bin/env python3
import json
d=json.load(open('/home/hermes/.hermes/projects/watchlist_data.json'))
print('asof', d['asof_run'])
print('err count', len(d['errors']))
ok=0
for t,c in sorted(d['charts'].items()):
    if c.get('ok') and c.get('price') is not None:
        ok+=1
        chg=c.get('chg_pct')
        chgs=f"{chg:.2f}" if chg is not None else "None"
        print(f"{t}\t{c['price']:.4f}\t{chgs}\t{c.get('asof')}\t{c.get('currency')}")
    else:
        print(f"{t}\tFAIL\t{c.get('err')}")
print('ok', ok)
