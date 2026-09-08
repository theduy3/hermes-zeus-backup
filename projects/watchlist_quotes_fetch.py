#!/usr/bin/env python3
import json, urllib.request, urllib.parse, ssl, time, http.cookiejar
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
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPSHandler(context=ctx))

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with opener.open(req, timeout=25) as r:
        return r.read().decode("utf-8", "replace")

# bootstrap crumb
try:
    get("https://fc.yahoo.com")
except Exception:
    pass
crumb = get("https://query1.finance.yahoo.com/v1/test/getcrumb").strip()
print("CRUMB", crumb[:20], "...", file=__import__("sys").stderr)

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

quote_map = {}
for batch in chunks(tickers, 10):
    syms = ",".join(urllib.parse.quote(t, safe="") for t in batch)
    # quote endpoint accepts comma-separated; don't over-encode commas
    syms = ",".join(batch)
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={urllib.parse.quote(syms, safe=',')}&crumb={urllib.parse.quote(crumb)}"
    try:
        raw = get(url)
        data = json.loads(raw)
        for item in (data.get("quoteResponse") or {}).get("result") or []:
            quote_map[item.get("symbol")] = item
        err = (data.get("quoteResponse") or {}).get("error")
        if err:
            print("batch err", batch, err, file=__import__("sys").stderr)
    except Exception as e:
        print("batch fail", batch, e, file=__import__("sys").stderr)
    time.sleep(0.2)

# Also try alternate symbols for BITF
for alt in ["BITF", "BITF.TO", "BITF.NE"]:
    if alt in quote_map:
        continue
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={urllib.parse.quote(alt)}&crumb={urllib.parse.quote(crumb)}"
        data = json.loads(get(url))
        for item in (data.get("quoteResponse") or {}).get("result") or []:
            quote_map[item.get("symbol")] = item
            print("alt ok", alt, item.get("symbol"), file=__import__("sys").stderr)
    except Exception as e:
        print("alt fail", alt, e, file=__import__("sys").stderr)

# quoteSummary for PEG / FCF / ROE for non-ETF majors
need_deep = [t for t in tickers if t not in ("VFV.TO","GLD","SMH","SPCX")]
qs_map = {}

def fetch_qs(t):
    modules = "defaultKeyStatistics,financialData,earningsTrend"
    url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(t)}?modules={modules}&crumb={urllib.parse.quote(crumb)}"
    try:
        data = json.loads(get(url))
        res = (data.get("quoteSummary") or {}).get("result")
        if not res:
            err = (data.get("quoteSummary") or {}).get("error")
            return t, None, str(err)
        return t, res[0], None
    except Exception as e:
        return t, None, str(e)

with ThreadPoolExecutor(max_workers=4) as ex:
    futs = [ex.submit(fetch_qs, t) for t in need_deep]
    for f in as_completed(futs):
        t, res, err = f.result()
        if res:
            qs_map[t] = res
        else:
            qs_map[t] = {"_err": err}
        time.sleep(0.05)

def raw(x):
    if x is None:
        return None
    if isinstance(x, dict):
        return x.get("raw", x.get("fmt"))
    return x

out = {}
for t in tickers:
    q = quote_map.get(t) or {}
    # sometimes VFV.TO stays as is
    if not q:
        # try find by fuzzy
        for k,v in quote_map.items():
            if k.replace("-",".") == t or k == t:
                q = v
                break
    qs = qs_map.get(t) or {}
    dks = qs.get("defaultKeyStatistics") or {}
    fd = qs.get("financialData") or {}
    et = qs.get("earningsTrend") or {}
    # growth from earningsTrend 0y/+1y
    trend = et.get("trend") or []
    growth = None
    for tr in trend:
        if tr.get("period") == "+1y":
            growth = raw(tr.get("growth"))
    out[t] = {
        "symbol": q.get("symbol", t),
        "price": q.get("regularMarketPrice"),
        "chg": q.get("regularMarketChangePercent"),
        "forwardPE": q.get("forwardPE") or raw(dks.get("forwardPE")),
        "trailingPE": q.get("trailingPE") or raw(dks.get("trailingPE")),
        "epsForward": q.get("epsForward"),
        "epsTrailing": q.get("epsTrailingTwelveMonths"),
        "marketCap": q.get("marketCap"),
        "peg": raw(dks.get("pegRatio")),
        "freeCashflow": raw(fd.get("freeCashflow")),
        "operatingCashflow": raw(fd.get("operatingCashflow")),
        "returnOnEquity": raw(fd.get("returnOnEquity")),
        "returnOnAssets": raw(fd.get("returnOnAssets")),
        "revenueGrowth": raw(fd.get("revenueGrowth")),
        "earningsGrowth": raw(fd.get("earningsGrowth")),
        "profitMargins": raw(fd.get("profitMargins")),
        "recommendationKey": fd.get("recommendationKey"),
        "targetMeanPrice": raw(fd.get("targetMeanPrice")),
        "earningsGrowthTrend": growth,
        "quoteType": q.get("quoteType"),
        "shortName": q.get("shortName"),
        "sector": None,
        "fiftyTwoWeekHigh": q.get("fiftyTwoWeekHigh"),
        "fiftyTwoWeekLow": q.get("fiftyTwoWeekLow"),
        "regularMarketTime": q.get("regularMarketTime"),
        "qs_err": qs.get("_err"),
        "has_quote": bool(q),
    }

# Retry BITF chart
def fetch_chart(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.loads(r.read().decode())
        result = data["chart"]["result"][0]
        meta = result["meta"]
        return {
            "price": meta.get("regularMarketPrice"),
            "chg": meta.get("regularMarketChangePercent"),
            "last_ts": meta.get("regularMarketTime"),
            "currency": meta.get("currency"),
            "symbol": meta.get("symbol"),
            "ok": True,
        }
    except Exception as e:
        return {"ok": False, "err": str(e)}

# fill missing prices from prior chart file
with open("/tmp/wl_data.json") as f:
    prior = {r["t"]: r for r in json.load(f)["rows"]}

for t in tickers:
    if out[t]["price"] is None and prior.get(t, {}).get("price") is not None:
        out[t]["price"] = prior[t]["price"]
        out[t]["chg"] = prior[t]["chg"]
        out[t]["from_chart"] = True
    if t == "BITF" and out[t]["price"] is None:
        for alt in ["BITF", "BITF.TO"]:
            ch = fetch_chart(alt)
            print("bitf chart", alt, ch, file=__import__("sys").stderr)
            if ch.get("ok"):
                out[t]["price"] = ch["price"]
                out[t]["chg"] = ch["chg"]
                out[t]["symbol"] = ch.get("symbol")
                break

print(json.dumps({"asof_utc": datetime.now(timezone.utc).isoformat(), "crumb_ok": True, "data": out}, indent=2, default=str))
