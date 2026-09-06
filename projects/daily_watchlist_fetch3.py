#!/usr/bin/env python3
"""Sequential Yahoo chart + statistics page scrape with backoff."""
import json, time, subprocess, random, os, re

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

OUT = "/home/hermes/.hermes/projects/daily_watchlist_data.json"
COOKIE = "/tmp/yf_cookies2.txt"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
HOSTS = [
    "https://query1.finance.yahoo.com",
    "https://query2.finance.yahoo.com",
]

def curl(url, out_file, extra=None):
    cmd = [
        "curl", "-sS", "-L", "--max-time", "20",
        "-A", UA,
        "-b", COOKIE, "-c", COOKIE,
        "-H", "Accept: */*",
        "-o", out_file,
        "-w", "%{http_code}",
        url,
    ]
    if extra:
        cmd = cmd[:-1] + extra + [url]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return p.stdout.strip(), p.returncode
    except Exception as e:
        return f"err:{e}", 1

# seed
subprocess.run(["curl","-sS","-L","--max-time","15","-A",UA,"-c",COOKIE,"-o","/dev/null","https://finance.yahoo.com/"], timeout=25)

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return None

def fetch_chart(t):
    last_err = None
    for host in HOSTS:
        for attempt in range(3):
            url = f"{host}/v8/finance/chart/{t}?range=5d&interval=1d"
            path = f"/tmp/yf_chart_{t.replace('.','_')}.json"
            code, rc = curl(url, path)
            if code == "200":
                data = load_json(path)
                if data and data.get("chart", {}).get("result"):
                    try:
                        result = data["chart"]["result"][0]
                        meta = result.get("meta", {})
                        quotes = result.get("indicators", {}).get("quote", [{}])[0]
                        closes = [c for c in (quotes.get("close") or []) if c is not None]
                        price = meta.get("regularMarketPrice")
                        prev = meta.get("chartPreviousClose") or meta.get("previousClose")
                        chg = meta.get("regularMarketChangePercent")
                        if price is None and closes:
                            price = closes[-1]
                        if prev is None and len(closes) >= 2:
                            prev = closes[-2]
                        if chg is None and price is not None and prev:
                            chg = (price - prev) / prev * 100.0
                        return {
                            "price": price, "prev": prev, "chg": chg,
                            "currency": meta.get("currency"),
                            "asof": meta.get("regularMarketTime"),
                            "tz": meta.get("timezone"),
                            "err": None,
                        }
                    except Exception as e:
                        last_err = str(e)
            elif code == "429":
                time.sleep(3 + attempt * 2 + random.random())
                last_err = "429"
            else:
                last_err = f"http_{code}"
                time.sleep(1 + attempt)
    return {"price": None, "chg": None, "err": last_err}

def fetch_qs(t):
    last_err = None
    modules = "summaryDetail,defaultKeyStatistics,financialData"
    for host in HOSTS:
        for attempt in range(2):
            url = f"{host}/v10/finance/quoteSummary/{t}?modules={modules}"
            path = f"/tmp/yf_qs_{t.replace('.','_')}.json"
            code, rc = curl(url, path)
            if code == "200":
                data = load_json(path)
                if data and data.get("quoteSummary", {}).get("result"):
                    try:
                        res = data["quoteSummary"]["result"][0]
                        sd = res.get("summaryDetail") or {}
                        ks = res.get("defaultKeyStatistics") or {}
                        fd = res.get("financialData") or {}
                        def gv(d, k):
                            v = d.get(k)
                            if isinstance(v, dict):
                                return v.get("raw", v.get("fmt"))
                            return v
                        return {
                            "trailingPE": gv(sd, "trailingPE") or gv(ks, "trailingPE"),
                            "forwardPE": gv(sd, "forwardPE") or gv(ks, "forwardPE"),
                            "peg": gv(ks, "pegRatio"),
                            "targetMean": gv(fd, "targetMeanPrice"),
                            "recKey": gv(fd, "recommendationKey"),
                            "roe": gv(fd, "returnOnEquity"),
                            "roa": gv(fd, "returnOnAssets"),
                            "fcf": gv(fd, "freeCashflow"),
                            "opcf": gv(fd, "operatingCashflow"),
                            "revGrowth": gv(fd, "revenueGrowth"),
                            "earningsGrowth": gv(fd, "earningsGrowth"),
                            "err": None,
                        }
                    except Exception as e:
                        last_err = str(e)
            elif code == "429":
                time.sleep(3 + attempt * 2)
                last_err = "429"
            else:
                last_err = f"http_{code}"
                time.sleep(0.8)
    return {"err": last_err}

def fmt(x, n=2):
    if x is None:
        return None
    try:
        return round(float(x), n)
    except Exception:
        return None

# Resume support
rows_by_t = {}
if os.path.exists(OUT):
    try:
        for r in json.load(open(OUT)):
            rows_by_t[r["ticker"]] = r
    except Exception:
        pass

rows = []
for i, t in enumerate(tickers):
    existing = rows_by_t.get(t)
    if existing and existing.get("price") is not None and existing.get("chart_err") is None:
        # still refresh qs if missing
        if existing.get("fwdPE") is not None or existing.get("qs_err") is None and "fwdPE" in existing:
            if existing.get("price") is not None:
                rows.append(existing)
                print(f"# skip {t}", flush=True)
                continue

    c = fetch_chart(t)
    time.sleep(1.2 + random.random() * 0.8)
    s = fetch_qs(t)
    time.sleep(1.2 + random.random() * 0.8)
    row = {
        "ticker": t,
        "price": fmt(c.get("price"), 2),
        "chg": fmt(c.get("chg"), 2),
        "fwdPE": fmt(s.get("forwardPE"), 2),
        "trailPE": fmt(s.get("trailingPE"), 2),
        "peg": fmt(s.get("peg"), 2),
        "fcf": s.get("fcf"),
        "opcf": s.get("opcf"),
        "roe": fmt(s.get("roe"), 4) if s.get("roe") is not None else None,
        "roa": fmt(s.get("roa"), 4) if s.get("roa") is not None else None,
        "earnGr": fmt(s.get("earningsGrowth"), 4) if s.get("earningsGrowth") is not None else None,
        "revGr": fmt(s.get("revGrowth"), 4) if s.get("revGrowth") is not None else None,
        "rec": s.get("recKey"),
        "target": fmt(s.get("targetMean"), 2),
        "currency": c.get("currency"),
        "asof": c.get("asof"),
        "tz": c.get("tz"),
        "chart_err": c.get("err"),
        "qs_err": s.get("err"),
    }
    rows.append(row)
    # checkpoint
    with open(OUT, "w") as f:
        # merge with remaining existing for full list later
        done = {r["ticker"]: r for r in rows}
        for tt in tickers:
            if tt not in done and tt in rows_by_t:
                done[tt] = rows_by_t[tt]
        json.dump([done.get(tt, {"ticker": tt}) for tt in tickers], f, indent=2)
    print(f"# {i+1}/{len(tickers)} {t} p={row['price']} chg={row['chg']} fwd={row['fwdPE']} peg={row['peg']} c={row['chart_err']} s={row['qs_err']}", flush=True)

# final write ordered
final = []
done = {r["ticker"]: r for r in rows}
for t in tickers:
    final.append(done.get(t) or rows_by_t.get(t) or {"ticker": t})
with open(OUT, "w") as f:
    json.dump(final, f, indent=2)
ok = sum(1 for r in final if r.get("price") is not None)
print(f"# DONE prices_ok={ok}/{len(final)}", flush=True)
