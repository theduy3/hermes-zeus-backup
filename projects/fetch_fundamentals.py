#!/usr/bin/env python3
"""Fetch forward PE / PEG / FCF / ROE via Yahoo crumb+cookie and page fallbacks."""
import json, re, ssl, time, concurrent.futures
import urllib.request, urllib.parse, http.cookiejar
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

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
ctx = ssl.create_default_context()
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cj),
    urllib.request.HTTPSHandler(context=ctx),
)
opener.addheaders = [("User-Agent", UA)]

def get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with opener.open(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace"), r.getcode()

# bootstrap cookies + crumb
try:
    get("https://finance.yahoo.com/")
except Exception as e:
    print("home fail", e)
try:
    crumb_raw, _ = get("https://query1.finance.yahoo.com/v1/test/getcrumb")
    crumb = crumb_raw.strip()
except Exception as e:
    crumb = ""
    print("crumb fail", e)
print("CRUMB", repr(crumb))

def gv(obj, key):
    if not obj:
        return None
    v = obj.get(key)
    if isinstance(v, dict):
        return v.get("raw", v.get("fmt"))
    return v

def parse_modules(data):
    res = data["quoteSummary"]["result"][0]
    dks = res.get("defaultKeyStatistics") or {}
    fd = res.get("financialData") or {}
    sd = res.get("summaryDetail") or {}
    fwd_pe = gv(dks, "forwardPE") or gv(sd, "forwardPE")
    peg = gv(dks, "pegRatio")
    trailing_pe = gv(dks, "trailingPE") or gv(sd, "trailingPE")
    fcf = gv(fd, "freeCashflow")
    roe = gv(fd, "returnOnEquity")
    roa = gv(fd, "returnOnAssets")
    rec = gv(fd, "recommendationKey")
    target = gv(fd, "targetMeanPrice")
    growth = None
    et = res.get("earningsTrend") or {}
    for tr in (et.get("trend") or []):
        if tr.get("period") == "+1y":
            g = tr.get("growth")
            if isinstance(g, dict) and g.get("raw") is not None:
                growth = g["raw"]
                break
    peg_calc = None
    if peg is None and fwd_pe is not None and growth is not None and growth > 0:
        peg_calc = float(fwd_pe) / (float(growth) * 100.0)
    return {
        "forwardPE": fwd_pe,
        "trailingPE": trailing_pe,
        "pegRatio": peg,
        "pegCalc": peg_calc,
        "freeCashflow": fcf,
        "returnOnEquity": roe,
        "returnOnAssets": roa,
        "recommendation": rec,
        "targetMeanPrice": target,
        "earningsGrowth": growth,
        "source": "quoteSummary",
    }

def fetch_quote_summary(t):
    modules = "defaultKeyStatistics,financialData,summaryDetail,earningsTrend"
    q = urllib.parse.urlencode({"modules": modules, "crumb": crumb})
    url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(t)}?{q}"
    try:
        body, code = get(url)
        data = json.loads(body)
        if data.get("quoteSummary", {}).get("result"):
            return t, parse_modules(data)
        return t, {"error": body[:200], "source": "quoteSummary"}
    except Exception as e:
        return t, {"error": str(e), "source": "quoteSummary"}

def fetch_v7_batch(symbols):
    q = urllib.parse.urlencode({"symbols": ",".join(symbols), "crumb": crumb})
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?{q}"
    try:
        body, code = get(url)
        data = json.loads(body)
        out = {}
        for row in (data.get("quoteResponse", {}) or {}).get("result") or []:
            sym = row.get("symbol")
            out[sym] = {
                "forwardPE": row.get("forwardPE"),
                "trailingPE": row.get("trailingPE"),
                "price": row.get("regularMarketPrice"),
                "chg_pct": row.get("regularMarketChangePercent"),
                "marketCap": row.get("marketCap"),
                "source": "v7",
            }
        err = data.get("finance", {}).get("error") or data.get("quoteResponse", {}).get("error")
        return out, err
    except Exception as e:
        return {}, str(e)

