import urllib.request, json, time
UA = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36','Accept':'application/json'}
def get(u):
    req = urllib.request.Request(u, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode()
inds = ["^VIX","^TNX","^GSPC","^RUT","CAD=X","CADUSD=X","BTC-USD","GC=F"]
out = {}
for t in inds:
    try:
        j = json.loads(get(f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=5d&interval=1d'))
        m = j['chart']['result'][0]['meta']
        p = m.get('regularMarketPrice'); prev = m.get('chartPreviousClose') or m.get('previousClose')
        chg = (p-prev)/prev*100 if (p is not None and prev) else None
        out[t] = {'price':p,'chg':chg,'name':m.get('shortName'),'cur':m.get('currency')}
    except Exception as e:
        out[t] = {'err':str(e)[:60]}
    time.sleep(0.1)
print(json.dumps(out, indent=2, default=str))
