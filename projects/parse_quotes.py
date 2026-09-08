#!/usr/bin/env python3
import json
d=json.load(open('/tmp/wl_quotes.json'))
print('asof', d['asof_utc'])
miss_pe=[]; miss_px=[]
for t,v in d['data'].items():
    pe=v.get('forwardPE'); px=v.get('price'); peg=v.get('peg'); fcf=v.get('freeCashflow'); roe=v.get('returnOnEquity')
    print(f"{t}\tpx={px}\tch={v.get('chg')}\tfpe={pe}\tpeg={peg}\tfcf={fcf}\troe={roe}\troa={v.get('returnOnAssets')}\teg={v.get('earningsGrowth')}\trg={v.get('revenueGrowth')}\trec={v.get('recommendationKey')}\ttgt={v.get('targetMeanPrice')}\thasq={v.get('has_quote')}\tqs={v.get('qs_err')}")
    if pe is None: miss_pe.append(t)
    if px is None: miss_px.append(t)
print('miss px', miss_px)
print('miss fpe count', len(miss_pe), miss_pe)
print('err file:')
try:
    print(open('/tmp/wl_quotes_err.txt').read()[:2000])
except Exception as e:
    print(e)
