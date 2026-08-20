import json, urllib.request, time, math

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
        closes = res["indicators"]["quote"][0]["close"]
        # filter None
        valid = [c for c in closes if c is not None]
        price = meta.get("regularMarketPrice")
        if price is None and valid:
            price = valid[-1]
        prev = None
        if len(valid) >= 2:
            prev = valid[-2]
        chg = None
        if price is not None and prev is not None and prev != 0:
            chg = (price - prev)/prev*100.0
        results[t] = {
            "price": price, "prevClose": prev, "chg": chg,
            "currency": meta.get("currency"), "time": meta.get("regularMarketTime"),
            "name": meta.get("shortName"), "exchange": meta.get("exchangeName"),
        }
        print("OK %-7s price=%.2f prev=%.2f chg=%s" % (t, price if price else 0, prev if prev else 0, ("%.2f%%"%chg) if chg is not None else "NA"))
    except Exception as e:
        results[t] = {"error": str(e)}
        print("FAIL %-7s %s" % (t, e))
    time.sleep(0.25)

with open("prices.json","w") as f:
    json.dump(results, f, indent=2, default=str)
print("Total:%d OK:%d" % (len(all_tickers), sum(1 for v in results.values() if "price" in v)))
