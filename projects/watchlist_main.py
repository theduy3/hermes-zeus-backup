import urllib.request, json, time, re, datetime

TICKERS = {
    "Mega-cap AI / Platforms": ["MSFT","AMZN","GOOG","META","AAPL"],
    "AI Infrastructure / Cloud": ["CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS"],
    "Consumer / Internet": ["TSLA","NFLX","MELI"],
    "Semiconductors": ["ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC"],
    "Data Centers / Power": ["BE","APLD","TE","PSIX","GLW","BW","PUMP"],
    "Crypto Miners / Bitcoin Infrastructure": ["IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE"],
    "ETFs / Funds": ["VFV.TO","GLD","SMH"],
    "Other / Unresolved": ["SPCX","RKLB","SEI","WYFI"],
}
ETFS = {"VFV.TO","GLD","SMH"}

UA = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36','Accept':'application/json, text/plain, */*','Accept-Language':'en-US,en;q=0.9'}

def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read() if binary else r.read().decode()

def yahoo_chart(t):
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=5d&interval=1d'
    j = json.loads(get(url))
    m = j['chart']['result'][0]['meta']
    price = m.get('regularMarketPrice')
    prev = m.get('chartPreviousClose') or m.get('previousClose')
    chg = None
    if price is not None and prev:
        chg = (price - prev)/prev*100
    return {
        'price': price, 'prev': prev, 'chg': chg,
        'hi52': m.get('fiftyTwoWeekHigh'), 'lo52': m.get('fiftyTwoWeekLow'),
        'time': m.get('regularMarketTime'), 'cur': m.get('currency'),
        'name': m.get('shortName')
    }

def sa_forward(t):
    base = t.lower().replace('.to','')
    paths = []
    if t in ETFS:
        paths = [f'https://stockanalysis.com/etf/{base}/', f'https://stockanalysis.com/etf/{base}']
    else:
        paths = [f'https://stockanalysis.com/stocks/{base}/', f'https://stockanalysis.com/stocks/{base}']
    for p in paths:
        try:
            html = get(p)
            mm = re.search(r'forwardPE:"([\d.]+)"', html)
            if mm:
                return float(mm.group(1))
        except Exception:
            continue
    return None

data = {}
allt = [t for v in TICKERS.values() for t in v]
for t in allt:
    rec = {'fwdpe': None}
    try:
        rec.update(yahoo_chart(t))
    except Exception as e:
        rec['yerr'] = str(e)[:80]
    try:
        rec['fwdpe'] = sa_forward(t)
    except Exception as e:
        rec['saerr'] = str(e)[:80]
    data[t] = rec
    time.sleep(0.15)

with open('/home/hermes/.hermes/projects/watchlist_data.json','w') as f:
    json.dump(data, f, indent=2, default=str)

# summary
ok = sum(1 for v in data.values() if v.get('price') is not None)
fp = sum(1 for v in data.values() if v.get('fwdpe') is not None)
print('price ok', ok, '/', len(allt), '| fwdpe ok', fp)
print('no price:', [t for t,v in data.items() if v.get('price') is None])
print('no fwdpe:', [t for t,v in data.items() if v.get('fwdpe') is None])
