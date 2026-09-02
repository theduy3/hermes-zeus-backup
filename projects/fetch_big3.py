#!/usr/bin/env python3
"""Scrape Yahoo analysis/financials for FCF, ROE, ROA; retry missing prices."""
import json, re, ssl, time, concurrent.futures
import urllib.request, urllib.parse, http.cookiejar
from datetime import datetime, timezone

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
ctx = ssl.create_default_context()
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cj),
    urllib.request.HTTPSHandler(context=ctx),
)

def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    with opener.open(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace"), r.getcode()

tickers_fin = [
"MSFT","AMZN","GOOG","META","AAPL","CRM","DELL","PLTR","ORCL","INFY",
"TSLA","NFLX","MELI","HD","LOW","WMT","TGT",
"ASML","AVGO","NVDA","AMD","MU","TSM","INTC","SNDK",
"BE","GLW","IREN","CRWV","NBIS","RKLB","BITF","SEI","TE","PSIX","PUMP","SPCX"
]

def extract_metrics(html):
    out = {}
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    blob = m.group(1) if m else html
    def find_raw(key):
        mm = re.search(rf'"{key}"\s*:\s*\{{"raw"\s*:\s*([-0-9.eE+]+)', blob)
        if mm:
            return float(mm.group(1))
        return None
    for key in [
        "forwardPE","trailingPE","pegRatio","freeCashflow","operatingCashflow",
        "returnOnEquity","returnOnAssets","returnOnCapital","profitMargins",
        "targetMeanPrice","recommendationMean","earningsGrowth","revenueGrowth",
        "totalCash","totalDebt","currentRatio","quickRatio","ebitda",
        "grossMargins","operatingMargins"
    ]:
        v = find_raw(key)
        if v is not None:
            out[key] = v
    # recommendationKey string
    mm = re.search(r'"recommendationKey"\s*:\s*"([a-zA-Z_]+)"', blob)
    if mm:
        out["recommendationKey"] = mm.group(1)
    return out

def scrape_ticker(t):
    pages = {}
    for path in ["key-statistics", "financials", "analysis", ""]:
        url = f"https://finance.yahoo.com/quote/{urllib.parse.quote(t)}" + (f"/{path}/" if path else "/")
        try:
            html, code = get(url)
            pages[path or "quote"] = extract_metrics(html)
        except Exception as e:
            pages[path or "quote"] = {"error": str(e)}
        time.sleep(0.1)
    merged = {}
    for p in pages.values():
        for k,v in p.items():
            if k == "error":
                continue
            if merged.get(k) is None and v is not None:
                merged[k] = v
    return t, merged, pages

# missing prices
def chart(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=5d&interval=1d"
    try:
        html, code = get(url)
        data = json.loads(html)
        meta = data["chart"]["result"][0]["meta"]
        return t, {
            "price": meta.get("regularMarketPrice"),
            "chg_pct": meta.get("regularMarketChangePercent"),
            "prev": meta.get("previousClose") or meta.get("chartPreviousClose"),
            "currency": meta.get("currency"),
            "as_of": meta.get("regularMarketTime"),
            "symbol": meta.get("symbol"),
            "instrument": meta.get("instrumentType"),
        }
    except Exception as e:
        return t, {"error": str(e)}

# try alternate symbols for problem tickers
alts = {
    "BITF": ["BITF","BITF.TO","BITF.V"],
    "SEI": ["SEI","SE","SE.TO"],  # SEI could be SEI Investments; watchlist SEI might be different
    "PUMP": ["PUMP","PRO"],
    "TE": ["TE","TE.PA"],
    "SPCX": ["SPCX"],
    "CRWV": ["CRWV"],
    "NBIS": ["NBIS"],
    "WYFI": ["WYFI"],
    "CRCL": ["CRCL"],
    "SNDK": ["SNDK"],
    "PSIX": ["PSIX"],
}

print("=== PRICE RETRIES ===")
price_fix = {}
for base, tries in alts.items():
    for t in tries:
        tt, d = chart(t)
        print(base, "->", t, d)
        if d.get("price") is not None:
            price_fix[base] = {**d, "resolved": t}
            break
    time.sleep(0.2)

print("=== FUNDAMENTALS SCRAPE ===")
fund = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
    futs = [ex.submit(scrape_ticker, t) for t in tickers_fin]
    for fut in concurrent.futures.as_completed(futs):
        t, merged, pages = fut.result()
        fund[t] = merged
        print(f"{t}|fpe={merged.get('forwardPE')}|peg={merged.get('pegRatio')}|fcf={merged.get('freeCashflow')}|roe={merged.get('returnOnEquity')}|roa={merged.get('returnOnAssets')}|tg={merged.get('targetMeanPrice')}|rec={merged.get('recommendationKey')}")

out = {
    "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
    "prices_fix": price_fix,
    "fund": fund,
}
path = "/home/hermes/.hermes/projects/watchlist_big3.json"
with open(path, "w") as f:
    json.dump(out, f, indent=2, default=str)
print("WROTE", path)
