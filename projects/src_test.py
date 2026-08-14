import urllib.request, json

def get(url):
    req = urllib.request.Request(url, headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
        'Accept':'application/json, text/plain, */*',
        'Accept-Language':'en-US,en;q=0.9'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode()

tests = [
    'https://stockanalysis.com/api/symbol/s/MSFT',
    'https://stockanalysis.com/api/symbol/s/MSFT/overview',
    'https://api.nasdaq.com/api/quote/MSFT/info',
    'https://api.nasdaq.com/api/quote/MSFT/extended-trading',
]
for u in tests:
    try:
        t = get(u)
        print('===', u)
        print(t[:600])
        print()
    except Exception as e:
        print('ERR', u, repr(e))
