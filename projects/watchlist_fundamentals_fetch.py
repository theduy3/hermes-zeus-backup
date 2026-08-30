#!/usr/bin/env python3
import re, json, urllib.request, ssl, time, http.cookiejar
from urllib.parse import quote

ctx = ssl.create_default_context()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

tickers = [
    "MSFT","AMZN","GOOG","META","AAPL",
    "CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS",
    "TSLA","NFLX","MELI",
    "HD","LOW","WMT","TGT",
    "ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC",
    "BE","APLD","TE","PSIX","GLW","BW","PUMP",
    "IREN","CORZ","RIOT","CLSK","BTDR","HIVE",
    "GLD","SMH","SPCX","RKLB","SEI","WYFI","CRCL",
]

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cj),
    urllib.request.HTTPSHandler(context=ctx),
)
opener.addheaders = [("User-Agent", UA), ("Accept-Language", "en-US,en;q=0.9")]


def fetch(url, timeout=25):
    with opener.open(url, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


# Yahoo crumb attempt
crumb = None
try:
    try:
        opener.open("https://fc.yahoo.com", timeout=15).read()
    except Exception as e:
        print("fc:", e)
    crumb = opener.open("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=15).read().decode()
    print("CRUMB", crumb)
except Exception as e:
    print("crumb fail", e)

yahoo = {}
if crumb:
    for t in tickers:
        url = (
            f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{quote(t)}"
            f"?modules=defaultKeyStatistics,financialData,earningsTrend&crumb={quote(crumb)}"
        )
        try:
            data = json.loads(fetch(url))
            res = data["quoteSummary"]["result"][0]
            ks = res.get("defaultKeyStatistics") or {}
            fd = res.get("financialData") or {}
            et = res.get("earningsTrend") or {}

            def raw(x):
                if x is None:
                    return None
                if isinstance(x, dict):
                    return x.get("raw", x.get("fmt"))
                return x

            growth = None
            for tr in et.get("trend") or []:
                if tr.get("period") == "0y":
                    growth = raw((tr.get("earningsEstimate") or {}).get("growth"))
                    if growth is None:
                        growth = raw(tr.get("growth"))
            yahoo[t] = {
                "fwd_pe": raw(ks.get("forwardPE")),
                "trailing_pe": raw(ks.get("trailingPE")),
                "peg": raw(ks.get("pegRatio")),
                "fcf": raw(fd.get("freeCashflow")),
                "roa": raw(fd.get("returnOnAssets")),
                "roe": raw(fd.get("returnOnEquity")),
                "earn_growth": growth,
                "target": raw(fd.get("targetMeanPrice")),
                "rec": raw(fd.get("recommendationKey")),
                "ok": True,
            }
            print("Y", t, yahoo[t].get("fwd_pe"), yahoo[t].get("peg"), yahoo[t].get("fcf"))
            time.sleep(0.12)
        except Exception as e:
            yahoo[t] = {"ok": False, "error": str(e)}
            print("Yerr", t, e)
            time.sleep(0.2)

# Finviz scrape
finviz = {}
for t in tickers:
    url = f"https://finviz.com/quote.ashx?t={t}&p=d"
    try:
        html = fetch(url)

        def grab(label):
            m = re.search(
                rf">\s*{re.escape(label)}\s*</td>\s*<td[^>]*>\s*([^<]+)\s*<",
                html,
                re.I,
            )
            return m.group(1).strip() if m else None

        row = {
            "fwd_pe": grab("Forward P/E"),
            "pe": grab("P/E"),
            "peg": grab("PEG"),
            "roi": grab("ROI"),
            "oper_margin": grab("Oper. Margin"),
            "profit_margin": grab("Profit Margin"),
            "eps_this_y": grab("EPS this Y"),
            "eps_next_y": grab("EPS next Y"),
            "eps_next_5y": grab("EPS next 5Y"),
            "target": grab("Target Price"),
            "recom": grab("Recom"),
            "price": grab("Price"),
            "ok": True,
        }
        finviz[t] = row
        print("F", t, row.get("fwd_pe"), row.get("peg"), row.get("roi"), row.get("eps_next_y"))
        time.sleep(0.4)
    except Exception as e:
        finviz[t] = {"ok": False, "error": str(e)}
        print("Ferr", t, e)
        time.sleep(0.6)

out = {"yahoo": yahoo, "finviz": finviz}
path = "/home/hermes/.hermes/projects/watchlist_fundamentals.json"
with open(path, "w") as f:
    json.dump(out, f, indent=2)
print("WROTE", path)
