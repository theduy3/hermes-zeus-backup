#!/usr/bin/env python3
import json, urllib.request, ssl, re, time, html as htmllib

ctx = ssl.create_default_context()
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

def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urllib.request.urlopen(req, context=ctx, timeout=25) as r:
        return r.read().decode("utf-8", errors="ignore")

results = {}

# Finviz batch screener - 20 tickers at a time
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

for batch in chunks([t for t in tickers if "." not in t], 15):
    tparam = ",".join(batch)
    url = f"https://finviz.com/screener.ashx?v=121&t={tparam}"
    try:
        page = fetch(url)
        # rows like: ticker ... marketcap pe forwardpe peg ...
        # parse table rows
        # Finviz often has: <a href="quote.ashx?t=MSFT"...>MSFT</a>
        # Then subsequent <td> values
        rows = re.findall(r'quote\.ashx\?t=([A-Z0-9.\-]+)"[^>]*>([A-Z0-9.\-]+)</a></td>(.*?)</tr>', page, re.S|re.I)
        for sym, sym2, rest in rows:
            tds = re.findall(r'<td[^>]*>(.*?)</td>', rest, re.S|re.I)
            texts = [re.sub(r'<[^>]+>', '', td).strip() for td in tds]
            # Valuation view columns roughly: No. Ticker Market Cap P/E Forward P/E PEG P/S P/B P/C P/FCF EPS this Y EPS next Y ... Price Change Volume
            # After ticker link, texts[0] might be Market Cap
            def num(x):
                x = x.replace('%','').replace(',','').strip()
                if x in ('-', '', 'N/A'): return None
                try: return float(x)
                except: return None
            entry = {"ok": True, "src": "finviz"}
            if len(texts) >= 5:
                entry["mcap"] = texts[0] if texts else None
                entry["trailingPE"] = num(texts[1]) if len(texts)>1 else None
                entry["forwardPE"] = num(texts[2]) if len(texts)>2 else None
                entry["peg"] = num(texts[3]) if len(texts)>3 else None
                # price often near end
                if len(texts) >= 14:
                    entry["price"] = num(texts[-3]) if len(texts)>=3 else None
                    entry["chg"] = texts[-2] if len(texts)>=2 else None
            results[sym.upper()] = entry
            print("FINVIZ", sym, entry.get("forwardPE"), entry.get("peg"), texts[:6] if texts else None)
    except Exception as e:
        print("FINVIZ_BATCH_FAIL", batch, e)
    time.sleep(0.5)

# stockanalysis for missing
for t in tickers:
    if t in results and results[t].get("forwardPE") is not None:
        continue
    sa_t = t.replace('.', '-')
    url = f"https://stockanalysis.com/stocks/{t.lower()}/statistics/"
    if t.endswith('.TO'):
        url = f"https://stockanalysis.com/quote/tsx/{t.split('.')[0].lower()}/statistics/"
    try:
        page = fetch(url)
        # Forward PE
        m_fpe = re.search(r'Forward PE</td>\s*<td[^>]*>\s*([0-9.,\-]+|n/a)', page, re.I)
        if not m_fpe:
            m_fpe = re.search(r'Forward P/?E[^0-9]*([0-9]+\.?[0-9]*)', page, re.I)
        m_pe = re.search(r'(?:PE Ratio|Trailing PE)</td>\s*<td[^>]*>\s*([0-9.,\-]+|n/a)', page, re.I)
        m_peg = re.search(r'PEG Ratio</td>\s*<td[^>]*>\s*([0-9.,\-]+|n/a)', page, re.I)
        def parse_num(m):
            if not m: return None
            s = m.group(1).replace(',','').strip().lower()
            if s in ('n/a','-','—'): return None
            try: return float(s)
            except: return None
        entry = results.get(t, {"ok": False})
        fpe = parse_num(m_fpe)
        pe = parse_num(m_pe)
        peg = parse_num(m_peg)
        if fpe or pe or peg:
            entry.update({"ok": True, "src": entry.get("src","")+"+sa", "forwardPE": entry.get("forwardPE") or fpe, "trailingPE": entry.get("trailingPE") or pe, "peg": entry.get("peg") or peg})
            results[t] = entry
            print("SA", t, fpe, pe, peg)
        else:
            # try main quote page
            url2 = f"https://stockanalysis.com/stocks/{t.lower()}/"
            page2 = fetch(url2)
            m_fpe2 = re.search(r'Forward PE["\s>]*</[^>]+>\s*<[^>]+>\s*([0-9.]+)', page2, re.I)
            print("SA_MISS", t, "fpe2", parse_num(m_fpe2) if m_fpe2 else None)
            if m_fpe2:
                results[t] = {"ok": True, "src": "sa_quote", "forwardPE": parse_num(m_fpe2)}
    except Exception as e:
        print("SA_FAIL", t, e)
        results.setdefault(t, {"ok": False, "err": str(e)[:100]})
    time.sleep(0.25)

print("====JSON====")
print(json.dumps(results, indent=2, default=str))
