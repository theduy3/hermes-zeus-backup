#!/usr/bin/env python3
import re, json, urllib.request, ssl

tickers1 = "MSFT,AMZN,GOOG,META,AAPL,CRM,DELL,PLTR,ORCL,CRWV,INFY,NBIS,TSLA,NFLX,MELI,HD,LOW,WMT,TGT"
tickers2 = "ASML,AVGO,NVDA,AMD,SNDK,MU,TSM,INTC,BE,APLD,TE,PSIX,GLW,BW,PUMP,IREN,CORZ,RIOT,CLSK,BTDR,HIVE"
tickers3 = "SPCX,RKLB,SEI,WYFI,CRCL,GLD,SMH"

ctx = ssl.create_default_context()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")

def num(x):
    if x is None:
        return None
    x = str(x).replace("%", "").replace(",", "").strip()
    if x in ("-", "—", "", "N/A"):
        return None
    try:
        return float(x)
    except Exception:
        return x

def parse_finviz(html):
    rows = []
    trs = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S)
    for tr in trs:
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if len(tds) < 10:
            continue
        texts = [re.sub(r"<[^>]+>", "", td).strip().replace("\xa0", " ") for td in tds]
        ticker = None
        for t in texts:
            if re.fullmatch(r"[A-Z]{1,5}(?:\.[A-Z]+)?", t):
                ticker = t
                break
        if not ticker:
            continue
        idx = texts.index(ticker)
        cols = texts[idx:]
        row = {
            "ticker": ticker,
            "mktcap": cols[1] if len(cols) > 1 else None,
            "pe": num(cols[2]) if len(cols) > 2 else None,
            "fwdPE": num(cols[3]) if len(cols) > 3 else None,
            "peg": num(cols[4]) if len(cols) > 4 else None,
            "pfcf": num(cols[8]) if len(cols) > 8 else None,
            "epsThisY": cols[9] if len(cols) > 9 else None,
            "epsNextY": cols[10] if len(cols) > 10 else None,
            "epsNext5Y": cols[12] if len(cols) > 12 else None,
            "price": num(cols[14]) if len(cols) > 14 else None,
            "chg": cols[15] if len(cols) > 15 else None,
        }
        rows.append(row)
    return rows

def parse_fin(html):
    rows = []
    trs = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S)
    for tr in trs:
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        texts = [re.sub(r"<[^>]+>", "", td).strip().replace("\xa0", " ") for td in tds]
        ticker = None
        for t in texts:
            if re.fullmatch(r"[A-Z]{1,5}", t):
                ticker = t
                break
        if not ticker or len(texts) < 8:
            continue
        idx = texts.index(ticker)
        cols = texts[idx:]
        rows.append(
            {
                "t": ticker,
                "roa": cols[3] if len(cols) > 3 else None,
                "roe": cols[4] if len(cols) > 4 else None,
                "roic": cols[5] if len(cols) > 5 else None,
            }
        )
    return rows

for label, tset in [("A", tickers1), ("B", tickers2), ("C", tickers3)]:
    url = f"https://finviz.com/screener.ashx?v=121&t={tset}"
    try:
        html = fetch(url)
        rows = parse_finviz(html)
        print(f"=== SET {label} count={len(rows)}")
        for r in rows:
            print(json.dumps(r))
        if not rows:
            open(f"/tmp/finviz_{label}.html", "w").write(html)
            print("saved html", len(html))
    except Exception as e:
        print("ERR", label, e)

for label, tset in [("FA", tickers1), ("FB", tickers2)]:
    url = f"https://finviz.com/screener.ashx?v=161&t={tset}"
    try:
        html = fetch(url)
        rows = parse_fin(html)
        print(f"=== FINANCIAL {label} count={len(rows)}")
        for r in rows:
            print(json.dumps(r))
    except Exception as e:
        print("ERR", label, e)
