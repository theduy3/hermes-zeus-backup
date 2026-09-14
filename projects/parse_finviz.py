#!/usr/bin/env python3
import re, json, glob, os

files = [
"/home/hermes/.hermes/profiles/charles/cache/web/finviz.com-8260b5352a.md",
"/home/hermes/.hermes/profiles/charles/cache/web/finviz.com-8d194272bb.md",
"/home/hermes/.hermes/profiles/charles/cache/web/finviz.com-1a807ec904.md",
"/tmp/fv1.html",
]

# Also parse HTML if present
results = {}

def parse_md(text):
    # Look for rows like: [TICKER](...) | [cap] | [PE] | [FwdPE] | [PEG] | ...
    # Pattern from truncated content - markdown table cells with links
    # Example: | [18](...) | ... [TSLA](...) | [1443.32B] | [339.53] | [161.09] | [6.81] | ...
    rows = re.findall(
        r'\[([A-Z0-9.\-]+)\]\(https://finviz\.com/stock\?t=\1[^)]*\)\s*\|\s*'
        r'\[([^\]]*)\]\([^)]*\)\s*\|\s*'  # mktcap
        r'\[([^\]]*)\]\([^)]*\)\s*\|\s*'  # PE
        r'\[([^\]]*)\]\([^)]*\)\s*\|\s*'  # Fwd PE
        r'\[([^\]]*)\]\([^)]*\)\s*\|\s*'  # PEG
        r'\[([^\]]*)\]\([^)]*\)\s*\|\s*'  # PS
        r'\[([^\]]*)\]\([^)]*\)\s*\|\s*'  # PB
        r'\[([^\]]*)\]\([^)]*\)\s*\|\s*'  # PC
        r'\[([^\]]*)\]\([^)]*\)',          # PFCF
        text
    )
    for r in rows:
        t = r[0]
        def num(x):
            x = x.strip().replace("%","")
            if x in ("-","", "N/A"): return None
            try: return float(x)
            except: return None
        results[t] = {
            "mktcap": r[1],
            "pe": num(r[2]),
            "fwdPE": num(r[3]),
            "peg": num(r[4]),
            "ps": num(r[5]),
            "pb": num(r[6]),
            "pc": num(r[7]),
            "pfcf": num(r[8]),
            "src": "finviz",
        }

def parse_html(text):
    # Finviz table rows often: <a href="quote.ashx?t=MSFT"...>MSFT</a>
    # or screener table td sequence
    # Try to find ticker then following numeric tds
    # Simpler: find patterns like >MSFT</a></td><td ...>cap</td><td>PE</td><td>FwdPE</td><td>PEG
    pat = re.compile(
        r'>([A-Z]{1,5}(?:\.[A-Z]+)?)</a></td>'
        r'<td[^>]*>([^<]*)</td>'  # maybe colored span inside
        , re.I
    )
    # better full row parse
    # look for tab-row-... 
    for m in re.finditer(r'tab-link[^>]*>([A-Z0-9.\-]{1,8})</a>', text):
        t = m.group(1)
        # take next 2000 chars and extract td values
        chunk = text[m.end():m.end()+2500]
        tds = re.findall(r'<td[^>]*>(?:<span[^>]*>)?([^<]*)(?:</span>)?</td>', chunk)
        # screener valuation columns after ticker: No is before ticker sometimes
        # columns: No. Ticker Market Cap P/E Forward P/E PEG P/S P/B P/C P/FCF EPS This Y EPS Next Y ...
        # after ticker link, first tds are Market Cap, P/E, Fwd P/E, PEG...
        if len(tds) >= 4:
            def num(x):
                x = x.strip().replace("%","").replace(",","")
                if x in ("-","", "N/A"): return None
                try: return float(x)
                except: return None
            # skip if looks like company name
            if t not in results or results[t].get("fwdPE") is None:
                results[t] = {
                    "mktcap": tds[0].strip(),
                    "pe": num(tds[1]),
                    "fwdPE": num(tds[2]),
                    "peg": num(tds[3]),
                    "ps": num(tds[4]) if len(tds)>4 else None,
                    "pb": num(tds[5]) if len(tds)>5 else None,
                    "src": "finviz-html",
                }

for f in files:
    if not os.path.exists(f):
        continue
    text = open(f, encoding="utf-8", errors="ignore").read()
    parse_md(text)
    if f.endswith(".html"):
        parse_html(text)

# Also parse full md with a looser approach - line by line looking for ticker rows
for f in files:
    if not os.path.exists(f):
        continue
    text = open(f, encoding="utf-8", errors="ignore").read()
    # find all [TICKER](finviz stock) occurrences with following bracket numbers
    for m in re.finditer(r'\[([A-Z][A-Z0-9.\-]{0,7})\]\(https://finviz\.com/stock\?t=\1[^)]*\)', text):
        t = m.group(1)
        chunk = text[m.end():m.end()+800]
        vals = re.findall(r'\[([^\]]+)\]\(https://finviz\.com/stock\?t='+re.escape(t)+r'[^)]*\)', chunk)
        # vals: mktcap, pe, fwdpe, peg, ps, pb, pc, pfcf, epsY, epsNY, ...
        if len(vals) >= 4:
            def num(x):
                x = x.strip().replace("%","").replace(",","")
                if x in ("-","", "N/A"): return None
                try: return float(x)
                except: return None
            results[t] = {
                "mktcap": vals[0],
                "pe": num(vals[1]),
                "fwdPE": num(vals[2]),
                "peg": num(vals[3]),
                "ps": num(vals[4]) if len(vals)>4 else None,
                "pb": num(vals[5]) if len(vals)>5 else None,
                "pc": num(vals[6]) if len(vals)>6 else None,
                "pfcf": num(vals[7]) if len(vals)>7 else None,
                "epsThisY": vals[8] if len(vals)>8 else None,
                "epsNextY": vals[9] if len(vals)>9 else None,
                "src": "finviz-md",
            }

print(json.dumps(results, indent=2, default=str))
print("COUNT", len(results), file=__import__("sys").stderr)
