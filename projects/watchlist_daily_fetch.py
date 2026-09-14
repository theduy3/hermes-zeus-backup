#!/usr/bin/env python3
import json, urllib.request, urllib.parse, ssl, time, concurrent.futures, datetime, sys

ctx = ssl.create_default_context()
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

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

def fetch_chart(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.loads(r.read().decode())
        result = data["chart"]["result"][0]
        meta = result["meta"]
        quotes = result["indicators"]["quote"][0]
        closes = [c for c in quotes["close"] if c is not None]
        price = meta.get("regularMarketPrice") or (closes[-1] if closes else None)
        prev_close = meta.get("regularMarketPreviousClose") or meta.get("chartPreviousClose") or meta.get("previousClose")
        if prev_close is None and len(closes) >= 2:
            prev_close = closes[-2]
        if price is not None and prev_close:
            chg_pct = (price - prev_close) / prev_close * 100
        else:
            chg_pct = None
        return {
            "t": t, "price": price, "prev": prev_close, "chg": chg_pct,
            "ccy": meta.get("currency"), "ex": meta.get("exchangeName"),
            "ts": meta.get("regularMarketTime"), "ok": True
        }
    except Exception as e:
        return {"t": t, "ok": False, "err": str(e)[:200]}

def fetch_quote_summary(t):
    mods = "defaultKeyStatistics,summaryDetail,financialData"
    url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(t)}?modules={mods}"
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = json.loads(r.read().decode())
        res = data["quoteSummary"]["result"][0]
        dks = res.get("defaultKeyStatistics") or {}
        sd = res.get("summaryDetail") or {}
        fd = res.get("financialData") or {}
        def gv(d, k):
            v = d.get(k)
            if isinstance(v, dict):
                return v.get("raw", v.get("fmt"))
            return v
        return {
            "t": t,
            "fwdPE": gv(dks, "forwardPE") or gv(sd, "forwardPE"),
            "trailPE": gv(dks, "trailingPE") or gv(sd, "trailingPE"),
            "peg": gv(dks, "pegRatio"),
            "fcf": gv(fd, "freeCashflow"),
            "roe": gv(fd, "returnOnEquity"),
            "ok": True
        }
    except Exception as e:
        return {"t": t, "ok": False, "err": str(e)[:200]}

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    subset = tickers
    if mode != "all":
        # mode is comma-separated tickers
        subset = mode.split(",")

    charts = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        for r in ex.map(fetch_chart, subset):
            charts[r["t"]] = r

    time.sleep(0.3)
    quotes = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for r in ex.map(fetch_quote_summary, subset):
            quotes[r["t"]] = r

    out = []
    for t in subset:
        c = charts.get(t, {})
        q = quotes.get(t, {})
        row = {"ticker": t}
        if c.get("ok"):
            row.update({k: c.get(k) for k in ("price","prev","chg","ccy","ex","ts")})
            row["chart_ok"] = True
        else:
            row["chart_ok"] = False
            row["chart_err"] = c.get("err")
        if q.get("ok"):
            row.update({k: q.get(k) for k in ("fwdPE","trailPE","peg","fcf","roe")})
            row["quote_ok"] = True
        else:
            row["quote_ok"] = False
            row["quote_err"] = q.get("err")
        out.append(row)

    print(json.dumps(out, indent=None, default=str))
    okc = sum(1 for r in out if r.get("chart_ok"))
    okq = sum(1 for r in out if r.get("quote_ok"))
    print(f"\n# charts_ok={okc}/{len(subset)} quotes_ok={okq}/{len(subset)}", file=sys.stderr)
    for r in out:
        if r.get("ts"):
            print(f"# sample_ts {r['ticker']} {datetime.datetime.utcfromtimestamp(r['ts']).isoformat()}Z", file=sys.stderr)
            break

if __name__ == "__main__":
    main()
