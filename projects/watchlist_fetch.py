import urllib.request, json, time, sys

TICKERS = {
    "Mega-cap AI / Platforms": ["MSFT","AMZN","GOOG","META","AAPL"],
    "AI Infrastructure / Cloud": ["CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS"],
    "Consumer / Internet": ["TSLA","NFLX","MELI"],
    "Semiconductors": ["ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC"],
    "Data Centers / Power": ["BE","APLD","TE","PSIX","GLW","BW","PUMP"],
    "Crypto Miners / Bitcoin Infrastructure": ["IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE"],
    "ETFs / Funds": ["VFV.TO","GLD","SMH"],
    "Other / Unresolved": ["SPCX","RKLB","SEI","WYFI"],
}

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())

all_t = [t for v in TICKERS.values() for t in v]
data = {}
# batch of 12
batch = 12
for i in range(0, len(all_t), batch):
    grp = all_t[i:i+batch]
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=" + ",".join(grp)
    try:
        j = fetch(url)
        for q in j.get("quoteResponse",{}).get("result",[]):
            sym = q.get("symbol")
            data[sym] = {
                "price": q.get("regularMarketPrice"),
                "chg": q.get("regularMarketChangePercent"),
                "fwdpe": q.get("forwardPE"),
                "trailingpe": q.get("trailingPE"),
                "mktcap": q.get("marketCap"),
                "name": q.get("shortName"),
                "time": q.get("regularMarketTime"),
                "currency": q.get("currency"),
            }
    except Exception as e:
        print(f"BATCH ERR {grp}: {e}", file=sys.stderr)
    time.sleep(0.3)

with open("/home/hermes/.hermes/projects/watchlist_data.json","w") as f:
    json.dump(data, f, indent=2, default=str)
print("OK fetched", len(data), "of", len(all_t))
print("MISSING:", [t for t in all_t if t not in data])
