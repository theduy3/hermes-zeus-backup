#!/usr/bin/env python3
"""Fetch forward PE / PEG / FCF / ROE via Yahoo with crumb auth and fallbacks."""
import json, ssl, time, concurrent.futures, http.cookiejar, urllib.request, urllib.parse, re
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
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPSHandler(context=ctx))
opener.addheaders = [("User-Agent", UA)]

def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with opener.open(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")

# seed cookies + crumb
crumb = None
for seed in ["https://fc.yahoo.com", "https://finance.yahoo.com"]:
    try:
        get(seed)
    except Exception as e:
        print("seed fail", seed, e)

try:
    crumb = get("https://query1.finance.yahoo.com/v1/test/getcrumb").strip()
    print("crumb", crumb[:20] if crumb else None, "len", len(crumb) if crumb else 0)
except Exception as e:
    print("crumb fail", e)
    crumb = None

def raw(x):
    if x is None:
        return None
    if isinstance(x, dict):
        return x.get("raw")
    return x

def quote_summary(ticker):
    mods = "defaultKeyStatistics,financialData,summaryDetail,earningsTrend"
    params = {"modules": mods}
    if crumb:
        params["crumb"] = crumb
    url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(ticker)}?{urllib.parse.urlencode(params)}"
    try:
        txt = get(url)
        data = json.loads(txt)
        res = data["quoteSummary"]["result"][0]
        dks = res.get("defaultKeyStatistics") or {}
        fd = res.get("financialData") or {}
        sd = res.get("summaryDetail") or {}
        fpe = raw(dks.get("forwardPE")) or raw(sd.get("forwardPE"))
        tpe = raw(dks.get("trailingPE")) or raw(sd.get("trailingPE"))
        peg = raw(dks.get("pegRatio"))
        eg = None
        et = res.get("earningsTrend") or {}
        for t in et.get("trend") or []:
            if t.get("period") in ("0y", "+1y"):
                eg = raw(t.get("growth"))
                if eg is not None:
                    break
        return {
            "ticker": ticker,
            "forwardPE": fpe,
            "trailingPE": tpe,
            "pegRatio": peg,
            "earningsGrowth": eg,
            "fcf": raw(fd.get("freeCashflow")),
            "ocf": raw(fd.get("operatingCashflow")),
            "roe": raw(fd.get("returnOnEquity")),
            "roa": raw(fd.get("returnOnAssets")),
            "rec": fd.get("recommendationKey"),
            "target": raw(fd.get("targetMeanPrice")),
            "ok": True,
            "src": "quoteSummary",
            "err": None,
        }
    except Exception as e:
        return {"ticker": ticker, "ok": False, "err": str(e), "src": "quoteSummary"}

def scrape_key_stats(ticker):
    """Parse forward PE / PEG from Yahoo key-statistics HTML as last resort."""
    url = f"https://finance.yahoo.com/quote/{urllib.parse.quote(ticker)}/key-statistics"
    try:
        html = get(url, timeout=30)
        # Look for Forward P/E and PEG Ratio near labels
        fpe = None
        peg = None
        # JSON embedded
        m = re.search(r'root\.App\.main\s*=\s*(\{.*?\});\s*\n', html, re.S)
        if m:
            try:
                blob = json.loads(m.group(1))
                # walk for forwardPE
                def find(obj, key, depth=0):
                    if depth > 12:
                        return None
                    if isinstance(obj, dict):
                        if key in obj:
                            return obj[key]
                        for v in obj.values():
                            r = find(v, key, depth+1)
                            if r is not None:
                                return r
                    elif isinstance(obj, list):
                        for v in obj[:50]:
                            r = find(v, key, depth+1)
                            if r is not None:
                                return r
                    return None
                fpe_o = find(blob, "forwardPE")
                peg_o = find(blob, "pegRatio")
                fpe = raw(fpe_o) if fpe_o is not None else None
                peg = raw(peg_o) if peg_o is not None else None
            except Exception:
                pass
        if fpe is None:
            m2 = re.search(r'Forward P/E.*?</td>\s*<td[^>]*>([^<]+)', html, re.I|re.S)
            if m2:
                try:
                    fpe = float(m2.group(1).strip().replace(",", ""))
                except Exception:
                    pass
        if peg is None:
            m3 = re.search(r'PEG Ratio \(5 yr expected\).*?</td>\s*<td[^>]*>([^<]+)', html, re.I|re.S)
            if m3:
                try:
                    peg = float(m3.group(1).strip().replace(",", ""))
                except Exception:
                    pass
        return {"ticker": ticker, "forwardPE": fpe, "pegRatio": peg, "ok": fpe is not None or peg is not None, "src": "html", "err": None if (fpe or peg) else "no parse"}
    except Exception as e:
        return {"ticker": ticker, "ok": False, "err": str(e), "src": "html"}

