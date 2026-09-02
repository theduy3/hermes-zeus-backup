#!/usr/bin/env python3
import json, urllib.request, urllib.parse, ssl, re, concurrent.futures
from datetime import datetime, timezone

print("ts", datetime.fromtimestamp(1788183000, tz=timezone.utc).isoformat())

ctx = ssl.create_default_context()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
cj = urllib.request.HTTPCookieProcessor()
opener = urllib.request.build_opener(cj, urllib.request.HTTPSHandler(context=ctx))
opener.addheaders = [("User-Agent", UA)]

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with opener.open(req, timeout=25) as r:
        return r.read().decode("utf-8", "replace"), r.geturl(), r.status

# crumb flow
try:
    get("https://fc.yahoo.com")
except Exception as e:
    print("fc err", e)
try:
    get("https://finance.yahoo.com")
except Exception as e:
    print("home err", e)
try:
    crumb_body, _, _ = get("https://query2.finance.yahoo.com/v1/test/getcrumb")
    print("crumb", crumb_body[:120])
    crumb = crumb_body.strip()
except Exception as e:
    print("crumb err", e)
    crumb = None

tickers = ["AAPL","MSFT","NVDA","META","GOOG","AMZN","AVGO","AMD","MU","TSM","ASML","INTC","CRM","PLTR","ORCL","TSLA","NFLX","HD","WMT","TGT","LOW","DELL","INFY","MELI"]
if crumb:
    for t in tickers[:8]:
        url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{t}?modules=defaultKeyStatistics,summaryDetail,financialData&crumb={urllib.parse.quote(crumb)}"
        try:
            body, _, st = get(url)
            print(t, st, body[:300].replace("\n"," "))
        except Exception as e:
            print(t, "err", e)

# finviz quote pages for key names
def parse_finviz(t):
    url = f"https://finviz.com/quote.ashx?t={urllib.parse.quote(t)}"
    try:
        body, _, st = get(url)
    except Exception as e:
        return {"t": t, "ok": False, "err": str(e)}
    # table cells: <td ...>Forward P/E</td><td ...>12.34</td>
    def find_metric(label):
        m = re.search(rf">{re.escape(label)}</td>\s*<td[^>]*>([^<]+)</td>", body, re.I)
        if m:
            return m.group(1).strip()
        return None
    out = {
        "t": t,
        "ok": True,
        "fwd_pe": find_metric("Forward P/E"),
        "pe": find_metric("P/E"),
        "peg": find_metric("PEG"),
        "roe": find_metric("ROE"),
        "roa": find_metric("ROA"),
        "oper_margin": find_metric("Oper. Margin"),
        "profit_margin": find_metric("Profit Margin"),
        "eps_this_y": find_metric("EPS this Y"),
        "eps_next_y": find_metric("EPS next Y"),
        "eps_next_5y": find_metric("EPS next 5Y"),
        "target": find_metric("Target Price"),
        "recom": find_metric("Recom"),
        "price": find_metric("Price"),
    }
    return out

all_t = [
"MSFT","AMZN","GOOG","META","AAPL",
"CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS",
"TSLA","NFLX","MELI",
"HD","LOW","WMT","TGT",
"ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC",
"BE","APLD","TE","PSIX","GLW","BW","PUMP",
"IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE",
"VFV.TO","GLD","SMH",
"SPCX","RKLB","SEI","WYFI","CRCL"
]

# finviz uses GOOGL sometimes; try as-is
results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
    futs = list(ex.map(parse_finviz, all_t))
    results = futs

with open("/home/hermes/.hermes/projects/watchlist_pe_out.json", "w") as f:
    json.dump(results, f, indent=2)
print("WROTE", len(results))
for r in results:
    if r.get("ok"):
        print(json.dumps({k: r.get(k) for k in ("t","fwd_pe","peg","roe","eps_next_y","eps_next_5y","recom","price")}))
    else:
        print(json.dumps({"t": r.get("t"), "ok": False, "err": r.get("err")}))
