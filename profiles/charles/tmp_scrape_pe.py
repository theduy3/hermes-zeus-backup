#!/usr/bin/env python3
import json, urllib.request, urllib.parse, urllib.error, ssl, re, time, random

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
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
OUT = "/home/hermes/.hermes/profiles/charles/tmp_watchlist_fundamentals.json"

# BITF chart alts
for t in ["BITF", "BITF.TO", "BITF.V", "BITF.CN"]:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=25) as r:
            data = json.loads(r.read().decode())
        res = (data.get("chart") or {}).get("result")
        if res:
            meta = res[0].get("meta", {})
            print("BITFALT", t, meta.get("regularMarketPrice"), meta.get("symbol"), meta.get("exchangeName"), meta.get("instrumentType"))
        else:
            print("BITFALT", t, "noresult", data)
    except Exception as e:
        print("BITFALT", t, "ERR", e)
    time.sleep(0.5)

def scrape_quote(t):
    # Yahoo quote page often embeds root.App.main JSON
    url = f"https://finance.yahoo.com/quote/{urllib.parse.quote(t)}"
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    })
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            html = r.read().decode("utf-8", "ignore")
    except Exception as e:
        return {"error": str(e)}

    out = {}
    # try JSON blob
    m = re.search(r"root\.App\.main\s*=\s*(\{.*?\});\s*\n", html, re.DOTALL)
    if not m:
        m = re.search(r"\"QuoteSummaryStore\"\s*:\s*(\{.*?\})\s*,\s*\"", html)
    blob = None
    if m:
        try:
            blob = json.loads(m.group(1))
        except Exception:
            blob = None

    def find_keys(obj, wanted, path=""):
        found = {}
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in wanted:
                    if isinstance(v, dict) and "raw" in v:
                        found[k] = v.get("raw")
                    else:
                        found[k] = v
                if isinstance(v, (dict, list)) and len(path) < 120:
                    found.update(find_keys(v, wanted, path + "/" + k))
        elif isinstance(obj, list) and len(obj) < 50:
            for i, v in enumerate(obj[:30]):
                found.update(find_keys(v, wanted, path + f"[{i}]"))
        return found

    wanted = {
        "forwardPE", "trailingPE", "pegRatio", "freeCashflow", "operatingCashflow",
        "returnOnEquity", "returnOnAssets", "revenueGrowth", "earningsGrowth",
        "recommendationKey", "targetMeanPrice", "profitMargins", "enterpriseToEbitda"
    }
    if blob:
        found = find_keys(blob, wanted)
        out.update(found)

    # regex fallbacks on visible text / json fragments
    patterns = {
        "forwardPE": [
            r'"forwardPE"\s*:\s*\{[^}]*"raw"\s*:\s*([-0-9.]+)',
            r'"forwardPE"\s*:\s*([-0-9.]+)',
            r'Forward P/E[^0-9-]*([-0-9.]+)',
            r'data-field="forwardPE"[^>]*>\s*([-0-9.]+)',
        ],
        "trailingPE": [
            r'"trailingPE"\s*:\s*\{[^}]*"raw"\s*:\s*([-0-9.]+)',
            r'Trailing P/E[^0-9-]*([-0-9.]+)',
        ],
        "pegRatio": [
            r'"pegRatio"\s*:\s*\{[^}]*"raw"\s*:\s*([-0-9.]+)',
            r'PEG Ratio[^0-9-]*([-0-9.]+)',
        ],
        "freeCashflow": [
            r'"freeCashflow"\s*:\s*\{[^}]*"raw"\s*:\s*([-0-9.eE+]+)',
        ],
        "returnOnEquity": [
            r'"returnOnEquity"\s*:\s*\{[^}]*"raw"\s*:\s*([-0-9.eE+]+)',
        ],
        "returnOnAssets": [
            r'"returnOnAssets"\s*:\s*\{[^}]*"raw"\s*:\s*([-0-9.eE+]+)',
        ],
        "earningsGrowth": [
            r'"earningsGrowth"\s*:\s*\{[^}]*"raw"\s*:\s*([-0-9.eE+]+)',
        ],
        "revenueGrowth": [
            r'"revenueGrowth"\s*:\s*\{[^}]*"raw"\s*:\s*([-0-9.eE+]+)',
        ],
        "targetMeanPrice": [
            r'"targetMeanPrice"\s*:\s*\{[^}]*"raw"\s*:\s*([-0-9.]+)',
        ],
    }
    for key, pats in patterns.items():
        if out.get(key) is not None:
            continue
        for p in pats:
            mm = re.search(p, html, re.I)
            if mm:
                try:
                    out[key] = float(mm.group(1))
                except Exception:
                    out[key] = mm.group(1)
                break
    out["source"] = "yahoo_quote_html"
    out["html_len"] = len(html)
    out["has_blob"] = blob is not None
    # snip title
    tm = re.search(r"<title>([^<]+)</title>", html, re.I)
    if tm:
        out["title"] = tm.group(1)[:120]
    return out

results = {}
for i, t in enumerate(tickers):
    d = scrape_quote(t)
    results[t] = d
    print(f"{t}|fwd={d.get('forwardPE')}|peg={d.get('pegRatio')}|fcf={d.get('freeCashflow')}|roe={d.get('returnOnEquity')}|eg={d.get('earningsGrowth')}|title={d.get('title')}|err={d.get('error')}|blob={d.get('has_blob')}|hlen={d.get('html_len')}")
    time.sleep(0.7 + random.uniform(0.1, 0.5))
    if (i + 1) % 10 == 0:
        with open(OUT, "w") as f:
            json.dump(results, f)

with open(OUT, "w") as f:
    json.dump(results, f)
print("DONE")
