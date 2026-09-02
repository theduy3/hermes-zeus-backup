#!/usr/bin/env python3
import json, urllib.request, urllib.parse, ssl, concurrent.futures

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
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def fetch_chart(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=25) as r:
            data = json.loads(r.read().decode())
        res = data["chart"]["result"][0]
        meta = res.get("meta", {})
        ts = res.get("timestamp") or []
        closes = (res.get("indicators") or {}).get("quote", [{}])[0].get("close") or []
        pairs = [(t_, c) for t_, c in zip(ts, closes) if c is not None]
        price = meta.get("regularMarketPrice")
        prev = meta.get("chartPreviousClose") or meta.get("previousClose")
        if pairs:
            if price is None:
                price = pairs[-1][1]
            if prev is None and len(pairs) >= 2:
                prev = pairs[-2][1]
        chg = None
        if price is not None and prev not in (None, 0):
            chg = (price / prev - 1.0) * 100.0
        return {
            "t": t,
            "price": price,
            "prev": prev,
            "chg": chg,
            "currency": meta.get("currency"),
            "name": meta.get("longName") or meta.get("shortName"),
            "mkt_state": meta.get("marketState"),
            "last_ts": pairs[-1][0] if pairs else None,
            "ok": True,
        }
    except Exception as e:
        return {"t": t, "ok": False, "err": str(e)}

def gv(d, k):
    v = (d or {}).get(k)
    if isinstance(v, dict):
        return v.get("raw", v.get("fmt"))
    return v

def fetch_modules(t):
    modules = "defaultKeyStatistics,financialData,summaryDetail,earningsTrend"
    url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(t)}?modules={modules}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=25) as r:
            data = json.loads(r.read().decode())
        res = data.get("quoteSummary", {}).get("result")
        if not res:
            return {"t": t, "ok": False, "err": "no result"}
        res = res[0]
        dks = res.get("defaultKeyStatistics") or {}
        fd = res.get("financialData") or {}
        sd = res.get("summaryDetail") or {}
        et = res.get("earningsTrend") or {}
        out = {"t": t, "ok": True}
        out["forwardPE"] = gv(dks, "forwardPE") or gv(sd, "forwardPE")
        out["trailingPE"] = gv(dks, "trailingPE") or gv(sd, "trailingPE")
        out["peg"] = gv(dks, "pegRatio")
        out["fcf"] = gv(fd, "freeCashflow")
        out["roe"] = gv(fd, "returnOnEquity")
        out["roa"] = gv(fd, "returnOnAssets")
        out["earnGrowth"] = gv(fd, "earningsGrowth")
        out["revGrowth"] = gv(fd, "revenueGrowth")
        out["rec"] = gv(fd, "recommendationKey")
        out["target"] = gv(fd, "targetMeanPrice")
        for tr in (et.get("trend") or []):
            if tr.get("period") in ("0y", "+1y"):
                out[f"growth_{tr.get('period')}"] = gv(tr, "growth")
        return out
    except Exception as e:
        return {"t": t, "ok": False, "err": str(e)}

results = {}
stats = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
    futs = {ex.submit(fetch_chart, t): t for t in tickers}
    for f in concurrent.futures.as_completed(futs):
        r = f.result()
        results[r["t"]] = r

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    futs = {ex.submit(fetch_modules, t): t for t in tickers}
    for f in concurrent.futures.as_completed(futs):
        r = f.result()
        stats[r["t"]] = r

out_rows = []
for t in tickers:
    c = results.get(t, {})
    s = stats.get(t, {})
    row = {
        "ticker": t,
        "price": c.get("price"),
        "chg": c.get("chg"),
        "currency": c.get("currency"),
        "mkt_state": c.get("mkt_state"),
        "last_ts": c.get("last_ts"),
        "forwardPE": s.get("forwardPE"),
        "trailingPE": s.get("trailingPE"),
        "peg": s.get("peg"),
        "fcf": s.get("fcf"),
        "roe": s.get("roe"),
        "earnGrowth": s.get("earnGrowth"),
        "revGrowth": s.get("revGrowth"),
        "growth_0y": s.get("growth_0y"),
        "growth_+1y": s.get("growth_+1y"),
        "rec": s.get("rec"),
        "target": s.get("target"),
        "chart_ok": c.get("ok"),
        "stat_ok": s.get("ok"),
        "chart_err": c.get("err"),
        "stat_err": s.get("err"),
    }
    out_rows.append(row)

print(json.dumps(out_rows, indent=None))
with open("/home/hermes/.hermes/projects/watchlist_daily_out.json", "w") as f:
    json.dump(out_rows, f, indent=2)
print("WROTE", len(out_rows), "rows", file=__import__("sys").stderr)
