#!/usr/bin/env python3
import json, time, subprocess, re, os, random

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

COOKIE_JAR = "/tmp/yf_cookies.txt"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

def curl_json(url, retries=4):
    for attempt in range(retries):
        cmd = [
            "curl", "-sS", "-L", "--max-time", "25",
            "-A", UA,
            "-b", COOKIE_JAR, "-c", COOKIE_JAR,
            "-H", "Accept: application/json,text/plain,*/*",
            "-H", "Accept-Language: en-US,en;q=0.9",
            url
        ]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            body = p.stdout
            if p.returncode != 0:
                time.sleep(1.5 + attempt)
                continue
            if "Too Many Requests" in body or body.strip() == "":
                time.sleep(2.5 + attempt * 2 + random.random())
                continue
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                time.sleep(1.5 + attempt)
                continue
        except Exception:
            time.sleep(1.5 + attempt)
    return None

# seed cookies
subprocess.run([
    "curl", "-sS", "-L", "--max-time", "20",
    "-A", UA, "-c", COOKIE_JAR, "-b", COOKIE_JAR,
    "-o", "/dev/null",
    "https://finance.yahoo.com/"
], timeout=30)

# try get crumb
crumb = None
try:
    p = subprocess.run([
        "curl", "-sS", "-L", "--max-time", "20",
        "-A", UA, "-b", COOKIE_JAR, "-c", COOKIE_JAR,
        "https://query1.finance.yahoo.com/v1/test/getcrumb"
    ], capture_output=True, text=True, timeout=25)
    if p.stdout and "Too Many" not in p.stdout and "<" not in p.stdout:
        crumb = p.stdout.strip()
except Exception:
    pass

print(f"# crumb={crumb!r}", flush=True)

def fetch_chart(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=5d&interval=1d&includePrePost=false"
    if crumb:
        url += f"&crumb={crumb}"
    data = curl_json(url)
    if not data or "chart" not in data:
        return {"t": t, "err": "chart_fail"}
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
            "t": t,
            "price": price,
            "prev": prev,
            "chg": chg,
            "currency": meta.get("currency"),
            "asof": meta.get("regularMarketTime"),
            "tz": meta.get("timezone"),
            "err": None,
        }
    except Exception as e:
        return {"t": t, "err": str(e)}

def fetch_qs(t):
    modules = "summaryDetail,defaultKeyStatistics,financialData"
    url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{t}?modules={modules}"
    if crumb:
        url += f"&crumb={crumb}"
    data = curl_json(url)
    if not data or "quoteSummary" not in data:
        # try query1
        url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{t}?modules={modules}"
        if crumb:
            url += f"&crumb={crumb}"
        data = curl_json(url)
    if not data or "quoteSummary" not in data:
        return {"t": t, "err": "qs_fail"}
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
            "t": t,
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
        return {"t": t, "err": str(e)}

def fmt(x, n=2):
    if x is None:
        return None
    try:
        return round(float(x), n)
    except Exception:
        return None

rows = []
for i, t in enumerate(tickers):
    c = fetch_chart(t)
    time.sleep(0.55 + random.random() * 0.35)
    s = fetch_qs(t)
    time.sleep(0.55 + random.random() * 0.35)
    row = {
        "ticker": t,
        "price": fmt(c.get("price"), 2 if (c.get("price") or 0) >= 10 else 4),
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
    print(f"# {i+1}/{len(tickers)} {t} p={row['price']} chg={row['chg']} fwd={row['fwdPE']} peg={row['peg']} errc={row['chart_err']} errs={row['qs_err']}", flush=True)

out_path = "/home/hermes/.hermes/projects/daily_watchlist_data.json"
with open(out_path, "w") as f:
    json.dump(rows, f, indent=2)
print(f"# wrote {out_path}", flush=True)
ok = sum(1 for r in rows if r["price"] is not None)
print(f"# prices_ok={ok}/{len(rows)}", flush=True)
