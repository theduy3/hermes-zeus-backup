#!/usr/bin/env python3
import re, json, glob, os

# Prefer newest full extracts
paths = sorted(glob.glob('/home/hermes/.hermes/profiles/charles/cache/web/finviz.com-*.md'), key=os.path.getmtime, reverse=True)
# also yesterday large files
all_data = {}

def pn(x):
    if x is None: return None
    x = str(x).replace('%','').replace(',','').strip()
    if x in ('-','','—'): return None
    try: return float(x)
    except: return None

for f in paths[:15]:
    text = open(f).read()
    # Row pattern spanning lines: [TICKER](url) | [mcap] | [pe] | [fpe] |\n[peg] | ...
    # Match ticker then consecutive bracketed values
    for m in re.finditer(r'\[([A-Z]{1,5})\]\(https://finviz\.com/stock\?t=\1[^)]*\)\s*\|\s*\[([^\]]+)\]\([^)]*\)\s*\|\s*\[([^\]]+)\]\([^)]*\)\s*\|\s*\[([^\]]+)\]\([^)]*\)\s*\|\s*\[([^\]]+)\]\([^)]*\)', text):
        t, mcap, pe, fpe, peg = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        # get more fields after
        start = m.end()
        rest = text[start:start+800]
        vals = re.findall(r'\[([^\]]+)\]\([^)]*\)', rest)
        # vals continue: P/S P/B P/C P/FCF EPS this EPS next ... price chg volume
        entry = {
            "mcap": mcap,
            "pe": pn(pe),
            "fpe": pn(fpe),
            "peg": pn(peg),
            "ps": pn(vals[0]) if len(vals)>0 else None,
            "pb": pn(vals[1]) if len(vals)>1 else None,
            "eps_this": pn(vals[7]) if len(vals)>7 else None,
            "eps_next": pn(vals[8]) if len(vals)>8 else None,
            "src": os.path.basename(f),
        }
        # find price as number before % change
        for i,v in enumerate(vals):
            if '%' in v and i>0:
                p = pn(vals[i-1])
                if p and 0.5 < p < 20000:
                    entry["price"] = p
                    entry["chg"] = pn(v)
                    break
        prev = all_data.get(t)
        # prefer entries with fpe, then newer
        if prev is None or (prev.get("fpe") is None and entry.get("fpe") is not None):
            all_data[t] = entry
        elif prev.get("fpe") is not None and entry.get("fpe") is not None:
            # keep if from newer file (already iterating newest first) - skip overwrite
            pass

print(json.dumps(all_data, indent=2, sort_keys=True))
print('COUNT', len(all_data))
