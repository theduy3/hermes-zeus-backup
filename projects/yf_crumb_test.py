import urllib.request, json, http.cookiejar

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def get(url, headers=None):
    h = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
         'Accept':'application/json','Accept-Language':'en-US,en;q=0.9'}
    if headers: h.update(headers)
    req = urllib.request.Request(url, headers=h)
    return opener.open(req, timeout=20).read().decode()

# get cookies
try:
    get('https://finance.yahoo.com/')
except Exception as e:
    print('cookie page err', e)
print('cookies:', [c.name for c in cj])
crumb = None
for host in ['query1.finance.yahoo.com','query2.finance.yahoo.com']:
    try:
        crumb = get(f'https://{host}/v1/test/getcrumb')
        print('crumb from', host, '=', repr(crumb)[:40])
        if crumb and len(crumb) > 5:
            break
    except Exception as e:
        print('crumb err', host, e)

if crumb and len(crumb) > 5:
    u = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/MSFT?modules=defaultKeyStatistics,summaryDetail&crumb={crumb}'
    try:
        j = json.loads(get(u))
        res = j.get('quoteSummary',{}).get('result',[{}])
        if res:
            dd = res[0]
            fwd = dd.get('defaultKeyStatistics',{}).get('forwardPE') or dd.get('summaryDetail',{}).get('forwardPE')
            print('FWD PE MSFT =', fwd)
        else:
            print('empty result', j)
    except Exception as e:
        print('qs err', e)
else:
    print('NO CRUMB')
