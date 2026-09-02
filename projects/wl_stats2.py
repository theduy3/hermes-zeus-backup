#!/usr/bin/env python3
import json, urllib.request, urllib.parse, ssl, time, http.cookiejar, re

tickers = [
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

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
ctx = ssl.create_default_context()
jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar), urllib.request.HTTPSHandler(context=ctx))

def get(url, timeout=30):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with opener.open(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace"), r.status

# multi-step cookie seed
for u in [
    "https://finance.yahoo.com/",
    "https://finance.yahoo.com/quote/AAPL",
]:
    try:
        get(u)
        time.sleep(0.3)
    except Exception as e:
        print("seed fail", u, e)

crumb = None
for host in ["query2", "query1"]:
    try:
        body, st = get(f"https://{host}.finance.yahoo.com/v1/test/getcrumb")
        print("crumb try", host, st, body[:80])
        if body and "Too Many" not in body and "<" not in body:
            crumb = body.strip()
            break
    except Exception as e:
        print("crumb err", host, e)

print("FINAL CRUMB", crumb)
print("COOKIES", [(c.domain, c.name, c.value[:20] if c.value else None) for c in jar])

def gv(d, k):
    v = (d or {}).get(k)
    if isinstance(v, dict):
        return v.get("raw", v.get("fmt"))
    return v

results = {}
if crumb:
    for i, t in enumerate(tickers):
        modules = "defaultKeyStatistics,financialData,summaryDetail,earningsTrend"
        url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(t)}?modules={modules}&crumb={urllib.parse.quote(crumb)}"
        try:
            body, st = get(url)
            data = json.loads(body)
            res = (data.get("quoteSummary") or {}).get("result")
            if not res:
                results[t] = {"t": t, "ok": False, "err": str((data.get("quoteSummary") or {}).get("error") or data)[:180]}
            else:
                res = res[0]
                dks = res.get("defaultKeyStatistics") or {}
                fd = res.get("financialData") or {}
                sd = res.get("summaryDetail") or {}
                et = res.get("earningsTrend") or {}
                out = {"t": t, "ok": True}
                out["forwardPE"] = gv(dks, "forwardPE") or gv(sd, "forwardPE")
                out["trailingPE"] = gv(dks, "trailingPE") or gv(sd, "trailingPE")
                out["peg"] = gv(dks, "pegRatio")
                out["fcf"] = gv(fd, "freeCashflow")
                out["roe"] = gv(fd, "returnOnEquity")
                out["roa"] = gv(fd, "returnOnAssets")
                out["earnGrowth"] = gv(fd, "earningsGrowth")
                out["revGrowth"] = gv(fd, "revenueGrowth")
                out["rec"] = gv(fd, "recommendationKey")
                out["target"] = gv(fd, "targetMeanPrice")
                for tr in (et.get("trend") or []):
                    p = tr.get("period")
                    if p in ("0y", "+1y"):
                        out[f"growth_{p}"] = gv(tr, "growth")
                results[t] = out
            print(t, results[t].get("ok"), results[t].get("forwardPE"), results[t].get("peg"), results[t].get("roe"), results[t].get("err"))
        except Exception as e:
            results[t] = {"t": t, "ok": False, "err": str(e)}
            print(t, "EXC", e)
        time.sleep(0.15)

# finviz screener batches as backup
def parse_finviz_screener(url):
    try:
        body, st = get(url, timeout=45)
    except Exception as e:
        print("finviz fail", e)
        return {}
    # rows often: <a href="quote.ashx?t=AAPL"...>AAPL</a> ... numbers in <td>
    # simpler: extract ticker blocks from table
    out = {}
    # Finviz valuation view columns: No. Ticker Market Cap P/E Forward P/E PEG ...
    rows = re.findall(r'quote\.ashx\?t=([A-Z0-9.\-]+)"[^>]*>([A-Z0-9.\-]+)</a></td><td[^>]*>([^<]*)</td><td[^>]*>([^<]*)</td><td[^>]*>([^<]*)</td><td[^>]*>([^<]*)</td>', body)
    print("finviz row matches", len(rows), "status", st, "len", len(body))
    for r in rows:
        t = r[0]
        out[t] = {"t": t, "mktcap": r[2], "pe": r[3], "fwd_pe": r[4], "peg": r[5]}
    if not rows:
        # dump snippet
        print("snippet", body[body.find("Ticker"):body.find("Ticker")+500] if "Ticker" in body else body[:400])
    return out

fv = {}
batches = [
    "MSFT,AMZN,GOOGL,META,AAPL,CRM,DELL,PLTR,ORCL,INFY,TSLA,NFLX,MELI,HD,LOW,WMT,TGT",
    "ASML,AVGO,NVDA,AMD,MU,TSM,INTC,BE,GLW,IREN,CORZ,RIOT,CLSK,BTDR,HIVE,RKLB,NFLX,ORCL",
    "SNDK,NBIS,CRWV,APLD,PSIX,BW,PUMP,TE,BITF,SPCX,SEI,WYFI,CRCL,GLD,SMH",
]
for b in batches:
    url = f"https://finviz.com/screener.ashx?v=121&t={b}"
    part = parse_finviz_screener(url)
    fv.update(part)
    time.sleep(1.0)

# merge: yahoo primary, finviz fill
merged = []
for t in tickers:
    y = results.get(t) or {"t": t, "ok": False}
    f = fv.get(t) or fv.get(t.replace("GOOG","GOOGL")) or {}
    row = dict(y)
    if not row.get("forwardPE") and f.get("fwd_pe") not in (None, "", "-"):
        try:
            row["forwardPE"] = float(f["fwd_pe"])
            row["fwd_src"] = "finviz"
        except Exception:
            row["forwardPE_raw"] = f.get("fwd_pe")
    if not row.get("peg") and f.get("peg") not in (None, "", "-"):
        try:
            row["peg"] = float(f["peg"])
            row["peg_src"] = "finviz"
        except Exception:
            pass
    if not row.get("trailingPE") and f.get("pe") not in (None, "", "-"):
        try:
            row["trailingPE"] = float(f["pe"])
        except Exception:
            pass
    merged.append(row)

with open("/home/hermes/.hermes/projects/watchlist_stats.json", "w") as f:
    json.dump({"yahoo": results, "finviz": fv, "merged": merged}, f, indent=2)
print("DONE merged", len(merged), "finviz", len(fv))
for r in merged:
    print(json.dumps({k: r.get(k) for k in ("t","ok","forwardPE","peg","roe","fcf","growth_+1y","rec","fwd_src","err")}))
