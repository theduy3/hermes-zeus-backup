#!/usr/bin/env python3
import json, urllib.request, urllib.parse, ssl, concurrent.futures
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
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def fetch_chart(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.loads(r.read().decode())
        result = data["chart"]["result"][0]
        meta = result["meta"]
        ts = result.get("timestamp") or []
        quotes = result["indicators"]["quote"][0]
        closes = quotes.get("close") or []
        valid = [(ts[i], closes[i]) for i in range(len(closes)) if closes[i] is not None]
        if not valid:
            # fall back to meta regularMarketPrice
            p = meta.get("regularMarketPrice")
            prev = meta.get("previousClose") or meta.get("chartPreviousClose")
            chg = meta.get("regularMarketChangePercent")
            return t, {
                "price": round(p, 2) if p else None,
                "prev": round(prev, 2) if prev else None,
                "chg_pct": round(chg, 2) if chg is not None else None,
                "currency": meta.get("currency"),
                "as_of": datetime.fromtimestamp(meta.get("regularMarketTime"), tz=timezone.utc).isoformat() if meta.get("regularMarketTime") else None,
                "source": "meta",
            }
        last_ts, last = valid[-1]
        prev = valid[-2][1] if len(valid) >= 2 else meta.get("previousClose") or meta.get("chartPreviousClose")
        # Prefer live regularMarketPrice if available and more recent
        rmp = meta.get("regularMarketPrice")
        rmc = meta.get("regularMarketChangePercent")
        if rmp is not None:
            price = rmp
            chg = rmc if rmc is not None else (((price - prev) / prev * 100) if prev else None)
            as_of = datetime.fromtimestamp(meta["regularMarketTime"], tz=timezone.utc).isoformat() if meta.get("regularMarketTime") else datetime.fromtimestamp(last_ts, tz=timezone.utc).isoformat()
        else:
            price = last
            chg = ((last - prev) / prev * 100) if prev else None
            as_of = datetime.fromtimestamp(last_ts, tz=timezone.utc).isoformat()
        return t, {
            "price": round(float(price), 2) if price is not None else None,
            "prev": round(float(prev), 2) if prev else None,
            "chg_pct": round(float(chg), 2) if chg is not None else None,
            "currency": meta.get("currency"),
            "as_of": as_of,
            "instrument": meta.get("instrumentType"),
            "exchange": meta.get("exchangeName"),
        }
    except Exception as e:
        return t, {"error": str(e)}

def fetch_modules(t):
    modules = "defaultKeyStatistics,financialData,summaryDetail,earningsTrend"
    url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(t)}?modules={modules}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.loads(r.read().decode())
        res = data["quoteSummary"]["result"][0]
        dks = res.get("defaultKeyStatistics") or {}
        fd = res.get("financialData") or {}
        sd = res.get("summaryDetail") or {}
        def gv(obj, key):
            v = obj.get(key)
            if isinstance(v, dict):
                return v.get("raw", v.get("fmt"))
            return v
        fwd_pe = gv(dks, "forwardPE") or gv(sd, "forwardPE")
        peg = gv(dks, "pegRatio")
        trailing_pe = gv(dks, "trailingPE") or gv(sd, "trailingPE")
        fcf = gv(fd, "freeCashflow")
        roe = gv(fd, "returnOnEquity")
        roa = gv(fd, "returnOnAssets")
        rec = gv(fd, "recommendationKey")
        target = gv(fd, "targetMeanPrice")
        op_cf = gv(fd, "operatingCashflow")
        growth = None
        et = res.get("earningsTrend") or {}
        for tr in (et.get("trend") or []):
            if tr.get("period") == "+1y":
                g = tr.get("growth")
                if isinstance(g, dict) and g.get("raw") is not None:
                    growth = g["raw"]
                    break
        if growth is None:
            for tr in (et.get("trend") or []):
                if tr.get("period") == "0y":
                    g = tr.get("growth")
                    if isinstance(g, dict) and g.get("raw") is not None:
                        growth = g["raw"]
                        break
        # compute PEG if missing: fwd_pe / (growth*100)
        peg_calc = None
        if peg is None and fwd_pe is not None and growth is not None and growth > 0:
            peg_calc = float(fwd_pe) / (float(growth) * 100.0)
        return t, {
            "forwardPE": fwd_pe,
            "trailingPE": trailing_pe,
            "pegRatio": peg,
            "pegCalc": peg_calc,
            "freeCashflow": fcf,
            "operatingCashflow": op_cf,
            "returnOnEquity": roe,
            "returnOnAssets": roa,
            "recommendation": rec,
            "targetMeanPrice": target,
            "earningsGrowth": growth,
        }
    except Exception as e:
        return t, {"error": str(e)}

results = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
    futs = [ex.submit(fetch_chart, t) for t in tickers]
    for fut in concurrent.futures.as_completed(futs):
        t, d = fut.result()
        results[t] = {"chart": d}

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
    futs = [ex.submit(fetch_modules, t) for t in tickers]
    for fut in concurrent.futures.as_completed(futs):
        t, d = fut.result()
        results.setdefault(t, {})["fund"] = d

out_path = "/home/hermes/.hermes/projects/watchlist_data.json"
with open(out_path, "w") as f:
    json.dump({
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "results": results,
    }, f, indent=2, default=str)

# compact summary
for t in tickers:
    c = results[t].get("chart", {})
    f = results[t].get("fund", {})
    price = c.get("price")
    chg = c.get("chg_pct")
    fpe = f.get("forwardPE")
    peg = f.get("pegRatio") if f.get("pegRatio") is not None else f.get("pegCalc")
    fcf = f.get("freeCashflow")
    roe = f.get("returnOnEquity")
    g = f.get("earningsGrowth")
    err = c.get("error") or f.get("error")
    print(f"{t}|p={price}|chg={chg}|fpe={fpe}|peg={peg}|fcf={fcf}|roe={roe}|g={g}|err={err}")

print("WROTE", out_path)
chart_errs = [t for t in tickers if results[t].get("chart", {}).get("error")]
fund_errs = [t for t in tickers if results[t].get("fund", {}).get("error")]
print("chart_errors", chart_errs)
print("fund_error_count", len(fund_errs))
