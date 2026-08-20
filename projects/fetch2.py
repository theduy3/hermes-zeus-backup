import json, urllib.request, time
from datetime import datetime, timezone

groups = {
    "Mega-cap AI / Platforms": ["MSFT","AMZN","GOOG","META","AAPL"],
    "AI Infrastructure / Cloud": ["CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS"],
    "Consumer / Internet": ["TSLA","NFLX","MELI"],
    "Retail": ["HD","LOW","WMT","TGT"],
    "Semiconductors": ["ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC"],
    "Data Centers / Power": ["BE","APLD","TE","PSIX","GLW","BW","PUMP"],
    "Crypto Miners / Bitcoin Infrastructure": ["IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE"],
    "ETFs / Funds": ["VFV.TO","GLD","SMH"],
    "Other / Unresolved": ["SPCX","RKLB","SEI","WYFI"],
}
all_tickers = [t for ts in groups.values() for t in ts]
UA = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")

results = {}
for t in all_tickers:
    try:
        raw = fetch("https://query1.finance.yahoo.com/v8/finance/chart/%s?range=5d&interval=1d" % t)
        j = json.loads(raw)
        res = j["chart"]["result"][0]
        meta = res["meta"]
        closes = [c for c in res["indicators"]["quote"][0]["close"] if c is not None]
        price = closes[-1] if closes else meta.get("regularMarketPrice")
        prev = closes[-2] if len(closes) >= 2 else None
        chg = (price-prev)/prev*100.0 if (price is not None and prev) else None
        ts = meta.get("regularMarketTime")
        dt = datetime.fromtimestamp(ts, tz=timezone.utc) if ts else None
        results[t] = {"price":round(price,2),"prevClose":round(prev,2) if prev else None,
                      "chg":round(chg,2) if chg is not None else None,
                      "metaPx":meta.get("regularMarketPrice"),
                      "currency":meta.get("currency"),"time":dt.isoformat() if dt else None,
                      "name":meta.get("shortName")}
        print("OK %-7s close=%.2f prev=%.2f chg=%s metaPx=%.2f t=%s" % (t,price,prev if prev else 0,("%.2f%%"%chg) if chg is not None else "NA", meta.get("regularMarketPrice"), dt))
    except Exception as e:
        results[t] = {"error":str(e)}
        print("FAIL %-7s %s" % (t,e))
    time.sleep(0.25)

# Test stockanalysis.com for forward PE on a sample
print("\n--- stockanalysis test ---")
for t in ["AAPL","NVDA","MSFT"]:
    try:
        raw = fetch("https://stockanalysis.com/api/symbol/s/%s" % t)
        j = json.loads(raw)
        d = j.get("data",{})
        print("%s fwdPE=%s trailPE=%s" % (t, d.get("forwardPE"), d.get("trailingPE")))
    except Exception as e:
        print("%s FAIL %s" % (t,e))
    time.sleep(0.3)

with open("prices2.json","w") as f:
    json.dump(results,f,indent=2,default=str)
print("\nSaved prices2.json OK:%d" % sum(1 for v in results.values() if "price" in v))
