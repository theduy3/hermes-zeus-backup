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
all_tickers = [t for g in groups.values() for t in g]

def fetch_summary(ticker):
    for host in ["query1","query2"]:
        url = f"https://{host}.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=summaryDetail,defaultKeyStatistics,price"
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.load(r)
            res = d.get("quoteSummary",{}).get("result")
            if not res:
                continue
            r0 = res[0]
            sd = r0.get("summaryDetail",{}) or {}
            dks = r0.get("defaultKeyStatistics",{}) or {}
            fpe = sd.get("forwardPE") or dks.get("forwardPE")
            if fpe is not None and isinstance(fpe, dict):
                fpe = fpe.get("raw")
            tpe = sd.get("trailingPE")
            if tpe is not None and isinstance(tpe, dict):
                tpe = tpe.get("raw")
            return fpe, tpe
        except Exception as e:
            print("ERR", ticker, host, e, file=sys.stderr)
            time.sleep(0.3)
    return None, None

out = {}
for t in all_tickers:
    fpe, tpe = fetch_summary(t)
    out[t] = {"fpe": fpe, "tpe": tpe}
    time.sleep(0.15)

print("=== FPE ===")
print(json.dumps(out, indent=2))
