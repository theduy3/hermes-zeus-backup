#!/usr/bin/env python3
import json, urllib.request, urllib.parse, ssl, datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

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
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def fetch_chart(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=25) as r:
            data = json.loads(r.read().decode())
        if not data.get("chart") or not data["chart"].get("result"):
            return t, {"error": "no result", "raw": str(data)[:200]}
        res = data["chart"]["result"][0]
        meta = res.get("meta", {})
        closes = (res.get("indicators") or {}).get("quote", [{}])[0].get("close") or []
        ts = res.get("timestamp") or []
        pairs = [(ts[i], closes[i]) for i in range(min(len(closes), len(ts))) if closes[i] is not None]
        if not pairs:
            # fallback to meta regularMarketPrice
            price = meta.get("regularMarketPrice")
            prev = meta.get("previousClose") or meta.get("chartPreviousClose")
            if price is None:
                return t, {"error": "no closes", "meta_keys": list(meta.keys())}
            chg = ((price - prev) / prev * 100) if prev else None
            return t, {
                "price": price,
                "prev": prev,
                "chg_pct": chg,
                "currency": meta.get("currency"),
                "name": meta.get("longName") or meta.get("shortName"),
                "last_ts": meta.get("regularMarketTime"),
            }
        last_ts, last = pairs[-1]
        prev = pairs[-2][1] if len(pairs) >= 2 else meta.get("previousClose") or meta.get("chartPreviousClose")
        # Prefer regularMarketPrice if present and market may be open
        rmp = meta.get("regularMarketPrice")
        if rmp is not None:
            # use prior close from meta if available for change vs prior session
            pc = meta.get("previousClose") or meta.get("chartPreviousClose") or prev
            chg = ((rmp - pc) / pc * 100) if pc else None
            return t, {
                "price": rmp,
                "prev": pc,
                "chg_pct": chg,
                "currency": meta.get("currency"),
                "name": meta.get("longName") or meta.get("shortName"),
                "last_ts": meta.get("regularMarketTime") or last_ts,
                "from": "meta_rmp",
            }
        chg = ((last - prev) / prev * 100) if prev else None
        return t, {
            "price": last,
            "prev": prev,
            "chg_pct": chg,
            "currency": meta.get("currency"),
            "name": meta.get("longName") or meta.get("shortName"),
            "last_ts": last_ts,
            "from": "close",
        }
    except Exception as e:
        return t, {"error": str(e)}

results = {}
with ThreadPoolExecutor(max_workers=10) as ex:
    futs = [ex.submit(fetch_chart, t) for t in tickers]
    for f in as_completed(futs):
        t, d = f.result()
        results[t] = d

for t in tickers:
    d = results[t]
    if "error" in d:
        print(f"{t}|ERR|{d['error']}")
    else:
        chg = f"{d['chg_pct']:.2f}" if d.get("chg_pct") is not None else "—"
        print(f"{t}|{d['price']:.4f}|{chg}|{d.get('currency')}|{d.get('last_ts')}|{d.get('name','')}")

ts_vals = [results[t].get("last_ts") for t in tickers if isinstance(results[t].get("last_ts"), (int, float))]
if ts_vals:
    mx = max(ts_vals)
    print("---META---")
    print("max_last_ts", int(mx), datetime.datetime.utcfromtimestamp(mx).isoformat() + "Z")

# dump json for later
with open("/home/hermes/.hermes/profiles/charles/tmp_watchlist_prices.json", "w") as f:
    json.dump(results, f)
print("WROTE_JSON")
