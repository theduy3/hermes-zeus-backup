import urllib.request, json, re
UA = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36','Accept':'application/json, text/plain, */*','Accept-Language':'en-US,en;q=0.9'}
def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode()

# 1. Yahoo chart
try:
    j = json.loads(get('https://query1.finance.yahoo.com/v8/finance/chart/BITF?range=5d&interval=1d'))
    m = j['chart']['result'][0]['meta']
    print('YAHOO', m.get('regularMarketPrice'), 'prev', m.get('chartPreviousClose'), 'time', m.get('regularMarketTime'))
except Exception as e:
    print('YAHOO err', repr(e))

# 2. StockAnalysis quotes
try:
    j = json.loads(get('https://stockanalysis.com/api/quotes/s/BITF'))
    d = j.get('data',{})
    print('SA quote', d.get('p'), d.get('cp'), d.get('cl'))
except Exception as e:
    print('SA quote err', repr(e))

# 3. StockAnalysis page for forwardPE
try:
    html = get('https://stockanalysis.com/stocks/bitf/')
    mm = re.search(r'forwardPE:"([\d.]+)"', html)
    print('SA fwdPE', mm.group(1) if mm else 'NONE')
except Exception as e:
    print('SA page err', repr(e))
