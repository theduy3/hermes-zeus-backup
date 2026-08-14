import urllib.request, json

def fetch(url):
    req = urllib.request.Request(url, headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept':'application/json'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())

# chart test
u='https://query1.finance.yahoo.com/v8/finance/chart/MSFT?range=5d&interval=1d'
j=fetch(u)
m=j['chart']['result'][0]['meta']
print('CHART meta keys:', list(m.keys()))
print('price', m.get('regularMarketPrice'), 'prevClose', m.get('chartPreviousClose'), m.get('previousClose'))
print('time', m.get('regularMarketTime'))

# quoteSummary test
u2='https://query1.finance.yahoo.com/v10/finance/quoteSummary/MSFT?modules=defaultKeyStatistics,summaryDetail'
try:
    j2=fetch(u2)
    res=j2.get('quoteSummary',{}).get('result',[{}])
    if res:
        dd=res[0]
        print('QS OK', list(dd.keys()))
        print('fwdPE dks', dd.get('defaultKeyStatistics',{}).get('forwardPE'))
        print('fwdPE sd', dd.get('summaryDetail',{}).get('forwardPE'))
    else:
        print('QS result empty', j2)
except Exception as e:
    print('QS ERR', repr(e))
