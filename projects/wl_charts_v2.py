#!/usr/bin/env python3
import json, urllib.request, urllib.parse, ssl, concurrent.futures, datetime

ctx = ssl.create_default_context()
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}

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

def fetch_chart(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.loads(r.read().decode())
        result = data["chart"]["result"][0]
        meta = result["meta"]
        ts = result.get("timestamp") or []
        q = result["indicators"]["quote"][0]
        closes = q["close"]
        # build pairs of valid close days
        days = []
        for i, c in enumerate(closes):
            if c is not None:
                days.append((ts[i] if i < len(ts) else None, c))
        price = meta.get("regularMarketPrice")
        if price is None and days:
            price = days[-1][1]
        # Prefer meta previous close for "daily" change vs last session
        prev = meta.get("regularMarketPreviousClose")
        if prev is None and len(days) >= 2:
            # if last day close == price (market closed), use prior day
            prev = days[-2][1]
        elif prev is None and days:
            prev = meta.get("chartPreviousClose")
        chg = ((price - prev) / prev * 100.0) if (price is not None and prev) else None
        # also compute last-two-closes change for cross-check
        chg2 = None
        if len(days) >= 2:
            chg2 = (days[-1][1] - days[-2][1]) / days[-2][1] * 100.0
        return {
            "t": t, "ok": True, "price": price, "prev": prev, "chg": chg, "chg2": chg2,
            "ccy": meta.get("currency"),
            "ts": meta.get("regularMarketTime"),
            "days": [(datetime.datetime.utcfromtimestamp(d[0]).strftime("%Y-%m-%d") if d[0] else None, d[1]) for d in days],
            "symbol": meta.get("symbol"),
        }
    except Exception as e:
        return {"t": t, "ok": False, "err": str(e)[:200]}

out = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
    for r in ex.map(fetch_chart, tickers):
        out[r["t"]] = r

print(json.dumps(out, indent=2, default=str))
