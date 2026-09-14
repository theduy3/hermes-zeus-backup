#!/usr/bin/env python3
"""Fetch forward PE from Yahoo Finance quote/statistics HTML or crumb-auth API."""
import json, re, ssl, time, urllib.request, urllib.parse, concurrent.futures, http.cookiejar

ctx = ssl.create_default_context()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

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

def session_with_crumb():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj),
        urllib.request.HTTPSHandler(context=ctx),
    )
    opener.addheaders = [("User-Agent", UA), ("Accept", "text/html,application/json")]
    # seed cookies
    try:
        opener.open("https://finance.yahoo.com/", timeout=20)
    except Exception as e:
        print("seed_err", e, flush=True)
    crumb = None
    try:
        r = opener.open("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=15)
        crumb = r.read().decode()
    except Exception as e:
        print("crumb_err", e, flush=True)
        # try alternate
        try:
            r = opener.open("https://query2.finance.yahoo.com/v1/test/getcrumb", timeout=15)
            crumb = r.read().decode()
        except Exception as e2:
            print("crumb_err2", e2, flush=True)
    return opener, crumb

def fetch_html_fwdpe(opener, t):
    # key-statistics page often has Forward P/E
    urls = [
        f"https://finance.yahoo.com/quote/{urllib.parse.quote(t)}/key-statistics",
        f"https://finance.yahoo.com/quote/{urllib.parse.quote(t)}",
    ]
    out = {"t": t}
    for url in urls:
        try:
            r = opener.open(url, timeout=25)
            html = r.read().decode("utf-8", "ignore")
            # try JSON embedded
            m = re.search(r'root\.App\.main\s*=\s*(\{.*?\});\n', html, re.S)
            if not m:
                m = re.search(r'"forwardPE"\s*:\s*\{[^}]*"raw"\s*:\s*([0-9eE+.\-]+)', html)
                if m:
                    out["fwdPE"] = float(m.group(1))
                    out["src"] = "html-regex"
                    return out
                # table label Forward P/E
                m2 = re.search(r'Forward P/E</span></td><td[^>]*>([0-9.,N/A\-]+)', html)
                if m2:
                    val = m2.group(1).replace(",", "")
                    if val not in ("N/A", "--", "-"):
                        try:
                            out["fwdPE"] = float(val)
                            out["src"] = "html-table"
                            return out
                        except: pass
                # peg
                continue
            data = json.loads(m.group(1))
            # walk for forwardPE
            def find_key(obj, key, depth=0):
                if depth > 12: return None
                if isinstance(obj, dict):
                    if key in obj:
                        return obj[key]
                    for v in obj.values():
                        found = find_key(v, key, depth+1)
                        if found is not None: return found
                elif isinstance(obj, list):
                    for v in obj[:50]:
                        found = find_key(v, key, depth+1)
                        if found is not None: return found
                return None
            fp = find_key(data, "forwardPE")
            peg = find_key(data, "pegRatio")
            if isinstance(fp, dict):
                fp = fp.get("raw", fp.get("fmt"))
            if isinstance(peg, dict):
                peg = peg.get("raw", peg.get("fmt"))
            if fp is not None:
                out["fwdPE"] = fp
                out["peg"] = peg
                out["src"] = "html-json"
                return out
        except Exception as e:
            out["err"] = str(e)[:120]
    return out

def fetch_api(opener, crumb, t):
    if not crumb:
        return None
    mods = "defaultKeyStatistics,summaryDetail,financialData"
    for base in ("query1", "query2"):
        url = f"https://{base}.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(t)}?modules={mods}&crumb={urllib.parse.quote(crumb)}"
        try:
            r = opener.open(url, timeout=20)
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
                "src": "api-crumb",
            }
        except Exception as e:
            last = str(e)[:100]
    return {"t": t, "err": last}

def main():
    opener, crumb = session_with_crumb()
    print("CRUMB", crumb, flush=True)
    results = {}
    # try API first for a few
    sample = ["MSFT", "NVDA", "BITF", "VFV.TO"]
    for t in sample:
        r = fetch_api(opener, crumb, t)
        print("API", r, flush=True)
        if r and r.get("fwdPE") is not None:
            results[t] = r

    # batch remaining via API if crumb works
    rest = [t for t in tickers if t not in results]
    if crumb:
        def one(t):
            return fetch_api(opener, crumb, t)
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
            for r in ex.map(one, rest):
                if r and r.get("fwdPE") is not None:
                    results[r["t"]] = r
                elif r:
                    # keep even without fwdPE if has other
                    if any(r.get(k) is not None for k in ("peg","fcf","trailPE")):
                        results[r["t"]] = r
                    else:
                        results.setdefault(r["t"], r)

    # HTML fallback for missing
    missing = [t for t in tickers if t not in results or results[t].get("fwdPE") is None]
    print("MISSING_AFTER_API", len(missing), flush=True)
    for t in missing:
        r = fetch_html_fwdpe(opener, t)
        print("HTML", t, r, flush=True)
        if r.get("fwdPE") is not None:
            results[t] = r
        time.sleep(0.15)

    # also try BITF variants via chart
    for alt in ["BITF", "BITF.TO", "BFTOF"]:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{alt}?range=5d&interval=1d"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
                d = json.loads(resp.read().decode())
                meta = d["chart"]["result"][0]["meta"]
                print("BITF_ALT", alt, meta.get("regularMarketPrice"), meta.get("symbol"), flush=True)
        except Exception as e:
            print("BITF_ALT_FAIL", alt, e, flush=True)

    print("===JSON===")
    print(json.dumps(results, default=str))

if __name__ == "__main__":
    main()
