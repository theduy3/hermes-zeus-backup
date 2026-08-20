import json, urllib.request, urllib.parse, time
from datetime import datetime, timezone

groups = {
    "Mega-cap AI / Platforms": ["MSFT","AMZN","GOOG","META","AAPL"],
    "AI Infrastructure / Cloud": ["CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS"],
    "Consumer / Internet": ["TSLA","NFLX","MELI"],
    "Retail": ["HD","LOW","WMT","TGT"],
    "Semiconductors": ["ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC"],
    "Data Centers / Power": ["BE","APLD","TE","PSIX","GLW","BW","PUMP"],
    "Crypto Miners / Bitcoin Infrastructure": ["IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE"],
    "ETFs / Funds": ["VFV.TO","GLD","SMH"],
    "Other / Unresolved": ["SPCX","RKLB","SEI","WYFI"],
}
all_tickers = [t for ts in groups.values() for t in ts]
UA = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
import http.cookiejar
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [(k,v) for k,v in UA.items()]
def get(url):
    req = urllib.request.Request(url, headers=UA)
    return op.open(req, timeout=20).read().decode("utf-8")

try:
    get("https://fc.yahoo.com")
except Exception: pass
crumb = get("https://query2.finance.yahoo.com/v1/test/getcrumb").strip()
print("crumb ok len", len(crumb))

pe = {}
for t in all_tickers:
    try:
        url = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/%s?modules=defaultKeyStatistics,price,summaryDetail&crumb=%s" % (t, urllib.parse.quote(crumb, safe=''))
        j = json.loads(get(url))
        r0 = j["quoteSummary"]["result"][0]
        dks = r0.get("defaultKeyStatistics",{})
        price = r0.get("price",{})
        sd = r0.get("summaryDetail",{})
        fpe = dks.get("forwardPE") or sd.get("forwardPE")
        tpe = dks.get("trailingPE") or price.get("trailingPE") or sd.get("trailingPE")
        peg = dks.get("pegRatio")
        def num(x): return x.get("raw") if isinstance(x,dict) else x
        pe[t] = {"fwdPE": num(fpe), "trailPE": num(tpe), "peg": num(peg),
                 "name": price.get("shortName")}
        print("%-7s fwdPE=%s ttmPE=%s peg=%s" % (t, pe[t]["fwdPE"], pe[t]["trailPE"], pe[t]["peg"]))
    except Exception as e:
        pe[t] = {"error": str(e)}
        print("%-7s ERR %s" % (t, e))
    time.sleep(0.2)

with open("pe.json","w") as f:
    json.dump(pe, f, indent=2, default=str)
print("OK:%d" % sum(1 for v in pe.values() if "fwdPE" in v))
