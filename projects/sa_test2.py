import urllib.request, re
def get(url):
    req = urllib.request.Request(url, headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
        'Accept':'text/html,application/json,*/*','Accept-Language':'en-US,en;q=0.9'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode()
# main stock page
html = get('https://stockanalysis.com/stocks/aapl')
print('len', len(html))
apis = sorted(set(re.findall(r'/api/[a-zA-Z0-9_/{}.\-]+', html)))
for a in apis:
    print(a)
# also look for forwardPE in page
m = re.findall(r'.{0,30}forwardPE.{0,30}', html, re.I)
print('forwardPE mentions:', len(m))
for x in m[:5]:
    print(x)
