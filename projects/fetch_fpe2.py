#!/usr/bin/env python3
import json, urllib.request, ssl, re, time

ctx = ssl.create_default_context()

tickers = [
"MSFT","AMZN","GOOG","META","AAPL",
"CRM","DELL","PLTR","ORCL","CRWV","INFY","NBIS",
"TSLA","NFLX","MELI",
"HD","LOW","WMT","TGT",
"ASML","AVGO","NVDA","AMD","SNDK","MU","TSM","INTC",
"BE","APLD","TE","PSIX","GLW","BW","PUMP",
"IREN","CORZ","RIOT","CLSK","BITF","BTDR","HIVE",
"GLD","SMH","VFV.TO",
"SPCX","RKLB","SEI","WYFI","CRCL"
]

def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urllib.request.urlopen(req, context=ctx, timeout=25) as r:
        return r.read().decode("utf-8", errors="ignore")

def parse_num(s):
    if s is None: return None
    s = re.sub(r'<[^>]+>', '', str(s)).strip().replace(',','')
    s = s.replace('%','')
    if s in ('','-','—','N/A','n/a','None'): return None
    try: return float(s)
    except: return None

results = {}

for t in tickers:
    entry = {"ok": False, "t": t}
    # Finviz quote
    try:
        ft = t.replace('.TO','')
        page = fetch(f"https://finviz.com/quote.ashx?t={ft}&p=d")
        # snapshot table: data-testid or classic
        # Pattern: Forward P/E</td><td...><b>21.48</b>
        pairs = re.findall(r'>(Forward P/E|PEG|P/E|EPS next Y|EPS this Y|ROI|ROE|ROA|Oper\. Margin|Profit Margin|Target Price|Rel Volume|Market Cap)</[^>]+>\s*<[^>]+>(?:<b>)?([^<]+)(?:</b>)?', page, re.I)
        d = {k: parse_num(v) if k not in ('Market Cap',) else v.strip() for k,v in pairs}
        # also try simpler
        if not d:
            for label in ['Forward P/E','PEG','P/E','EPS next Y','ROI','ROE','Target Price']:
                m = re.search(rf'{re.escape(label)}</td>\s*<td[^>]*>\s*(?:<b>)?([^<]+)', page, re.I)
                if m:
                    d[label] = parse_num(m.group(1)) if label != 'Market Cap' else m.group(1).strip()
        entry.update({
            "ok": bool(d),
            "src": "finviz",
            "forwardPE": d.get("Forward P/E"),
            "trailingPE": d.get("P/E"),
            "peg": d.get("PEG"),
            "eps_next_y": d.get("EPS next Y"),
            "eps_this_y": d.get("EPS this Y"),
            "roi": d.get("ROI"),
            "roe": d.get("ROE"),
            "roa": d.get("ROA"),
            "op_margin": d.get("Oper. Margin"),
            "profit_margin": d.get("Profit Margin"),
            "target": d.get("Target Price"),
            "mcap": d.get("Market Cap"),
            "raw_keys": list(d.keys())[:20],
        })
        print(t, "FPE", entry.get("forwardPE"), "PEG", entry.get("peg"), "ROI", entry.get("roi"), "keys", entry.get("raw_keys"))
    except Exception as e:
        entry["finviz_err"] = str(e)[:120]
        print(t, "FINVIZ_ERR", e)

    # Yahoo key-statistics HTML fallback if needed
    if entry.get("forwardPE") is None:
        try:
            yurl = f"https://finance.yahoo.com/quote/{t}/key-statistics/"
            page = fetch(yurl)
            m = re.search(r'Forward P/E[^0-9\-]*([0-9]+\.[0-9]+|[0-9]+)', page)
            m2 = re.search(r'PEG Ratio \(5[- ]yr expected\)[^0-9\-]*([0-9]+\.[0-9]+|[0-9]+)', page)
            m3 = re.search(r'Trailing P/E[^0-9\-]*([0-9]+\.[0-9]+|[0-9]+)', page)
            if m or m2:
                entry["ok"] = True
                entry["src"] = (entry.get("src") or "") + "+yh"
                if m: entry["forwardPE"] = float(m.group(1))
                if m2: entry["peg"] = float(m2.group(1))
                if m3: entry["trailingPE"] = float(m3.group(1))
                print(t, "YH", entry.get("forwardPE"), entry.get("peg"))
        except Exception as e:
            entry["yh_err"] = str(e)[:100]
            print(t, "YH_ERR", e)

    results[t] = entry
    time.sleep(0.35)

print("====JSON====")
print(json.dumps(results, indent=2, default=str))
