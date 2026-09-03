#!/usr/bin/env python3
import json, urllib.request, urllib.parse, ssl, time, concurrent.futures
from datetime import datetime, timezone

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

ctx = ssl.create_default_context()
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def fetch_json(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, context=ctx, timeout=timeout) as r:
        return json.loads(r.read().decode())

def chart(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(ticker)}?range=5d&interval=1d"
    try:
        data = fetch_json(url)
        res = data["chart"]["result"][0]
        meta = res["meta"]
        quote = (res.get("indicators") or {}).get("quote", [{}])[0]
        closes = [c for c in (quote.get("close") or []) if c is not None]
        price = meta.get("regularMarketPrice") or meta.get("postMarketPrice") or (closes[-1] if closes else None)
        prev = meta.get("chartPreviousClose") or meta.get("previousClose")
        if prev is None and len(closes) >= 2:
            prev = closes[-2]
        chg = None
        if price is not None and prev not in (None, 0):
            chg = (price - prev) / prev * 100.0
        rt = meta.get("regularMarketTime")
        asof = datetime.fromtimestamp(rt, tz=timezone.utc).isoformat() if rt else None
        return {
            "ticker": ticker,
            "price": price,
            "prev": prev,
            "chg_pct": chg,
            "currency": meta.get("currency"),
            "asof": asof,
            "exchange": meta.get("exchangeName"),
            "ok": True,
            "err": None,
        }
    except Exception as e:
        return {"ticker": ticker, "ok": False, "err": str(e)}

def modules(ticker):
    mods = "defaultKeyStatistics,financialData,summaryDetail,price,earningsTrend"
    url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(ticker)}?modules={mods}"
    try:
        data = fetch_json(url)
        res = data["quoteSummary"]["result"][0]
        dks = res.get("defaultKeyStatistics") or {}
        fd = res.get("financialData") or {}
        sd = res.get("summaryDetail") or {}
        def raw(x):
            if x is None:
                return None
            if isinstance(x, dict):
                return x.get("raw")
            return x
        fpe = raw(dks.get("forwardPE")) or raw(sd.get("forwardPE"))
        tpe = raw(dks.get("trailingPE")) or raw(sd.get("trailingPE"))
        peg = raw(dks.get("pegRatio"))
        eg = None
        et = res.get("earningsTrend") or {}
        for t in et.get("trend") or []:
            if t.get("period") == "0y":
                eg = raw(t.get("growth"))
                break
        if eg is None:
            for t in et.get("trend") or []:
                if t.get("period") == "+1y":
                    eg = raw(t.get("growth"))
                    break
        fcf = raw(fd.get("freeCashflow"))
        ocf = raw(fd.get("operatingCashflow"))
        roe = raw(fd.get("returnOnEquity"))
        roa = raw(fd.get("returnOnAssets"))
        rec = fd.get("recommendationKey")
        target = raw(fd.get("targetMeanPrice"))
        return {
            "ticker": ticker,
            "forwardPE": fpe,
            "trailingPE": tpe,
            "pegRatio": peg,
            "earningsGrowth": eg,
            "fcf": fcf,
            "ocf": ocf,
            "roe": roe,
            "roa": roa,
            "rec": rec,
            "target": target,
            "ok": True,
            "err": None,
        }
    except Exception as e:
        return {"ticker": ticker, "ok": False, "err": str(e)}

def both(t):
    c = chart(t)
    time.sleep(0.08)
    m = modules(t)
    return c, m

charts = {}
mods = {}
errors = []
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(both, t): t for t in tickers}
    for fut in concurrent.futures.as_completed(futs):
        t = futs[fut]
        try:
            c, m = fut.result()
            charts[t] = c
            mods[t] = m
            if not c.get("ok"):
                errors.append(("chart", t, c.get("err")))
            if not m.get("ok"):
                errors.append(("mod", t, m.get("err")))
        except Exception as e:
            errors.append(("both", t, str(e)))

out = {"asof_run": datetime.now(timezone.utc).isoformat(), "charts": charts, "mods": mods, "errors": errors}
with open("/home/hermes/.hermes/projects/watchlist_data.json", "w") as f:
    json.dump(out, f)
print("OK", len(charts), "charts", len([m for m in mods.values() if m.get("ok")]), "mods_ok", "errors", len(errors))
for e in errors[:30]:
    print("ERR", e)
