#!/usr/bin/env python3
import json, urllib.request, urllib.parse, ssl
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
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.loads(r.read().decode())
        result = data["chart"]["result"][0]
        meta = result.get("meta", {})
        quotes = result.get("indicators", {}).get("quote", [{}])[0]
        closes = [c for c in (quotes.get("close") or []) if c is not None]
        price = meta.get("regularMarketPrice")
        prev = meta.get("chartPreviousClose") or meta.get("previousClose")
        chg_pct = meta.get("regularMarketChangePercent")
        if price is None and closes:
            price = closes[-1]
        if prev is None and len(closes) >= 2:
            prev = closes[-2]
        if chg_pct is None and price is not None and prev:
            chg_pct = (price - prev) / prev * 100.0
        return {
            "t": t, "price": price, "prev": prev, "chg": chg_pct,
            "currency": meta.get("currency"),
            "asof": meta.get("regularMarketTime"),
            "tz": meta.get("timezone"),
            "err": None,
        }
    except Exception as e:
        return {"t": t, "price": None, "prev": None, "chg": None, "err": str(e)}

def fetch_quote_summary(t):
    modules = "summaryDetail,defaultKeyStatistics,financialData,price"
    url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(t)}?modules={modules}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.loads(r.read().decode())
        res = data["quoteSummary"]["result"][0]
        sd = res.get("summaryDetail") or {}
        ks = res.get("defaultKeyStatistics") or {}
        fd = res.get("financialData") or {}
        pr = res.get("price") or {}
        def gv(d, k):
            v = d.get(k)
            if isinstance(v, dict):
                return v.get("raw", v.get("fmt"))
            return v
        return {
            "t": t,
            "trailingPE": gv(sd, "trailingPE") or gv(ks, "trailingPE"),
            "forwardPE": gv(sd, "forwardPE") or gv(ks, "forwardPE"),
            "peg": gv(ks, "pegRatio"),
            "marketCap": gv(sd, "marketCap") or gv(pr, "marketCap"),
            "targetMean": gv(fd, "targetMeanPrice"),
            "recKey": gv(fd, "recommendationKey"),
            "roe": gv(fd, "returnOnEquity"),
            "roic_proxy": gv(fd, "returnOnAssets"),
            "profitMargin": gv(fd, "profitMargins"),
            "fcf": gv(fd, "freeCashflow"),
            "opcf": gv(fd, "operatingCashflow"),
            "revGrowth": gv(fd, "revenueGrowth"),
            "earningsGrowth": gv(fd, "earningsGrowth"),
            "err": None,
        }
    except Exception as e:
        return {"t": t, "err": str(e)}

out = {}
with ThreadPoolExecutor(max_workers=10) as ex:
    futs = {ex.submit(fetch_chart, t): t for t in tickers}
    for f in as_completed(futs):
        r = f.result()
        out[r["t"]] = r

qs = {}
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(fetch_quote_summary, t): t for t in tickers}
    for f in as_completed(futs):
        r = f.result()
        qs[r["t"]] = r

def fmt(x, n=2):
    if x is None:
        return None
    try:
        return round(float(x), n)
    except Exception:
        return x

rows = []
for t in tickers:
    c = out.get(t, {})
    s = qs.get(t, {})
    row = {
        "ticker": t,
        "price": fmt(c.get("price"), 2),
        "chg": fmt(c.get("chg"), 2),
        "fwdPE": fmt(s.get("forwardPE"), 2),
        "trailPE": fmt(s.get("trailingPE"), 2),
        "peg": fmt(s.get("peg"), 2),
        "fcf": s.get("fcf"),
        "opcf": s.get("opcf"),
        "roe": fmt(s.get("roe"), 4) if s.get("roe") is not None else None,
        "roa": fmt(s.get("roic_proxy"), 4) if s.get("roic_proxy") is not None else None,
        "earnGr": fmt(s.get("earningsGrowth"), 4) if s.get("earningsGrowth") is not None else None,
        "revGr": fmt(s.get("revGrowth"), 4) if s.get("revGrowth") is not None else None,
        "rec": s.get("recKey"),
        "target": fmt(s.get("targetMean"), 2),
        "currency": c.get("currency"),
        "asof": c.get("asof"),
        "tz": c.get("tz"),
        "chart_err": c.get("err"),
        "qs_err": s.get("err"),
    }
    rows.append(row)

print(json.dumps(rows, indent=2))
