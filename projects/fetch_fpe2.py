#!/usr/bin/env python3
import json, urllib.request, urllib.error, time, sys, re, http.cookiejar

groups = {
    "Mega-cap AI / Platforms": ["MSFT","AMZN","GOOG","META","AAPL"],
    "AI Infrastructure / Cloud": ["CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS"],
    "Consumer / Internet": ["TSLA","NFLX","MELI"],
    "Semiconductors": ["ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC"],
    "Data Centers / Power": ["BE","APLD","TE","PSIX","GLW","BW","PUMP"],
    "Crypto Miners / Bitcoin Infrastructure": ["IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE"],
    "ETFs / Funds": ["VFV.TO","GLD","SMH"],
    "Other / Unresolved": ["SPCX","RKLB","SEI","WYFI"],
}
all_tickers = [t for g in groups.values() for t in g]

def get_crumb():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    hdr = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}
    try:
        opener.open("https://fc.yahoo.com", timeout=20)
    except Exception as e:
        print("fc err", e, file=sys.stderr)
    try:
        r = opener.open("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=20)
        crumb = r.read().decode().strip()
        if crumb and len(crumb) < 50:
            return crumb, opener
    except Exception as e:
        print("crumb err", e, file=sys.stderr)
    return None, opener

crumb, opener = get_crumb()
print("CRUMB:", repr(crumb), file=sys.stderr)

def fetch_summary(ticker, crumb, opener):
    if not crumb:
        return None, None
    url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=summaryDetail,defaultKeyStatistics&crumb={crumb}"
    hdr = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}
    try:
        r = opener.open(urllib.request.Request(url, headers=hdr), timeout=30)
        d = json.loads(r.read().decode())
        res = d.get("quoteSummary",{}).get("result")
        if not res:
            return None, None
        r0 = res[0]
        sd = r0.get("summaryDetail",{}) or {}
        dks = r0.get("defaultKeyStatistics",{}) or {}
        fpe = sd.get("forwardPE") or dks.get("forwardPE")
        if isinstance(fpe, dict): fpe = fpe.get("raw")
        return fpe, None
    except Exception as e:
        print("ERR", ticker, e, file=sys.stderr)
        return None, None

out = {}
if crumb:
    for t in all_tickers:
        fpe, _ = fetch_summary(t, crumb, opener)
        out[t] = fpe
        time.sleep(0.12)
else:
    for t in all_tickers:
        out[t] = None

print("=== FPE ===")
print(json.dumps(out, indent=2))
