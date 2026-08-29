#!/usr/bin/env python3
import json, urllib.request, urllib.parse, ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

tickers = [
"MSFT","AMZN","GOOG","META","AAPL",
"CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS",
"TSLA","NFLX","MELI",
"HD","LOW","WMT","TGT",
"ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC",
"BE","APLD","TE","PSIX","GLW","BW","PUMP",
"IREN","CORZ","RIOT","CLSK","BTDR","HIVE",
"VFV.TO","GLD","SMH",
"SPCX","RKLB","SEI","WYFI","CRCL"
]

ctx = ssl.create_default_context()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def fetch(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.loads(r.read().decode())
        result = data["chart"]["result"][0]
        meta = result["meta"]
        closes = result["indicators"]["quote"][0]["close"]
        timestamps = result["timestamp"]
        pairs = [(ts, c) for ts, c in zip(timestamps, closes) if c is not None]
        rmp = meta.get("regularMarketPrice")
        prev = meta.get("chartPreviousClose") or meta.get("previousClose")
        # Prefer two last session closes for chg if market closed; if open use rmp vs previousClose
        if rmp is not None and prev:
            price = rmp
            chg = (rmp - prev) / prev * 100.0
            src = "rmp/prev"
        elif len(pairs) >= 2:
            price = pairs[-1][1]
            prev = pairs[-2][1]
            chg = (price - prev) / prev * 100.0
            src = "closes"
        else:
            return t, {"error": "no data"}
        return t, {
            "price": round(price, 2) if price >= 1 else round(price, 4),
            "prev": round(prev, 4),
            "chg": round(chg, 2),
            "src": src,
            "asof": meta.get("regularMarketTime"),
            "currency": meta.get("currency"),
        }
    except Exception as e:
        return t, {"error": str(e)}

out = {}
with ThreadPoolExecutor(max_workers=12) as ex:
    for f in as_completed({ex.submit(fetch, t): t for t in tickers}):
        t, d = f.result()
        out[t] = d

print("ASOF", datetime.now(timezone.utc).isoformat())
for t in tickers:
    print(json.dumps({"t": t, **out.get(t, {})}))
