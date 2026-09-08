#!/usr/bin/env python3
import json, urllib.request, ssl
ctx=ssl.create_default_context()
UA="Mozilla/5.0"
for t in ["BITF","BITF.TO","BITF.NE","BFARF","BITF.V","BIT.TO","KEEL"]:
    url=f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=5d&interval=1d"
    req=urllib.request.Request(url, headers={"User-Agent":UA})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
            data=json.loads(r.read().decode())
        meta=data["chart"]["result"][0]["meta"]
        print(t, "OK", meta.get("symbol"), meta.get("regularMarketPrice"), meta.get("regularMarketChangePercent"), meta.get("shortName") or meta.get("longName"))
    except Exception as e:
        print(t, "FAIL", e)

d=json.load(open("/tmp/wl_quotes.json"))
for t in ["TE","SEI","SPCX","CRWV","NBIS","CRCL","WYFI","PUMP","BW","PSIX","SNDK","NFLX","ORCL","DELL"]:
    v=d["data"][t]
    print("NAME", t, v.get("shortName"), v.get("quoteType"), "fpe", v.get("forwardPE"), "peg", v.get("peg"))
