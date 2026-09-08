#!/usr/bin/env python3
import json, urllib.request, http.cookiejar, ssl, urllib.parse
ctx=ssl.create_default_context()
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
cj=http.cookiejar.CookieJar()
op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPSHandler(context=ctx))
def get(url):
    req=urllib.request.Request(url, headers={"User-Agent":UA})
    with op.open(req, timeout=20) as r: return r.read().decode()
try: get("https://fc.yahoo.com")
except: pass
crumb=get("https://query1.finance.yahoo.com/v1/test/getcrumb").strip()
url=f"https://query1.finance.yahoo.com/v7/finance/quote?symbols=KEEL&crumb={urllib.parse.quote(crumb)}"
print(get(url)[:2000])
url2=f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/KEEL?modules=defaultKeyStatistics,financialData&crumb={urllib.parse.quote(crumb)}"
print(get(url2)[:2500])
