#!/usr/bin/env python3
import json, urllib.request, urllib.error, time, sys

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
order = []
for g, lst in groups.items():
    for t in lst:
        order.append((g, t))

HDR = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
    "Referer":"https://www.cnbc.com/",
    "Accept":"application/json",
}

def fetch(ticker):
    url = ("https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol"
           f"?symbols={ticker}&requestMethod=itv&noform=1&partnerId=2&fund=1&exthrs=1&output=json&events=quote")
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=HDR)
            with urllib.request.urlopen(req, timeout=25) as r:
                d = json.load(r)
            qr = d.get("FormattedQuoteResult",{}).get("FormattedQuote",[{}])
            q = qr[0] if qr else {}
            if q.get("code") == 0:
                return q
            return None
        except Exception as e:
            if attempt == 2:
                print("ERR", ticker, e, file=sys.stderr)
            time.sleep(0.4)
    return None

def num(s):
    if s is None: return None
    s = str(s).replace(",","").replace("%","").replace("$","").strip()
    if s in ("","N/A","--","NA"): return None
    try: return float(s)
    except: return None

results = {}
for g, t in order:
    q = fetch(t)
    if not q:
        results[t] = {"group":g, "ok":False}
        time.sleep(0.12)
        continue
    ext = q.get("ExtendedMktQuote") or {}
    results[t] = {
        "group": g, "ok": True,
        "last": num(q.get("last")),
        "chg_pct": num(q.get("change_pct")),
        "pe": num(q.get("pe")),
        "fpe": num(q.get("fpe")),
        "mktcap": q.get("mktcapView"),
        "yrhi": num(q.get("yrhiprice")),
        "yrlo": num(q.get("yrloprice")),
        "name": q.get("name"),
        "curmktstatus": q.get("curmktstatus"),
        "ext_last": num(ext.get("last")) if ext else None,
        "ext_chg": num(ext.get("change_pct")) if ext else None,
        "ext_type": ext.get("type") if ext else None,
    }
    time.sleep(0.12)

print(json.dumps(results, indent=2))
