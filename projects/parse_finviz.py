#!/usr/bin/env python3
import re, json, html
from pathlib import Path

def parse_finviz(path):
    text = Path(path).read_text(errors='ignore')
    # Find table rows with ticker links
    # pattern like: quote.ashx?t=MSFT ... >MSFT</a></td><td ...>numbers
    rows = {}
    # Split by ticker quote links
    parts = re.split(r'quote\.ashx\?t=([A-Z0-9.\-]+)', text)
    # parts[0] preamble, then ticker, content, ticker, content...
    i = 1
    while i + 1 < len(parts):
        t = parts[i]
        chunk = parts[i+1][:2500]
        # strip tags to get cell values after ticker
        # after </a> we get a series of <td>...</td>
        tds = re.findall(r'<td[^>]*>(.*?)</td>', chunk, flags=re.I|re.S)
        # clean
        cells = []
        for td in tds[:20]:
            c = re.sub(r'<[^>]+>', '', td)
            c = html.unescape(c).strip()
            cells.append(c)
        # Expected valuation view columns roughly:
        # No. Ticker Market Cap P/E Forward P/E PEG P/S P/B P/C P/FCF EPS this Y EPS next Y ... Price Change Volume
        # After split on ticker, first cells may start with Market Cap
        if cells:
            rows[t] = cells
        i += 2
    return rows

all_rows = {}
for p in ['/tmp/fv1.html','/tmp/fv2.html','/tmp/fv3.html']:
    r = parse_finviz(p)
    all_rows.update(r)
    print(f'{p}: {len(r)} tickers')

# Print raw first cells for a few
for t in ['MSFT','NVDA','AMZN','META','MU','AMD','TSLA','PLTR','IREN','GLD']:
    print(t, all_rows.get(t, ['MISSING'])[:15])

# Map: typically after ticker link cells are:
# Market Cap, P/E, Forward P/E, PEG, P/S, P/B, P/C, P/FCF, EPS this Y, EPS next Y, EPS past 5Y, EPS next 5Y, Sales past 5Y, Price, Change, Volume
out = {}
for t, cells in all_rows.items():
    # Try to detect layout by finding a price-like float near end and PE-like
    def num(s):
        if s is None: return None
        s=str(s).replace(',','').replace('%','').strip()
        if s in ('','-','N/A','—'): return None
        try: return float(s)
        except: return None
    # Heuristic: Market Cap often has B/T/M
    mcap=cells[0] if cells else None
    pe=num(cells[1]) if len(cells)>1 else None
    fpe=num(cells[2]) if len(cells)>2 else None
    peg=num(cells[3]) if len(cells)>3 else None
    # price often near end before change%
    price=None; chg=None
    for j in range(len(cells)-1, 5, -1):
        # volume is integer large
        v=cells[j]
        if re.fullmatch(r'[\d,]+', v or '') and len(v.replace(',',''))>=4:
            # prior might be change%, prior price
            if j>=2:
                chg=num(cells[j-1])
                price=num(cells[j-2])
            break
    out[t] = {
        'mcap': mcap, 'pe': pe, 'fwdPE': fpe, 'peg': peg,
        'ps': num(cells[4]) if len(cells)>4 else None,
        'pb': num(cells[5]) if len(cells)>5 else None,
        'pfcf': num(cells[7]) if len(cells)>7 else None,
        'epsThisY': cells[8] if len(cells)>8 else None,
        'epsNextY': cells[9] if len(cells)>9 else None,
        'epsNext5Y': cells[11] if len(cells)>11 else None,
        'price': price, 'chg': chg,
        'raw': cells[:16],
    }

with open('/home/hermes/.hermes/projects/finviz_vals.json','w') as f:
    json.dump(out,f,indent=2)
print('saved', len(out))
for t,v in sorted(out.items()):
    print(f"{t}\tfwd={v['fwdPE']}\tpeg={v['peg']}\tpe={v['pe']}\tpx={v['price']}\tchg={v['chg']}\teps5={v['epsNext5Y']}")
