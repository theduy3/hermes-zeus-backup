#!/usr/bin/env python3
import json, datetime
from pathlib import Path

# timestamp
m=json.load(open("/tmp/msft_chart.json"))["chart"]["result"][0]["meta"]
ts=m.get("regularMarketTime")
print("ASOF", datetime.datetime.utcfromtimestamp(ts).isoformat()+"Z", "EDT offset", m.get("gmtoffset"), "price", m.get("regularMarketPrice"), "chg%", m.get("regularMarketChangePercent"))

# bitf
for p in ["/tmp/bitf_chart.json","/tmp/bitfto_chart.json"]:
    print(p, open(p).read()[:200])

# parsed summary
text=Path("/tmp/ks_parsed.txt").read_text()
# print summary section
if "---SUMMARY---" in text:
    print(text.split("---SUMMARY---",1)[1])
else:
    print(text[-8000:])

# parse APLD from new html
import re
html=open("/tmp/apld_ks2.html",encoding="utf-8",errors="replace").read()
for pat,key in [
    (r'"forwardPE"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "fwd_pe"),
    (r'"pegRatio"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "peg"),
    (r'"returnOnEquity"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "roe"),
    (r'"returnOnAssets"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "roa"),
    (r'"freeCashflow"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "fcf"),
    (r'"operatingCashflow"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "ocf"),
    (r'"profitMargins"\s*:\s*\{\s*"raw"\s*:\s*([^,}]+)', "pm"),
]:
    mm=re.search(pat, html)
    print("APLD", key, mm.group(1) if mm else None)

plain=re.sub(r"<script[\s\S]*?</script>"," ",html,flags=re.I)
plain=re.sub(r"<[^>]+>"," ",plain)
plain=re.sub(r"\s+"," ",plain)
for lab in ["Forward P/E","PEG Ratio","Return on Equity","Levered Free Cash Flow","Profit Margin"]:
    i=plain.find(lab)
    print("APLD snip", lab, plain[i:i+70] if i>=0 else "MISSING")
