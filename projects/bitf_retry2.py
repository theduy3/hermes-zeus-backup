import urllib.request, json
UA = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36','Accept':'application/json, text/plain, */*','Accept-Language':'en-US,en;q=0.9'}
def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode()

for host in ['query1','query2']:
    try:
        u=f'https://{host}.finance.yahoo.com/v8/finance/chart/BITF?range=5d&interval=1d'
        j=json.loads(get(u))
        m=j['chart']['result'][0]['meta']
        print(host,'YAHOO', m.get('regularMarketPrice'),'prev',m.get('chartPreviousClose'),'time',m.get('regularMarketTime'))
    except Exception as e:
        print(host,'err',repr(e))

# Nasdaq
try:
    j=json.loads(get('https://api.nasdaq.com/api/quote/BITF/info?assetclass=stocks'))
    d=j.get('data',{})
    pd=d.get('primaryData',{})
    print('NASDAQ', pd.get('lastSalePrice'), pd.get('percentageChange'), pd.get('lastTradeTimestamp'))
except Exception as e:
    print('NASDAQ err', repr(e))
