import urllib.request, re

def get(url):
    req = urllib.request.Request(url, headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
        'Accept':'application/json, text/plain, */*','Accept-Language':'en-US,en;q=0.9'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode()

# Try stockanalysis statistics/valuation API variants
variants = [
    'https://stockanalysis.com/api/symbol/s/AAPL/overview',
    'https://stockanalysis.com/api/symbol/s/AAPL/statistics',
    'https://stockanalysis.com/api/symbol/s/AAPL/valuation',
    'https://stockanalysis.com/api/symbol/s/AAPL/ratios',
    'https://stockanalysis.com/api/symbol/s/AAPL/financials',
]
for u in variants:
    try:
        t = get(u)
        print('===', u, 'len', len(t))
        print(t[:500]); print()
    except Exception as e:
        print('ERR', u, repr(e))

# Inspect overview page for API hints
print('--- page scan ---')
try:
    html = get('https://stockanalysis.com/stocks/aapl/overview')
    # find api endpoints referenced
    apis = set(re.findall(r'/api/[a-zA-Z0-9_/{}.\-]+', html))
    for a in sorted(apis)[:40]:
        print(a)
except Exception as e:
    print('page err', e)
