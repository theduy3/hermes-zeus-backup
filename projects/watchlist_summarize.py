#!/usr/bin/env python3
import json
with open('/tmp/watchlist_out.json') as f:
    data=json.load(f)
rows=data['rows']
ok=sum(1 for r in rows if r.get('price') is not None)
err=sum(1 for r in rows if r.get('error'))
qs_err=sum(1 for r in rows if r.get('qs_error'))
fwd=sum(1 for r in rows if r.get('fwd_pe') is not None)
print(f"price_ok={ok} chart_err={err} qs_err={qs_err} fwd_pe_ok={fwd} total={len(rows)}")
for r in rows:
    e=r.get('error')
    print(f"{r['ticker']}\tpx={r.get('price')}\tchg={r.get('chg_pct')}\tfwd={r.get('fwd_pe')}\tpeg={r.get('peg')}\tfcf={r.get('fcf')}\troe={r.get('roe')}\terr={e}\tqs={r.get('qs_error')}")