def scrape_key_stats(t):
    url = f"https://finance.yahoo.com/quote/{urllib.parse.quote(t)}/key-statistics/"
    try:
        html, code = get(url, timeout=25)
    except Exception as e:
        return t, {"error": str(e), "source": "scrape"}
    out = {"source": "scrape", "http": code}
    # __NEXT_DATA__
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if m:
        try:
            data = json.loads(m.group(1))
            s = json.dumps(data)
            def find_raw(key):
                # "forwardPE":{"raw":12.3
                mm = re.search(rf'"{key}"\s*:\s*\{{"raw"\s*:\s*([-0-9.eE+]+)', s)
                if mm:
                    return float(mm.group(1))
                mm = re.search(rf'"{key}"\s*:\s*([-0-9.eE+]+)', s)
                if mm:
                    try:
                        return float(mm.group(1))
                    except Exception:
                        return None
                return None
            out["forwardPE"] = find_raw("forwardPE")
            out["trailingPE"] = find_raw("trailingPE")
            out["pegRatio"] = find_raw("pegRatio")
            out["freeCashflow"] = find_raw("freeCashflow")
            out["returnOnEquity"] = find_raw("returnOnEquity")
            out["returnOnAssets"] = find_raw("returnOnAssets")
            out["targetMeanPrice"] = find_raw("targetMeanPrice")
            if out.get("forwardPE") is not None:
                return t, out
        except Exception as e:
            out["next_err"] = str(e)
    # plain text Forward P/E near number
    m = re.search(r'Forward P/E[:\s]*</[^>]+>\s*<[^>]+>([0-9.]+|N/A|—)', html)
    if m and m.group(1) not in ("N/A", "—"):
        try:
            out["forwardPE"] = float(m.group(1))
        except Exception:
            pass
    m = re.search(r'PEG Ratio \(5yr expected\)[:\s]*</[^>]+>\s*<[^>]+>([0-9.N/A—-]+)', html)
    if m and m.group(1) not in ("N/A", "—", "--"):
        try:
            out["pegRatio"] = float(m.group(1))
        except Exception:
            pass
    # raw JSON fragments
    for key in ("forwardPE", "pegRatio", "trailingPE"):
        if out.get(key) is None:
            mm = re.search(rf'"{key}"\s*:\s*\{{"raw"\s*:\s*([-0-9.eE+]+)', html)
            if mm:
                out[key] = float(mm.group(1))
    return t, out

results = {}

# 1) v7 batch in chunks
print("Trying v7 batches...")
for i in range(0, len(tickers), 10):
    chunk = tickers[i:i+10]
    out, err = fetch_v7_batch(chunk)
    print("v7 chunk", chunk[0], "n=", len(out), "err=", err)
    for t, d in out.items():
        # map symbol quirks
        results[t] = d
    time.sleep(0.3)

# 2) quoteSummary per ticker where missing forwardPE
missing = [t for t in tickers if results.get(t, {}).get("forwardPE") is None]
print("missing after v7", len(missing))
for t in missing:
    tt, d = fetch_quote_summary(t)
    if d.get("forwardPE") is not None:
        results[t] = d
        print("qs ok", t, d.get("forwardPE"))
    else:
        results.setdefault(t, {}).update({k: v for k, v in d.items() if v is not None})
    time.sleep(0.15)

# 3) scrape for still missing (limit concurrency)
still = [t for t in tickers if results.get(t, {}).get("forwardPE") is None]
print("still missing", still)
# scrape key names only - batch of important ones first then rest
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    futs = [ex.submit(scrape_key_stats, t) for t in still]
    for fut in concurrent.futures.as_completed(futs):
        t, d = fut.result()
        if d.get("forwardPE") is not None or d.get("pegRatio") is not None:
            cur = results.get(t, {})
            for k, v in d.items():
                if v is not None and cur.get(k) is None:
                    cur[k] = v
            cur["source"] = d.get("source", "scrape")
            results[t] = cur
            print("scrape ok", t, d.get("forwardPE"), d.get("pegRatio"))
        else:
            results.setdefault(t, {}).update({"scrape_error": d.get("error"), "scrape_http": d.get("http")})
            print("scrape fail", t, d.get("error"), d.get("http"))

# normalize keys for BITF etc - yahoo may return different symbols
# also try BITF-related
for t in tickers:
    if t not in results:
        # try alternate keys
        for k in list(results.keys()):
            if k.upper().startswith(t) or t in k:
                results[t] = results[k]
                break

out_path = "/home/hermes/.hermes/projects/watchlist_fundamentals.json"
with open(out_path, "w") as f:
    json.dump({
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "crumb_present": bool(crumb),
        "results": results,
    }, f, indent=2, default=str)

print("---SUMMARY---")
have_fpe = 0
for t in tickers:
    r = results.get(t, {})
    fpe = r.get("forwardPE")
    peg = r.get("pegRatio") or r.get("pegCalc")
    fcf = r.get("freeCashflow")
    roe = r.get("returnOnEquity")
    if fpe is not None:
        have_fpe += 1
    print(f"{t}|fpe={fpe}|peg={peg}|fcf={fcf}|roe={roe}|src={r.get('source')}|err={r.get('error')}")
print("have_fpe", have_fpe, "/", len(tickers))
print("WROTE", out_path)
