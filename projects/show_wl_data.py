#!/usr/bin/env python3
import json
p='/home/hermes/.hermes/projects/daily_watchlist_data.json'
d=json.load(open(p))
ok=sum(1 for r in d if r.get('price') is not None)
print('rows',len(d),'prices',ok)
for r in d:
    if r.get('price') is not None:
        print(r['ticker'], r['price'], r.get('chg'), r.get('fwdPE'), r.get('peg'), r.get('qs_err'))
