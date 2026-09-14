#!/usr/bin/env python3
import json, urllib.request, ssl, re, time, random, html as htmlmod

ctx = ssl.create_default_context()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

batches = [
"MSFT,AMZN,GOOG,META,AAPL,CRM,DELL,PLTR,ORCL,CRWV",
"INFY,NBIS,TSLA,NFLX,MELI,HD,LOW,WMT,TGT,ASML",
"AVGO,NVDA,AMD,SNDK,MU,TSM,INTC,BE,APLD,TE",
"PSIX,GLW,BW,PUMP,IREN,CORZ,RIOT,CLSK,BTDR,HIVE",
"RKLB,SEI,WYFI,CRCL,GLD,SMH,SPCX,BITF,VFV.TO",
]

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, context=ctx, timeout=40) as r:
        return r.read().decode("utf-8", "ignore")

results = {}
for b in batches:
    url = f"https://finviz.com/screener.ashx?v=121&t={b}"
    try:
        page = fetch(url)
    except Exception as e:
        print("BATCH ERR", b, e)
        time.sleep(2)
        continue
    # rows often like <td ...><a href="quote.ashx?t=MSFT"...>MSFT</a></td>
    # Parse table rows after header
    # Simpler: find all ticker links and following numeric cells in valuation view
    # Finviz table structure: Ticker, Market Cap, P/E, Forward P/E, PEG, P/S, P/B, P/C, P/FCF, EPS This Y, EPS Next Y, ...
    rows = re.findall(r'<tr[^>]*class="[^"]*"[^>]*>(.*?)</tr>', page, re.I|re.S)
    if not rows:
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', page, re.I|re.S)
    print("batch", b[:30], "rows", len(rows), "len", len(page))
    for row in rows:
        m = re.search(r'quote\.ashx\?t=([A-Z0-9.\-]+)', row, re.I)
        if not m:
            continue
        t = m.group(1).upper()
        # get text cells
        cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.I|re.S)
        texts = []
        for c in cells:
            c2 = re.sub(r'<[^>]+>', '', c)
            c2 = htmlmod.unescape(c2).strip()
            texts.append(c2)
        # Expect: No., Ticker, Market Cap, P/E, Forward P/E, PEG, ...
        # Find ticker index
        if t not in texts:
            # sometimes ticker only in link
            pass
        # map by known column positions if len enough
        # From known: No Ticker MarketCap PE FwdPE PEG PS PB PC PFCF EPSthis EPSnext ...
        pe = fwd = peg = pf = None
        # try locate numbers after ticker appearance
        try:
            # texts often start with number
            # find index of ticker symbol exact
            idx = None
            for i, x in enumerate(texts):
                if x.upper() == t:
                    idx = i
                    break
            if idx is not None and len(texts) > idx + 5:
                # Market Cap idx+1, PE idx+2, FwdPE idx+3, PEG idx+4
                pe = texts[idx+2]
                fwd = texts[idx+3]
                peg = texts[idx+4]
                pf = texts[idx+8] if len(texts) > idx+8 else None
            else:
                # fallback: grab all hyphen/number-like after first
                nums = [x for x in texts if re.fullmatch(r'[-]?[0-9,.]+%?', x) or x == '-']
                # unstable
        except Exception:
            pass
        results[t] = {"pe": pe, "fwdPE": fwd, "peg": peg, "pfcf": pf, "cells": texts[:16], "src": "finviz"}
        print(t, "fwd", fwd, "peg", peg, "pe", pe, "cells", texts[:12])
    time.sleep(1.5 + random.random())

# Also try stockanalysis statistics pages for key names missing
def sa_stats(t):
    url = f"https://stockanalysis.com/stocks/{t.lower()}/statistics/"
    try:
        page = fetch(url)
    except Exception as e:
        return {"error": str(e)}
    out = {"src": "stockanalysis"}
    # Forward PE
    patterns = {
        "forwardPE": [r'Forward PE[:\s]*</td>\s*<td[^>]*>\s*([0-9.n/aN/A\-]+)', r'Forward PE[^0-9]*([0-9.]+)', r'forward PE ratio is ([0-9.]+)', r'Forward PE</td><td[^>]*>([0-9.n/aN/A\-]+)'],
        "pe": [r'PE Ratio</td>\s*<td[^>]*>\s*([0-9.n/aN/A\-]+)', r'trailing PE ratio is ([0-9.]+)'],
        "peg": [r'PEG Ratio</td>\s*<td[^>]*>\s*([0-9.n/aN/A\-]+)', r"PEG ratio is ([0-9.]+)"],
        "fcf": [r'Free Cash Flow</td>\s*<td[^>]*>\s*([^<]+)', r'Levered Free Cash Flow</td>\s*<td[^>]*>\s*([^<]+)'],
        "roe": [r'Return on Equity \(ttm\)</td>\s*<td[^>]*>\s*([^<]+)', r'Return on Equity</td>\s*<td[^>]*>\s*([^<]+)'],
        "roic": [r'Return on Capital \(ttm\)</td>\s*<td[^>]*>\s*([^<]+)', r'Return on Capital</td>\s*<td[^>]*>\s*([^<]+)', r'ROIC</td>\s*<td[^>]*>\s*([^<]+)'],
    }
    for k, pats in patterns.items():
        for p in pats:
            m = re.search(p, page, re.I|re.S)
            if m:
                out[k] = htmlmod.unescape(re.sub(r'\s+', ' ', m.group(1))).strip()
                break
    # table pairs
    pairs = re.findall(r'<td[^>]*>([^<]{3,60})</td>\s*<td[^>]*>([^<]{1,40})</td>', page)
    wanted = {
        "Forward PE": "forwardPE",
        "PE Ratio": "pe",
        "PEG Ratio": "peg",
        "Return on Equity (ttm)": "roe",
        "Return on Capital (ttm)": "roic",
        "Return on Assets (ttm)": "roa",
        "Free Cash Flow": "fcf",
        "Levered Free Cash Flow": "fcf_lev",
        "Profit Margin": "margin",
        "Operating Cash Flow": "ocf",
    }
    for a,b in pairs:
        a=a.strip(); b=b.strip()
        if a in wanted and wanted[a] not in out:
            out[wanted[a]] = b
    out["title"] = (re.search(r'<title>([^<]+)</title>', page, re.I) or [None,None])[1]
    return out

need_sa = ["MSFT","AMZN","GOOG","META","AAPL","CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS","TSLA","NFLX","MELI","HD","LOW","WMT","TGT","ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC","BE","APLD","GLW","IREN","CORZ","RIOT","CLSK","BTDR","HIVE","RKLB","SEI","CRCL","NFLX","ORCL"]
# unique preserve
seen=set(); need=[]
for t in need_sa:
    if t not in seen:
        seen.add(t); need.append(t)

sa = {}
for t in need:
    d = sa_stats(t)
    sa[t] = d
    print("SA", t, {k:d.get(k) for k in ["forwardPE","pe","peg","fcf","roe","roic","error","title"]})
    time.sleep(0.6 + random.random()*0.5)

out = {"finviz": results, "stockanalysis": sa}
with open("/home/hermes/.hermes/profiles/charles/tmp_watchlist_fundamentals.json","w") as f:
    json.dump(out, f, indent=1)
print("WROTE fundamentals", len(results), len(sa))
