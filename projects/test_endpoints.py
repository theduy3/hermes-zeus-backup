import json, urllib.request

UA = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")

# Test chart endpoint (prices) - skill primary method
print("=== CHART (AAPL) ===")
try:
    raw = fetch("https://query1.finance.yahoo.com/v8/finance/chart/AAPL?range=5d&interval=1d")
    j = json.loads(raw)
    meta = j["chart"]["result"][0]["meta"]
    print("regularMarketPrice:", meta.get("regularMarketPrice"))
    print("previousClose:", meta.get("previousClose"))
    print("chartPreviousClose:", meta.get("chartPreviousClose"))
    print("regularMarketTime:", meta.get("regularMarketTime"))
    print("currency:", meta.get("currency"))
except Exception as e:
    print("CHART FAIL:", e)

# Test quoteSummary for forward PE
print("=== QUOTE SUMMARY (AAPL) ===")
try:
    raw = fetch("https://query1.finance.yahoo.com/v10/finance/quoteSummary/AAPL?modules=defaultKeyStatistics,price,summaryDetail")
    j = json.loads(raw)
    dks = j["quoteSummary"]["result"][0]["defaultKeyStatistics"]
    price = j["quoteSummary"]["result"][0]["price"]
    print("forwardPE:", dks.get("forwardPE"))
    print("trailingPE (price):", price.get("trailingPE"))
    if dks.get("forwardPE"): print("forwardPE raw:", dks["forwardPE"])
except Exception as e:
    print("QUOTE SUMMARY FAIL:", repr(e))
