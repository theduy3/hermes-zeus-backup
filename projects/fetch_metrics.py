#!/usr/bin/env python3
import json, urllib.request, urllib.parse, time, ssl

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

# Also try BITF alternate symbols
extra = ["BITF.TO", "BITF"]

ctx = ssl.create_default_context()
results = {}

def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json,text/html"
    })
    with urllib.request.urlopen(req, context=ctx, timeout=timeout) as r:
        return r.read().decode()

modules = "summaryDetail,defaultKeyStatistics,financialData,price,earningsTrend"
for t in tickers:
    try:
        url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(t, safe='')}?modules={modules}"
        raw = fetch(url)
        data = json.loads(raw)
        qs = data["quoteSummary"]["result"][0]
        sd = qs.get("summaryDetail") or {}
        ks = qs.get("defaultKeyStatistics") or {}
        fd = qs.get("financialData") or {}
        pr = qs.get("price") or {}
        et = qs.get("earningsTrend") or {}

        def gv(d, key):
            v = d.get(key)
            if isinstance(v, dict):
                return v.get("raw", v.get("fmt"))
            return v

        # earnings trend for growth
        growth = None
        try:
            trends = et.get("trend") or []
            for tr in trends:
                if tr.get("period") == "0y" or tr.get("period") == "+1y":
                    g = tr.get("growth")
                    if isinstance(g, dict) and g.get("raw") is not None:
                        growth = g["raw"]
                        if tr.get("period") == "+1y":
                            break
            if growth is None:
                for tr in trends:
                    g = tr.get("growth")
                    if isinstance(g, dict) and g.get("raw") is not None:
                        growth = g["raw"]
                        break
        except Exception:
            pass

        trailing_pe = gv(sd, "trailingPE") or gv(ks, "trailingPE")
        forward_pe = gv(sd, "forwardPE") or gv(ks, "forwardPE")
        peg = gv(ks, "pegRatio")
        fcf = gv(fd, "freeCashflow")
        opcf = gv(fd, "operatingCashflow")
        roe = gv(fd, "returnOnEquity")
        roa = gv(fd, "returnOnAssets")
        profit_m = gv(fd, "profitMargins")
        rec = gv(fd, "recommendationMean")
        rec_key = fd.get("recommendationKey")
        target = gv(fd, "targetMeanPrice")
        price = gv(pr, "regularMarketPrice") or gv(pr, "postMarketPrice")
        mcap = gv(pr, "marketCap") or gv(sd, "marketCap")

        # If peg missing, compute from fwd pe and growth
        peg_calc = None
        if peg is None and forward_pe and growth and growth > 0:
            # growth is often decimal e.g. 0.15 = 15%
            g_pct = growth * 100 if abs(growth) < 2 else growth
            if g_pct > 0:
                peg_calc = forward_pe / g_pct

        results[t] = {
            "ok": True,
            "price": price,
            "trailingPE": trailing_pe,
            "forwardPE": forward_pe,
            "peg": peg,
            "peg_calc": peg_calc,
            "growth": growth,
            "fcf": fcf,
            "opcf": opcf,
            "roe": roe,
            "roa": roa,
            "profitMargins": profit_m,
            "rec": rec,
            "recKey": rec_key,
            "target": target,
            "mcap": mcap,
        }
    except Exception as e:
        results[t] = {"ok": False, "err": str(e)[:200]}
    time.sleep(0.12)

# BITF chart retry with query2
for t in ["BITF", "BITF.TO"]:
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=5d&interval=1d"
        raw = fetch(url)
        data = json.loads(raw)
        if data.get("chart", {}).get("result"):
            meta = data["chart"]["result"][0]["meta"]
            results[f"chart_{t}"] = {
                "ok": True,
                "price": meta.get("regularMarketPrice"),
                "prev": meta.get("previousClose") or meta.get("chartPreviousClose"),
            }
    except Exception as e:
        results[f"chart_{t}"] = {"ok": False, "err": str(e)[:120]}

print(json.dumps(results, indent=2, default=str))
