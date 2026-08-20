import json, urllib.request, urllib.error, time, sys

# Watchlist tickers (parsed from /vault/System/Stock Watchlist.md, excluding the Indicators section)
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

all_tickers = []
for g, ts in groups.items():
    all_tickers.extend(ts)

UA = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

def fetch_url(url, data=None, headers=None, timeout=20):
    h = dict(UA)
    if headers: h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8")

# 1) Batch quote endpoint for price, change, forward PE
results = {}
quote_url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=" + ",".join(all_tickers)
try:
    raw = fetch_url(quote_url)
    j = json.loads(raw)
    for q in j.get("quoteResponse",{}).get("result",[]):
        t = q.get("symbol")
        results[t] = {
            "price": q.get("regularMarketPrice"),
            "prevClose": q.get("regularMarketPreviousClose"),
            "fwdPE": q.get("forwardPE"),
            "trailPE": q.get("trailingPE"),
            "marketCap": q.get("marketCap"),
            "name": q.get("shortName"),
            "currency": q.get("currency"),
            "marketTime": q.get("regularMarketTime"),
            "source":"quote",
        }
    print("QUOTE_OK count=%d" % len(results))
except Exception as e:
    print("QUOTE_FAIL: %s" % e)

# Persist quote results
with open("quote_results.json","w") as f:
    json.dump(results,f,indent=2,default=str)
print("Saved quote_results.json with %d tickers" % len(results))
