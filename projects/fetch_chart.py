#!/usr/bin/env python3
import json, urllib.request, urllib.error, time, sys

tickers = [
    "MSFT","AMZN","GOOG","META","AAPL",
    "CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS",
    "TSLA","NFLX","MELI",
    "HD","LOW","WMT","TGT",
    "ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC",
    "BE","APLD","TE","PSIX","GLW","BW","PUMP",
    "IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE",
    "VFV.TO","GLD","SMH",
    "SPCX","RKLB","SEI","WYFI","CRCL",
]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
hosts = ["query1.finance.yahoo.com", "query2.finance.yahoo.com"]

def get(url):
    last = None
    for h in hosts:
        u = url.replace("__HOST__", h)
        try:
            req = urllib.request.Request(u, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.load(r)
        except Exception as e:
            last = e
    if last is None:
        raise RuntimeError("all hosts failed")
    raise last

def chart(sym):
    url = "https://__HOST__/v8/finance/chart/{}?range=5d&interval=1d".format(sym)
    d = get(url)
    res = d["chart"]["result"][0]
    meta = res["meta"]
    closes = [c for c in res["indicators"]["quote"][0]["close"] if c is not None]
    last = closes[-1]
    prev = closes[-2] if len(closes) >= 2 else meta.get("chartPreviousClose", last)
    chg = (last - prev) / prev * 100 if prev else None
    return {
        "price": last,
        "prev": prev,
        "chg": chg,
        "currency": meta.get("currency"),
        "exchange": meta.get("exchangeName"),
        "name": meta.get("shortName"),
        "time": meta.get("regularMarketTime"),
    }

def summary(sym):
    url = "https://__HOST__/v10/finance/quoteSummary/{}?modules=summaryDetail,defaultKeyStatistics,financialData".format(sym)
    try:
        d = get(url)
        r = d["quoteSummary"]["result"][0]
        sd = r.get("summaryDetail", {})
        fwd = sd.get("forwardPE", {}).get("raw")
        trl = sd.get("trailingPE", {}).get("raw")
        # try defaultKeyStatistics as backup
        if fwd is None:
            dks = r.get("defaultKeyStatistics", {})
            fwd = dks.get("forwardPE", {}).get("raw")
        return {"fwdPE": fwd, "trlPE": trl}
    except Exception as e:
        return {"fwdPE": None, "trlPE": None, "err": str(e)}

out = {}
for sym in tickers:
    rec = {}
    try:
        rec.update(chart(sym))
    except Exception as e:
        rec["chart_err"] = str(e)
    time.sleep(0.15)
    try:
        rec.update(summary(sym))
    except Exception as e:
        rec["summary_err"] = str(e)
    out[sym] = rec
    time.sleep(0.15)

print(json.dumps(out, indent=2))