def v7_quote(batch):
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=" + urllib.parse.quote(",".join(batch), safe=",")
    if crumb:
        url += "&crumb=" + urllib.parse.quote(crumb)
    try:
        data = json.loads(get(url))
        out = {}
        for q in data.get("quoteResponse", {}).get("result", []) or []:
            out[q.get("symbol")] = {
                "forwardPE": q.get("forwardPE"),
                "trailingPE": q.get("trailingPE"),
                "price": q.get("regularMarketPrice"),
                "chg": q.get("regularMarketChangePercent"),
                "ok": True,
            }
        return out, None
    except Exception as e:
        return {}, str(e)

# try v7 in batches of 10
v7 = {}
v7_err = []
for i in range(0, len(tickers), 10):
    batch = tickers[i:i+10]
    part, err = v7_quote(batch)
    v7.update(part)
    if err:
        v7_err.append(err)
    time.sleep(0.15)
print("v7 count", len(v7), "err", v7_err[:3])

# quoteSummary with crumb
mods = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    futs = {ex.submit(quote_summary, t): t for t in tickers}
    for fut in concurrent.futures.as_completed(futs):
        t = futs[fut]
        mods[t] = fut.result()
        time.sleep(0.02)

ok_mod = sum(1 for m in mods.values() if m.get("ok"))
print("mods ok", ok_mod)

# for missing FPE, try HTML scrape on a subset of important names first then all missing
missing = [t for t in tickers if not (mods.get(t, {}).get("forwardPE") or v7.get(t, {}).get("forwardPE"))]
print("missing fpe", len(missing), missing[:15])

htmls = {}
# scrape all missing with limit concurrency 3
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
    futs = {ex.submit(scrape_key_stats, t): t for t in missing}
    for fut in concurrent.futures.as_completed(futs):
        t = futs[fut]
        htmls[t] = fut.result()
        time.sleep(0.05)
print("html ok", sum(1 for h in htmls.values() if h.get("ok")))

# merge
merged = {}
for t in tickers:
    m = mods.get(t) or {}
    v = v7.get(t) or {}
    h = htmls.get(t) or {}
    fpe = m.get("forwardPE") if m.get("ok") else None
    if fpe is None:
        fpe = v.get("forwardPE")
    if fpe is None:
        fpe = h.get("forwardPE")
    peg = m.get("pegRatio") if m.get("ok") else None
    if peg is None:
        peg = h.get("pegRatio")
    merged[t] = {
        "forwardPE": fpe,
        "trailingPE": (m.get("trailingPE") if m.get("ok") else None) or v.get("trailingPE"),
        "pegRatio": peg,
        "earningsGrowth": m.get("earningsGrowth") if m.get("ok") else None,
        "fcf": m.get("fcf") if m.get("ok") else None,
        "ocf": m.get("ocf") if m.get("ok") else None,
        "roe": m.get("roe") if m.get("ok") else None,
        "roa": m.get("roa") if m.get("ok") else None,
        "rec": m.get("rec") if m.get("ok") else None,
        "target": m.get("target") if m.get("ok") else None,
        "mod_ok": m.get("ok"),
        "mod_err": m.get("err"),
        "html_ok": h.get("ok"),
        "v7": bool(v),
    }

out = {
    "asof_run": datetime.now(timezone.utc).isoformat(),
    "crumb_ok": bool(crumb),
    "merged": merged,
    "v7_err": v7_err,
}
with open("/home/hermes/.hermes/projects/watchlist_pe.json", "w") as f:
    json.dump(out, f)
print("wrote pe json")
for t in tickers:
    m = merged[t]
    print(f"{t}\tfpe={m.get('forwardPE')}\tpeg={m.get('pegRatio')}\tfcf={m.get('fcf')}\troe={m.get('roe')}\tmod={m.get('mod_ok')}")
