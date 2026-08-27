import json, urllib.request
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
def get(url):
    req=urllib.request.Request(url, headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()

candidates = [
    "https://stockanalysis.com/api/symbol/s/AAPL",
    "https://stockanalysis.com/api/quotes/s/AAPL",
    "https://stockanalysis.com/api/symbol/s/AAPL/overview?range=1d",
    "https://api.stockanalysis.com/api/symbol/s/AAPL",
]
for u in candidates:
    try:
        d=json.loads(get(u))
        print("OK", u, json.dumps(d)[:300])
    except Exception as e:
        print("ERR", u, e)
