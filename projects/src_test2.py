import urllib.request, json

def get(url):
    req = urllib.request.Request(url, headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
        'Accept':'application/json, text/plain, */*','Accept-Language':'en-US,en;q=0.9'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode()

tests = [
    'https://api.nasdaq.com/api/quote/MSFT/info?assetclass=stocks',
    'https://stockanalysis.com/api/symbol/s/AAPL/overview',
    'https://stockanalysis.com/api/quotes/s/AAPL',
    'https://stockanalysis.com/api/symbol/s/AAPL/statistics',
]
for u in tests:
    try:
        t = get(u)
        print('===', u)
        print(t[:700])
        print()
    except Exception as e:
        print('ERR', u, repr(e))
