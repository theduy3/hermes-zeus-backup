#!/usr/bin/env python3
import json, urllib.request, urllib.error, time, sys

# Watchlist tickers (excluding indicator section)
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

# Build order mapping to preserve watchlist order
order = []
for g, lst in groups.items():
    for t in lst:
        order.append((g, t))

def fetch_quotes(symbols):
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=" + ",".join(symbols)
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        return data.get("quoteResponse",{}).get("result",[])
    except Exception as e:
        print("QUOTE ERR:", e, file=sys.stderr)
        return None

def fetch_chart_price(ticker):
    # Fallback for price/change via chart
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
        res = d["chart"]["result"][0]
        closes = res["indicators"]["quote"][0]["close"]
        # regular market closes from timestamp-adjacent; use meta regularMarketPrice
        meta = res["meta"]
        price = meta.get("regularMarketPrice")
        prev = meta.get("chartPreviousClose") or meta.get("previousClose")
        return price, prev
    except Exception as e:
        print("CHART ERR", ticker, e, file=sys.stderr)
        return None, None

# Batch quote fetch (all at once; Yahoo handles ~50)
quotes = fetch_quotes(all_tickers)
qmap = {}
if quotes:
    for q in quotes:
        qmap[q.get("symbol")] = q

results = {}
for g, t in order:
    q = qmap.get(t)
    price = None; prev = None; fpe = None; tpe = None; mcap = None
    if q:
        price = q.get("regularMarketPrice")
        prev = q.get("regularMarketPreviousClose") or q.get("previousClose")
        fpe = q.get("forwardPE")
        tpe = q.get("trailingPE")
        mcap = q.get("marketCap")
    if price is None or prev is None:
        p, pr = fetch_chart_price(t)
        if price is None: price = p
        if prev is None: prev = pr
    chg = None
    if price is not None and prev not in (None,0):
        chg = (price - prev)/prev*100.0
    results[t] = {
        "group": g, "price": price, "prev": prev, "chg": chg,
        "fpe": fpe, "tpe": tpe, "mcap": mcap,
    }

print("=== RESULTS ===")
print(json.dumps(results, indent=2))
