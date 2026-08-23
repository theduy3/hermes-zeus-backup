import urllib.request, json, ssl, http.cookiejar

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Step 1: get cookies
try:
    req = urllib.request.Request("https://fc.yahoo.com/", headers={'User-Agent':'Mozilla/5.0'})
    opener.open(req, timeout=15)
    print("cookie fetch ok", [c.name for c in cj])
except Exception as e:
    print("cookie fetch err", e)

# Step 2: get crumb
crumb = None
try:
    req = urllib.request.Request("https://query1.finance.yahoo.com/v1/test/getcrumb", headers={'User-Agent':'Mozilla/5.0'})
    with opener.open(req, timeout=15) as r:
        crumb = r.read().decode().strip()
    print("crumb:", crumb)
except Exception as e:
    print("crumb err", e)

# Step 3: quoteSummary with crumb
if crumb:
    url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/MSFT?modules=summaryDetail,defaultKeyStatistics&crumb={crumb}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
        with opener.open(req, timeout=15) as r:
            data = json.load(r)
        fpe = data["quoteSummary"]["result"][0]["summaryDetail"]["forwardPE"]
        print("MSFT fwdPE:", fpe)
    except Exception as e:
        print("qs err", e)
