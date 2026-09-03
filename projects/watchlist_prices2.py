#!/usr/bin/env python3
import json, urllib.request, urllib.parse, ssl, concurrent.futures, time
from datetime import datetime, timezone

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
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def fetch(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(ticker)}?range=10d&interval=1d"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, context=ctx, timeout=25) as r:
            data = json.loads(r.read().decode())
        res = data["chart"]["result"][0]
        meta = res["meta"]
        ts = res.get("timestamp") or []
        q = (res.get("indicators") or {}).get("quote", [{}])[0]
        closes = q.get("close") or []
        # build pairs of valid closes with timestamps
        pairs = [(t,c) for t,c in zip(ts, closes) if c is not None]
        price = meta.get("regularMarketPrice")
        if price is None and pairs:
            price = pairs[-1][1]
        # prior close = last completed daily close before today if possible
        prev = None
        if len(pairs) >= 2:
            # if last pair is today (same calendar day as regularMarketTime), use previous
            rt = meta.get("regularMarketTime")
            last_t, last_c = pairs[-1]
            # always use second-to-last daily close as prior session close when we have live price
            prev = pairs[-2][1]
            # if market closed and last close equals price, still use pairs[-2]
        if prev is None:
            prev = meta.get("previousClose") or meta.get("chartPreviousClose")
        chg = ((price - prev) / prev * 100.0) if (price is not None and prev) else None
        asof = datetime.fromtimestamp(meta["regularMarketTime"], tz=timezone.utc).isoformat() if meta.get("regularMarketTime") else None
        return {
            "ticker": ticker,
            "price": price,
            "prev": prev,
            "chg_pct": chg,
            "currency": meta.get("currency"),
            "asof": asof,
            "last_closes": [p[1] for p in pairs[-5:]],
            "ok": True,
        }
    except Exception as e:
        return {"ticker": ticker, "ok": False, "err": str(e)}

out = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    for fut in concurrent.futures.as_completed({ex.submit(fetch, t): t for t in tickers}):
        r = fut.result()
        out[r["ticker"]] = r
        time.sleep(0.01)

with open("/home/hermes/.hermes/projects/watchlist_prices2.json","w") as f:
    json.dump({"asof_run": datetime.now(timezone.utc).isoformat(), "data": out}, f)
for t in tickers:
    r = out[t]
    if r.get("ok"):
        print(f"{t}\t{r['price']}\t{r['chg_pct']}\tprev={r['prev']}\tcloses={r.get('last_closes')}")
    else:
        print(t, "FAIL", r.get("err"))
