#!/usr/bin/env python3
import json, urllib.request, urllib.error, time, sys

tickers = [
    # Mega-cap AI / Platforms
    "MSFT","AMZN","GOOG","META","AAPL",
    # AI Infrastructure / Cloud
    "CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS",
    # Consumer / Internet
    "TSLA","NFLX","MELI",
    # Retail
    "HD","LOW","WMT","TGT",
    # Semiconductors
    "ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC",
    # Data Centers / Power
    "BE","APLD","TE","PSIX","GLW","BW","PUMP",
    # Crypto Miners / Bitcoin Infrastructure
    "IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE",
    # ETFs / Funds
    "VFV.TO","GLD","SMH",
    # Other / Unresolved
    "SPCX","RKLB","SEI","WYFI","CRCL",
]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

def fetch(symbols):
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=" + ",".join(symbols)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

# batch in groups of 20
out = {}
batch_size = 20
for i in range(0, len(tickers), batch_size):
    batch = tickers[i:i+batch_size]
    try:
        data = fetch(batch)
        for q in data.get("quoteResponse", {}).get("result", []):
            sym = q.get("symbol")
            out[sym] = {
                "price": q.get("regularMarketPrice"),
                "chg": q.get("regularMarketChangePercent"),
                "trailingPE": q.get("trailingPE"),
                "forwardPE": q.get("forwardPE"),
                "marketCap": q.get("marketCap"),
                "regularMarketTime": q.get("regularMarketTime"),
                "currency": q.get("currency"),
                "exchange": q.get("fullExchangeName"),
                "shortName": q.get("shortName"),
            }
    except Exception as e:
        print(f"BATCH ERR {batch}: {e}", file=sys.stderr)
    time.sleep(0.3)

print(json.dumps(out, indent=2))
