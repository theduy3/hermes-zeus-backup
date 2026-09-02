#!/usr/bin/env python3
import json, urllib.request, ssl
from datetime import datetime, timezone
import concurrent.futures

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

def fetch_chart(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.request.quote(t)}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.load(r)
        res = data["chart"]["result"][0]
        meta = res.get("meta", {})
        ts = res.get("timestamp") or []
        q = res["indicators"]["quote"][0]
        closes = q.get("close") or []
        pairs = [(ts[i], closes[i]) for i in range(len(closes)) if closes[i] is not None]
        if not pairs:
            return {"t": t, "err": "no closes"}
        last_ts, last = pairs[-1]
        prior = pairs[-2][1] if len(pairs) >= 2 else meta.get("chartPreviousClose") or meta.get("previousClose")
        price = meta.get("regularMarketPrice") or last
        prev = meta.get("chartPreviousClose") or meta.get("previousClose") or prior
        chg = None
        if prev and prev != 0:
            chg = (price - prev) / prev * 100.0
        return {
            "t": t,
            "price": price,
            "prev": prev,
            "chg": chg,
            "last_close": last,
            "last_ts": last_ts,
            "currency": meta.get("currency"),
            "exch": meta.get("exchangeName"),
            "asof": datetime.fromtimestamp(last_ts, tz=timezone.utc).isoformat() if last_ts else None,
        }
    except Exception as e:
        return {"t": t, "err": str(e)}

def fetch_modules(t):
    modules = "defaultKeyStatistics,financialData,summaryDetail"
    url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{urllib.request.quote(t)}?modules={modules}"
    req = urllib.request.Request(url, headers=UA)
    out = {"t": t}
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.load(r)
        res = data["quoteSummary"]["result"][0]
        dks = res.get("defaultKeyStatistics") or {}
        fd = res.get("financialData") or {}
        sd = res.get("summaryDetail") or {}
        def gv(d, k):
            v = d.get(k)
            if isinstance(v, dict):
                return v.get("raw", v.get("fmt"))
            return v
        out["fwdPE"] = gv(dks, "forwardPE") or gv(sd, "forwardPE")
        out["trailPE"] = gv(dks, "trailingPE") or gv(sd, "trailingPE")
        out["peg"] = gv(dks, "pegRatio")
        out["roe"] = gv(fd, "returnOnEquity")
        out["fcf"] = gv(fd, "freeCashflow")
        out["opcf"] = gv(fd, "operatingCashflow")
        out["rec"] = gv(fd, "recommendationKey")
        out["target"] = gv(fd, "targetMeanPrice")
        out["profitM"] = gv(fd, "profitMargins")
        out["revGrowth"] = gv(fd, "revenueGrowth")
        out["earnGrowth"] = gv(fd, "earningsGrowth")
        return out
    except Exception as e:
        out["err"] = str(e)
        return out

def main():
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(fetch_chart, t): t for t in tickers}
        for f in concurrent.futures.as_completed(futs):
            r = f.result()
            results[r["t"]] = r

    mods = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(fetch_modules, t): t for t in tickers}
        for f in concurrent.futures.as_completed(futs):
            r = f.result()
            mods[r["t"]] = r

    merged = []
    for t in tickers:
        m = {**results.get(t, {}), **{k: v for k, v in mods.get(t, {}).items() if k != "t"}}
        merged.append(m)

    out = {"fetched_at": datetime.now(timezone.utc).isoformat(), "n": len(merged), "rows": merged}
    with open("/home/hermes/.hermes/projects/watchlist_data.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    # compact summary for stdout
    for m in merged:
        t = m.get("t")
        if m.get("err") and "price" not in m:
            print(f"{t}\tERR\t{m.get('err')}")
        else:
            pe = m.get("fwdPE")
            peg = m.get("peg")
            fcf = m.get("fcf")
            print(f"{t}\t{m.get('price')}\t{m.get('chg')}\t{pe}\t{peg}\t{fcf}\t{m.get('roe')}\t{m.get('earnGrowth')}\t{m.get('asof')}")

if __name__ == "__main__":
    main()
