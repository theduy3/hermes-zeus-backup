#!/usr/bin/env python3
import json, urllib.request, urllib.parse, urllib.error, ssl, time, random, os

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
# BITF alts
"BITF.TO","BITF.V"
]

OUT = "/home/hermes/.hermes/profiles/charles/tmp_watchlist_fundamentals.json"
ctx = ssl.create_default_context()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
modules = "summaryDetail,defaultKeyStatistics,financialData,earningsTrend"

results = {}
if os.path.exists(OUT):
    try:
        with open(OUT) as f:
            results = json.load(f)
    except Exception:
        results = {}

def g(d, *keys):
    cur = d
    for k in keys:
        if cur is None:
            return None
        if isinstance(cur, dict):
            cur = cur.get(k)
        else:
            return None
    if isinstance(cur, dict) and "raw" in cur:
        return cur.get("raw")
    return cur

def fetch(t, attempt=1):
    hosts = [
        "https://query1.finance.yahoo.com",
        "https://query2.finance.yahoo.com",
    ]
    host = hosts[(attempt - 1) % len(hosts)]
    url = f"{host}/v10/finance/quoteSummary/{urllib.parse.quote(t)}?modules={modules}"
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            data = json.loads(r.read().decode())
        res = (data.get("quoteSummary") or {}).get("result")
        if not res:
            err = (data.get("quoteSummary") or {}).get("error")
            return {"error": f"no result {err}"}
        r0 = res[0]
        sd = r0.get("summaryDetail") or {}
        ks = r0.get("defaultKeyStatistics") or {}
        fd = r0.get("financialData") or {}
        et = r0.get("earningsTrend") or {}
        # try growth from earningsTrend
        growth = None
        try:
            trends = et.get("trend") or []
            for tr in trends:
                if tr.get("period") in ("+1y", "0y", "+5y"):
                    gr = g(tr, "growth")
                    if gr is not None:
                        growth = gr
                        if tr.get("period") == "+1y":
                            break
        except Exception:
            pass
        out = {
            "forwardPE": g(sd, "forwardPE") if g(sd, "forwardPE") is not None else g(ks, "forwardPE"),
            "trailingPE": g(sd, "trailingPE") if g(sd, "trailingPE") is not None else g(ks, "trailingPE"),
            "pegRatio": g(ks, "pegRatio"),
            "pegYFinance": g(ks, "pegRatio"),
            "enterpriseToEbitda": g(ks, "enterpriseToEbitda"),
            "profitMargins": g(fd, "profitMargins"),
            "operatingCashflow": g(fd, "operatingCashflow"),
            "freeCashflow": g(fd, "freeCashflow"),
            "returnOnEquity": g(fd, "returnOnEquity"),
            "returnOnAssets": g(fd, "returnOnAssets"),
            "revenueGrowth": g(fd, "revenueGrowth"),
            "earningsGrowth": g(fd, "earningsGrowth"),
            "recommendationKey": g(fd, "recommendationKey") if not isinstance(fd.get("recommendationKey"), dict) else fd.get("recommendationKey"),
            "targetMeanPrice": g(fd, "targetMeanPrice"),
            "currentPrice": g(fd, "currentPrice"),
            "totalCash": g(fd, "totalCash"),
            "totalDebt": g(fd, "totalDebt"),
            "earningsGrowthTrend": growth,
            "shortName": None,
        }
        # recommendationKey sometimes plain string
        if isinstance(fd.get("recommendationKey"), str):
            out["recommendationKey"] = fd.get("recommendationKey")
        return out
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "retry": e.code in (429, 500, 502, 503)}
    except Exception as e:
        return {"error": str(e), "retry": True}

pending = [t for t in tickers if "forwardPE" not in results.get(t, {}) and "error" not in results.get(t, {})]
# also retry previous errors that are retryable
pending = [t for t in tickers if not (
    t in results and "error" not in results[t] and ("forwardPE" in results[t] or "trailingPE" in results[t] or results[t].get("done"))
)]
# simplify: refetch all missing good
pending = []
for t in tickers:
    d = results.get(t)
    if not d or d.get("error") or d.get("retry"):
        pending.append(t)
    elif "scraped" not in d and "forwardPE" not in d and "trailingPE" not in d and d.get("freeCashflow") is None:
        pending.append(t)

# force all primary tickers if empty file mostly
if len(results) < 5:
    pending = list(tickers)

print("pending", len(pending))
for i, t in enumerate(pending):
    ok = False
    last = {}
    for attempt in range(1, 5):
        d = fetch(t, attempt)
        last = d
        if "error" not in d:
            d["done"] = True
            results[t] = d
            print(f"OK {t}|fwdPE={d.get('forwardPE')}|PEG={d.get('pegRatio')}|FCF={d.get('freeCashflow')}|ROE={d.get('returnOnEquity')}|rec={d.get('recommendationKey')}")
            ok = True
            break
        if d.get("retry"):
            sleep = min(2 ** attempt + random.uniform(0.5, 1.5), 25)
            print(f"RETRY {t} {d.get('error')} sleep {sleep:.1f}")
            time.sleep(sleep)
        else:
            results[t] = d
            print(f"FAIL {t}|{d}")
            ok = True
            break
    if not ok:
        results[t] = last
        print(f"GIVEUP {t}|{last}")
    time.sleep(0.9 + random.uniform(0.2, 0.8))
    if (i + 1) % 8 == 0:
        with open(OUT, "w") as f:
            json.dump(results, f)

with open(OUT, "w") as f:
    json.dump(results, f)
print("WROTE", OUT)
