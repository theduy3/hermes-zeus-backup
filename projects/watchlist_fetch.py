#!/usr/bin/env python3
import json, urllib.request, urllib.parse, ssl, time, concurrent.futures
from datetime import datetime, timezone

ctx = ssl.create_default_context()

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

def fetch_chart(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(ticker)}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
            data = json.loads(r.read().decode())
        result = data["chart"]["result"][0]
        meta = result.get("meta", {})
        quotes = result["indicators"]["quote"][0]
        closes = [c for c in quotes.get("close", []) if c is not None]
        price = meta.get("regularMarketPrice") or (closes[-1] if closes else None)
        prev = meta.get("chartPreviousClose") or meta.get("previousClose")
        if prev is None and len(closes) >= 2:
            prev = closes[-2]
        chg = None
        if price is not None and prev not in (None, 0):
            chg = (price / prev - 1) * 100
        ts = meta.get("regularMarketTime")
        asof = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat() if ts else None
        return {"ticker": ticker, "price": price, "prev": prev, "chg": chg, "currency": meta.get("currency"), "asof": asof, "ok": True}
    except Exception as e:
        return {"ticker": ticker, "ok": False, "err": str(e)}

def fetch_modules(ticker):
    modules = "defaultKeyStatistics,financialData,summaryDetail"
    url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(ticker)}?modules={modules}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    out = {"ticker": ticker}
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
            data = json.loads(r.read().decode())
        res = data["quoteSummary"]["result"][0]
        dks = res.get("defaultKeyStatistics") or {}
        fd = res.get("financialData") or {}
        sd = res.get("summaryDetail") or {}
        def g(d, k):
            v = d.get(k)
            if isinstance(v, dict):
                return v.get("raw", v.get("fmt"))
            return v
        out.update({
            "forwardPE": g(dks, "forwardPE") or g(sd, "forwardPE"),
            "trailingPE": g(dks, "trailingPE") or g(sd, "trailingPE"),
            "peg": g(dks, "pegRatio"),
            "fcf": g(fd, "freeCashflow"),
            "opcf": g(fd, "operatingCashflow"),
            "roe": g(fd, "returnOnEquity"),
            "roa": g(fd, "returnOnAssets"),
            "profitMargin": g(fd, "profitMargins"),
            "revGrowth": g(fd, "revenueGrowth"),
            "earningsGrowth": g(fd, "earningsGrowth"),
            "targetMean": g(fd, "targetMeanPrice"),
            "rec": g(fd, "recommendationKey"),
            "ok": True
        })
    except Exception as e:
        out["ok"] = False
        out["err"] = str(e)
    return out

def fetch_quote_v7(tickers_batch):
    q = ",".join(tickers_batch)
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={urllib.parse.quote(q, safe=',')}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.loads(r.read().decode())
        return {x["symbol"]: x for x in data.get("quoteResponse", {}).get("result", [])}
    except Exception as e:
        return {"_error": str(e)}

charts = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
    for res in ex.map(fetch_chart, tickers):
        charts[res["ticker"]] = res

modules = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    for res in ex.map(fetch_modules, tickers):
        modules[res["ticker"]] = res

quotes = {}
for i in range(0, len(tickers), 20):
    batch = tickers[i:i+20]
    q = fetch_quote_v7(batch)
    if "_error" in q and len(q) == 1:
        print("quote batch error", q)
    else:
        quotes.update({k: v for k, v in q.items() if k != "_error"})
    time.sleep(0.2)

print("ASOF_RUN", datetime.now(timezone.utc).isoformat())
for t in tickers:
    c = charts.get(t, {})
    m = modules.get(t, {})
    q = quotes.get(t, {})
    fpe = m.get("forwardPE")
    if fpe is None:
        fpe = q.get("forwardPE")
    peg = m.get("peg")
    if peg is None:
        peg = q.get("pegRatio")
    price = c.get("price")
    if price is None:
        price = q.get("regularMarketPrice")
    chg = c.get("chg")
    if chg is None and q.get("regularMarketChangePercent") is not None:
        chg = q.get("regularMarketChangePercent")
    print(json.dumps({
        "t": t,
        "price": price,
        "chg": chg,
        "fpe": fpe,
        "tpe": m.get("trailingPE") or q.get("trailingPE"),
        "peg": peg,
        "fcf": m.get("fcf"),
        "roe": m.get("roe"),
        "roa": m.get("roa"),
        "eg": m.get("earningsGrowth"),
        "rg": m.get("revGrowth"),
        "rec": m.get("rec") or q.get("averageAnalystRating"),
        "tgt": m.get("targetMean") or q.get("targetMeanPrice"),
        "curr": c.get("currency") or q.get("currency"),
        "asof": c.get("asof"),
        "chart_ok": c.get("ok"),
        "mod_ok": m.get("ok"),
        "q_ok": bool(q),
        "cerr": c.get("err"),
        "merr": m.get("err"),
    }))
