#!/usr/bin/env python3
import json, urllib.request, ssl, urllib.parse, http.cookiejar, time

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

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cj),
    urllib.request.HTTPSHandler(context=ctx),
)
opener.addheaders = [
    ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
    ("Accept", "application/json"),
]

crumb = None
try:
    opener.open("https://fc.yahoo.com", timeout=15).read()
    crumb = opener.open("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=15).read().decode()
    print("CRUMB_OK", crumb[:20] if crumb else None)
except Exception as e:
    print("CRUMB_FAIL", e)

results = {}

def gv(d, key):
    if not d:
        return None
    v = d.get(key)
    if isinstance(v, dict):
        return v.get("raw", v.get("fmt"))
    return v

for t in tickers:
    entry = {"ok": False}
    # try quote v7
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={urllib.parse.quote(t, safe='')}"
        if crumb:
            url += f"&crumb={urllib.parse.quote(crumb)}"
        raw = opener.open(url, timeout=15).read().decode()
        data = json.loads(raw)
        qs = (data.get("quoteResponse") or {}).get("result") or []
        if qs:
            q = qs[0]
            entry.update({
                "ok": True,
                "src": "v7",
                "price": q.get("regularMarketPrice"),
                "forwardPE": q.get("forwardPE"),
                "trailingPE": q.get("trailingPE"),
                "epsCurrentYear": q.get("epsCurrentYear"),
                "priceEpsCurrentYear": q.get("priceEpsCurrentYear"),
                "epsForward": q.get("epsForward"),
                "target": q.get("targetMeanPrice"),
                "mcap": q.get("marketCap"),
            })
    except Exception as e:
        entry["v7err"] = str(e)[:120]

    # quoteSummary with crumb
    try:
        modules = "summaryDetail,defaultKeyStatistics,financialData,earningsTrend"
        url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(t, safe='')}?modules={modules}"
        if crumb:
            url += f"&crumb={urllib.parse.quote(crumb)}"
        raw = opener.open(url, timeout=20).read().decode()
        data = json.loads(raw)
        r0 = data["quoteSummary"]["result"][0]
        sd = r0.get("summaryDetail") or {}
        ks = r0.get("defaultKeyStatistics") or {}
        fd = r0.get("financialData") or {}
        et = r0.get("earningsTrend") or {}
        growth = None
        for tr in (et.get("trend") or []):
            if tr.get("period") in ("+1y", "0y"):
                g = tr.get("growth")
                if isinstance(g, dict) and g.get("raw") is not None:
                    growth = g["raw"]
                    if tr.get("period") == "+1y":
                        break
        entry.update({
            "ok": True,
            "src": entry.get("src", "") + "+qs",
            "forwardPE": entry.get("forwardPE") or gv(sd, "forwardPE") or gv(ks, "forwardPE"),
            "trailingPE": entry.get("trailingPE") or gv(sd, "trailingPE") or gv(ks, "trailingPE"),
            "peg": gv(ks, "pegRatio"),
            "fcf": gv(fd, "freeCashflow"),
            "roe": gv(fd, "returnOnEquity"),
            "roa": gv(fd, "returnOnAssets"),
            "rec": gv(fd, "recommendationMean"),
            "recKey": fd.get("recommendationKey"),
            "target": entry.get("target") or gv(fd, "targetMeanPrice"),
            "growth": growth,
            "profitMargins": gv(fd, "profitMargins"),
        })
        if entry.get("peg") is None and entry.get("forwardPE") and growth and growth != 0:
            g_pct = growth * 100 if abs(growth) < 5 else growth
            if g_pct > 0:
                entry["peg_calc"] = entry["forwardPE"] / g_pct
    except Exception as e:
        entry["qserr"] = str(e)[:120]

    results[t] = entry
    time.sleep(0.08)

# BITF chart alts
for t in ["BITF", "BITF.TO", "BITF.V"]:
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=5d&interval=1d"
        raw = opener.open(url, timeout=15).read().decode()
        data = json.loads(raw)
        res = (data.get("chart") or {}).get("result")
        if res:
            meta = res[0]["meta"]
            results[f"chart_{t}"] = {
                "ok": True,
                "price": meta.get("regularMarketPrice"),
                "prev": meta.get("previousClose") or meta.get("chartPreviousClose"),
                "currency": meta.get("currency"),
            }
        else:
            results[f"chart_{t}"] = {"ok": False, "err": data.get("chart", {}).get("error")}
    except Exception as e:
        results[f"chart_{t}"] = {"ok": False, "err": str(e)[:120]}

print(json.dumps(results, indent=2, default=str))
