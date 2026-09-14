#!/usr/bin/env python3
import json, urllib.request, urllib.parse, time, ssl

tickers = [
"MSFT","AMZN","GOOG","META","AAPL",
"CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS",
"TSLA","NFLX","MELI",
"HD","LOW","WMT","TGT",
"ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC",
"BE","APLD","TE","PSIX","GLW","BW","PUMP",
"IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE",
"VFV.TO","GLD","SMH",
"SPCX","RKLB","SEI","WYFI","CRCL"
]

ctx = ssl.create_default_context()
results = {}

def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    })
    with urllib.request.urlopen(req, context=ctx, timeout=timeout) as r:
        return json.loads(r.read().decode())

for t in tickers:
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t, safe='')}?range=5d&interval=1d"
        data = fetch(url)
        result = data["chart"]["result"][0]
        meta = result["meta"]
        closes = result["indicators"]["quote"][0]["close"]
        timestamps = result["timestamp"]
        pairs = [(ts, c) for ts, c in zip(timestamps, closes) if c is not None]
        if len(pairs) >= 2:
            prev_close = pairs[-2][1]
            last_close = pairs[-1][1]
            last_ts = pairs[-1][0]
        elif len(pairs) == 1:
            last_close = pairs[0][1]
            prev_close = meta.get("previousClose") or meta.get("chartPreviousClose")
            last_ts = pairs[0][0]
        else:
            last_close = meta.get("regularMarketPrice")
            prev_close = meta.get("previousClose") or meta.get("chartPreviousClose")
            last_ts = meta.get("regularMarketTime")
        rmp = meta.get("regularMarketPrice")
        if rmp is not None:
            last_close = rmp
        prev_for_chg = meta.get("previousClose") or meta.get("chartPreviousClose") or prev_close
        chg = None
        if last_close is not None and prev_for_chg:
            chg = (last_close - prev_for_chg) / prev_for_chg * 100.0
        results[t] = {
            "price": last_close,
            "prev": prev_for_chg,
            "chg_pct": chg,
            "currency": meta.get("currency"),
            "ts": last_ts,
            "exchange": meta.get("exchangeName"),
            "ok": True
        }
    except Exception as e:
        results[t] = {"ok": False, "err": str(e)}
    time.sleep(0.05)

print(json.dumps(results, indent=2))
