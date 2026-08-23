import urllib.request, json, ssl, http.cookiejar
from concurrent.futures import ThreadPoolExecutor

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

TICKERS = [
 "MSFT","AMZN","GOOG","META","AAPL",
 "CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS",
 "TSLA","NFLX","MELI",
 "HD","LOW","WMT","TGT",
 "ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC",
 "BE","APLD","TE","PSIX","GLW","BW","PUMP",
 "IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE",
 "VFV.TO","GLD","SMH",
 "SPCX","RKLB","SEI","WYFI",
]

def get_crumb():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    # fc.yahoo may 404 but crumb endpoint still works
    try:
        opener.open(urllib.request.Request("https://fc.yahoo.com/", headers={'User-Agent':'Mozilla/5.0'}), timeout=15)
    except Exception:
        pass
    try:
        with opener.open(urllib.request.Request("https://query1.finance.yahoo.com/v1/test/getcrumb", headers={'User-Agent':'Mozilla/5.0'}), timeout=15) as r:
            crumb = r.read().decode().strip()
    except Exception as e:
        crumb = None
    return crumb

CRUMB = get_crumb()

def fetch_one(t):
    out = {"ticker": t}
    # ---- chart for price + change ----
    data = None
    for host in ("query1","query2"):
        try:
            url = f"https://{host}.finance.yahoo.com/v8/finance/chart/{t}?range=5d&interval=1d"
            req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
                data = json.load(r)
            break
        except Exception as e:
            out["chart_err"] = str(e)
    if data and data.get("chart",{}).get("result"):
        try:
            res = data["chart"]["result"][0]
            ts = res["timestamp"]
            closes = res["indicators"]["quote"][0]["close"]
            valid = [(a,c) for a,c in zip(ts,closes) if c is not None]
            last = valid[-1][1]
            prev = valid[-2][1]
            out["price"] = round(last,2)
            out["chg_pct"] = round((last/prev-1)*100,2)
        except Exception as e:
            out["chart_err"] = str(e)
    # ---- quoteSummary for forward PE ----
    if CRUMB:
        qdata = None
        for host in ("query1","query2"):
            try:
                url = f"https://{host}.finance.yahoo.com/v10/finance/quoteSummary/{t}?modules=summaryDetail,defaultKeyStatistics&crumb={CRUMB}"
                req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
                    qdata = json.load(r)
                break
            except Exception as e:
                out["qs_err"] = str(e)
        if qdata and qdata.get("quoteSummary",{}).get("result"):
            try:
                sd = qdata["quoteSummary"]["result"][0].get("summaryDetail",{})
                fpe = sd.get("forwardPE",{})
                out["fwd_pe"] = fpe.get("raw") if isinstance(fpe,dict) else None
            except Exception as e:
                out["qs_err"] = str(e)
    return out

results = []
with ThreadPoolExecutor(max_workers=12) as ex:
    results = list(ex.map(fetch_one, TICKERS))

with open("/home/hermes/.hermes/projects/watchlist_data.json","w") as f:
    json.dump(results, f, indent=2)

for r in results:
    print(f"{r['ticker']:8} price={r.get('price')} chg={r.get('chg_pct')} fwdPE={r.get('fwd_pe')} err={r.get('chart_err') or r.get('qs_err') or ''}")
print("TOTAL", len(results), "CRUMB_OK", bool(CRUMB))
