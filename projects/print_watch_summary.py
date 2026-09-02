#!/usr/bin/env python3
import json, urllib.request, ssl
from datetime import datetime, timezone
UA = "Mozilla/5.0"
ctx = ssl.create_default_context()
for t in ["KEEL", "BITF", "SEI"]:
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=5d&interval=1d"
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        data = json.loads(urllib.request.urlopen(req, context=ctx, timeout=15).read())
        m = data["chart"]["result"][0]["meta"]
        print(t, m.get("regularMarketPrice"), m.get("regularMarketChangePercent"), m.get("symbol"))
    except Exception as e:
        print(t, "ERR", e)
d = json.load(open("/home/hermes/.hermes/projects/watchlist_data.json"))
print("price_fetched", d["fetched_at_utc"])
f = json.load(open("/home/hermes/.hermes/projects/watchlist_fundamentals.json"))
print("fund_fetched", f["fetched_at_utc"])
for t in ["MSFT","NVDA","MU","META","GOOG","AVGO","ORCL","AAPL","TSLA","AMD","PLTR","WMT","DELL","CRM","NFLX","TSM","AMZN","LOW","HD","TGT","MELI","INFY","ASML","INTC","BE","GLW"]:
    r = f["results"].get(t, {})
    c = d["results"].get(t, {}).get("chart", {})
    print(f"{t}|{c.get('price')}|{c.get('chg_pct')}|{r.get('forwardPE')}|{r.get('pegRatio')}")
