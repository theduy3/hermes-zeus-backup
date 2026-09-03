#!/usr/bin/env python3
import json, urllib.request, ssl
ctx=ssl.create_default_context()
UA={"User-Agent":"Mozilla/5.0"}
for t in ["BITF","BITF.TO","BITF.NE"]:
    url=f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=5d&interval=1d"
    try:
        req=urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            d=json.loads(r.read().decode())
        res=(d.get("chart") or {}).get("result")
        if res:
            m=res[0]["meta"]
            q=(res[0].get("indicators") or {}).get("quote",[{}])[0]
            closes=[c for c in (q.get("close") or []) if c is not None]
            price=m.get("regularMarketPrice") or (closes[-1] if closes else None)
            prev=m.get("chartPreviousClose") or m.get("previousClose")
            chg=((price-prev)/prev*100) if price and prev else None
            print(t, "OK", price, chg, m.get("currency"), m.get("exchangeName"))
        else:
            print(t, "ERR", (d.get("chart") or {}).get("error"))
    except Exception as e:
        print(t, "EX", e)
