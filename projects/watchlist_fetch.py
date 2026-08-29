#!/usr/bin/env python3
import json, urllib.request, urllib.parse, ssl
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
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def gv(obj, key):
    if not obj:
        return None
    v = obj.get(key)
    if isinstance(v, dict):
        return v.get("raw", v.get("fmt"))
    return v

def fetch_chart(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.loads(r.read().decode())
        result = data["chart"]["result"][0]
        meta = result["meta"]
        closes = result["indicators"]["quote"][0]["close"]
        timestamps = result["timestamp"]
        pairs = [(ts, c) for ts, c in zip(timestamps, closes) if c is not None]
        if not pairs:
            # fallback to meta regularMarketPrice
            p = meta.get("regularMarketPrice")
            prev = meta.get("previousClose") or meta.get("chartPreviousClose")
            chg = ((p - prev) / prev * 100.0) if p and prev else None
            return t, {"price": p, "chg": round(chg, 2) if chg is not None else None, "asof_ts": meta.get("regularMarketTime"), "src": "meta"}
        last_ts, last = pairs[-1]
        prev = pairs[-2][1] if len(pairs) >= 2 else meta.get("previousClose") or meta.get("chartPreviousClose")
        # Prefer regularMarketPrice if present and fresher feel
        rmp = meta.get("regularMarketPrice")
        if rmp is not None:
            last = rmp
            prev_m = meta.get("previousClose") or meta.get("chartPreviousClose") or prev
            if prev_m:
                prev = prev_m
        chg = ((last - prev) / prev * 100.0) if prev else None
        price = round(last, 2) if last >= 1 else round(last, 4)
        return t, {
            "price": price,
            "prev": prev,
            "chg": round(chg, 2) if chg is not None else None,
            "asof_ts": meta.get("regularMarketTime") or last_ts,
            "currency": meta.get("currency"),
        }
    except Exception as e:
        return t, {"error": str(e)}

def fetch_quote_summary(t):
    modules = "defaultKeyStatistics,financialData,summaryDetail,earningsTrend"
    url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(t)}?modules={modules}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.loads(r.read().decode())
        res = data["quoteSummary"]["result"][0]
        dks = res.get("defaultKeyStatistics") or {}
        fd = res.get("financialData") or {}
        sd = res.get("summaryDetail") or {}
        et = res.get("earningsTrend") or {}
        fpe = gv(dks, "forwardPE") or gv(sd, "forwardPE")
        tpe = gv(dks, "trailingPE") or gv(sd, "trailingPE")
        peg = gv(dks, "pegRatio")
        fcf = gv(fd, "freeCashflow")
        roe = gv(fd, "returnOnEquity")
        roa = gv(fd, "returnOnAssets")
        rev_g = gv(fd, "revenueGrowth")
        earn_g = gv(fd, "earningsGrowth")
        rec = gv(fd, "recommendationKey")
        target = gv(fd, "targetMeanPrice")
        trend_growth = None
        try:
            for tr in (et.get("trend") or []):
                if tr.get("period") == "0y":
                    g = tr.get("growth")
                    if isinstance(g, dict):
                        trend_growth = g.get("raw")
                    break
        except Exception:
            pass
        # next year growth +0y already; also try +1y
        growth_1y = None
        try:
            for tr in (et.get("trend") or []):
                if tr.get("period") == "+1y":
                    g = tr.get("growth")
                    if isinstance(g, dict):
                        growth_1y = g.get("raw")
        except Exception:
            pass
        def rnd(x, n=2):
            if isinstance(x, (int, float)):
                return round(x, n)
            return x
        return t, {
            "fwdPE": rnd(fpe),
            "trailPE": rnd(tpe),
            "peg": rnd(peg),
            "fcf": fcf,
            "roe": rnd(roe, 4) if isinstance(roe, (int, float)) else roe,
            "roa": rnd(roa, 4) if isinstance(roa, (int, float)) else roa,
            "earnGrowth": earn_g,
            "trendGrowth": trend_growth,
            "growth1y": growth_1y,
            "revGrowth": rev_g,
            "rec": rec,
            "target": target,
        }
    except Exception as e:
        return t, {"error": str(e)}

out = {}
qs = {}
with ThreadPoolExecutor(max_workers=10) as ex:
    futs = {ex.submit(fetch_chart, t): ("c", t) for t in tickers}
    futs.update({ex.submit(fetch_quote_summary, t): ("q", t) for t in tickers})
    for f in as_completed(futs):
        kind, t = futs[f]
        _, d = f.result()
        if kind == "c":
            out[t] = d
        else:
            qs[t] = d

print("ASOF_UTC", datetime.now(timezone.utc).isoformat())
for t in tickers:
    c = out.get(t, {})
    q = qs.get(t, {})
    row = {
        "ticker": t,
        "price": c.get("price"),
        "chg": c.get("chg"),
        "asof_ts": c.get("asof_ts"),
        "err_c": c.get("error"),
        "fwdPE": q.get("fwdPE"),
        "trailPE": q.get("trailPE"),
        "peg": q.get("peg"),
        "fcf": q.get("fcf"),
        "roe": q.get("roe"),
        "roa": q.get("roa"),
        "earnGrowth": q.get("earnGrowth"),
        "trendGrowth": q.get("trendGrowth"),
        "growth1y": q.get("growth1y"),
        "revGrowth": q.get("revGrowth"),
        "rec": q.get("rec"),
        "target": q.get("target"),
        "err_q": q.get("error"),
    }
    print(json.dumps(row, default=str))
