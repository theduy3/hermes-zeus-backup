#!/usr/bin/env python3
import json, urllib.request, ssl

rows = json.load(open("/tmp/wl_data.json"))
for r in rows:
    if not r.get("chart_ok"):
        print("FAIL", r["ticker"], r.get("chart_err"))
    else:
        chg = r.get("chg")
        chgs = f"{chg:+.2f}%" if isinstance(chg, (int, float)) else "—"
        print(f"{r['ticker']}|{r.get('price')}|{chgs}|{r.get('ccy')}|qok={r.get('quote_ok')}|qerr={str(r.get('quote_err'))[:100]}")

print("--- probe endpoints ---")
ctx = ssl.create_default_context()
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
urls = [
    "https://query1.finance.yahoo.com/v10/finance/quoteSummary/MSFT?modules=defaultKeyStatistics",
    "https://query2.finance.yahoo.com/v10/finance/quoteSummary/MSFT?modules=defaultKeyStatistics",
    "https://query1.finance.yahoo.com/v7/finance/quote?symbols=MSFT,AAPL,NVDA",
    "https://query2.finance.yahoo.com/v7/finance/quote?symbols=MSFT,AAPL,NVDA,GOOG,META",
]
for url in urls:
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
            body = r.read()
            print("OK", r.status, url[:80], "len", len(body), body[:180])
    except Exception as e:
        print("ERR", url[:80], type(e).__name__, e)
