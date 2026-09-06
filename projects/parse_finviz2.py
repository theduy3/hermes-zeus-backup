#!/usr/bin/env python3
import re, json, html
from pathlib import Path

def parse_finviz(path):
    text = Path(path).read_text(errors='ignore')
    rows = {}
    # Each data row has data-boxover-ticker="XXX" on the ticker cell
    # Split by table rows that contain tab-link ticker
    trs = re.findall(r'<tr[^>]*class=\"styled-row[^\"]*\"[^>]*>(.*?)</tr>', text, flags=re.I|re.S)
    for tr in trs:
        m = re.search(r'data-boxover-ticker=\"([A-Z0-9.\-]+)\"', tr)
        if not m:
            m = re.search(r'class=\"tab-link\">([A-Z0-9.\-]+)</a>', tr)
        if not m:
            continue
        t = m.group(1)
        # extract cell texts
        tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, flags=re.I|re.S)
        cells = []
        for td in tds:
            c = re.sub(r'<[^>]+>', ' ', td)
            c = html.unescape(c)
            c = re.sub(r'\s+', ' ', c).strip()
            cells.append(c)
        # cells: No, Ticker(+maybe logo letter), MarketCap, P/E, Fwd P/E, PEG, P/S, P/B, P/C, P/FCF, EPS This Y, EPS Next Y, EPS Past 5Y, EPS Next 5Y, Sales Past 5Y, Price, Change, Volume
        # Ticker cell may be like "M MSFT" due to logo letter
        def num(s):
            if s is None: return None
            s = str(s).replace(',', '').replace('%', '').strip()
            if s in ('', '-', '—', 'N/A'): return None
            try: return float(s)
            except: return None
        # find ticker index
        ti = None
        for i, c in enumerate(cells):
            if t in c.split() or c == t:
                ti = i
                break
        if ti is None:
            continue
        rest = cells[ti+1:]
        # rest[0]=mcap, 1=pe, 2=fwdpe, 3=peg ... price near end
        out = {
            'mcap': rest[0] if rest else None,
            'pe': num(rest[1]) if len(rest)>1 else None,
            'fwdPE': num(rest[2]) if len(rest)>2 else None,
            'peg': num(rest[3]) if len(rest)>3 else None,
            'ps': num(rest[4]) if len(rest)>4 else None,
            'pb': num(rest[5]) if len(rest)>5 else None,
            'pc': num(rest[6]) if len(rest)>6 else None,
            'pfcf': num(rest[7]) if len(rest)>7 else None,
            'epsThisY': rest[8] if len(rest)>8 else None,
            'epsNextY': rest[9] if len(rest)>9 else None,
            'epsPast5Y': rest[10] if len(rest)>10 else None,
            'epsNext5Y': rest[11] if len(rest)>11 else None,
            'salesPast5Y': rest[12] if len(rest)>12 else None,
            'price': num(rest[13]) if len(rest)>13 else None,
            'chg': num(rest[14]) if len(rest)>14 else None,
            'raw': rest[:16],
        }
        rows[t] = out
    return rows

all_rows = {}
for p in ['/tmp/fv1.html','/tmp/fv2.html','/tmp/fv3.html']:
    r = parse_finviz(p)
    print(p, len(r))
    all_rows.update(r)

with open('/home/hermes/.hermes/projects/finviz_vals.json','w') as f:
    json.dump(all_rows, f, indent=2)

for t in sorted(all_rows):
    v = all_rows[t]
    print(f"{t}\tfwd={v['fwdPE']}\tpeg={v['peg']}\tpe={v['pe']}\tpx={v['price']}\tchg={v['chg']}\teps5={v['epsNext5Y']}\tpfcf={v['pfcf']}")
print('TOTAL', len(all_rows))
