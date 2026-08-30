#!/usr/bin/env python3
import json, urllib.request, urllib.parse, ssl, time, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
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

def get_json(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, context=ctx, timeout=timeout) as r:
        return json.loads(r.read().decode())

def fetch_chart(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=5d&interval=1d"
    try:
        data = get_json(url)
        result = data["chart"]["result"][0]
        meta = result.get("meta", {})
        ts = result.get("timestamp") or []
        quote = (result.get("indicators") or {}).get("quote", [{}])[0]
        closes = quote.get("close") or []
        pairs = [(ts[i], closes[i]) for i in range(min(len(ts), len(closes))) if closes[i] is not None]
        if len(pairs) >= 2:
            last_ts, last = pairs[-1]
            prev = pairs[-2][1]
            chg = (last - prev) / prev * 100 if prev else None
        elif len(pairs) == 1:
            last_ts, last = pairs[-1]
            prev = meta.get("chartPreviousClose") or meta.get("previousClose")
            chg = (last - prev) / prev * 100 if prev else None
        else:
            last = meta.get("regularMarketPrice")
            prev = meta.get("chartPreviousClose") or meta.get("previousClose")
            last_ts = meta.get("regularMarketTime")
            chg = (last - prev) / prev * 100 if (last is not None and prev) else None
        # prefer meta regular market for latest if available
        rmp = meta.get("regularMarketPrice")
        rmc = meta.get("regularMarketChangePercent")
        if rmp is not None:
            last = rmp
        if rmc is not None:
            chg = rmc
        return {
            "ticker": t,
            "price": last,
            "chg_pct": chg,
            "last_ts": last_ts or meta.get("regularMarketTime"),
            "currency": meta.get("currency"),
            "name": meta.get("shortName") or meta.get("longName"),
            "ok": True,
            "error": None,
        }
    except Exception as e:
        return {"ticker": t, "ok": False, "error": str(e), "price": None, "chg_pct": None}

def fetch_modules(t):
    """defaultKeyStatistics + financialData + earningsTrend for fwd PE, PEG, FCF, ROIC proxies."""
    modules = "defaultKeyStatistics,financialData,earningsTrend,incomeStatementHistory"
    url = (
        f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(t)}"
        f"?modules={modules}"
    )
    out = {"ticker": t, "fwd_pe": None, "trailing_pe": None, "peg": None,
           "fcf": None, "fcf_prev": None, "roic": None, "profit_margins": None,
           "recommendation": None, "target": None, "ok": False, "error": None}
    try:
        data = get_json(url)
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

        out["fwd_pe"] = raw(ks.get("forwardPE"))
        out["trailing_pe"] = raw(ks.get("trailingPE"))
        out["peg"] = raw(ks.get("pegRatio"))
        out["fcf"] = raw(fd.get("freeCashflow"))
        out["profit_margins"] = raw(fd.get("profitMargins"))
        out["recommendation"] = raw(fd.get("recommendationKey"))
        out["target"] = raw(fd.get("targetMeanPrice"))
        # ROIC not always direct; try returnOnAssets / returnOnEquity as weak proxies later
        out["roa"] = raw(fd.get("returnOnAssets"))
        out["roe"] = raw(fd.get("returnOnEquity"))
        # earnings growth from trend
        trends = et.get("trend") or []
        growth = None
        for tr in trends:
            if tr.get("period") == "0y":
                growth = raw((tr.get("earningsEstimate") or {}).get("growth"))
                if growth is None:
                    growth = raw(tr.get("growth"))
        out["earn_growth"] = growth
        # PEG from fwd PE / (growth*100) if missing
        if out["peg"] is None and out["fwd_pe"] and growth and growth > 0:
            # growth often as decimal 0.15 = 15%
            g_pct = growth * 100 if growth < 1 else growth
            if g_pct > 0:
                out["peg_est"] = out["fwd_pe"] / g_pct
        out["ok"] = True
    except Exception as e:
        out["error"] = str(e)
        # fallback: v7 quote
        try:
            qurl = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={urllib.parse.quote(t)}"
            q = get_json(qurl)
            r = q["quoteResponse"]["result"][0]
            out["fwd_pe"] = r.get("forwardPE")
            out["trailing_pe"] = r.get("trailingPE")
            out["ok"] = True
            out["error"] = f"modules_fail:{e}; used v7"
        except Exception as e2:
            out["error"] = f"{e} | v7:{e2}"
    return out

results = {}
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(fetch_chart, t): ("chart", t) for t in tickers}
    for f in as_completed(futs):
        d = f.result()
        results[d["ticker"]] = d
        time.sleep(0.05)

fund = {}
with ThreadPoolExecutor(max_workers=4) as ex:
    futs = {ex.submit(fetch_modules, t): t for t in tickers}
    for f in as_completed(futs):
        d = f.result()
        fund[d["ticker"]] = d
        time.sleep(0.08)

# merge
merged = []
for t in tickers:
    m = dict(results.get(t) or {})
    f = fund.get(t) or {}
    m["fwd_pe"] = f.get("fwd_pe")
    m["trailing_pe"] = f.get("trailing_pe")
    m["peg"] = f.get("peg") or f.get("peg_est")
    m["peg_est"] = f.get("peg_est")
    m["fcf"] = f.get("fcf")
    m["roa"] = f.get("roa")
    m["roe"] = f.get("roe")
    m["earn_growth"] = f.get("earn_growth")
    m["recommendation"] = f.get("recommendation")
    m["target"] = f.get("target")
    m["fund_error"] = f.get("error")
    m["fund_ok"] = f.get("ok")
    merged.append(m)

out_path = "/home/hermes/.hermes/projects/watchlist_daily_data.json"
with open(out_path, "w") as fh:
    json.dump({"asof_utc": datetime.now(timezone.utc).isoformat(), "rows": merged}, fh, indent=2)

# human table
for m in merged:
    p = m.get("price")
    c = m.get("chg_pct")
    pe = m.get("fwd_pe")
    peg = m.get("peg")
    fcf = m.get("fcf")
    roa = m.get("roa")
    ps = f"{p:.2f}" if isinstance(p, (int, float)) else "—"
    cs = f"{c:+.2f}" if isinstance(c, (int, float)) else "—"
    pes = f"{pe:.1f}" if isinstance(pe, (int, float)) else "—"
    pegs = f"{peg:.2f}" if isinstance(peg, (int, float)) else "—"
    fcfs = f"{fcf/1e9:.2f}B" if isinstance(fcf, (int, float)) else "—"
    roas = f"{roa*100:.1f}%" if isinstance(roa, (int, float)) else "—"
    print(f"{m['ticker']}\t{ps}\t{cs}\t{pes}\tPEG:{pegs}\tFCF:{fcfs}\tROA:{roas}\tok={m.get('ok')}\tfund={m.get('fund_ok')}\terr={m.get('error') or m.get('fund_error')}")

print("WROTE", out_path)
