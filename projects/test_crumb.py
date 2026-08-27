import json, urllib.request, http.cookiejar
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
cj=http.cookiejar.CookieJar()
op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
def get(url):
    req=urllib.request.Request(url, headers={"User-Agent":UA})
    with op.open(req, timeout=25) as r:
        return r.read()

# get cookie
try:
    get("https://fc.yahoo.com")
except Exception as e:
    print("fc err", e)
# get crumb
try:
    crumb=json.loads(get("https://query1.finance.yahoo.com/v1/test/getcrumb").decode())
    print("CRUMB:", crumb)
except Exception as e:
    print("crumb err", e)
    crumb=None

if crumb:
    u=f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/AAPL?modules=summaryDetail,defaultKeyStatistics&crumb={crumb}"
    try:
        d=json.loads(get(u))
        sd=d["quoteSummary"]["result"][0]["summaryDetail"]
        print("FWD PE:", sd.get("forwardPE"))
        print("TRL PE:", sd.get("trailingPE"))
    except Exception as e:
        print("qs err", e)
