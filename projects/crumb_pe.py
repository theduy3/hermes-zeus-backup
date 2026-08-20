import json, urllib.request, urllib.error, http.cookiejar

UA = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [(k,v) for k,v in UA.items()]

def get(url):
    req = urllib.request.Request(url, headers=UA)
    return op.open(req, timeout=20).read().decode("utf-8")

# Step 1: get cookies
try:
    get("https://fc.yahoo.com")
except Exception as e:
    print("cookie priming err:", e)
# Step 2: get crumb
crumb = None
try:
    crumb = get("https://query2.finance.yahoo.com/v1/test/getcrumb").strip()
    print("CRUMB:", crumb[:40] if crumb else None)
except Exception as e:
    print("CRUMB FAIL:", e)

if crumb:
    for t in ["AAPL","NVDA","MSFT"]:
        try:
            url = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/%s?modules=defaultKeyStatistics,price&crumb=%s" % (t, crumb)
            raw = get(url)
            j = json.loads(raw)
            dks = j["quoteSummary"]["result"][0]["defaultKeyStatistics"]
            fp = dks.get("forwardPE")
            tp = j["quoteSummary"]["result"][0]["price"].get("trailingPE")
            print("%s forwardPE=%s trailingPE=%s" % (t, fp, tp))
        except Exception as e:
            print("%s FAIL %s" % (t, e))
