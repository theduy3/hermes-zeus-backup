#!/usr/bin/env python3
import json, urllib.request, urllib.parse, ssl, time, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
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
headers = {"User-Agent": "Mozilla/5.0 (compatible; research/1.0)"}

def fetch_chart(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.loads(r.read().decode())
        if not data.get("chart") or not data["chart"].get("result"):
            return {"t": t, "ok": False, "err": "no result"}
        result = data["chart"]["result"][0]
        meta = result["meta"]
        ts = result.get("timestamp") or []
        quote = (result.get("indicators") or {}).get("quote") or [{}]
        closes = quote[0].get("close") or []
        pairs = [(ts[i], closes[i]) for i in range(len(closes)) if i < len(ts) and closes[i] is not None]
        # Prefer meta regular market when available for latest
        last = meta.get("regularMarketPrice")
        prev = meta.get("chartPreviousClose") or meta.get("previousClose")
        last_ts = meta.get("regularMarketTime")
        chg_meta = meta.get("regularMarketChangePercent")
        if last is None and pairs:
            last = pairs[-1][1]
            last_ts = pairs[-1][0]
        if prev is None and len(pairs) >= 2:
            prev = pairs[-2][1]
        if chg_meta is not None:
            chg = float(chg_meta)
        elif last is not None and prev not in (None, 0):
            chg = (last - prev) / prev * 100.0
        else:
            chg = None
        return {
            "t": t,
            "price": last,
            "prev": prev,
            "chg": chg,
            "currency": meta.get("currency"),
            "exchange": meta.get("exchangeName"),
            "last_ts": last_ts,
            "symbol": meta.get("symbol"),
            "name": meta.get("shortName") or meta.get("longName"),
            "ok": True,
        }
    except Exception as e:
        return {"t": t, "ok": False, "err": str(e)}

def fetch_quote_summary(t):
    """Try modules for forwardPE, trailingPE, peg, etc."""
    modules = "defaultKeyStatistics,summaryDetail,financialData,price"
    url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(t)}?modules={modules}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.loads(r.read().decode())
        res = data.get("quoteSummary", {}).get("result")
        if not res:
            return {"t": t, "ok": False, "err": "no qs"}
        r0 = res[0]
        dks = r0.get("defaultKeyStatistics") or {}
        sd = r0.get("summaryDetail") or {}
        fd = r0.get("financialData") or {}
        def raw(x):
            if x is None:
                return None
            if isinstance(x, dict):
                return x.get("raw", x.get("fmt"))
            return x
        return {
            "t": t,
            "ok": True,
            "forwardPE": raw(dks.get("forwardPE")) or raw(sd.get("forwardPE")),
            "trailingPE": raw(dks.get("trailingPE")) or raw(sd.get("trailingPE")),
            "peg": raw(dks.get("pegRatio")),
            "enterpriseToEbitda": raw(dks.get("enterpriseToEbitda")),
            "profitMargins": raw(fd.get("profitMargins")),
            "revenueGrowth": raw(fd.get("revenueGrowth")),
            "freeCashflow": raw(fd.get("freeCashflow")),
            "operatingCashflow": raw(fd.get("operatingCashflow")),
            "returnOnEquity": raw(fd.get("returnOnEquity")),
            "returnOnAssets": raw(fd.get("returnOnAssets")),
            "recommendationKey": (fd.get("recommendationKey") if isinstance(fd.get("recommendationKey"), str) else raw(fd.get("recommendationKey"))),
            "targetMeanPrice": raw(fd.get("targetMeanPrice")),
            "currentPrice": raw(fd.get("currentPrice")),
        }
    except Exception as e:
        return {"t": t, "ok": False, "err": str(e)}

results = {}
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(fetch_chart, t): t for t in tickers}
    for f in as_completed(futs):
        r = f.result()
        results[r["t"]] = r

qs = {}
with ThreadPoolExecutor(max_workers=4) as ex:
    futs = {ex.submit(fetch_quote_summary, t): t for t in tickers}
    for f in as_completed(futs):
        r = f.result()
        qs[r["t"]] = r
        time.sleep(0.05)

out = []
for t in tickers:
    r = results.get(t, {})
    q = qs.get(t, {})
    row = {
        "t": t,
        "price": r.get("price"),
        "chg": r.get("chg"),
        "currency": r.get("currency"),
        "last_ts": r.get("last_ts"),
        "chart_ok": r.get("ok"),
        "chart_err": r.get("err"),
        "forwardPE": q.get("forwardPE"),
        "trailingPE": q.get("trailingPE"),
        "peg": q.get("peg"),
        "freeCashflow": q.get("freeCashflow"),
        "returnOnEquity": q.get("returnOnEquity"),
        "returnOnAssets": q.get("returnOnAssets"),
        "revenueGrowth": q.get("revenueGrowth"),
        "recommendationKey": q.get("recommendationKey"),
        "targetMeanPrice": q.get("targetMeanPrice"),
        "qs_ok": q.get("ok"),
        "qs_err": q.get("err"),
        "name": r.get("name"),
    }
    out.append(row)

print(json.dumps({"asof_utc": datetime.now(timezone.utc).isoformat(), "rows": out}, indent=2, default=str))
