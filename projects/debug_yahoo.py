import importlib.util, urllib.request
print('yfinance', importlib.util.find_spec('yfinance') is not None)
url='https://query1.finance.yahoo.com/v7/finance/quote?symbols=MSFT,NVDA&fields=regularMarketPrice,regularMarketChangePercent,forwardPE,trailingPE,marketCap,sector,industry,averageAnalystRating,targetMeanPrice'
req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        data=r.read().decode()
        print(r.status, data[:1000])
except Exception as e:
    print('ERR', type(e).__name__, e)
url2='https://query1.finance.yahoo.com/v8/finance/chart/MSFT?range=5d&interval=1d'
req=urllib.request.Request(url2, headers={'User-Agent':'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        data=r.read().decode()
        print('chart', r.status, data[:1000])
except Exception as e:
    print('ERR2', type(e).__name__, e)
