#!/usr/bin/env python3
import json, urllib.request, urllib.parse, ssl, time, concurrent.futures

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
cj = urllib.request.HTTPCookieProcessor()
opener = urllib.request.build_opener(cj, urllib.request.HTTPSHandler(context=ctx))

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with opener.open(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")

# seed cookies + crumb
try:
    get("https://finance.yahoo.com")
except Exception:
    pass
crumb = get("https://query2.finance.yahoo.com/v1/test/getcrumb").strip()
print("CRUMB", crumb)

def gv(d, k):
    v = (d or {}).get(k)
    if isinstance(v, dict):
        return v.get("raw", v.get("fmt"))
    return v

def fetch(t):
    modules = "defaultKeyStatistics,financialData,summaryDetail,earningsTrend"
    url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(t)}?modules={modules}&crumb={urllib.parse.quote(crumb)}"
    try:
        data = json.loads(get(url))
        res = data.get("quoteSummary", {}).get("result")
        if not res:
            err = data.get("quoteSummary", {}).get("error") or data
            return {"t": t, "ok": False, "err": str(err)[:200]}
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
        out["opcf"] = gv(fd, "operatingCashflow")
        out["roe"] = gv(fd, "returnOnEquity")
        out["roa"] = gv(fd, "returnOnAssets")
        out["earnGrowth"] = gv(fd, "earningsGrowth")
        out["revGrowth"] = gv(fd, "revenueGrowth")
        out["profitMargins"] = gv(fd, "profitMargins")
        out["rec"] = gv(fd, "recommendationKey")
        out["target"] = gv(fd, "targetMeanPrice")
        out["currentPrice"] = gv(fd, "currentPrice")
        for tr in (et.get("trend") or []):
            p = tr.get("period")
            if p in ("0y", "+1y", "0q", "+1q"):
                out[f"growth_{p}"] = gv(tr, "growth")
                out[f"earnings_{p}"] = gv(tr, "earnings")
        return out
    except Exception as e:
        return {"t": t, "ok": False, "err": str(e)}

# sequential with small delay to avoid rate limit - but crumb works fast
results = []
# use limited concurrency
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    futs = {ex.submit(fetch, t): t for t in tickers}
    for f in concurrent.futures.as_completed(futs):
        results.append(f.result())

# order
by_t = {r["t"]: r for r in results}
ordered = [by_t[t] for t in tickers]
with open("/home/hermes/.hermes/projects/watchlist_stats.json", "w") as f:
    json.dump(ordered, f, indent=2)
print("WROTE", len(ordered))
for r in ordered:
    print(json.dumps({k: r.get(k) for k in (
        "t","ok","forwardPE","trailingPE","peg","fcf","roe","earnGrowth","revGrowth",
        "growth_0y","growth_+1y","rec","target","err")}))
