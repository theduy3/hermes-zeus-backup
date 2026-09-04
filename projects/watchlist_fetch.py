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
UA = {"User-Agent": "Mozilla/5.0 (compatible; CharlesBot/1.0)"}

def fetch_chart(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.loads(r.read().decode())
        if not data.get("chart") or not data["chart"].get("result"):
            return t, {"error": "no result", "raw": str(data)[:200]}
        result = data["chart"]["result"][0]
        meta = result["meta"]
        quote = result["indicators"]["quote"][0]
        closes = [c for c in (quote.get("close") or []) if c is not None]
        price = meta.get("regularMarketPrice")
        if price is None and closes:
            price = closes[-1]
        # Daily change: prefer Yahoo's regularMarketChangePercent if present vs prior close
        prev = meta.get("chartPreviousClose") or meta.get("previousClose")
        chg_meta = meta.get("regularMarketChangePercent")
        if chg_meta is not None:
            chg = float(chg_meta)
            # derive prev if needed
            if prev is None and price is not None and chg != -100:
                prev = price / (1 + chg/100.0)
        elif price is not None and prev:
            chg = (price - prev) / prev * 100.0
        elif len(closes) >= 2:
            price = price if price is not None else closes[-1]
            prev = closes[-2]
            chg = (price - prev) / prev * 100.0
        else:
            chg = None
        return t, {
            "price": price,
            "prev": prev,
            "chg_pct": chg,
            "currency": meta.get("currency"),
            "exchange": meta.get("exchangeName") or meta.get("fullExchangeName"),
            "instrument": meta.get("instrumentType"),
            "ts": meta.get("regularMarketTime"),
            "name": meta.get("shortName") or meta.get("longName"),
        }
    except Exception as e:
        return t, {"error": str(e)}

def fetch_quote_summary(t):
    """modules for forward PE, PEG, financial data"""
    modules = "defaultKeyStatistics,financialData,summaryDetail,earningsTrend"
    url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(t)}?modules={modules}"
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.loads(r.read().decode())
        res = data.get("quoteSummary", {}).get("result")
        if not res:
            return t, {"error": "no quoteSummary", "raw": str(data)[:300]}
        r0 = res[0]
        dks = r0.get("defaultKeyStatistics") or {}
        fd = r0.get("financialData") or {}
        sd = r0.get("summaryDetail") or {}
        def gv(obj, key):
            v = obj.get(key)
            if isinstance(v, dict):
                return v.get("raw", v.get("fmt"))
            return v
        fwd_pe = gv(dks, "forwardPE") or gv(sd, "forwardPE")
        peg = gv(dks, "pegRatio")
        trailing_pe = gv(dks, "trailingPE") or gv(sd, "trailingPE")
        fcf = gv(fd, "freeCashflow")
        opcf = gv(fd, "operatingCashflow")
        roe = gv(fd, "returnOnEquity")
        roa = gv(fd, "returnOnAssets")
        profit_m = gv(fd, "profitMargins")
        rec = gv(fd, "recommendationKey")
        target = gv(fd, "targetMeanPrice")
        # earnings growth from trend if available
        et = r0.get("earningsTrend") or {}
        growth = None
        try:
            for tr in (et.get("trend") or []):
                if tr.get("period") == "0y" or tr.get("period") == "+1y":
                    eg = tr.get("growth")
                    if isinstance(eg, dict) and eg.get("raw") is not None:
                        growth = eg["raw"]
                        if tr.get("period") == "+1y":
                            break
        except Exception:
            pass
        return t, {
            "fwd_pe": fwd_pe,
            "peg": peg,
            "trailing_pe": trailing_pe,
            "fcf": fcf,
            "ocf": opcf,
            "roe": roe,
            "roa": roa,
            "profit_m": profit_m,
            "rec": rec,
            "target": target,
            "growth": growth,
        }
    except Exception as e:
        return t, {"error": str(e)}

out_chart = {}
out_qs = {}
with ThreadPoolExecutor(max_workers=10) as ex:
    futs = {ex.submit(fetch_chart, t): ("c", t) for t in tickers}
    futs.update({ex.submit(fetch_quote_summary, t): ("q", t) for t in tickers})
    for f in as_completed(futs):
        kind, t = futs[f]
        tt, d = f.result()
        if kind == "c":
            out_chart[tt] = d
        else:
            out_qs[tt] = d

rows = []
for t in tickers:
    c = out_chart.get(t, {})
    q = out_qs.get(t, {})
    row = {"ticker": t, **{k: c.get(k) for k in ("price","chg_pct","currency","ts","name","error")},
           **{k: q.get(k) for k in ("fwd_pe","peg","trailing_pe","fcf","ocf","roe","roa","profit_m","rec","target","growth")}}
    if "error" in q and "fwd_pe" not in q:
        row["qs_error"] = q.get("error")
    rows.append(row)

print(json.dumps({"rows": rows}, indent=2, default=str))
