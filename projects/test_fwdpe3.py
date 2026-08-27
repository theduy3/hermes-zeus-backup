import json, urllib.request
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
def get(url):
    req=urllib.request.Request(url, headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()

# full quotes data
d=json.loads(get("https://stockanalysis.com/api/quotes/s/AAPL"))
print("QUOTES KEYS:", list(d["data"].keys()))
print()

# try financials/valuation endpoints
for u in [
    "https://stockanalysis.com/api/symbol/s/AAPL/overview",
    "https://stockanalysis.com/api/symbol/s/AAPL/financials/growth",
    "https://stockanalysis.com/api/symbol/s/AAPL/ratios",
    "https://stockanalysis.com/api/symbol/s/AAPL/valuation",
]:
    try:
        dd=json.loads(get(u))
        print("OK", u, list(dd.get("data",{}).keys()) if isinstance(dd.get("data"),dict) else json.dumps(dd)[:200])
    except Exception as e:
        print("ERR", u, e)
