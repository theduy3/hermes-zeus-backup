import json, urllib.request
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
def get(url):
    req=urllib.request.Request(url, headers={"User-Agent":UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()

# stockanalysis quotes for BITF
for sym in ["BITF","BITF.C"]:
    try:
        d=json.loads(get(f"https://stockanalysis.com/api/quotes/s/{sym}"))
        print("SA", sym, d.get("data",{}).get("p"), d.get("data",{}).get("cp"))
    except Exception as e:
        print("SA ERR", sym, e)

# yahoo chart 1d for BITF
for host in ["query1","query2"]:
    try:
        d=json.loads(get(f"https://{host}.finance.yahoo.com/v8/finance/chart/BITF?range=1d&interval=1d"))
        print("YH", host, d["chart"]["result"][0]["meta"]["regularMarketPrice"])
        break
    except Exception as e:
        print("YH ERR", host, e)
