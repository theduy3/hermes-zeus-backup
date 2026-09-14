#!/usr/bin/env python3
import json, urllib.request, urllib.parse, urllib.error, ssl, datetime, time, random, os

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

OUT = "/home/hermes/.hermes/profiles/charles/tmp_watchlist_prices.json"
ctx = ssl.create_default_context()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

results = {}
if os.path.exists(OUT):
    try:
        with open(OUT) as f:
            results = json.load(f)
    except Exception:
        results = {}

def fetch_chart(t, attempt=1):
    hosts = [
        "https://query1.finance.yahoo.com",
        "https://query2.finance.yahoo.com",
    ]
    host = hosts[(attempt - 1) % len(hosts)]
    url = f"{host}/v8/finance/chart/{urllib.parse.quote(t)}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
    })
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            data = json.loads(r.read().decode())
        if not data.get("chart") or not data["chart"].get("result"):
            err = (data.get("chart") or {}).get("error")
            return {"error": f"no result: {err}"}
        res = data["chart"]["result"][0]
        meta = res.get("meta", {})
        closes = (res.get("indicators") or {}).get("quote", [{}])[0].get("close") or []
        ts = res.get("timestamp") or []
        pairs = [(ts[i], closes[i]) for i in range(min(len(closes), len(ts))) if closes[i] is not None]
        rmp = meta.get("regularMarketPrice")
        pc = meta.get("previousClose") or meta.get("chartPreviousClose")
        if rmp is not None:
            if pc is None and len(pairs) >= 2:
                pc = pairs[-2][1]
            chg = ((rmp - pc) / pc * 100) if pc else None
            return {
                "price": float(rmp),
                "prev": float(pc) if pc is not None else None,
                "chg_pct": chg,
                "currency": meta.get("currency"),
                "name": meta.get("longName") or meta.get("shortName"),
                "last_ts": meta.get("regularMarketTime") or (pairs[-1][0] if pairs else None),
            }
        if not pairs:
            return {"error": "no closes"}
        last_ts, last = pairs[-1]
        prev = pairs[-2][1] if len(pairs) >= 2 else pc
        chg = ((last - prev) / prev * 100) if prev else None
        return {
            "price": float(last),
            "prev": float(prev) if prev is not None else None,
            "chg_pct": chg,
            "currency": meta.get("currency"),
            "name": meta.get("longName") or meta.get("shortName"),
            "last_ts": last_ts,
        }
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "retry": e.code in (429, 500, 502, 503)}
    except Exception as e:
        return {"error": str(e), "retry": True}

pending = [t for t in tickers if "error" in results.get(t, {"error": True}) or "price" not in results.get(t, {})]
print(f"pending {len(pending)} already_ok {len(tickers)-len(pending)}")

for i, t in enumerate(pending):
    ok = False
    for attempt in range(1, 6):
        d = fetch_chart(t, attempt)
        if "price" in d:
            results[t] = d
            chg = f"{d['chg_pct']:.2f}" if d.get("chg_pct") is not None else "—"
            print(f"OK {t}|{d['price']:.4f}|{chg}")
            ok = True
            break
        if d.get("retry"):
            sleep = min(2 ** attempt + random.uniform(0.3, 1.2), 20)
            print(f"RETRY {t} attempt {attempt} {d.get('error')} sleep {sleep:.1f}")
            time.sleep(sleep)
        else:
            results[t] = d
            print(f"FAIL {t}|{d}")
            ok = True
            break
    if not ok:
        results[t] = d
        print(f"GIVEUP {t}|{d}")
    # polite delay between tickers
    time.sleep(0.8 + random.uniform(0.2, 0.7))
    if (i + 1) % 10 == 0:
        with open(OUT, "w") as f:
            json.dump(results, f)

with open(OUT, "w") as f:
    json.dump(results, f)

print("---FINAL---")
for t in tickers:
    d = results.get(t, {})
    if "price" in d:
        chg = f"{d['chg_pct']:.2f}" if d.get("chg_pct") is not None else "—"
        print(f"{t}|{d['price']:.4f}|{chg}|{d.get('currency')}|{d.get('last_ts')}|{d.get('name','')}")
    else:
        print(f"{t}|ERR|{d.get('error')}")

ts_vals = [results[t].get("last_ts") for t in tickers if isinstance(results.get(t, {}).get("last_ts"), (int, float))]
if ts_vals:
    mx = max(ts_vals)
    print("max_last_ts", int(mx), datetime.datetime.utcfromtimestamp(mx).isoformat() + "Z")
