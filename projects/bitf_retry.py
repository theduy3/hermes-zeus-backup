import urllib.request, json, ssl, http.cookiejar
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
CJ=http.cookiejar.CookieJar(); OP=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CJ))
for host in ('query1','query2'):
    try:
        url=f'https://{host}.finance.yahoo.com/v8/finance/chart/BITF?range=5d&interval=1d'
        with OP.open(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=15) as r:
            d=json.load(r)
        res=d['chart']['result'][0]; ts=res['timestamp']; cl=res['indicators']['quote'][0]['close']
        v=[(a,c) for a,c in zip(ts,cl) if c is not None]
        print('BITF last',v[-1][1],'prev',v[-2][1])
        break
    except Exception as e:
        print('err',host,e)
