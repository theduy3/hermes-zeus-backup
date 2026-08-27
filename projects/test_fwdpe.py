import json, urllib.request
UA="Mozilla/5.0"
def get(url):
    req=urllib.request.Request(url, headers={"User-Agent":UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()

for s in ["AAPL","NVDA"]:
    try:
        u=f"https://stockanalysis.com/api/symbol/s/{s}/overview"
        d=json.loads(get(u))
        print(s, json.dumps(d.get("data",{}))[:400])
    except Exception as e:
        print(s,"ERR",e)

# retry BITF chart
for host in ["query1","query2"]:
    try:
        u=f"https://{host}.finance.yahoo.com/v8/finance/chart/BITF?range=5d&interval=1d"
        d=json.loads(get(u))
        print("BITF", d["chart"]["result"][0]["meta"]["regularMarketPrice"])
        break
    except Exception as e:
        print("BITF ERR", host, e)
